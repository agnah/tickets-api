from typing import Optional
from pydantic import parse_obj_as

from app.repositories.area import AreaRepository
from app.schemas.area import AreaSchema
from .layer import register_service, ServiceLayer


@register_service("Area")
class AreaService(ServiceLayer):
    async def get_area_by_id(
        self, area_id: int
    ) -> Optional[AreaSchema]:

        repo = AreaRepository(db=self.db)
        area = await repo.get_area_by_id(
            area_id=area_id
        )

        return parse_obj_as(AreaSchema, area) if area else None
