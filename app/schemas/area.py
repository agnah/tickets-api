from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class EAreaField(str, Enum):
    ID = "id"


class EPreTareas(str, Enum):
    TAREA1 = "tarea1"
    TAREA2 = "tarea2"
    TAREA3 = "tarea3"


class AreaAsignar(str, Enum):
    GDE = "gde"
    COMPUTOS = "computos"
    SOPORTE = "soporte"
    TELEFONIA = "telefonia"
    SISTEMAS = "sistemas"


class AreasSolicitante(str, Enum):
    ADMINISTRACION = "administracion"
    RRHH = "rrhh"
    CONTABILIDAD = "contabilidad"
    LEGALES = "legales"


class AreaSchema(BaseModel):
    id: int
    nombre: AreaAsignar

    fecha_creacion: datetime
    fecha_modificacion: datetime
    fecha_eliminacion: datetime = None

    class Config:
        orm_mode = True


class TareaAreaSchema(BaseModel):
    id: int
    tarea: str
    area_id: int

    fecha_creacion: datetime
    fecha_modificacion: datetime
    fecha_eliminacion: datetime = None

    class Config:
        orm_mode = True


class TareaAreaResponse(BaseModel):
    id: int
    tarea: str

    class Config:
        orm_mode = True


class AreaResponse(BaseModel):
    id: int
    nombre: AreaAsignar
    tareas: Optional[list[TareaAreaResponse]] = []

    class Config:
        orm_mode = True
