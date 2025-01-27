from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_DB_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "db"
    JWT_SECRET: str = "secret"


settings = Settings()
