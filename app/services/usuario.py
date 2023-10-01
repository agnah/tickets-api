from typing import Optional, Union

from pydantic import parse_obj_as
from app.repositories.usuario import UsuarioRepository
from app.schemas.usuario import EUSerField, UsuarioSchema
from .layer import register_service, ServiceLayer


@register_service("Usuario")
class UsuarioService(ServiceLayer):
    async def get_user_by_field(
        self,
        field: EUSerField,
        value: Union[str, int],
    ) -> Optional[UsuarioSchema]:
        repo = UsuarioRepository(db=self.db)
        user = await repo.get_user_by_field(field=field, value=value)

        return parse_obj_as(UsuarioSchema, user) if user else None
