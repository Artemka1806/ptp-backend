from datetime import datetime, timedelta

from beanie import Document, PydanticObjectId
from src.schemas.plant import PlantStatistics

class PlantHistoricalStatistics(Document):
    plant_id: PydanticObjectId
    user_id: PydanticObjectId 
    statistics: PlantStatistics
    created_at: datetime = datetime.utcnow()

    @classmethod
    async def create(cls, plant_id: PydanticObjectId, user_id: PydanticObjectId, statistics: PlantStatistics):
        historical_stat = cls(plant_id=plant_id, user_id=user_id, statistics=statistics)
        await historical_stat.insert()
        return historical_stat.dump()

    @classmethod
    async def create_if_needed(cls, plant_id: PydanticObjectId, user_id: PydanticObjectId, statistics: PlantStatistics):
        latest = await cls.find_one(
            {"$and": [
                {"plant_id": plant_id},
                {"user_id": user_id}
            ]},
            sort=[("created_at", -1)]
        )

        should_create = True
        if latest:
            time_diff = datetime.utcnow() - latest.created_at
            if time_diff < timedelta(minutes=10):
                should_create = False

        if should_create:
            return await cls.create(plant_id, user_id, statistics)
        return None

    @classmethod
    async def get_by_plant(cls, plant_id: PydanticObjectId, user_id: PydanticObjectId, limit: int = 100):
        return await cls.find(
            {"$and": [
                {"plant_id": plant_id},
                {"user_id": user_id}
            ]}
        ).sort(-cls.created_at).limit(limit).to_list()

    @classmethod
    async def get_by_user(cls, user_id: PydanticObjectId, limit: int = 100):
        return await cls.find(
            cls.user_id == user_id
        ).sort(-cls.created_at).limit(limit).to_list()

    def dump(self):
        return {
            **self.model_dump(),
            "id": str(self.id),
            "plant_id": str(self.plant_id),
            "user_id": str(self.user_id)
        }

    class Settings:
        name = "plant_statistics_history"