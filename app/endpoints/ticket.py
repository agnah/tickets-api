from fastapi import APIRouter, Depends, HTTPException, Header, status
from pydantic import Required

from app.dependencies.service import get_ticket_service, get_usuario_service
from app.schemas.ticket import TicketSchema
from app.schemas.usuario import EUSerField
from app.services.ticket import TicketService
from app.services.usuario import UsuarioService

router = APIRouter()


@router.get("/")
async def get_last_months_tickets_by_user_id(
    token: str = Header(Required, alias="X-Token"),
    usuario_service: UsuarioService = Depends(get_usuario_service),
    tickets_service: TicketService = Depends(get_ticket_service)
) -> list[TicketSchema]:

    user = await usuario_service.get_user_by_field(field=EUSerField.TOKEN,value=token)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "Usuario no encontrado"},
        )

    tickets = await tickets_service.get_last_months_tickets_by_user(
        user_id=user.id
    )
    return tickets
