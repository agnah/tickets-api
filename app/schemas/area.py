from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class EAreaField(str, Enum):
    ID = "id"


class EPreTareas(str, Enum):
    TAREA1 = "tarea1"
    TAREA2 = "tarea2"
    TAREA3 = "tarea3"


class NombreArea(str, Enum):
    COMPUTOS = "computos"
    TELEFONIA = "telefonia"
    SOPORTE_TECNICO = "soporte_tecnico"
    CID = "cid"
    GDE = "gde"


class AreaSchema(BaseModel):
    id: int
    nombre: NombreArea

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
