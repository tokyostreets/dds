import os 
from pathlib import Path
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class ClickhouseDatabaseSettings(BaseSettings):
    """Nested configuration for ClickHouse"""

    clickhouse_user: str = Field(default="default")
    clickhouse_password: str = Field(default="")
    clickhouse_host: str = Field(default="localhost")
    clickhouse_port: int = Field(default=9000)
    clickhouse_secure: bool = Field(default=False)
    pool_size: int = Field(default=5, ge=1, le=20)


class RedisSettings(BaseSettings): 
    """Nested configuration for Airflow's Redis db=1"""
    redis_host: str = Field(default="localhost")
    redis_port: int = Field(default=6379)
    redis_db: int = Field(default=1)


class Settings(BaseSettings): 
    """Main settinghs configuration loaded from .env variables"""

    # Application Mode 
    ENV: Literal["development", "testing", "production"] = "development"
    DEBUG: bool = True

    # Server configuration
    APP_NAME: str = "Deadlock Draft Simulator"
    HOST: str = "localhost"
    PORT: int = 8000

    DEADLOCK_API_BASE_URL: str

    CLICKHOUSE: ClickhouseDatabaseSettings = ClickhouseDatabaseSettings() 
    REDIS: RedisSettings = RedisSettings() 

    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="__",
        extra="ignore"
    )

settings = Settings()

