from datetime import datetime, timedelta

from pydantic import parse_obj_as

from app.repositories.ticket import TicketRepository
from app.schemas.area import EAreaField, TareaAreaSchema
from app.schemas.ticket import (
    AddTareaTicketPayload,
    CreateTicketHistorialPayload,
    CreateTicketPayload,
    EnrichedTicketSchema,
    EnrichedTicketTareaSchema,
    EstadoTicket,
    ETicketField,
    TicketHistorialResponse,
    TicketSchema,
    TicketTareaSchema,
    UpdateTicketPayload,
)
from app.schemas.usuario import EUSerField
from app.services.area import AreaService
from app.services.usuario import UsuarioService

from .layer import ServiceLayer, register_service


@register_service("Ticket")
class TicketService(ServiceLayer):
    async def get_last_ten_days_tickets(self):
        repo = TicketRepository(db=self.db)
        tickets = await repo.get_last_ten_days_tickets()

        for ticket in tickets:
            if datetime.now() > (ticket.fecha_creacion + timedelta(days=3)):
                ticket.demorado = True

        return parse_obj_as(list[TicketSchema], tickets) if tickets else []

    async def enriching_tickets(
        self, tickets: list[TicketSchema]
    ) -> list[EnrichedTicketSchema]:
        usuario_service: UsuarioService = self.get_service("Usuario")
        area_service: AreaService = self.get_service("Area")

        enriched_tickets = []
        for ticket in tickets:
            tecnico = await usuario_service.get_user_by_field(
                field=EUSerField.ID, value=ticket.tecnico_asignado_id
            )
            area = await area_service.get_area_by_field(
                field=EAreaField.ID, value=ticket.area_asignada_id
            )
            tareas = await self.get_tareas_by_ticket_id(ticket_id=ticket.id)

            enriched_ticket = EnrichedTicketSchema(
                **ticket.dict(), tecnico=tecnico, area=area, tareas=tareas
            )

            enriched_tickets.append(enriched_ticket)

        return enriched_tickets

    async def get_tickets_by_field_in_date_range(
        self,
        field: ETicketField = None,
        value: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
    ):
        repo = TicketRepository(db=self.db)
        tickets = await repo.get_tickets_by_field_in_date_range(
            field=field, value=value, start_date=start_date, end_date=end_date
        )

        return parse_obj_as(list[TicketSchema], tickets) if tickets else []

    async def get_tareas_by_ticket_id(self, ticket_id: int):
        ticket_repo = TicketRepository(db=self.db)
        tareas = await ticket_repo.get_tareas_by_ticket_id(ticket_id=ticket_id)

        return parse_obj_as(list[TicketTareaSchema], tareas) if tareas else []

    async def create_new_ticket(self, payload: CreateTicketPayload):
        ticket_repo = TicketRepository(db=self.db)
        area_service: AreaService = self.get_service("Area")
        area = await area_service.get_area_by_id(area_id=payload.area_asignada_id)

        prefix = area.nombre[0:3].upper()

        ticket = await ticket_repo.create_new_ticket(payload=payload, prefix=prefix)
        # TBD: Deberiamos llamar a método para almacenar historial,
        # se creo el ticket con el estado inicial

        return parse_obj_as(TicketSchema, ticket) if ticket else None

    async def update_ticket(self, ticket_id: int, payload: UpdateTicketPayload):
        ticket_repo = TicketRepository(db=self.db)

        # TBD: Deberiamos llamar a método para almacenar historial,
        # para almacenar que campos se actualizaron y con que valores en el ticket

        ticket_id = await ticket_repo.update_ticket(
            ticket_id=ticket_id, payload=payload
        )

        updated_ticket = await self.get_ticket_by_id(ticket_id=ticket_id)

        return updated_ticket

    async def get_ticket_by_id(self, ticket_id: int):
        repo = TicketRepository(db=self.db)
        ticket = await repo.get_ticket_by_id(ticket_id=ticket_id)

        return parse_obj_as(TicketSchema, ticket) if ticket else None

    async def anular_ticket(self, ticket_id: int):
        repo = TicketRepository(db=self.db)
        ticket = await repo.anular_ticket_by_id(ticket_id=ticket_id)

        # TBD: Deberiamos llamar a método para almacenar historial,
        # para registrar que el ticket se anulo

        return parse_obj_as(TicketSchema, ticket) if ticket else None

    async def actualizar_estado_ticket(self, ticket_id: int, estado: EstadoTicket):
        repo = TicketRepository(db=self.db)

        # TBD: Deberiamos llamar a método para almacenar historial
        # para registrar que el ticket cambio de estado

        ticket = await repo.actualizar_estado_ticket(ticket_id=ticket_id, estado=estado)

        return parse_obj_as(TicketSchema, ticket) if ticket else None

    async def derivar_ticket(self, ticket_id: int, area_id: int):
        repo = TicketRepository(db=self.db)

        # TBD: Deberiamos llamar a método para almacenar historial
        # para registrar que el ticket cambio de area

        ticket = await repo.derivar_ticket(ticket_id=ticket_id, area_id=area_id)

        return parse_obj_as(TicketSchema, ticket) if ticket else None

    async def agregar_tarea(self, ticket: TicketSchema, tarea: TareaAreaSchema):
        repo = TicketRepository(db=self.db)

        # TBD: Deberiamos llamar a método para almacenar historial
        # para registrar que al ticket se le asigno una tarea
        payload = AddTareaTicketPayload(
            ticket_id=ticket.id,
            tarea_id=tarea.id,
            tecnico_id=ticket.tecnico_asignado_id,
        )

        ticket_tarea_relacion = await repo.agregar_tarea(payload=payload)

        if not ticket_tarea_relacion:
            return None

        ticket_tarea_relacion_data = parse_obj_as(
            TicketTareaSchema, ticket_tarea_relacion
        )

        return EnrichedTicketTareaSchema(
            **ticket_tarea_relacion_data.dict(), tarea=tarea
        )

    async def finalizar_tarea(self, ticket_id: int, tarea_id: int):
        repo = TicketRepository(db=self.db)

        # TBD: Deberiamos llamar a método para almacenar historial
        # para registrar que el ticket finalizo
        ticket_tarea_relacion = await repo.finalizar_tarea(
            ticket_id=ticket_id, tarea_id=tarea_id
        )

        return (
            parse_obj_as(TicketTareaSchema, ticket_tarea_relacion)
            if ticket_tarea_relacion
            else None
        )

    async def eliminar_tarea(self, ticket_id: int, tarea_id: int):
        repo = TicketRepository(db=self.db)

        # TBD: Deberiamos llamar a método para almacenar historial
        # para registrar que el ticket se elimino y no perder este registro!
        tarea_id = await repo.eliminar_tarea(ticket_id=ticket_id, tarea_id=tarea_id)

        return tarea_id if tarea_id else None

    async def get_historial_by_ticket_id(self, ticket_id: int):
        repo = TicketRepository(db=self.db)
        historial = await repo.get_historial_by_ticket_id(ticket_id=ticket_id)

        return (
            parse_obj_as(list[TicketHistorialResponse], historial) if historial else []
        )

    async def agregar_historial(
        self,
        ticket_id: int,
        payload: CreateTicketHistorialPayload,
    ):
        repo = TicketRepository(db=self.db)

        historial = await repo.agregar_historial(payload=payload)

        if not historial:
            return None

        ticket_historial = await repo.get_historial_by_ticket_id(ticket_id=ticket_id)

        return (
            parse_obj_as(list[TicketHistorialResponse], ticket_historial)
            if ticket_historial
            else []
        )
