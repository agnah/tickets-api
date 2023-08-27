from datetime import datetime, timedelta

from pydantic import parse_obj_as
from app.repositories.ticket import TicketRepository
from app.schemas.ticket import ETicketField, TicketSchema
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
