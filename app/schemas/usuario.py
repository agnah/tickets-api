from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class EUSerField(str, Enum):
    ID = "id"
    TOKEN = "token"
    EMAIL = "email"
    NOMBRE_APELLIDO = "nombre_apellido"
    PERFIL = "perfil"
    ROL = "rol"


class PerfilUsuario(str, Enum):
    ADMINISTRADOR = 'administrador'
    TECNICO = 'tecnico'
    ADMINISTRATIVO = 'administrativo'
    SUPERADMIN = 'superadmin'


class RolUsuario(str, Enum):
    DIOS = "dios"
    ADMIN = "admin"
    EDITOR = "editor"
    LECTOR = "lector"


class UsuarioSchema(BaseModel):
    id: int
    token: str

    nombre: str
    apellido: str
    email: str
    celular: str = None
    telefono: str = None
    interno: str = None

    area_id: int
    sede: str
    piso: str = None

    perfil: PerfilUsuario
    rol: RolUsuario

    fecha_creacion: datetime
    fecha_modificacion: datetime
    fecha_eliminacion: datetime = None

    class Config:
        orm_mode = True


class CreateUsuarioPayload(BaseModel):
    nombre: str
    apellido: str
    email: str
    celular: str
    telefono: str
    interno: str

    area_id: int
    piso: str

    perfil: PerfilUsuario
    rol: RolUsuario

    token: str


class UpdateUsuarioPayload(BaseModel):
    nombre: str = None
    apellido: str = None
    email: str = None
    celular: str = None
    telefono: str = None
    interno: str = None

    area_id: int = None
    piso: str = None

    perfil: PerfilUsuario = None
    rol: RolUsuario = None
