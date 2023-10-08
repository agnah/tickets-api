from typing import Optional

from attr import define
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.area import Area, TareaAreaRelacion
from app.repositories.base import BaseRepository


@define
class AreaRepository(BaseRepository):
    """ "
    Repository to handle CRUD operations on Area model
    """

    async def get_area_by_id(self, area_id: int):
        area: Optional[Area] = (
            await self.db.execute(
                select(Area)
                .options(selectinload(Area.tareas))
                .where(Area.id == area_id, Area.fecha_eliminacion.is_(None))
            )
        ).scalar_one_or_none()

        return area

    async def get_all_tareas_by_area_id(self, area_id: int):
        tareas: list[TareaAreaRelacion] = (
            (
                await self.db.execute(
                    select(TareaAreaRelacion).where(
                        TareaAreaRelacion.area_id == area_id,
                        TareaAreaRelacion.fecha_eliminacion.is_(None),
                    )
                )
            )
            .scalars()
            .all()
        )

        return tareas
