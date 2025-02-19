from datetime import datetime, timedelta

from beanie import Document, PydanticObjectId
from pydantic.fields import Field


class RefreshToken(Document):
    user_id: PydanticObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime

    def dump(self):
        return {**self.model_dump(), "id": str(self.id), "user_id": str(self.user_id)}

    @classmethod
    async def create(cls, user_id: PydanticObjectId):
        return await cls.insert_one(
            cls(
                user_id=user_id,
                expires_at=datetime.utcnow() + timedelta(days=30)
            )
        )

    @classmethod
    async def get_by_token(cls, token: str):
        return await cls.find_one({"_id": PydanticObjectId(token)})
    
    @classmethod
    async def get_by_user(cls, user_id: PydanticObjectId):
        return await cls.find_one(cls.user_id == user_id)
    
    @classmethod
    async def generate(cls, user_id: PydanticObjectId):
        t = await cls.get_by_user(user_id)
        if t:
            await t.delete()
        return await cls.insert_one(
            cls(
                user_id=user_id,
                expires_at=datetime.utcnow() + timedelta(days=30)
            )
        )
    
    @classmethod
    async def delete(cls, token: str):
        return await cls.find_one({"_id": PydanticObjectId(token)}).delete()

    class Settings:
        name = "refresh_tokens"
