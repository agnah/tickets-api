from datetime import datetime, timedelta
from typing import Optional, Union
from pydantic import parse_obj_as

from app.repositories.ticket import TicketRepository
from app.schemas.area import TareaAreaSchema
from app.schemas.ticket import AddTareaTicketPayload, CreateTicketPayload, ETicketField, EstadoTicket, TicketSchema, TicketTareaSchema, UpdateTicketPayload
from .layer import register_service, ServiceLayer


@register_service("Ticket")
class TicketService(ServiceLayer):

    async def get_last_months_tickets_by_user(
        self,
        user_id: int,
    ):

        repo = TicketRepository(db=self.db)
        tickets = await repo.get_last_months_tickets_by_user(
            user_id=user_id
        )

        for ticket in tickets:
            if datetime.now() > (ticket.fecha_creacion + timedelta(days=3)):
                ticket.demorado = True

        return parse_obj_as(list[TicketSchema], tickets) if tickets else []

    async def get_tickets_by_field_in_date_range(
        self,
        field: ETicketField = None,
        value: str = None,
        start_date: datetime = None,
        end_date: datetime = None
    ):

        repo = TicketRepository(db=self.db)
        tickets = await repo.get_tickets_by_field_in_date_range(
            field=field,
            value=value,
            start_date=start_date,
            end_date=end_date
        )

        return parse_obj_as(list[TicketSchema], tickets) if tickets else []

    async def create_new_ticket(self, payload: CreateTicketPayload):

        ticket_repo = TicketRepository(db=self.db)

        ticket = await ticket_repo.create_new_ticket(payload=payload)

        return parse_obj_as(TicketSchema, ticket) if ticket else None

    async def update_ticket(self,
                            ticket_id: int,
                            payload: UpdateTicketPayload
                            ):

        ticket_repo = TicketRepository(db=self.db)

        # TBD: Deberiamos llamar a método para almacenar historial

        ticket_id = await ticket_repo.update_ticket(ticket_id=ticket_id, payload=payload)

        return ticket_id

    async def get_ticket_by_id(self, ticket_id: int):

        repo = TicketRepository(db=self.db)
        ticket = await repo.get_ticket_by_id(ticket_id=ticket_id)

        return parse_obj_as(TicketSchema, ticket) if ticket else None

    async def anular_ticket(self, ticket_id: int):

        repo = TicketRepository(db=self.db)
        ticket = await repo.anular_ticket_by_id(ticket_id=ticket_id)

        return parse_obj_as(TicketSchema, ticket) if ticket else None

    async def actualizar_estado_ticket(self, ticket_id: int, estado: EstadoTicket):

        repo = TicketRepository(db=self.db)

        # TBD: Deberiamos llamar a método para almacenar historial

        ticket = await repo.actualizar_estado_ticket(ticket_id=ticket_id, estado=estado)

        return parse_obj_as(TicketSchema, ticket) if ticket else None

    async def derivar_ticket(
        self, ticket_id: int, area_id: int
    ):

        repo = TicketRepository(db=self.db)

        # TBD: Deberiamos llamar a método para almacenar historial

        ticket = await repo.derivar_ticket(ticket_id=ticket_id, area_id=area_id)

        return parse_obj_as(TicketSchema, ticket) if ticket else None

    async def agregar_tarea(
        self, ticket: TicketSchema, tarea: TareaAreaSchema
    ):

        repo = TicketRepository(db=self.db)

        # TBD: Deberiamos llamar a método para almacenar historial
        payload = AddTareaTicketPayload(
            ticket_id=ticket.id,
            tarea_id=tarea.id,
            tecnico_id=ticket.tecnico_asignado_id
        )

        ticket_tarea_relacion = await repo.agregar_tarea(
            payload=payload
        )

        return parse_obj_as(TicketTareaSchema, ticket_tarea_relacion) if ticket_tarea_relacion else None

    async def finalizar_tarea(
        self, ticket_id: int, tarea_id: int
    ):

        repo = TicketRepository(db=self.db)

        # TBD: Deberiamos llamar a método para almacenar historial
        ticket_tarea_relacion = await repo.finalizar_tarea(
            ticket_id=ticket_id, tarea_id=tarea_id
        )

        return parse_obj_as(TicketTareaSchema, ticket_tarea_relacion) if ticket_tarea_relacion else None
