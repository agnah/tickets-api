from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Header, status
from pydantic import Required

from app.dependencies.service import get_ticket_service, get_usuario_service
from app.schemas.ticket import CreateTicketPayload, EstadoTicket, TicketSchema
from app.schemas.usuario import EUSerField
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
):
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
):
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
):
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
