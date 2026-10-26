from pathlib import Path
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

# Automatically resolves the path to .envs/.env.local relative to this file
ENV_FILE = Path(__file__).resolve().parent.parent.parent.parent / ".envs" / ".env.local"


class Settings(BaseSettings):
    environment: Literal["local", "staging", "production"] = "local"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_ignore_empty=True,
        extra="ignore",
    )

    API_V1_STRING: str = ""
    PROJECT_NAME: str = ""
    PROJECT_DESCRIPTION: str = ""
    SITE_NAME: str = ""


settings = Settings()
