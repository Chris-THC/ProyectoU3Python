from datetime import datetime

from modelo.Entidades.Identificable import Identificable
from modelo.Entidades.Mantenible import Mantenible
from modelo.Entidades.Ubicacion import Ubicacion


# Clase Equipo con herencia múltiple
class Equipo(Identificable, Mantenible):
    """
        Clase que representa un equipo que puede requerir mantenimiento.
    """

    def __init__(self, id: str, nombre: str, ubicacion: Ubicacion,
                 fecha_instalacion: datetime, horas_uso: int = 0,
                 horas_mantenimiento: int = 100):
        """
                Inicializador de la clase Equipo.

                :param id: Identificador único del equipo.
                :param nombre: Nombre del equipo.
                :param ubicacion: Ubicación del equipo.
                :param fecha_instalacion: Fecha de instalación del equipo.
                :param horas_uso: Horas de uso acumuladas del equipo.
                :param horas_mantenimiento: Horas de uso requeridas para mantenimiento.
        """
        self._id = id
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.fecha_instalacion = fecha_instalacion
        self.horas_uso = horas_uso
        self.horas_mantenimiento = horas_mantenimiento

    @property
    def id(self) -> str:
        """
                Devuelve el identificador único del equipo.
        """
        return self._id

    def necesita_mantenimiento(self) -> bool:
        """
                Indica si el equipo necesita mantenimiento basado en las horas de uso.
        """
        return self.horas_uso >= self.horas_mantenimiento
