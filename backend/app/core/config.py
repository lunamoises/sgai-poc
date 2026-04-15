from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://sgai:sgai_secret@postgres:5432/sgai"
settings = Settings()
