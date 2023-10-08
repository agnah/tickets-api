from typing import Optional, Union

from pydantic import parse_obj_as

from app.repositories.usuario import UsuarioRepository
from app.schemas.usuario import (
    CreateUsuarioPayload,
    EUSerField,
    RolUsuario,
    UpdateUsuarioPayload,
    UsuarioSchema,
)

from .layer import ServiceLayer, register_service


@register_service("Usuario")
class UsuarioService(ServiceLayer):
    async def get_user_by_field(
        self,
        field: EUSerField,
        value: Union[str, int],
    ) -> Optional[UsuarioSchema]:
        repo = UsuarioRepository(db=self.db)
        usuario = await repo.get_user_by_field(field=field, value=value)

        return parse_obj_as(UsuarioSchema, usuario) if usuario else None

    async def get_users_list(
        self,
        area_id: int,
        rol: RolUsuario,
    ) -> Optional[UsuarioSchema]:
        repo = UsuarioRepository(db=self.db)
        users = await repo.get_users_list(area_id=area_id, rol=rol)

        return parse_obj_as(list[UsuarioSchema], users) if users else []

    async def create_user(self, payload: CreateUsuarioPayload):
        repo = UsuarioRepository(db=self.db)
        user = await repo.create_user(payload)

        return parse_obj_as(UsuarioSchema, user) if user else None

    async def update_user(
        self, field: EUSerField, value: Union[int, str], payload: UpdateUsuarioPayload
    ):
        repo = UsuarioRepository(db=self.db)
        update_user_id = await repo.update_user(field, value, payload)

        return update_user_id
