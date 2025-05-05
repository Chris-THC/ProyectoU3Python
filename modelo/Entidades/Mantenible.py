from abc import ABC, abstractmethod


class Mantenible(ABC):
    """
    Interfaz abstracta que define el comportamiento de los objetos que requieren mantenimiento.
    """

    @abstractmethod
    def necesita_mantenimiento(self) -> bool:
        """
        Indica si el objeto necesita mantenimiento.
        """
        pass
