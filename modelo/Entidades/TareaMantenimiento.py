from datetime import datetime
from typing import Optional

from modelo.Entidades.Equipo import Equipo
from modelo.Entidades.EstadoTarea import EstadoTarea
from modelo.Entidades.Tecnico import Tecnico
from modelo.Entidades.TipoMantenimiento import TipoMantenimiento


class TareaMantenimiento:
    """
        Clase que representa una tarea de mantenimiento asignada a un equipo.
    """

    def __init__(self, id: str, tipo: TipoMantenimiento, equipo: Equipo,
                 fecha_programada: datetime, tecnico_asignado: Tecnico,
                 estado: EstadoTarea = EstadoTarea.PENDIENTE,
                 observaciones: str = "", fecha_realizacion: Optional[datetime] = None,
                 duracion_minutos: Optional[int] = None):
        """
                Inicializador de la clase TareaMantenimiento.

                :param id: Identificador único de la tarea.
                :param tipo: Tipo de mantenimiento (PREVENTIVO o CORRECTIVO).
                :param equipo: Equipo al que se le realizará el mantenimiento.
                :param fecha_programada: Fecha programada para realizar la tarea.
                :param tecnico_asignado: Técnico asignado a la tarea.
                :param estado: Estado actual de la tarea.
                :param observaciones: Observaciones adicionales sobre la tarea.
                :param fecha_realizacion: Fecha en la que se realizó la tarea (opcional).
                :param duracion_minutos: Duración de la tarea en minutos (opcional).
        """
        self.id = id
        self.tipo = tipo
        self.equipo = equipo
        self.fecha_programada = fecha_programada
        self.tecnico_asignado = tecnico_asignado
        self.estado = EstadoTarea.PENDIENTE
        self.observaciones = observaciones
        self.fecha_realizacion = fecha_realizacion
        self.duracion_minutos = duracion_minutos
