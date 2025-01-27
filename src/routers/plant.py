from fastapi import APIRouter, Depends

from src.models import Plant, PlantCreate, User
from src.utils import current_user

router = APIRouter(tags=["plant"], prefix="/v1")


@router.post("/plant")
async def create_plant(body: PlantCreate, user: User = Depends(current_user)):
    plant = Plant(**body.model_dump(), owner_id=user.id)
    await plant.insert()
    return plant.dump()


@router.get("/plant/{code}")
async def get_plant_by_code(code: str):
    plant = await Plant.get_by_code(code)
    return plant.dump()
