from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum, auto
from typing import List, Optional


# Enum para tipos de mantenimiento
class TipoMantenimiento(Enum):
    PREVENTIVO = auto()
    CORRECTIVO = auto()


# Enum para estados de tarea
class EstadoTarea(Enum):
    PENDIENTE = auto()
    EN_PROCESO = auto()
    COMPLETADA = auto()
    CANCELADA = auto()


# Interfaces abstractas
class Identificable(ABC):
    @property
    @abstractmethod
    def id(self) -> str:
        pass


class Mantenible(ABC):
    @abstractmethod
    def necesita_mantenimiento(self) -> bool:
        pass


# Clase base Persona
class Persona:
    def __init__(self, id: str, nombre: str):
        self._id = id
        self.nombre = nombre

    @property
    def id(self) -> str:
        return self._id


# Clase Ubicacion
class Ubicacion:
    def __init__(self, id: str, nombre: str, descripcion: str = ""):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion


# Clase Equipo con herencia múltiple
class Equipo(Identificable, Mantenible):
    def __init__(self, id: str, nombre: str, ubicacion: Ubicacion,
                 fecha_instalacion: datetime, horas_uso: int = 0,
                 horas_mantenimiento: int = 100):
        self._id = id
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.fecha_instalacion = fecha_instalacion
        self.horas_uso = horas_uso
        self.horas_mantenimiento = horas_mantenimiento

    @property
    def id(self) -> str:
        return self._id

    def necesita_mantenimiento(self) -> bool:
        return self.horas_uso >= self.horas_mantenimiento


# Clase Tecnico hereda de Persona
class Tecnico(Persona):
    def __init__(self, id: str, nombre: str, especialidad: str, activo: bool = True):
        super().__init__(id, nombre)
        self.especialidad = especialidad
        self.activo = activo


# Clase TareaMantenimiento
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


# Clase principal del sistema
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
