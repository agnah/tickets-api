from datetime import datetime, timedelta

from pydantic import parse_obj_as

from app.repositories.ticket import TicketRepository
from app.schemas.area import EAreaField, TareaAreaSchema
from app.schemas.tarea import EEstadoTarea
from app.schemas.ticket import (
    AddTareaTicketPayload,
    CreateTicketHistorialPayload,
    CreateTicketPayload,
    ETipoPedido,
    EnrichedTicketSchema,
    EnrichedTicketTareaSchema,
    EstadoTicket,
    ETicketField,
    TicketHistorialResponse,
    TicketSchema,
    TicketTareaSchema,
    UpdateTicketPayload,
)
from app.schemas.usuario import EUSerField, UsuarioSchema
from app.services.area import AreaService
from app.services.tarea import TareaService
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

    async def get_tickets_busqueda_avanzada(
        self,
        filters: dict = None,
    ):
        repo = TicketRepository(db=self.db)
        tickets = await repo.get_tickets_busqueda_avanzada(filters=filters)

        return parse_obj_as(list[TicketSchema], tickets) if tickets else []

    async def get_tareas_by_ticket_id(self, ticket_id: int):
        ticket_repo = TicketRepository(db=self.db)
        tareas = await ticket_repo.get_tareas_by_ticket_id(ticket_id=ticket_id)

        return parse_obj_as(list[TicketTareaSchema], tareas) if tareas else []

    async def create_new_ticket(self, tipo: ETipoPedido, payload: CreateTicketPayload, usuario: UsuarioSchema):
        ticket_repo = TicketRepository(db=self.db)
        area_service: AreaService = self.get_service("Area")

        area = await area_service.get_area_by_id(area_id=payload.area_asignada_id)

        # prefix = area.nombre[0:3].upper()
        prefix = tipo.value

        ticket = await ticket_repo.create_new_ticket(payload=payload, prefix=prefix)

        if ticket:
            # Se guarda el ticket con el estado inicial
            await ticket_repo.agregar_historial(
                payload=CreateTicketHistorialPayload(
                    ticket_id=ticket.id,
                    creado_por_id=usuario.id,
                    notas=f"{usuario.nombre.capitalize()} {usuario.apellido.capitalize()} creo el ticket",
                )
            )

        return parse_obj_as(TicketSchema, ticket) if ticket else None

    async def update_ticket(
        self, usuario: UsuarioSchema, ticket_id: int, payload: UpdateTicketPayload
    ):
        ticket_repo = TicketRepository(db=self.db)

        ticket_id = await ticket_repo.update_ticket(
            ticket_id=ticket_id, payload=payload
        )

        # Almacenando en historial informacion de los campos que se actualizaron
        if ticket_id:
            await ticket_repo.agregar_historial(
                payload=CreateTicketHistorialPayload(
                    ticket_id=ticket_id,
                    creado_por_id=usuario.id,
                    notas=f"{usuario.nombre.capitalize()} {usuario.apellido.capitalize()} actualizó el ticket",
                )
            )

        updated_ticket = await self.get_ticket_by_id(ticket_id=ticket_id)

        return updated_ticket

    async def get_ticket_by_id(self, ticket_id: int):
        repo = TicketRepository(db=self.db)
        ticket = await repo.get_ticket_by_id(ticket_id=ticket_id)

        return parse_obj_as(TicketSchema, ticket) if ticket else None

    async def anular_ticket(self, usuario: UsuarioSchema, ticket_id: int):
        repo = TicketRepository(db=self.db)
        ticket = await repo.anular_ticket_by_id(ticket_id=ticket_id)

        if ticket:
            # Registrando que el ticket se anulo
            await repo.agregar_historial(
                payload=CreateTicketHistorialPayload(
                    ticket_id=ticket_id,
                    creado_por_id=usuario.id,
                    notas=f"{usuario.nombre.capitalize()} {usuario.apellido.capitalize()} anuló el ticket",
                )
            )

        return parse_obj_as(TicketSchema, ticket) if ticket else None

    async def actualizar_estado_ticket(
        self, usuario: UsuarioSchema, ticket_id: int, estado: EstadoTicket
    ):
        repo = TicketRepository(db=self.db)

        ticket = await repo.actualizar_estado_ticket(ticket_id=ticket_id, estado=estado)

        if ticket:
            # Registrando que el ticket cambio de estado
            await repo.agregar_historial(
                payload=CreateTicketHistorialPayload(
                    ticket_id=ticket_id,
                    creado_por_id=usuario.id,
                    notas=f"{usuario.nombre.capitalize()} {usuario.apellido.capitalize()} cambio el estado del ticket a {estado}",
                )
            )

        return parse_obj_as(TicketSchema, ticket) if ticket else None

    async def derivar_ticket(self, usuario: UsuarioSchema, ticket: TicketSchema, area_id: int):
        repo = TicketRepository(db=self.db)

        area_service: AreaService = self.get_service("Area")
        area_anterior = await area_service.get_area_by_id(
            area_id=ticket.area_asignada_id
        )
        area_nueva = await area_service.get_area_by_id(area_id=area_id)

        ticket_derivado = await repo.derivar_ticket(
            ticket_id=ticket.id, area_id=area_id
        )

        if ticket_derivado:
            # Registrando que el ticket cambio de area
            await repo.agregar_historial(
                payload=CreateTicketHistorialPayload(
                    ticket_id=ticket.id,
                    area_anterior_id=ticket.area_asignada_id,
                    tecnico_anterior_id=ticket.tecnico_asignado_id,
                    creado_por_id=usuario.id,
                    notas=f"{usuario.nombre.capitalize()} {usuario.apellido.capitalize()} derivó el ticket del area {area_anterior.nombre} al area {area_nueva.nombre}",
                )
            )

        return parse_obj_as(TicketSchema, ticket_derivado) if ticket_derivado else None

    async def agregar_tarea(
        self, ticket: TicketSchema, tarea: TareaAreaSchema, usuario: UsuarioSchema
    ):
        repo = TicketRepository(db=self.db)

        tareas_ticket = await self.get_tareas_by_ticket_id(ticket_id=ticket.id)

        tarea_existente = next(
            filter(
                lambda tarea_ticket: (
                    tarea_ticket.estado == EEstadoTarea.ACTIVA
                    and tarea_ticket.tarea_id == tarea.id
                ),
                tareas_ticket,
            ),
            None,
        )

        if tarea_existente:
            return None

        payload = AddTareaTicketPayload(
            ticket_id=ticket.id,
            tarea_id=tarea.id,
            tecnico_id=ticket.tecnico_asignado_id,
        )

        ticket_tarea_relacion = await repo.agregar_tarea(payload=payload)

        if not ticket_tarea_relacion:
            return None
        else:
            # Registrando que al ticket se le asigno una tarea
            await repo.agregar_historial(
                payload=CreateTicketHistorialPayload(
                    ticket_id=ticket.id,
                    creado_por_id=usuario.id,
                    notas=f"{usuario.nombre.capitalize()} {usuario.apellido.capitalize()} asigno la tarea '{tarea.tarea}' al ticket",
                )
            )

        ticket_tarea_relacion_data = parse_obj_as(
            TicketTareaSchema, ticket_tarea_relacion
        )

        return EnrichedTicketTareaSchema(
            **ticket_tarea_relacion_data.dict(), tarea=tarea
        )

    async def finalizar_tarea(self, usuario: UsuarioSchema, ticket_id: int, tarea_id: int):
        repo = TicketRepository(db=self.db)

        ticket_tarea_relacion = await repo.finalizar_tarea(
            ticket_id=ticket_id, tarea_id=tarea_id
        )

        if ticket_tarea_relacion:
            # Registrando que el ticket finalizo
            await repo.agregar_historial(
                payload=CreateTicketHistorialPayload(
                    ticket_id=ticket_id,
                    creado_por_id=usuario.id,
                    notas=f"{usuario.nombre.capitalize()} {usuario.apellido.capitalize()} finalizó la tarea {tarea_id}",
                )
            )

        return (
            parse_obj_as(TicketTareaSchema, ticket_tarea_relacion)
            if ticket_tarea_relacion
            else None
        )

    async def eliminar_tarea(self, usuario: UsuarioSchema, ticket_id: int, tarea_id: int):
        repo = TicketRepository(db=self.db)

        ticket_tarea_id = await repo.eliminar_tarea(
            ticket_id=ticket_id, tarea_id=tarea_id
        )

        if ticket_tarea_id:
            # Registrando que la tarea se elimino del ticket y no perder este registro
            await repo.agregar_historial(
                payload=CreateTicketHistorialPayload(
                    ticket_id=ticket_id,
                    creado_por_id=usuario.id,
                    notas=f"{usuario.nombre.capitalize()} {usuario.apellido.capitalize()} eliminó la tarea {tarea_id}",
                )
            )

        return ticket_tarea_id if ticket_tarea_id else None

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
