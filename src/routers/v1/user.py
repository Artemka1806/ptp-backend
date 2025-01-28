from fastapi import APIRouter, Depends, HTTPException
from passlib.hash import bcrypt

from src.models import User
from src.utils import current_user

router = APIRouter(tags=["user"], prefix="/v1/user")


@router.get("/me")
async def me(user: User = Depends(current_user)):
    """Get the current user"""
    return user.dump()


@router.get("/plants")
async def get_user_plants(user: User = Depends(current_user)):
    """Get all plants owned by the current user"""
    plants = await user.get_plants()
    return {"plants": [plant.dump() for plant in plants]}
