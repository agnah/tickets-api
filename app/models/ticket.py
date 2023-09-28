from sqlalchemy import Boolean, Column, Enum, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.schemas.area import EPreTareas
from app.schemas.tarea import EEstadoTarea

from app.schemas.ticket import PrioridadTicket, EstadoTicket


from .base import Base, UnsignedInt


class Ticket(Base):
    __tablename__ = "ticket"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(UnsignedInt, autoincrement=True, primary_key=True)

    email_solicitante = Column(String(256), nullable=True)
    nombre_solicitante = Column(String(256), nullable=True)
    apellido_solicitante = Column(String(256), nullable=True)
    telefono_solicitante = Column(String(256), nullable=True)
    celular_solicitante = Column(String(256), nullable=True)
    area_solicitante = Column(UnsignedInt, ForeignKey("area.id"), nullable=True)
    # sede_solicitante = Column(Enum(ESede))  # TODO: Completar una vez que nos pasen los datos
    piso_solicitante = Column(String(256), nullable=True)

    referencia = Column(String(256), nullable=True)
    area_asignada_id = Column(UnsignedInt, ForeignKey("area.id"), nullable=False)
    tecnico_asignado_id = Column(UnsignedInt, ForeignKey("usuario.id"), nullable=False)

    prioridad = Column(Enum(PrioridadTicket), nullable=False,
                       default=PrioridadTicket.BAJA)
    estado = Column(Enum(EstadoTicket), nullable=False, default=EstadoTicket.PENDIENTE)

    descripcion = Column(Text(1048576), nullable=False)  # 1MiB

    pre_tarea = Column(Enum(EPreTareas), nullable=False)

    archivos = Column(String(256), nullable=True)

    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_modificacion = Column(
        DateTime, server_default=func.now(), server_onupdate=func.now())
    fecha_eliminacion = Column(DateTime, default=None)


class TicketTareaRelacion(Base):
    __tablename__ = "ticket_tarea_relacion"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(UnsignedInt, autoincrement=True, primary_key=True)
    ticket_id = Column(UnsignedInt, ForeignKey("ticket.id"), nullable=False)
    area_id = Column(UnsignedInt, ForeignKey("area.id"), nullable=False)

    tarea = Column(Enum(EPreTareas), nullable=False)

    tecnico_id = Column(UnsignedInt, ForeignKey("usuario.id"), nullable=False)

    estado = Column(Enum(EEstadoTarea), nullable=False, default=EEstadoTarea.ACTIVA)

    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_modificacion = Column(
        DateTime, server_default=func.now(), server_onupdate=func.now())
    fecha_eliminacion = Column(DateTime, default=None)

    ticket = relationship("Ticket")
    area = relationship("Area")


class TicketHistorial(Base):
    __tablename__ = "ticket_historial"
    __mapper_args__ = {"eager_defaults": True}

    id = Column(UnsignedInt, autoincrement=True, primary_key=True)

    ticket_id = Column(UnsignedInt, ForeignKey("ticket.id"), nullable=False)

    registro_anterior_id = Column(UnsignedInt, ForeignKey(
        "ticket_historial.id"), nullable=True)
    area_anterior_id = Column(UnsignedInt, ForeignKey("area.id"), nullable=True)
    tecnico_anterior_id = Column(UnsignedInt, ForeignKey("usuario.id"), nullable=True)

    notas = Column(Text(1048576), nullable=True)  # 1MiB
    creado_por_id = Column(UnsignedInt, ForeignKey("usuario.id"), nullable=False)

    fecha_creacion = Column(DateTime, server_default=func.now())
    fecha_modificacion = Column(
        DateTime, server_default=func.now(), server_onupdate=func.now())
