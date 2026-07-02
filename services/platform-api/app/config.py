from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_REPO_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(_REPO_ROOT / ".env", ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Phoenix Platform API"
    app_version: str = "0.1.0"
    debug: bool = False

    host: str = "0.0.0.0"
    port: int = 8000

    database_url: str = "postgresql+asyncpg://phoenix:changeme-phoenix-db@postgres.phoenix-platform.svc:5432/phoenix"
    redis_url: str = "redis://redis.phoenix-platform.svc:6379/0"
    kafka_bootstrap_servers: str = "redpanda.phoenix-platform.svc:9092"
    kafka_topic_prefix: str = "phoenix"

    cors_origins: list[str] = ["https://portal.ocp1.npd.co"]

    ocp_base_domain: str = "ocp1.npd.co"
    harbor_registry: str = "harbor.ocp1.npd.co"
    harbor_project: str = "phoenix"
    templates_dir: str = ""

    @property
    def golden_path_templates_dir(self) -> Path:
        if self.templates_dir:
            return Path(self.templates_dir)
        return _REPO_ROOT / "templates" / "golden-path"


@lru_cache
def get_settings() -> Settings:
    return Settings()
