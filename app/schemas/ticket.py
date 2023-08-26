from datetime import datetime

from enum import Enum

from pydantic import BaseModel


class PrioridadTicket(str, Enum):
    ALTA = "alta"
    BAJA = "baja"


class EstadoTicket(str, Enum):
    PENDIENTE = "pendiente"
    EN_CURSO = "en_curso"
    FINALIZADO = "finalizado"
    DERIVADO = "derivado"
    ANULADO = "anulado"


class TicketSchema(BaseModel):
    id: int

    email_solicitante: str
    nombre_solicitante: str
    apellido_solicitante: str
    telefono_solicitante: str
    celular_solicitante: str
    area_solicitante: int
    piso_solicitante: str

    referencia: str
    area_asignada_id: int
    tecnico_asignado_id: int

    prioridad: PrioridadTicket
    estado: EstadoTicket

    descripcion: str

    pre_tarea: str

    archivos: str

    fecha_creacion: datetime
    fecha_modificacion: datetime
    fecha_eliminacion: datetime = None

    demorado: bool = False

    class Config:
        orm_mode = True
