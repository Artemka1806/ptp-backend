__all__ = [
    "plant_router",
    "user_router",
]

from .plant import router as plant_router
from .user import router as user_router

ALL_ROUTERS = [
    plant_router,
    user_router
]