from asyncio import sleep as async_sleep

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, WebSocketException
from fastapi.encoders import jsonable_encoder

from src.models import User
from src.services import user_service
from src.utils import current_user

router = APIRouter(tags=["user"], prefix="/v1/user")


@router.get("/me")
async def me(user: User = Depends(current_user)):
    """Get the current user"""
    return user.dump()


@router.get("/plants")
async def get_user_plants(user: User = Depends(current_user)):
    """Get all plants owned by the current user"""
    return await user_service.get_plants(user)


@router.websocket("/plants")
async def get_user_plants_ws(websocket: WebSocket):
    token = websocket.query_params.get("token")
    try:
        user = await current_user(token=token)
    except Exception as e:
        await websocket.close(code=1008)
        return
    await websocket.accept()
    try:
        while True:
            data = await user_service.get_plants(user)
            encoded_data = jsonable_encoder(data)
            await websocket.send_json(encoded_data)
            await async_sleep(10)
    except (WebSocketDisconnect, WebSocketException):
        pass
    finally:
        await websocket.close()
