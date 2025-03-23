from asyncio import sleep as async_sleep

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, WebSocketException, HTTPException
from fastapi.encoders import jsonable_encoder

from src.models import User, Subscription
from src.schemas import SubscriptionCreate
from src.services import subscription_service
from src.utils import current_user

router = APIRouter(tags=["subscription"], prefix="/v1/subscription")


@router.post("/subscribe")
async def subscribe(
    body: SubscriptionCreate,
    user: User = Depends(current_user),
):
    """
    Subscribe to notifications.
    """
    subscription = await subscription_service.create(body, user.id)
    return jsonable_encoder(subscription)