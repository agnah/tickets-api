from typing import Optional

from pydantic import parse_obj_as

from app.repositories.area import AreaRepository
from app.schemas.area import AreaResponse, AreaSchema, TareaAreaSchema

from .layer import ServiceLayer, register_service


@register_service("Area")
class AreaService(ServiceLayer):
    async def get_area_by_field(
        self,
        field: str,
        value: str,
    ) -> Optional[AreaSchema]:
        repo = AreaRepository(db=self.db)
        area = await repo.get_area_by_field(field=field, value=value)

        return parse_obj_as(AreaSchema, area) if area else None

    async def get_area_tareas_by_ids(self, area_id: int, tareas_ids: list[int]
                                     ) -> Optional[TareaAreaSchema]:
        repo = AreaRepository(db=self.db)
        tarea = await repo.get_area_tareas_by_ids(area_id=area_id, tareas_ids=tareas_ids)

        return parse_obj_as(list[TareaAreaSchema], tarea) if tarea else None

    async def get_area_by_id(self, area_id: int) -> Optional[AreaResponse]:
        repo = AreaRepository(db=self.db)
        area = await repo.get_area_by_id(area_id=area_id)

        return parse_obj_as(AreaResponse, area) if area else None

    async def get_all_tareas_by_area_id(self, area_id: int) -> list[TareaAreaSchema]:
        repo = AreaRepository(db=self.db)
        tareas = await repo.get_all_tareas_by_area_id(area_id=area_id)

        return parse_obj_as(list[TareaAreaSchema], tareas) if tareas else []
