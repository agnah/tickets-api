from typing import Callable, Type

from fastapi import Depends

from app.models import SessionLocal as SchedulerSessionLocal
from app.services.area import AreaService
from app.services.layer import ServiceLayer
from app.services.ticket import TicketService
from app.services.usuario import UsuarioService

from .db import get_db


def get_service(
    service_cls: Type[ServiceLayer],
) -> Callable[[SchedulerSessionLocal], ServiceLayer]:
    def _get_service(
        scheduler_db: SchedulerSessionLocal = Depends(get_db),
    ) -> ServiceLayer:
        return service_cls(db=scheduler_db)

    return _get_service


def get_ticket_service(
    ticket_service: TicketService = Depends(get_service(TicketService)),
) -> TicketService:
    return ticket_service


def get_area_service(
    area_service: AreaService = Depends(get_service(AreaService)),
) -> AreaService:
    return area_service


def get_usuario_service(
    usuario_service: UsuarioService = Depends(get_service(UsuarioService)),
) -> UsuarioService:
    return usuario_service
