from typing import Optional

from pydantic import BaseModel

class PlantCreate(BaseModel):
    name: str
    type: str
    code: str


class PlantStatistics(BaseModel):
    temperature: Optional[str] = None
    humidity: Optional[str] = None
    soil_moisture: Optional[str] = None
    light_level: Optional[str] = None
