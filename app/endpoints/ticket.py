from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import Required

from app.dependencies.service import (
    get_area_service,
    get_ticket_service,
    get_usuario_service,
)
from app.schemas.ticket import (
    CreateTicketHistorialPayload,
    CreateTicketPayload,
    EnrichedTicketSchema,
    EstadoTicket,
    ETicketField,
    TicketSchema,
    TicketTareaSchema,
    UpdateTicketPayload,
)
from app.schemas.usuario import EUSerField
from app.services.area import AreaService
from app.services.ticket import TicketService
from app.services.usuario import UsuarioService

router = APIRouter()


@router.get("/inicio/")
async def get_last_ten_days_tickets_by_user(
    token: str = Header(Required, alias="X-Token"),
    usuario_service: UsuarioService = Depends(get_usuario_service),
    tickets_service: TicketService = Depends(get_ticket_service),
) -> list[EnrichedTicketSchema]:
    user = await usuario_service.get_user_by_field(field=EUSerField.TOKEN, value=token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Usuario no encontrado"},
        )

    tickets = await tickets_service.get_last_ten_days_tickets()
    enriched_tickets = await tickets_service.enriching_tickets(tickets=tickets)
    return enriched_tickets


@router.get("/")
async def get_tickets_by_field(
    token: str = Header(Required, alias="X-Token"),
    field: ETicketField = ETicketField.ID,
    value: str = None,
    start_date: datetime = None,
    end_date: datetime = None,
    usuario_service: UsuarioService = Depends(get_usuario_service),
    tickets_service: TicketService = Depends(get_ticket_service),
) -> list[EnrichedTicketSchema]:
    user = await usuario_service.get_user_by_field(field=EUSerField.TOKEN, value=token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Usuario no encontrado"},
        )

    tickets = await tickets_service.get_tickets_by_field_in_date_range(
        field=field, value=value, start_date=start_date, end_date=end_date
    )

    enriched_tickets = await tickets_service.enriching_tickets(tickets=tickets)

    return enriched_tickets


@router.get("/busqueda-avanzada/")
async def get_tickets_busqueda_avanzada(
    token: str = Header(Required, alias="X-Token"),
    start_date: datetime = None,
    end_date: datetime = None,
    identificador: str = None,
    area_solicitante: str = None,
    email_solicitante: str = None,
    descripcion: str = None,
    nombre_solicitante: str = None,
    usuario_service: UsuarioService = Depends(get_usuario_service),
    tickets_service: TicketService = Depends(get_ticket_service),
):
    user = await usuario_service.get_user_by_field(field=EUSerField.TOKEN, value=token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Usuario no encontrado"},
        )

    filters = {
        "start_date": start_date,
        "end_date": end_date,
        "identificador": identificador,
        "area_solicitante": area_solicitante,
        "email_solicitante": email_solicitante,
        "descripcion": descripcion,
        "nombre_solicitante": nombre_solicitante,
    }

    # Elimino los filtros que no tienen valor
    filters = {k: v for k, v in filters.items() if v is not None}

    tickets = await tickets_service.get_tickets_busqueda_avanzada(filters=filters)

    enriched_tickets = await tickets_service.enriching_tickets(tickets=tickets)

    return enriched_tickets


@router.post("/")
async def create_new_ticket(
    payload: CreateTicketPayload,
    ticket_service: TicketService = Depends(get_ticket_service),
) -> Optional[TicketSchema]:
    ticket = await ticket_service.create_new_ticket(payload=payload)

    return ticket


