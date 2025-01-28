from fastapi import APIRouter, HTTPException
from passlib.hash import bcrypt

from src.models import User, UserCreate, UserAuth

router = APIRouter(tags=["auth"], prefix="/v1/auth")


@router.post("/signup")
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


@router.post("/login")
async def login(body: UserAuth):
    """Log in an existing user"""
    user = await User.get_by_email(body.email)
    if not user:
        return HTTPException(status_code=400, detail="User not found")
    
    if not bcrypt.verify(body.password, user.hashed_password):
        return HTTPException(status_code=400, detail="Invalid password")
    
    return {"token": user.generate_token()}