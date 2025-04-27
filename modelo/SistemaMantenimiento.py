from typing import List

from modelo.Entidades.Equipo import Equipo
from modelo.Entidades.TareaMantenimiento import TareaMantenimiento
from modelo.Entidades.Tecnico import Tecnico
from modelo.Entidades.Ubicacion import Ubicacion


class SistemaMantenimiento:
    """
        Clase principal que gestiona los equipos, técnicos, tareas y ubicaciones del sistema.
    """

    def __init__(self):
        """
                Inicializador de la clase SistemaMantenimiento.
        """
        self.equipos: List[Equipo] = []
        self.tecnicos: List[Tecnico] = []
        self.tareas: List[TareaMantenimiento] = []
        self.ubicaciones: List[Ubicacion] = []

    def agregar_equipo(self, equipo: Equipo):
        """
        Agrega un equipo al sistema.

        :param equipo: Instancia de la clase Equipo.
        """
        self.equipos.append(equipo)

    def agregar_tecnico(self, tecnico: Tecnico):
        """
        Agrega un técnico al sistema.

        :param tecnico: Instancia de la clase Tecnico.
        """
        self.tecnicos.append(tecnico)

    def agregar_tarea(self, tarea: TareaMantenimiento):
        """
        Agrega una tarea de mantenimiento al sistema.

        :param tarea: Instancia de la clase TareaMantenimiento.
        """
        self.tareas.append(tarea)

    def agregar_ubicacion(self, ubicacion: Ubicacion):
        """
        Agrega una ubicación al sistema.

        :param ubicacion: Instancia de la clase Ubicacion.
        """
        self.ubicaciones.append(ubicacion)
