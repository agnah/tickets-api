from .base import Base, get_database_session

from .ticket import Ticket, TicketTareaRelacion, TicketHistorial
from .usuario import Usuario
from .area import Area

SessionLocal = get_database_session()

__all__ = [
    "Base",
    "SessionLocal",
    "Ticket",
    "TicketTareaRelacion",
    "TicketHistorial",
    "Usuario",
    "Area",
]