@router.patch("/actualizaciones/{ticket_id}/")
async def update_ticket(
    ticket_id: int,
    payload: UpdateTicketPayload,
    usuario_id: int = Header(Required, alias="X-Usuario"),
    ticket_service: TicketService = Depends(get_ticket_service),
    usuario_service: UsuarioService = Depends(get_usuario_service),
) -> TicketSchema:
    usuario = await usuario_service.get_user_by_field(
        field=EUSerField.ID, value=usuario_id
    )
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Usuario no encontrado"},
        )

    updated_ticket = await ticket_service.update_ticket(
        ticket_id=ticket_id, payload=payload, usuario_id=usuario.id
    )
    if not updated_ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Ticket no encontrado"},
        )

    return updated_ticket


@router.delete("/{ticket_id}/")
async def anular_ticket(
    ticket_id: int,
    usuario_id: int = Header(Required, alias="X-Usuario"),
    ticket_service: TicketService = Depends(get_ticket_service),
    usuario_service: UsuarioService = Depends(get_usuario_service),
) -> TicketSchema:
    usuario = await usuario_service.get_user_by_field(
        field=EUSerField.ID, value=usuario_id
    )
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Usuario no encontrado"},
        )

    ticket = await ticket_service.anular_ticket(
        usuario_id=usuario.id, ticket_id=ticket_id
    )
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Ticket no encontrado"},
        )

    return ticket


@router.patch("/finalizar/{ticket_id}/")
async def cerrar_ticket(
    ticket_id: int,
    usuario_id: int = Header(Required, alias="X-Usuario"),
    ticket_service: TicketService = Depends(get_ticket_service),
    usuario_service: UsuarioService = Depends(get_usuario_service),
) -> TicketSchema:
    usuario = await usuario_service.get_user_by_field(
        field=EUSerField.ID, value=usuario_id
    )
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Usuario no encontrado"},
        )

    ticket = await ticket_service.actualizar_estado_ticket(
        usuario_id=usuario.id, ticket_id=ticket_id, estado=EstadoTicket.FINALIZADO
    )
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Ticket no encontrado"},
        )

    return ticket


@router.patch("/derivaciones/{ticket_id}/")
async def derivar_ticket(
    ticket_id: int,
    area_id: int,
    usuario_id: int = Header(Required, alias="X-Usuario"),
    ticket_service: TicketService = Depends(get_ticket_service),
    usuario_service: UsuarioService = Depends(get_usuario_service),
) -> TicketSchema:
    usuario = await usuario_service.get_user_by_field(
        field=EUSerField.ID, value=usuario_id
    )
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Usuario no encontrado"},
        )

    ticket = await ticket_service.derivar_ticket(
        usuario_id=usuario.id, ticket_id=ticket_id, area_id=area_id
    )
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Ticket no encontrado"},
        )

    return ticket


@router.post("/{ticket_id}/tareas/")
async def agregar_tarea(
    ticket_id: int,
    tarea: str,
    usuario_id: int = Header(Required, alias="X-Usuario"),
    ticket_service: TicketService = Depends(get_ticket_service),
    usuario_service: UsuarioService = Depends(get_usuario_service),
    area_service: AreaService = Depends(get_area_service),
) -> Optional[TicketTareaSchema]:
    usuario = await usuario_service.get_user_by_field(
        field=EUSerField.ID, value=usuario_id
    )
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Usuario no encontrado"},
        )

    ticket = await ticket_service.get_ticket_by_id(ticket_id=ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Ticket no encontrado"},
        )

    """
    if usuario.id != ticket.tecnico_asignado_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Usuario no autorizado a agregar tareas a este ticket"},
        )
    """

    if not ticket.tecnico_asignado_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "No se puede agregar tareas a un ticket sin tecnico asignado"
            },
        )

    area_tareas = await area_service.get_all_tareas_by_area_id(
        area_id=ticket.area_asignada_id
    )
    tarea_a_agregar = next(
        (
            area_tarea
            for area_tarea in area_tareas
            if (area_tarea.tarea).upper() == (tarea.upper())
        ),
        None,
    )
    if not tarea_a_agregar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "Tarea no encontrada para el area que el ticket tiene asignada"
            },
        )

    ticket_tarea_relation = await ticket_service.agregar_tarea(
        ticket=ticket, tarea=tarea_a_agregar
    )

    if not ticket_tarea_relation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "No se agrego la tarea al ticket o la tarea ya existe en el ticket"
            },
        )

    return ticket_tarea_relation


