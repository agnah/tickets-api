from enum import Enum


class PrioridadTicket(str, Enum):
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"

class EstadoTicket(str, Enum):
    NUEVO = "nuevo"
    ASIGNADO = "asignado"
    EN_CURSO = "en_curso"
    RECHAZADO = "rechazado"
    DERIVADO = "derivado"
    FINALIZADO = "finalizado"
