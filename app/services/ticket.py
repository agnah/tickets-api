from datetime import datetime, timedelta

from pydantic import parse_obj_as
from app.repositories.ticket import TicketRepository
from app.schemas.ticket import TicketSchema
from app.schemas.usuario import EUSerField
from .layer import register_service, ServiceLayer


@register_service("Ticket")
class TicketService(ServiceLayer):

    async def get_last_months_tickets_by_user(
        self,
        user_id: int,
    ) -> list[TicketSchema]:

        repo = TicketRepository(db=self.db)
        tickets = await repo.get_last_months_tickets_by_user(
            user_id=user_id
        )

        # tickets = [ ticket.__setattr__('demorado',True) for ticket in tickets if(datetime.now() > (ticket.fecha_creacion + timedelta(days=3)))]


        return parse_obj_as(list[TicketSchema], tickets)
