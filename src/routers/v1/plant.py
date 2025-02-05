from fastapi import APIRouter, Depends

from src.models import Plant, PlantCreate, PlantStatistics, User
from src.utils import current_user

router = APIRouter(tags=["plant"], prefix="/v1/plant")


@router.post("")
async def create_plant(body: PlantCreate, user: User = Depends(current_user)):
    """Create a new plant"""
    return await Plant.create(body, user.id)


@router.get("/{code}")
async def get_plant_by_code(code: str):
    """Get a plant by its code"""
    plant = await Plant.get_by_code(code)
    return plant.dump()


@router.put("/{code}")
async def update_plant_by_code(code: str, body: PlantStatistics):
    """Update a plant's statistics by its code"""
    plant = await Plant.get_by_code(code)
    return await plant.update_statistics(body)
