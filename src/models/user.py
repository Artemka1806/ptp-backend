from datetime import datetime, timedelta
from enum import Enum
from beanie import Document, Indexed
from pydantic import EmailStr, Field, validator
from typing import Optional
import jwt

from src.utils import settings

class Sex(str, Enum):
    MALE = "male"
    FEMALE = "female"

class User(Document):
    email: Indexed(EmailStr, unique=True)  # type: ignore[valid-type]
    name: str
    sex: Sex
    year_of_birth: int
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @validator('year_of_birth')
    def validate_year_of_birth(cls, v):
        if v is not None:
            current_year = datetime.now().year
            if v < 1900 or v > current_year:
                raise ValueError(f'Year must be between 1900 and {current_year}')
        return v

    @classmethod
    async def create(cls, email: str, name: str, hashed_password: str, sex: Sex, year_of_birth: Optional[int] = None):
        user = await cls.get_by_email(email)
        if user:
            return None
        return await cls.insert_one(cls(
            email=email, 
            name=name, 
            hashed_password=hashed_password,
            sex=sex,
            year_of_birth=year_of_birth
        ))
    
    @classmethod
    async def get_by_id(cls, id: int):
        return await cls.find_one(cls.id == id)

    @classmethod
    async def get_by_email(cls, email: str):
        return await cls.find_one(cls.email == email)

    def dump(self):
        return {**self.model_dump(), "id": str(self.id)}
    
    async def get_plants(self):
        from src.models import Plant
        return await Plant.get_by_owner(self.id)

    def generate_token(self):
        return jwt.encode(
            {
                "email": self.email,
                "is_active": self.is_active,
                "is_superuser": self.is_superuser,
                "exp": datetime.utcnow() + timedelta(seconds=settings.JWT_EXPIRATION)
            },
            settings.JWT_SECRET,
            algorithm="HS256"
        )
    
    @classmethod
    async def get_by_token(cls, token: str):
        try:
            data = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        return await cls.find_one(cls.email == data["email"])
    
    class Settings:
        name = "users"
