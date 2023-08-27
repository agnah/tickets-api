import os
from typing import Optional

from pydantic import BaseModel, BaseSettings, conlist

secrets_dir = os.environ.get("SECRETS_DIR", "/tmp")


class RoutingDatabaseSettings(BaseModel):
    leader: str
    followers: conlist(str, min_items=1)  # type: ignore


class Settings(BaseSettings):
    SERVICE_NAME: str = "tickets-api"

    # Tickets Database settings
    TICKETS_API_DATABASE_URL: str
    TICKETS_API_ECHO_QUERIES: bool = False
    TICKETS_API_DATABASE_ROUTING_CONFIG: Optional[RoutingDatabaseSettings] = None

    # todo: cambiar url del endpoint
    ACTIVITY_DIRECTORY_API_BASE_URL: str = "http://tasks.ministerio.login"

    class Config:
        secrets_dir = secrets_dir
        env_file = ".env"
        case_sensitive = True


settings = Settings()
