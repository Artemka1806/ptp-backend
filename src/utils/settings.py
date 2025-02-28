from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_DB_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "db"
    JWT_SECRET: str = "secret"
    JWT_EXPIRATION: int = 120
    OPENAI_API_KEY: str = "sk-1234567890"


settings = Settings()
