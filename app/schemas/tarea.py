from enum import Enum


class EEstadoTarea(str, Enum):
    ACTIVA = "ACTIVA"
    FINALIZADA = "FINALIZADA"