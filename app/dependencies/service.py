from typing import Callable, Type

from fastapi import Depends
from app.services.usuario import UsuarioService
from app.services.login import LoginService

from app.models import SessionLocal as SchedulerSessionLocal
from app.services.layer import ServiceLayer

from .db import get_db


def get_service(
    service_cls: Type[ServiceLayer],
) -> Callable[[SchedulerSessionLocal], ServiceLayer]:
    def _get_service(
        scheduler_db: SchedulerSessionLocal = Depends(get_db),
    ) -> ServiceLayer:
        return service_cls(db=scheduler_db)

    return _get_service


def get_usuario_service(
    usuario_service: UsuarioService = Depends(get_service(UsuarioService)),
) -> UsuarioService:
    return usuario_service


def get_login_service(
    login_service: LoginService = Depends(get_service(LoginService)),
) -> LoginService:
    return login_service
