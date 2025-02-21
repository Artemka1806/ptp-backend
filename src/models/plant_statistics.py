from datetime import datetime

from beanie import Document, PydanticObjectId
from src.schemas.plant import PlantStatistics

class PlantHistoricalStatistics(Document):
    plant_id: PydanticObjectId
    user_id: PydanticObjectId 
    statistics: PlantStatistics
    date: datetime
    update_count: int = 1
    created_at: datetime = datetime.utcnow()

    @classmethod
    async def create(cls, plant_id: PydanticObjectId, user_id: PydanticObjectId, statistics: PlantStatistics):
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        historical_stat = cls(
            plant_id=plant_id, 
            user_id=user_id, 
            statistics=statistics,
            date=today
        )
        await historical_stat.insert()
        return historical_stat.dump()

    @classmethod
    async def create_or_update(cls, plant_id: PydanticObjectId, user_id: PydanticObjectId, statistics: PlantStatistics):
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        today_stat = await cls.find_one(
            {"$and": [
                {"plant_id": plant_id},
                {"user_id": user_id},
                {"date": today}
            ]}
        )

        if today_stat:
            new_stats = PlantStatistics(
                temperature=str((float(today_stat.statistics.temperature or 0) * today_stat.update_count + 
                               float(statistics.temperature or 0)) / (today_stat.update_count + 1)),
                humidity=str((float(today_stat.statistics.humidity or 0) * today_stat.update_count + 
                            float(statistics.humidity or 0)) / (today_stat.update_count + 1)),
                soil_moisture=str((float(today_stat.statistics.soil_moisture or 0) * today_stat.update_count + 
                                 float(statistics.soil_moisture or 0)) / (today_stat.update_count + 1)),
                light_level=str((float(today_stat.statistics.light_level or 0) * today_stat.update_count + 
                               float(statistics.light_level or 0)) / (today_stat.update_count + 1))
            )
            
            today_stat.statistics = new_stats
            today_stat.update_count += 1
            await today_stat.save()
            return today_stat.dump()
        else:
            return await cls.create(plant_id, user_id, statistics)

    @classmethod
    async def get_by_plant(cls, plant_id: PydanticObjectId, user_id: PydanticObjectId, limit: int = 100):
        return await cls.find(
            {"$and": [
                {"plant_id": plant_id},
                {"user_id": user_id}
            ]}
        ).sort(-cls.date).limit(limit).to_list()

    @classmethod
    async def get_by_user(cls, user_id: PydanticObjectId, limit: int = 100):
        return await cls.find(
            cls.user_id == user_id
        ).sort(-cls.date).limit(limit).to_list()

    def dump(self):
        return {
            **self.model_dump(),
            "id": str(self.id),
            "plant_id": str(self.plant_id),
            "user_id": str(self.user_id),
            "date": self.date.isoformat()
        }

    class Settings:
        name = "plant_statistics_history"