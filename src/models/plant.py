from datetime import datetime
from typing import Optional

from beanie import Document, PydanticObjectId
from pydantic import BaseModel


class PlantCreate(BaseModel):
    name: str
    code: str


class Plant(Document):
    name: str
    code: str
    owner_id: PydanticObjectId
    created_at: datetime = datetime.utcnow()

    @classmethod
    async def get_by_code(cls, code: str):
        return await cls.find_one(cls.code == code)

    @classmethod
    async def get_by_owner(cls, owner_id: PydanticObjectId):
        return await cls.find(cls.owner_id == owner_id).to_list()
    
    def dump(self):
        return {**self.model_dump(), "id": str(self.id), "owner_id": str(self.owner_id)}
    

    class Settings:
        name = "plants"
