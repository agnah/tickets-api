
from datetime import datetime, timedelta
from typing import Optional
from attr import define

from sqlalchemy import select
from sqlalchemy.orm import InstrumentedAttribute, joinedload

from app.models.ticket import Ticket

from app.repositories.base import BaseRepository

from app.schemas.ticket import CreateTicketPayload, ETicketField, TicketSchema


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

    async def get_tickets_by_field_in_date_range(
        self,
        field: ETicketField = None, value: str = None,
        start_date: datetime = None, end_date: datetime = None
    ):

        query = select(Ticket).where(
            Ticket.fecha_eliminacion.is_(None),
        )

        if field and value:
            column: InstrumentedAttribute = getattr(Ticket, field)
            query = query.where(column == value)
        elif start_date:
            query = query.where(Ticket.fecha_creacion >= start_date)
        elif end_date:
            query = query.where(Ticket.fecha_creacion <= end_date)

        if not (start_date or end_date):
            query = query.where(Ticket.fecha_creacion >=
                                datetime.now() - timedelta(days=30))

        tickets: list[TicketSchema] = (await self.db.execute(query)).scalars().all()

        return tickets

    async def create_new_ticket(
        self, payload: CreateTicketPayload
    ) -> TicketSchema:

        new_ticket = Ticket(**payload.dict())
        self.db.add(new_ticket)
        await self.db.commit()

        return new_ticket