@router.get("/tareas/{ticket_id}/")
async def get_tareas_by_ticket_id(
    ticket_id: int,
    token: str = Header(Required, alias="X-Token"),
    usuario_service: UsuarioService = Depends(get_usuario_service),
    tickets_service: TicketService = Depends(get_ticket_service),
) -> list[EnrichedTicketSchema]:
    user = await usuario_service.get_user_by_field(field=EUSerField.TOKEN, value=token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Usuario no encontrado"},
        )

    ticket = await tickets_service.get_ticket_by_id(ticket_id=ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Ticket no encontrado"},
        )

    enriched_ticket = await tickets_service.enriching_tickets(tickets=[ticket])

    return enriched_ticket


@router.patch("/{ticket_id}/tareas/{tarea_id}/")
async def finalizar_tarea(
    ticket_id: int,
    tarea_id: int,
    usuario_id: int = Header(Required, alias="X-Usuario"),
    ticket_service: TicketService = Depends(get_ticket_service),
    usuario_service: UsuarioService = Depends(get_usuario_service),
) -> Optional[TicketTareaSchema]:
    usuario = await usuario_service.get_user_by_field(
        field=EUSerField.ID, value=usuario_id
    )
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Usuario no encontrado"},
        )

    ticket = await ticket_service.get_ticket_by_id(ticket_id=ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Ticket no encontrado"},
        )

    ticket_tarea_relation = await ticket_service.finalizar_tarea(
        usuario_id=usuario.id, ticket_id=ticket_id, tarea_id=tarea_id
    )

    return ticket_tarea_relation


@router.delete("/{ticket_id}/tareas/{tarea_id}/")
async def eliminar_tarea(
    ticket_id: int,
    tarea_id: int,
    usuario_id: int = Header(Required, alias="X-Usuario"),
    ticket_service: TicketService = Depends(get_ticket_service),
    usuario_service: UsuarioService = Depends(get_usuario_service),
) -> Optional[TicketTareaSchema]:
    usuario = await usuario_service.get_user_by_field(
        field=EUSerField.ID, value=usuario_id
    )

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Usuario no encontrado"},
        )

    ticket = await ticket_service.get_ticket_by_id(ticket_id=ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Ticket no encontrado"},
        )

    ticket_tarea_id = await ticket_service.eliminar_tarea(
        usuario_id=usuario.id, ticket_id=ticket_id, tarea_id=tarea_id
    )

    if ticket_tarea_id:
        return jsonable_encoder(
            {
                "ticket_tarea_id": ticket_tarea_id,
                "detail": f"La tarea con id={tarea_id} ha sido eliminada del ticket con id={ticket_id}.",
            }
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Tarea no encontrada en el ticket"},
        )


@router.get("/{ticket_id}/historial")
async def get_historial_by_ticket_id(
    ticket_id: int,
    ticket_service: TicketService = Depends(get_ticket_service),
) -> list[EnrichedTicketSchema]:
    historial = await ticket_service.get_historial_by_ticket_id(ticket_id=ticket_id)

    if not historial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Historial no encontrado"},
        )

    return historial


@router.post("/{ticket_id}/historial")
async def agregar_historial(
    ticket_id: int,
    payload: CreateTicketHistorialPayload,
    ticket_service: TicketService = Depends(get_ticket_service),
) -> list[EnrichedTicketSchema]:
    ticket = await ticket_service.get_ticket_by_id(ticket_id=ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Ticket no encontrado"},
        )

    historial = await ticket_service.agregar_historial(
        ticket_id=ticket_id, payload=payload
    )

    if not historial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "No se agrego el historial"},
        )

    return historial
