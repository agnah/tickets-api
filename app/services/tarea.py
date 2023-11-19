from pydantic import parse_obj_as
from app.repositories.tarea import TareaAreaRepository
from app.schemas.area import TareaAreaSchema

from .layer import ServiceLayer, register_service


@register_service("Tarea")
class TareaService(ServiceLayer):
    async def get_tarea_by_id(self, tarea_id: int) -> TareaAreaSchema:
        tarea_repo = TareaAreaRepository(db=self.db)

        tarea = await tarea_repo.get_tarea_by_id(tarea_id=tarea_id)

        return parse_obj_as(TareaAreaSchema, tarea) if tarea else None

    async def get_tarea_by_area_and_tarea_id(self, tarea_id: int, area_id: int) -> TareaAreaSchema:
        tarea_repo = TareaAreaRepository(db=self.db)

        tarea = await tarea_repo.get_tarea_by_area_and_tarea_id(tarea_id=tarea_id, area_id=area_id)

        return parse_obj_as(TareaAreaSchema, tarea) if tarea else None

    async def get_tareas_by_area_id(self, area_id: int) -> list[TareaAreaSchema]:
        tarea_repo = TareaAreaRepository(db=self.db)

        tareas = await tarea_repo.get_tareas_by_area_id(area_id=area_id)

        return parse_obj_as(list[TareaAreaSchema], tareas) if tareas else []
