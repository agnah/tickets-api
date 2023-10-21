from datetime import datetime, timedelta

from attr import define
from sqlalchemy import select, update
from sqlalchemy.orm import InstrumentedAttribute

from app.helpers import identificador_generator
from app.models.ticket import Ticket, TicketTareaRelacion
from app.repositories.base import BaseRepository
from app.schemas.tarea import EEstadoTarea
from app.schemas.ticket import (
    AddTareaTicketPayload,
    CreateTicketPayload,
    EstadoTicket,
    ETicketField,
    TicketSchema,
    TicketTareaSchema,
    UpdateTicketPayload,
)


@define
class TicketRepository(BaseRepository):
    """ "
    Repository to handle CRUD operations on Ticket model
    """

    async def get_last_ten_days_tickets(self) -> list[TicketSchema]:
        tickets: list[TicketSchema] = (
            (
                await self.db.execute(
                    select(Ticket)
                    .where(
                        Ticket.fecha_creacion >= datetime.now() - timedelta(days=10),
                    )
                    .order_by(Ticket.prioridad.asc())
                )
            )
            .scalars()
            .all()
        )

        return tickets

    async def get_tickets_by_field_in_date_range(
        self,
        field: ETicketField = None,
        value: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
    ) -> list[TicketSchema]:
        query = select(Ticket)

        if field and value:
            column: InstrumentedAttribute = getattr(Ticket, field)
            query = query.where(column == value)
        elif start_date:
            query = query.where(Ticket.fecha_creacion >= start_date)
        elif end_date:
            query = query.where(Ticket.fecha_creacion <= end_date)

        if not (start_date or end_date):
            query = query.where(
                Ticket.fecha_creacion >= datetime.now() - timedelta(days=30)
            )

        tickets: list[TicketSchema] = (
            (await self.db.execute(query.order_by(Ticket.prioridad.asc())))
            .scalars()
            .all()
        )

        return tickets

    async def get_tareas_by_ticket_id(self, ticket_id: int) -> list[TicketTareaSchema]:
        tareas: list[TicketTareaSchema] = (
            (
                await self.db.execute(
                    select(TicketTareaRelacion).where(
                        TicketTareaRelacion.ticket_id == ticket_id,
                        # TicketTareaRelacion.fecha_eliminacion.is_(None),
                    )
                )
            )
            .scalars()
            .all()
        )

        return tareas

    async def create_new_ticket(self, payload: CreateTicketPayload, prefix: str):
        new_ticket = Ticket(
            identificador=identificador_generator.generate_custom_identificador(prefix),
            **payload.dict(exclude_none=True)
        )
        self.db.add(new_ticket)
        await self.db.commit()

        return new_ticket

    async def update_ticket(self, ticket_id: int, payload: UpdateTicketPayload):
        current_ticket = await self.get_ticket_by_id(ticket_id=ticket_id)

        if (current_ticket.tecnico_asignado_id is None) and payload.tecnico_asignado_id:
            current_ticket.estado = EstadoTicket.EN_CURSO

        await self.db.execute(
            update(Ticket)
            .where(Ticket.id == ticket_id)
            .values(**payload.dict(exclude_none=True))
        )

        await self.db.commit()

        return current_ticket.id

    async def get_ticket_by_id(self, ticket_id: int) -> TicketSchema:
        ticket: TicketSchema = (
            await self.db.execute(select(Ticket).where(Ticket.id == ticket_id))
        ).scalar_one_or_none()

        return ticket

    async def anular_ticket_by_id(self, ticket_id: int) -> TicketSchema:
        ticket: TicketSchema = (
            await self.db.execute(
                select(Ticket).where(
                    Ticket.id == ticket_id, Ticket.fecha_eliminacion.is_(None)
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
                select(Ticket).where(
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

    async def derivar_ticket(self, ticket_id: int, area_id: int) -> TicketSchema:
        ticket: TicketSchema = (
            await self.db.execute(
                select(Ticket).where(
                    Ticket.id == ticket_id,
                    Ticket.fecha_eliminacion.is_(None)
                )
            )
        ).scalar_one_or_none()

        if ticket:
            ticket.area_asignada_id = area_id
            ticket.estado = EstadoTicket.DERIVADO
            ticket.tecnico_asignado_id = None

            await self.db.commit()

        return ticket

    async def agregar_tarea(self, payload: AddTareaTicketPayload):
        ticket_tarea = TicketTareaRelacion(**payload.dict())
        self.db.add(ticket_tarea)
        await self.db.commit()

        return ticket_tarea

    async def finalizar_tarea(self, ticket_id: int, tarea_id: int) -> TicketTareaSchema:
        ticket_tarea: TicketTareaSchema = (
            await self.db.execute(
                select(TicketTareaRelacion).where(
                    TicketTareaRelacion.ticket_id == ticket_id,
                    TicketTareaRelacion.tarea_id == tarea_id,
                    TicketTareaRelacion.fecha_eliminacion.is_(None),
                )
            )
        ).scalar_one_or_none()

        if ticket_tarea:
            ticket_tarea.estado = EEstadoTarea.FINALIZADA
            ticket_tarea.fecha_eliminacion = datetime.now()

            await self.db.commit()

        return ticket_tarea

    async def eliminar_tarea(self, ticket_id: int, tarea_id: int) -> TicketTareaSchema:
        ticket_tarea: TicketTareaSchema = (
            await self.db.execute(
                select(TicketTareaRelacion).where(
                    TicketTareaRelacion.ticket_id == ticket_id,
                    TicketTareaRelacion.tarea_id == tarea_id,
                    TicketTareaRelacion.fecha_eliminacion.is_(None),
                )
            )
        ).scalar_one_or_none()

        if ticket_tarea:
            # Eliminar registro de la base de datos
            await self.db.delete(ticket_tarea)
            await self.db.commit()

        return ticket_tarea.tarea_id if ticket_tarea else None