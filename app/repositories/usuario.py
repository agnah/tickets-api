from typing import Optional, Union
from attr import define

from sqlalchemy import select
from sqlalchemy.orm import InstrumentedAttribute
from app.models.usuario import Usuario

from app.repositories.base import BaseRepository
from app.schemas.usuario import EUSerField


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
