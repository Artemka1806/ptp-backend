__all__ = [
    "User",
    "Plant",
    "PlantCreate",
    "PlantStatistics",
    "RefreshToken",
    "PlantHistoricalStatistics"
]

from .user import User
from .plant import Plant, PlantCreate, PlantStatistics
from .refresh_token import RefreshToken
from .plant_statistics import PlantHistoricalStatistics

ALL_DB_MODELS = [
    User,
    Plant,
    RefreshToken,
    PlantHistoricalStatistics
]
