from enum import Enum


class PrioridadTicket(str, Enum):
    ALTA = "alta"
    BAJA = "baja"


class EstadoTicket(str, Enum):
    PENDIENTE = "pendiente"
    EN_CURSO = "en_curso"
    FINALIZADO = "finalizado"
    DERIVADO = "derivado"
    ANULADO = "anulado"
