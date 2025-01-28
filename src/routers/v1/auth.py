from typing import Annotated

from fastapi import APIRouter, Cookie, HTTPException, Response
from passlib.hash import bcrypt

from src.models import User, UserCreate, UserAuth, RefreshToken

router = APIRouter(tags=["auth"], prefix="/v1/auth")


@router.post("/signup")
async def signup(body: UserCreate, response: Response):
    """Sign up a new user"""
    user = await User.get_by_email(body.email)
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user = User(
        email=body.email,
        name=body.name,
        hashed_password=bcrypt.hash(body.password)
    )
    await user.insert()
    token = await RefreshToken.generate(user.id)
    response.set_cookie("refresh_token", token.id, httponly=True)
    return {"token": user.generate_token()}


@router.post("/login")
async def login(body: UserAuth, response: Response):
    """Log in an existing user"""
    user = await User.get_by_email(body.email)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    if not bcrypt.verify(body.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid password")
    
    token = await RefreshToken.generate(user.id)
    response.set_cookie("refresh_token", token.id, httponly=True)
    
    return {"token": user.generate_token()}


@router.post("/exchange")
async def exchange(refresh_token: Annotated[str, Cookie] = Cookie()):
    """Exchange a refresh token for a new access token"""
    print(refresh_token)
    old_token = await RefreshToken.get_by_token(refresh_token)
    if not old_token:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    user = await User.find_one(User.id == old_token.user_id)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    return {"token": user.generate_token()}