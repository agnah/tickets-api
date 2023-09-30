from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Header, status
from pydantic import Required

from app.dependencies.service import get_area_service, get_ticket_service, get_usuario_service
from app.schemas.ticket import CreateTicketPayload, EstadoTicket, TicketSchema
from app.schemas.usuario import EUSerField
from app.services.area import AreaService
from app.services.ticket import TicketService
from app.services.usuario import UsuarioService

router = APIRouter()


@router.get("/inicio/")
async def get_last_months_tickets_by_user(
    token: str = Header(Required, alias="X-Token"),
    usuario_service: UsuarioService = Depends(get_usuario_service),
    tickets_service: TicketService = Depends(get_ticket_service)
) -> list[TicketSchema]:

    user = await usuario_service.get_user_by_field(field=EUSerField.TOKEN, value=token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Usuario no encontrado"},
        )

    tickets = await tickets_service.get_last_months_tickets_by_user(
        user_id=user.id
    )
    return tickets


@router.get("/")
async def get_tickets_by_field(
    field: str = None,
    value: str = None,
    start_date: datetime = None,
    end_date: datetime = None,
    tickets_service: TicketService = Depends(get_ticket_service)
) -> list[TicketSchema]:

    tickets = await tickets_service.get_tickets_by_field_in_date_range(
        field=field,
        value=value,
        start_date=start_date,
        end_date=end_date
    )

    return tickets


@router.post("/")
async def create_new_ticket(
    payload: CreateTicketPayload,
    ticket_service: TicketService = Depends(get_ticket_service)
):
    ticket = await ticket_service.create_new_ticket(
        payload=payload
    )

    return ticket


@router.delete("/{ticket_id}/")
async def anular_ticket(
    ticket_id: int,
    usuario_id: int = Header(Required, alias="X-Usuario"),
    ticket_service: TicketService = Depends(get_ticket_service),
    usuario_service: UsuarioService = Depends(get_usuario_service),
) -> TicketSchema:
    usuario = await usuario_service.get_user_by_field(
        field=EUSerField.ID, value=usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Usuario no encontrado"},
        )
    if usuario.rol not in ["administrador", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Usuario no autorizado"},
        )

    ticket = await ticket_service.anular_ticket(
        ticket_id=ticket_id
    )
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Ticket no encontrado"},
        )

    return ticket


@router.patch("/{ticket_id}/")
async def cerrar_ticket(
    ticket_id: int,
    usuario_id: int = Header(Required, alias="X-Usuario"),
    ticket_service: TicketService = Depends(get_ticket_service),
    usuario_service: UsuarioService = Depends(get_usuario_service),
) -> TicketSchema:
    usuario = await usuario_service.get_user_by_field(
        field=EUSerField.ID, value=usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Usuario no encontrado"},
        )
    if usuario.rol not in ["administrador", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Usuario no autorizado"},
        )

    ticket = await ticket_service.actualizar_estado_ticket(ticket_id=ticket_id, estado=EstadoTicket.ANULADO)
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
        field=EUSerField.ID, value=usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Usuario no encontrado"},
        )
    if usuario.rol not in ["administrador", "editor"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Usuario no autorizado"},
        )

    ticket = await ticket_service.derivar_ticket(
        ticket_id=ticket_id, area_id=area_id
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
):
    usuario = await usuario_service.get_user_by_field(
        field=EUSerField.ID, value=usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Usuario no encontrado"}
        )

    ticket = await ticket_service.get_ticket_by_id(ticket_id=ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Ticket no encontrado"}
        )

    tareas = await area_service.get_all_tareas_by_area_id(area_id=ticket.area_id)
    tarea_a_agregar = next((tarea for tarea in tareas if tarea.tarea == tarea), None)
    if not tarea_a_agregar:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": f"Tarea no encontrada para el area que el ticket tiene asignada"},
        )

    ticket_tarea_relation = await ticket_service.agregar_tarea(ticket=ticket, tarea=tarea_a_agregar)

    return ticket_tarea_relation

@router.patch("/{ticket_id}/tareas/{tarea_id}/")
async def finalizar_tarea(
    ticket_id: int,
    tarea_id: int,
    usuario_id: int = Header(Required, alias="X-Usuario"),
    ticket_service: TicketService = Depends(get_ticket_service),
    usuario_service: UsuarioService = Depends(get_usuario_service),
    area_service: AreaService = Depends(get_area_service),
):
    usuario = await usuario_service.get_user_by_field(
        field=EUSerField.ID, value=usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Usuario no encontrado"}
        )

    ticket = await ticket_service.get_ticket_by_id(ticket_id=ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Ticket no encontrado"}
        )

    ticket_tarea_relation = await ticket_service.finalizar_tarea(ticket=ticket, tarea_id=tarea_id)

    return ticket_tarea_relation