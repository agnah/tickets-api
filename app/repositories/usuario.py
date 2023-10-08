from typing import Optional, Union

from attr import define
from sqlalchemy import select, update
from sqlalchemy.orm import InstrumentedAttribute

from app.models.usuario import Usuario
from app.repositories.base import BaseRepository
from app.schemas.usuario import (
    CreateUsuarioPayload,
    EUSerField,
    RolUsuario,
    UpdateUsuarioPayload,
)


@define
class UsuarioRepository(BaseRepository):
    """ "
    Repository to handle CRUD operations on Usuario model
    """

    async def get_user_by_field(
        self, field: EUSerField, value: Union[str, int]
    ) -> Optional[Usuario]:
        column: InstrumentedAttribute = getattr(Usuario, field, Usuario.id)

        user: Optional[Usuario] = (
            await self.db.execute(
                select(Usuario).where(
                    column == value, Usuario.fecha_eliminacion.is_(None)
                )
            )
        ).scalar_one_or_none()

        return user

    async def get_users_list(
        self,
        area_id: int,
        rol: RolUsuario,
    ) -> list[Usuario]:
        users: list[Usuario] = (
            (
                await self.db.execute(
                    select(Usuario).where(
                        Usuario.area_id == area_id,
                        Usuario.rol == rol,
                        Usuario.fecha_eliminacion.is_(None),
                    )
                )
            )
            .scalars()
            .all()
        )

        return users

    async def create_user(self, payload: CreateUsuarioPayload):
        user = Usuario(**payload.dict())

        self.db.add(user)
        await self.db.commit()

        return user

    async def update_user(
        self, field: EUSerField, value: Union[int, str], payload: UpdateUsuarioPayload
    ):
        column: InstrumentedAttribute = getattr(Usuario, field, Usuario.id)

        current_user = await self.get_user_by_field(field, value)

        await self.db.execute(
            update(Usuario)
            .where(column == value, Usuario.fecha_eliminacion.is_(None))
            .values(**payload.dict(exclude_none=True))
        )

        await self.db.commit()

        return current_user.id
