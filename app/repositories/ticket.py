
from datetime import datetime, timedelta
from typing import Optional
from attr import define

from sqlalchemy import select
from sqlalchemy.orm import InstrumentedAttribute, joinedload

from app.models.ticket import Ticket

from app.repositories.base import BaseRepository

from app.schemas.ticket import CreateTicketPayload, ETicketField, EstadoTicket, TicketSchema


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

    async def get_ticket_by_id(self, ticket_id: int) -> TicketSchema:

        ticket: TicketSchema = (
            await self.db.execute(
                select(Ticket)
                .where(
                    Ticket.id == ticket_id,
                    Ticket.fecha_eliminacion.is_(None)
                )
            )
        ).scalar_one_or_none()

        return ticket

    async def anular_ticket_by_id(self, ticket_id: int) -> TicketSchema:

        ticket: TicketSchema = (
            await self.db.execute(
                select(Ticket)
                .where(
                    Ticket.id == ticket_id,
                    Ticket.fecha_eliminacion.is_(None)
                )
            )
        ).scalar_one_or_none()

        if ticket:
            ticket.estado = "anulado"
            ticket.fecha_eliminacion = datetime.now()

            await self.db.commit()

        return ticket

    async def actualizar_estado_ticket(
        self, ticket_id: int, estado: EstadoTicket
    ) -> TicketSchema:

        ticket: TicketSchema = (
            await self.db.execute(
                select(Ticket)
                .where(
                    Ticket.id == ticket_id,
                    Ticket.fecha_eliminacion.is_(None)
                )
            )
        ).scalar_one_or_none()

        if ticket:
            ticket.estado = estado
            if estado == EstadoTicket.FINALIZADO:
                ticket.fecha_eliminacion = datetime.now()

            await self.db.commit()

        return ticket

    async def derivar_ticket(
        self, ticket_id: int, area_id: int
    ) -> TicketSchema:

        ticket: TicketSchema = (
            await self.db.execute(
                select(Ticket)
                .where(
                    Ticket.id == ticket_id,
                    Ticket.fecha_eliminacion.is_(None)
                )
            )
        ).scalar_one_or_none()

        if ticket:
            ticket.area_asignada_id = area_id
            ticket.estado = EstadoTicket.DERIVADO

            await self.db.commit()

        return ticket
