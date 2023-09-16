from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Header, status
from pydantic import Required

from app.dependencies.service import get_ticket_service, get_usuario_service
from app.schemas.ticket import CreateTicketPayload, TicketSchema
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