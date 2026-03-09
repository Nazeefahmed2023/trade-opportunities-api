from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # API Configuration
    API_KEY: str = "default_api_key_change_this"
    GEMINI_API_KEY: str = ""
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 10
    RATE_LIMIT_PERIOD: int = 3600  # 1 hour in seconds
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # Security
    SECRET_KEY: str = "your_secret_key_here"
    
    # API Metadata
    APP_NAME: str = "Trade Opportunities API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "AI-powered market analysis for Indian sectors"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
