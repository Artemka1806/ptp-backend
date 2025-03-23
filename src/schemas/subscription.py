from pydantic import BaseModel

class SubscriptionCreate(BaseModel):
    endpoint: str
    keys: dict
