from fastapi import APIRouter, Depends

from src.models import Plant, PlantCreate, User
from src.utils import current_user

router = APIRouter(tags=["plant"], prefix="/v1/plant")


@router.post("")
async def create_plant(body: PlantCreate, user: User = Depends(current_user)):
    """Create a new plant"""
    plant = Plant(**body.model_dump(), owner_id=user.id)
    await plant.insert()
    return plant.dump()


@router.get("/{code}")
async def get_plant_by_code(code: str):
    """Get a plant by its code"""
    plant = await Plant.get_by_code(code)
    return plant.dump()
