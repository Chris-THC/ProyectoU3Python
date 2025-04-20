from dataclasses import dataclass, field
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


@dataclass
class Ubicacion:
    id: str
    nombre: str
    descripcion: str = ""


@dataclass
class Equipo:
    id: str
    nombre: str
    ubicacion: Ubicacion
    fecha_instalacion: datetime
    horas_uso: int = 0
    horas_mantenimiento: int = 100  # Default cada 100 horas


@dataclass
class Tecnico:
    id: str
    nombre: str
    especialidad: str
    activo: bool = True


@dataclass
class TareaMantenimiento:
    id: str
    tipo: TipoMantenimiento
    equipo: Equipo
    fecha_programada: datetime
    tecnico_asignado: Tecnico
    estado: EstadoTarea = EstadoTarea.PENDIENTE
    observaciones: str = ""
    fecha_realizacion: Optional[datetime] = None
    duracion_minutos: Optional[int] = None


@dataclass
class SistemaMantenimiento:
    equipos: List[Equipo] = field(default_factory=list)
    tecnicos: List[Tecnico] = field(default_factory=list)
    tareas: List[TareaMantenimiento] = field(default_factory=list)
    ubicaciones: List[Ubicacion] = field(default_factory=list)

    def agregar_equipo(self, equipo: Equipo):
        self.equipos.append(equipo)

    def agregar_tecnico(self, tecnico: Tecnico):
        self.tecnicos.append(tecnico)

    def agregar_tarea(self, tarea: TareaMantenimiento):
        self.tareas.append(tarea)

    def agregar_ubicacion(self, ubicacion: Ubicacion):
        self.ubicaciones.append(ubicacion)
