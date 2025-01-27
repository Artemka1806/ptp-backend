__all__ = [
    "User",
    "UserAuth",
    "UserCreate",
    "Plant",
    "PlantCreate"
]

from .user import User, UserAuth, UserCreate
from .plant import Plant, PlantCreate

ALL_DB_MODELS = [
    User,
    Plant,
]
