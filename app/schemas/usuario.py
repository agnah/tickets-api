from enum import Enum


class PerfilUsuario(str, Enum):
    SOLICITANTE = "solicitante"
    RESPONSABLE_DE_AREA = "responsable_de_area"
    COLABORADOR = "colaborador"
    OPERADOR = "operador"


class RolUsuario(str, Enum):
    ADMINISTRADOR = "administrador"
    EDITOR = "editor"
    LECTOR = "lector"
