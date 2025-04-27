from enum import Enum, auto

class EstadoTarea(Enum):
    """
    Enum que define los tipos de mantenimiento disponibles.
    """
    PENDIENTE = auto()
    EN_PROCESO = auto()
    COMPLETADA = auto()
    CANCELADA = auto()
