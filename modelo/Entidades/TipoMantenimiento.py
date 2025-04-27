from enum import Enum, auto

class TipoMantenimiento(Enum):
    """
    Enum que define los tipos de mantenimiento disponibles.
    """
    PREVENTIVO = auto()
    CORRECTIVO = auto()
