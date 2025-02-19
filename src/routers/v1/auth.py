from typing import Annotated, Optional

from fastapi import APIRouter, Cookie, HTTPException, Response
from passlib.hash import bcrypt

from src.schemas import UserAuth, UserCreate
from src.services import user_service, auth_service

router = APIRouter(tags=["auth"], prefix="/v1/auth")


@router.post("/signup")
async def signup(body: UserCreate, response: Response):
    """Sign up a new user"""
    user = await user_service.get_by_email(body.email)
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    user = await user_service.create(body.email, body.name, bcrypt.hash(body.password))
    token = await auth_service.generate(user.id)
    response.set_cookie(
        key="refresh_token",
        value=token.id,
        httponly=True,
        samesite="None",
        secure=True
    )
    return {"token": user.generate_token()}


@router.post("/login")
async def login(body: UserAuth, response: Response):
    """Log in an existing user"""
    user = await user_service.get_by_email(body.email)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    if not bcrypt.verify(body.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid password")
    
    token = await auth_service.generate(user.id)
    response.set_cookie(
        key="refresh_token",
        value=token.id,
        httponly=True,
        samesite="None",
        secure=True,
        expires=30*24*60*60
    )
    return {"token": user.generate_token()}


@router.post("/exchange")
async def exchange(refresh_token: Optional[str] = Cookie(None)):
    """Exchange a refresh token for a new access token"""
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Missing refresh token")
    
    old_token = await auth_service.get_by_token(refresh_token)
    if not old_token:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    user = await user_service.get_by_id(old_token.user_id)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    return {"token": user.generate_token()}


@router.post("/logout")
async def logout(
    response: Response,
    refresh_token: Optional[str] = Cookie(None)
):
    """Log out the current user by invalidating their refresh token"""
    if refresh_token:
        await auth_service.delete(refresh_token)
    
    response.delete_cookie(
        key="refresh_token",
        path="/",
        httponly=True,
        samesite="None",
        secure=True
    )
    
    return {"message": "Logged out successfully"}
