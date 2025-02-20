from fastapi import APIRouter, Depends

from src.models import PlantCreate, PlantStatistics, User
from src.services import plant_service
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


@router.delete("/{code}")
async def delete_plant_by_code(code: str):
    """Delete a plant by its code"""
    return await plant_service.delete_by_code(code)
