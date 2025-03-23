__all__ = [
    "auth_router",
    "user_router",
    "plant_router",
    "subscription_router",
    "ALL_ROUTERS",
]

from .auth import router as auth_router
from .plant import router as plant_router
from .user import router as user_router
from .subscription import router as subscription_router

ALL_ROUTERS = [
    auth_router,
    user_router,
    plant_router,
    subscription_router,
]