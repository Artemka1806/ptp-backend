from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Query
from datetime import datetime, timedelta

from src.models import PlantCreate, PlantStatistics, User
from src.models.plant_statistics import PlantHistoricalStatistics
from src.services import plant_service, ai_service
from src.utils import current_user

router = APIRouter(tags=["plant"], prefix="/v1/plant")


@router.post("")
async def create_plant(body: PlantCreate, user: User = Depends(current_user)):
    """Create a new plant"""
    return await plant_service.create(body, user)


@router.get("/{code}")
async def get_plant_by_code(code: str, user: User = Depends(current_user)):
    """Get a plant by its code"""
    return await plant_service.get_by_code_and_owner(code, user)


@router.put("/{code}")
async def update_plant_by_code(code: str, body: PlantStatistics):
    """Update all plants with a matching code"""
    return await plant_service.update_all_by_code(code, body)


@router.delete("/{id}")
async def delete_plant_by_id(id: str, user: User = Depends(current_user)):
    return await plant_service.delete_by_id(id)


@router.get("/{id}/history")
async def get_plant_history(
    id: str, 
    limit: int = Query(default=100, le=1000), 
    user: User = Depends(current_user)
):
    """Get historical statistics for a specific plant"""
    plant = await plant_service.get_by_id(id)
    if not plant:
        return []
    return await PlantHistoricalStatistics.get_by_plant(
        PydanticObjectId(plant.id), 
        PydanticObjectId(user.id), 
        limit
    )


@router.get("/history/all")
async def get_user_plants_history(
    limit: int = Query(default=100, le=1000),
    user: User = Depends(current_user)
):
    """Get historical statistics for all user's plants"""
    return await PlantHistoricalStatistics.get_by_user(user.id, limit)


@router.get("/{id}/advice")
async def get_plant_advice(id: str, user: User = Depends(current_user)):
    """Get plant care advice based on the provided plant and conditions"""
    plant = await plant_service.get_by_id(id)

    if not plant or str(plant.owner_id) != str(user.id) or not plant.statistics:
        return {"advice": ""}
    
    if hasattr(plant, 'advice_updated_at') and plant.advice_updated_at and plant.advice_updated_at > datetime.utcnow() - timedelta(days=1):
        return {"advice": plant.advice}
    
    data = ai_service.get_plant_care_advice(plant.type, plant.statistics)
    plant.advice = data["advice"]
    plant.advice_updated_at = datetime.utcnow()
    await plant.save()
    return {"advice": data["advice"]}


@router.get("/{id}/weekly-advice")
async def get_plant_weekly_advice(id: str, user: User = Depends(current_user)):
    """Get plant care advice based on the last 7 days of statistics"""
    plant = await plant_service.get_by_id(id)
    
    if not plant or str(plant.owner_id) != str(user.id):
        return {"advice": ""}
    
    if hasattr(plant, 'weekly_advice_updated_at') and plant.weekly_advice_updated_at and plant.weekly_advice_updated_at > datetime.utcnow() - timedelta(days=1):
        return {"advice": getattr(plant, 'weekly_advice', "")}

    historical_stats = await PlantHistoricalStatistics.get_by_plant(
        PydanticObjectId(id),
        PydanticObjectId(user.id), 
        limit=7
    )
    
    if not historical_stats:
        return {"advice": ""}
    
    data = ai_service.analyze_plant_statistics(plant.type, historical_stats)
    plant.weekly_advice = data["advice"]
    plant.weekly_advice_updated_at = datetime.utcnow()
    await plant.save()
    return {"advice": data["advice"]}
