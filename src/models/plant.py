from datetime import datetime
from typing import Optional

from beanie import Document, PydanticObjectId
from pydantic import BaseModel


class PlantCreate(BaseModel):
    name: str
    code: str


class PlantStatistics(BaseModel):
    temperature: Optional[str] = None
    humidity: Optional[str] = None
    soil_moisture: Optional[str] = None
    light_level: Optional[str] = None


class Plant(Document):
    name: str
    code: str
    owner_id: PydanticObjectId
    statistics: Optional[PlantStatistics] = None
    created_at: datetime = datetime.utcnow()

    @classmethod
    async def create(cls, body: PlantCreate, owner_id: PydanticObjectId):
        plant = cls(**body.model_dump(), owner_id=owner_id)
        await plant.insert()
        return plant.dump()

    @classmethod
    async def get_by_code(cls, code: str):
        return await cls.find_one(cls.code == code)

    @classmethod
    async def get_by_owner(cls, owner_id: PydanticObjectId):
        return await cls.find(cls.owner_id == owner_id).to_list()
    
    async def update_statistics(self, statistics: PlantStatistics):
        self.statistics = statistics
        await self.save()
        return self.dump()

    def dump(self):
        return {**self.model_dump(), "id": str(self.id), "owner_id": str(self.owner_id)}
    

    class Settings:
        name = "plants"
