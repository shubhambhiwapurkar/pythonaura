import os
from typing import List
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
from functools import lru_cache
from azure.appconfiguration.provider import load, SettingSelector
from pydantic import Field

class Settings(BaseSettings):
    # MongoDB settings
    MONGODB_URI: str = Field(..., alias="MONGO_URI")

    # JWT settings
    JWT_SECRET_KEY: str = Field(..., alias="JWT_SECRET")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # External API keys
    GOOGLE_MAPS_API_KEY: str = Field(..., alias="GOOGLE_CLIENT_SECRET")
    GOOGLE_AI_API_KEY: str = Field(..., alias="GEMINI_API_KEY")

    # Google OAuth settings
    GOOGLE_CLIENT_ID: str = Field(..., alias="GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = Field(..., alias="GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI: str = Field(..., alias="GOOGLE_REDIRECT_URI")

    # Service URLs
    ASTROLOGY_SERVICE_URL: str

    # CORS settings
    FRONTEND_CORS_ORIGINS: List[AnyHttpUrl] = Field(..., alias="CORS_ORIGIN")

    model_config = {
        "case_sensitive": True,
    }

@lru_cache()
def get_settings() -> Settings:
    if os.getenv("AZURE_APP_CONFIG_CONNECTION_STRING"):
        config = load(
            connection_string=os.getenv("AZURE_APP_CONFIG_CONNECTION_STRING"),
            selectors=[SettingSelector(key_filter="*", label_filter="\0")]
        )
        return Settings(**config)
    return Settings()

settings = get_settings()
