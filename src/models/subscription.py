from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from datetime import datetime

class SubscriptionKeys(BaseModel):
    p256dh: str
    auth: str

class Subscription(Document):
    endpoint: str
    keys: SubscriptionKeys
    user_id: PydanticObjectId
    created_at: datetime

    class Settings:
        name = "subscriptions"

    def dump(self):
        return {
            "endpoint": self.endpoint,
            "keys": self.keys.dict(),
            "created_at": self.created_at.isoformat()
        }

    @classmethod
    async def create(cls, endpoint: str, keys: SubscriptionKeys, user_id: PydanticObjectId):
        subscription = cls(endpoint=endpoint, keys=keys, user_id=user_id, created_at=datetime.utcnow())
        await subscription.insert()
        return subscription

    @classmethod
    async def get_by_endpoint(cls, endpoint: str):
        return await cls.find_one(cls.endpoint == endpoint)

    @classmethod
    async def get_by_user_id(cls, user_id: PydanticObjectId):
        return await cls.find_one(cls.user_id == user_id)
