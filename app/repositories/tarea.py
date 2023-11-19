from attr import define
from sqlalchemy import select

from app.models.area import TareaAreaRelacion


from app.repositories.base import BaseRepository


@define
class TareaAreaRepository(BaseRepository):
    """
    Repository to handle CRUD operations on TareaAreaRelacion model
    """

    async def get_tarea_by_id(self, tarea_id: int):
        tarea: TareaAreaRelacion = (
            await self.db.execute(select(TareaAreaRelacion).where(TareaAreaRelacion.id == tarea_id))
        ).scalar_one_or_none()

        return tarea

    async def get_tarea_by_area_and_tarea_id(self, tarea_id: int, area_id: int):
        tarea: TareaAreaRelacion = (
            await self.db.execute(
                select(TareaAreaRelacion).where(
                    TareaAreaRelacion.id == tarea_id, TareaAreaRelacion.area_id == area_id
                )
            )
        ).scalar_one_or_none()

        return tarea

    async def get_tareas_by_area_id(self, area_id: int):
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
