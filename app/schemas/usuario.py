from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr


class EUSerField(str, Enum):
    ID = "id"
    TOKEN = "token"
    EMAIL = "email"
    NOMBRE = "nombre"
    APELLIDO = "apellido"
    PERFIL = "perfil"
    ROL = "rol"


class PerfilUsuario(str, Enum):
    SOLICITANTE = "solicitante"
    RESPONSABLE_DE_AREA = "responsable_de_area"
    COLABORADOR = "colaborador"
    OPERADOR = "operador"


class RolUsuario(str, Enum):
    ADMINISTRADOR = "administrador"
    EDITOR = "editor"
    LECTOR = "lector"


class UsuarioSchema(BaseModel):
    id: int
    token: str

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

    fecha_creacion: datetime
    fecha_modificacion: datetime
    fecha_eliminacion: datetime = None

    class Config:
        orm_mode = True


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
