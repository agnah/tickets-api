from attrs import define

from app.models import SessionLocal


@define
class BaseRepository:
    db: SessionLocal