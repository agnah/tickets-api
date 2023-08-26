
from datetime import datetime, timedelta
from typing import Optional
from attr import define

from sqlalchemy import select
from app.models.ticket import Ticket

from app.repositories.base import BaseRepository

from app.schemas.ticket import TicketSchema


@define
class TicketRepository(BaseRepository):
    """"
    Repository to handle CRUD operations on Ticket model
    """

    async def get_last_months_tickets_by_user(
        self, user_id: int
    ) -> list[TicketSchema]:

        tickets: Optional[TicketSchema] = (
            await self.db.execute(
                select(Ticket)
                .where(
                    Ticket.tecnico_asignado_id == user_id,
                    Ticket.fecha_creacion >= datetime.now() - timedelta(days=30),
                    Ticket.estado.not_in(["anulado", "finalizado"]),
                    Ticket.fecha_eliminacion.is_(None))
            )
        ).scalars().all()

        return tickets
