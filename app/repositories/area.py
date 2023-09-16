from typing import Optional
from attr import define

from sqlalchemy import select
from sqlalchemy.orm import InstrumentedAttribute, joinedload
from app.models.area import Area


from app.repositories.base import BaseRepository
from app.schemas.area import AreaSchema


@define
class AreaRepository(BaseRepository):
    """"
    Repository to handle CRUD operations on Area model
    """

    async def get_area_by_id(
        self, area_id: int
    ) -> Optional[AreaSchema]:

        area: Optional[AreaSchema] = (
            await self.db.execute(
                select(Area)
                .where(
                    Area.id == area_id,
                    Area.fecha_eliminacion.is_(None))
            )
        ).scalar_one_or_none()

        return area
