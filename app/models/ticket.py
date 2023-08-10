from sqlalchemy import Boolean, Column, Enum, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.schemas.ticket import PrioridadTicket, EstadoTicket


from .base import Base, UnsignedInt


class Ticket(Base):
    __tablename__ = "ticket"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(UnsignedInt, autoincrement=True, primary_key=True)
    prioridad = Column(Enum(PrioridadTicket), nullable=False)
    estado = Column(Enum(EstadoTicket), nullable=False)
    # sector_id = Column(UnsignedInt, ForeignKey("sector.id"), nullable=False)
    adjuntos = Column(Text(1048576), nullable=False)  # 1MiB
    referencia = Column(String(256), nullable=False)
    solicitante_id = Column(UnsignedInt, ForeignKey("usuario.id"), nullable=False)
    nro_gde = Column(UnsignedInt, nullable=False)
    observaciones = Column(Text(1048576), nullable=False)  # 1MiB

    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_modificacion = Column(
        DateTime, server_default=func.now(), server_onupdate=func.now())
    fecha_eliminacion = Column(DateTime, default=None)

    # sector = relationship("Sector")
    usuario = relationship("Usuario")


class TicketAreaRelation(Base):
    __tablename__ = "ticket_area_relation"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(UnsignedInt, autoincrement=True, primary_key=True)
    ticket_id = Column(UnsignedInt, ForeignKey("ticket.id"), nullable=False)
    area_id = Column(UnsignedInt, ForeignKey("area.id"), nullable=False)
    area_asignada_id = Column(UnsignedInt, ForeignKey("area.id"), nullable=False)

    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_modificacion = Column(
        DateTime, server_default=func.now(), server_onupdate=func.now())
    fecha_eliminacion = Column(DateTime, default=None)

    ticket = relationship("Ticket")
    area = relationship("Area")
