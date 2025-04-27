from abc import ABC, abstractmethod

class Identificable(ABC):
    """
    Interfaz abstracta que define un identificador único para las clases que la implementen.
    """

    @property
    @abstractmethod
    def id(self) -> str:
        """
        Devuelve el identificador único de la instancia.
        """
        pass
