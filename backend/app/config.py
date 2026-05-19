"""Configuration module for managing environment variables and application settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "AI Test Data Generator"
    app_version: str = "0.1.0"
    debug: bool = False

    database_url: str = "sqlite:///./test_data_generator.db"

    qwen_api_key: str = ""
    qwen_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"

    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:5174"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
