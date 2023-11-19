

from fastapi import APIRouter, Depends, HTTPException, status
from app.dependencies.service import get_area_service
from app.schemas.area import AreaSchema
from app.services.area import AreaService

router = APIRouter()


@router.get("/{area_id}/")
async def get_area_by_id(
    area_id: int,
    area_service: AreaService = Depends(get_area_service)
) -> AreaSchema:

    area = await area_service.get_area_by_id(
        area_id=area_id
    )

    if not area:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Area no encontrada"},
        )

    return area


@router.get("/tareas/{area_id}/")
async def get_tareas_by_area_id(
    area_id: int,
    area_service: AreaService = Depends(get_area_service)
) -> AreaSchema:

    area = await area_service.get_area_by_id(
        area_id=area_id
    )

    if not area:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Area no encontrada"},
        )

    tareas = await area_service.get_all_tareas_by_area_id(area_id=area_id)

    if not tareas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Tareas no encontradas para esta area"},
        )

    return tareas
