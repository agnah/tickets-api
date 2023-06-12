from typing import Optional

from pydantic import BaseModel, BaseSettings, conlist



class RoutingDatabaseSettings(BaseModel):
    leader: str
    followers: conlist(str, min_items=1)


class Settings(BaseSettings):
    TICKETS_API_SYNC_DATABASE_URL: str
    TICKETS_API_DATABASE_URL: str
    TICKETS_API_DATABASE_ROUTING_CONFIG: Optional[RoutingDatabaseSettings] = None
    TICKETS_MODELS_ECHO_QUERIES: bool = False

    class Config:
        env_file = ".env"


settings = Settings()