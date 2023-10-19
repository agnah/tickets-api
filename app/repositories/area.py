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

    async def get_area_by_field(self, field: str, value: str):
        area: Optional[Area] = (
            await self.db.execute(
                select(Area)
                .where(getattr(Area, field) == value, Area.fecha_eliminacion.is_(None))
            )
        ).scalar_one_or_none()

        return area

    async def get_area_by_id(self, area_id: int):
        area: Optional[Area] = (
            await self.db.execute(
                select(Area)
                .options(selectinload(Area.tareas))
                .where(Area.id == area_id, Area.fecha_eliminacion.is_(None))
            )
        ).scalar_one_or_none()

        return area

    async def get_area_tareas_by_ids(self, area_id: int, tareas_ids: list[int]):
        tareas: list[TareaAreaRelacion] = (
            (
                await self.db.execute(
                    select(TareaAreaRelacion).where(
                        TareaAreaRelacion.area_id == area_id,
                        TareaAreaRelacion.tarea_id.in_(tareas_ids),
                        TareaAreaRelacion.fecha_eliminacion.is_(None),
                    )
                )
            )
            .scalars()
            .all()
        )

        return tareas

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
