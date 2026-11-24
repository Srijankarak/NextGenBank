from pathlib import Path
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

# Dynamically locate the project root (NextGenBank)
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
ENV_FILE = ROOT_DIR / ".envs" / ".env.local"


class Settings(BaseSettings):
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_ignore_empty=True,
        extra="ignore",
    )

    # Core Application Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "NextGenBank API"
    PROJECT_DESCRIPTION: str = "A high-performance Neo-Banking and Financial Ledger API"
    SITE_NAME: str = "NextGenBank"


# Singleton instance used across the entire backend
settings = Settings()
