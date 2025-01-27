from fastapi import APIRouter, Depends, HTTPException
from passlib.hash import bcrypt

from src.models import User, UserCreate, UserAuth
from src.utils import current_user

router = APIRouter(tags=["user"], prefix="/v1")


@router.post("/user/signup")
async def signup(body: UserCreate):
    """Sign up a new user"""
    user = await User.get_by_email(body.email)
    if user:
        return HTTPException(status_code=400, detail="User already exists")
    
    user = User(
        email=body.email,
        name=body.name,
        hashed_password=bcrypt.hash(body.password)
    )
    await user.insert()
    return {"token": user.generate_token()}


@router.post("/user/login")
async def login(body: UserAuth):
    """Log in an existing user"""
    user = await User.get_by_email(body.email)
    if not user:
        return HTTPException(status_code=400, detail="User not found")
    
    if not bcrypt.verify(body.password, user.hashed_password):
        return HTTPException(status_code=400, detail="Invalid password")
    
    return {"token": user.generate_token()}


@router.get("/user/me")
async def me(user: User = Depends(current_user)):
    """Get the current user"""
    return user.dump()


@router.get("/user/plants")
async def get_user_plants(user: User = Depends(current_user)):
    """Get all plants owned by the current user"""
    plants = await user.get_plants()
    return {"plants": [plant.dump() for plant in plants]}
