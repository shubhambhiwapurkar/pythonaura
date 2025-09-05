import os
from typing import List
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings
from functools import lru_cache
from azure.appconfiguration.provider import load, SettingSelector
from pydantic import Field
from dotenv import load_dotenv
import os

# Construct the path to the .env file within the 'app' directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

class Settings(BaseSettings):
    # MongoDB settings
    MONGODB_URI: str = Field(..., alias="mongo-uri")

    # JWT settings
    JWT_SECRET_KEY: str = Field(..., alias="jwt-secret")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # External API keys
    GOOGLE_MAPS_API_KEY: str = Field(..., alias="google-maps-api-key")
    GOOGLE_AI_API_KEY: str = Field(..., alias="gemini-api-key")

    # Google OAuth settings
    GOOGLE_CLIENT_ID: str = Field(..., alias="google-client-id")
    GOOGLE_CLIENT_SECRET: str = Field(..., alias="google-client-secret")
    GOOGLE_REDIRECT_URI: str = Field(..., alias="google-redirect-uri")

    # Service URLs
    ASTROLOGY_SERVICE_URL: str = Field(..., alias="astrology-service-url")

    # CORS settings
    FRONTEND_CORS_ORIGINS: List[AnyHttpUrl] = Field(..., alias="cors-origin")

    model_config = {
        "case_sensitive": True,
    }

@lru_cache()
def get_settings() -> Settings:
    # Updated to use the hyphenated environment variable name
    azure_connection_string = os.environ.get("azure-app-config-connection-string")
    
    if azure_connection_string:
        config = load(
            connection_string=azure_connection_string,
            selectors=[SettingSelector(key_filter="*", label_filter="\0")]
        )
        return Settings(**config)
    return Settings()

settings = get_settings()