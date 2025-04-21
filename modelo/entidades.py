from datetime import datetime
from enum import Enum, auto
from typing import List, Optional

class TipoMantenimiento(Enum):
    PREVENTIVO = auto()
    CORRECTIVO = auto()

class EstadoTarea(Enum):
    PENDIENTE = auto()
    EN_PROCESO = auto()
    COMPLETADA = auto()
    CANCELADA = auto()

class Ubicacion:
    def __init__(self, id: str, nombre: str, descripcion: str = ""):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion

class Equipo:
    def __init__(self, id: str, nombre: str, ubicacion: Ubicacion,
                 fecha_instalacion: datetime, horas_uso: int = 0,
                 horas_mantenimiento: int = 100):
        self.id = id
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.fecha_instalacion = fecha_instalacion
        self.horas_uso = horas_uso
        self.horas_mantenimiento = horas_mantenimiento

class Tecnico:
    def __init__(self, id: str, nombre: str, especialidad: str, activo: bool = True):
        self.id = id
        self.nombre = nombre
        self.especialidad = especialidad
        self.activo = activo

class TareaMantenimiento:
    def __init__(self, id: str, tipo: TipoMantenimiento, equipo: Equipo,
                 fecha_programada: datetime, tecnico_asignado: Tecnico,
                 estado: EstadoTarea = EstadoTarea.PENDIENTE,
                 observaciones: str = "", fecha_realizacion: Optional[datetime] = None,
                 duracion_minutos: Optional[int] = None):
        self.id = id
        self.tipo = tipo
        self.equipo = equipo
        self.fecha_programada = fecha_programada
        self.tecnico_asignado = tecnico_asignado
        self.estado = estado
        self.observaciones = observaciones
        self.fecha_realizacion = fecha_realizacion
        self.duracion_minutos = duracion_minutos

class SistemaMantenimiento:
    def __init__(self):
        self.equipos: List[Equipo] = []
        self.tecnicos: List[Tecnico] = []
        self.tareas: List[TareaMantenimiento] = []
        self.ubicaciones: List[Ubicacion] = []

    def agregar_equipo(self, equipo: Equipo):
        self.equipos.append(equipo)

    def agregar_tecnico(self, tecnico: Tecnico):
        self.tecnicos.append(tecnico)

    def agregar_tarea(self, tarea: TareaMantenimiento):
        self.tareas.append(tarea)

    def agregar_ubicacion(self, ubicacion: Ubicacion):
        self.ubicaciones.append(ubicacion)
