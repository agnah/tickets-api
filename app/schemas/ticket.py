from datetime import datetime

from enum import Enum

from pydantic import BaseModel

from app.schemas.area import EPreTareas


class ETicketField(str, Enum):
    ID = "id"

    EMAIL_SOLICITANTE = "email_solicitante"

    AREA_ASIGNADA_ID = "area_asignada_id"
    TECNICO_ASIGNADO_ID = "tecnico_asignado_id"

    PRIORIDAD = "prioridad"
    ESTADO = "estado"


class PrioridadTicket(str, Enum):
    ALTA = "alta"
    BAJA = "baja"


class EstadoTicket(str, Enum):
    PENDIENTE = "pendiente"
    EN_CURSO = "en_curso"
    FINALIZADO = "finalizado"
    DERIVADO = "derivado"
    ANULADO = "anulado"


class CreateTicketPayload(BaseModel):
    email_solicitante: str
    nombre_solicitante: str = None
    apellido_solicitante: str = None
    telefono_solicitante: str = None
    celular_solicitante: str = None
    area_solicitante: int = None
    piso_solicitante: str = None

    referencia: str
    area_asignada_id: int
    tecnico_asignado_id: int

    prioridad: PrioridadTicket
    estado: EstadoTicket

    descripcion: str

    pre_tarea: EPreTareas

    archivos: str = None

    class Config:
        orm_mode = True


class TicketSchema(BaseModel):
    id: int

    email_solicitante: str
    nombre_solicitante: str = None
    apellido_solicitante: str = None
    telefono_solicitante: str = None
    celular_solicitante: str = None
    area_solicitante: int = None
    piso_solicitante: str = None

    referencia: str
    area_asignada_id: int
    tecnico_asignado_id: int

    prioridad: PrioridadTicket
    estado: EstadoTicket

    descripcion: str

    pre_tarea: str

    archivos: str = None

    fecha_creacion: datetime
    fecha_modificacion: datetime
    fecha_eliminacion: datetime = None

    demorado: bool = False

    class Config:
        orm_mode = True
