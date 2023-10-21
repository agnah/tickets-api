from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from app.schemas.area import AreaSchema, AreasSolicitante, TareaAreaSchema
from app.schemas.usuario import UsuarioSchema


class ETicketField(str, Enum):
    ID = "id"
    IDENTIFICADOR = "identificador"

    EMAIL_SOLICITANTE = "email_solicitante"

    AREA_ASIGNADA_ID = "area_asignada_id"
    TECNICO_ASIGNADO_ID = "tecnico_asignado_id"

    PRIORIDAD = "prioridad"
    ESTADO = "estado"


class ESede(str, Enum):
    NUEVE_DE_JULIO = "nueve_de_julio"
    ANEXO1 = "anexo1"
    ANEXO2 = "anexo2"
    ANEXO3 = "anexo3"


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
    telefono_solicitante: str = None
    celular_solicitante: str = None
    area_solicitante: Optional[AreasSolicitante] = AreasSolicitante.ADMINISTRACION
    sede_solicitante: ESede = ESede.NUEVE_DE_JULIO
    piso_solicitante: str = None

    referencia: str = None
    area_asignada_id: int
    tecnico_asignado_id: int = None

    prioridad: Optional[PrioridadTicket] = PrioridadTicket.BAJA
    estado: Optional[EstadoTicket] = EstadoTicket.PENDIENTE

    descripcion: str

    archivos: str = None

    class Config:
        orm_mode = True


class UpdateTicketPayload(BaseModel):
    nombre_solicitante: str = None
    telefono_solicitante: str = None
    celular_solicitante: str = None
    area_solicitante: str = None
    sede_solicitante: Optional[ESede]
    piso_solicitante: str = None

    referencia: str = None

    tecnico_asignado_id: int = None

    prioridad: Optional[PrioridadTicket]
    estado: Optional[EstadoTicket]
    descripcion: str = None
    archivos: str = None

    class Config:
        orm_mode = True


class AddTareaTicketPayload(BaseModel):
    ticket_id: int
    tarea_id: int
    tecnico_id: int

    class Config:
        orm_mode = True


class TicketTareaSchema(BaseModel):
    id: int
    ticket_id: int
    tarea_id: int
    tecnico_id: int
    estado: str

    fecha_creacion: datetime
    fecha_modificacion: datetime
    fecha_eliminacion: datetime = None

    class Config:
        orm_mode = True

class EnrichedTicketTareaSchema(TicketTareaSchema):
    tarea: TareaAreaSchema


class TicketSchema(BaseModel):
    id: int
    identificador: str

    email_solicitante: str
    nombre_solicitante: str = None
    telefono_solicitante: str = None
    celular_solicitante: str = None
    sede_solicitante: Optional[ESede] = ESede.NUEVE_DE_JULIO
    area_solicitante: Optional[AreasSolicitante] = AreasSolicitante.ADMINISTRACION
    piso_solicitante: str = None

    referencia: str = None
    area_asignada_id: int
    tecnico_asignado_id: int = None

    prioridad: PrioridadTicket
    estado: EstadoTicket

    descripcion: str = None

    pre_tarea: str = None

    archivos: str = None

    fecha_creacion: datetime
    fecha_modificacion: datetime
    fecha_eliminacion: datetime = None

    demorado: bool = False

    class Config:
        orm_mode = True


class EnrichedTicketSchema(TicketSchema):
    tareas: list[TicketTareaSchema] = []
    tecnico: UsuarioSchema = None
    area: AreaSchema

class TicketHistorialSchema(BaseModel):
    ticket_id: int = None
    tarea_id: int = None
    tecnico_id: int = None
    estado: str = None

    fecha_creacion: datetime
    fecha_modificacion: datetime
    fecha_eliminacion: datetime = None

    class Config:
        orm_mode = True