from collections import defaultdict
from typing import List, Dict, Tuple

from modelo.Entidades.Equipo import Equipo
from modelo.Entidades.EstadoTarea import EstadoTarea
from modelo.Entidades.Tecnico import Tecnico
from modelo.Entidades.TipoMantenimiento import TipoMantenimiento
from modelo.SistemaMantenimiento import SistemaMantenimiento


class GeneradorReportes:
    def __init__(self, sistema: SistemaMantenimiento):
        self.sistema = sistema

    def equipos_con_mas_mantenimientos(self, top_n: int = 5) -> List[Tuple[Equipo, int]]:
        conteo = defaultdict(int)
        for tarea in self.sistema.tareas:
            conteo[tarea.equipo.id] += 1

        equipos_ordenados = sorted(
            self.sistema.equipos,
            key=lambda e: conteo[e.id],
            reverse=True
        )

        return [(e, conteo[e.id]) for e in equipos_ordenados[:top_n]]

    def tecnicos_mas_activos(self, top_n: int = 5) -> List[Tuple[Tecnico, int]]:
        conteo = defaultdict(int)
        for tarea in self.sistema.tareas:
            if tarea.estado == EstadoTarea.COMPLETADA:
                conteo[tarea.tecnico_asignado.id] += 1

        tecnicos_ordenados = sorted(
            self.sistema.tecnicos,
            key=lambda t: conteo[t.id],
            reverse=True
        )

        return [(t, conteo[t.id]) for t in tecnicos_ordenados[:top_n]]

    def fallas_recurrentes(self) -> Dict[str, int]:
        palabras_clave = [
            "falla", "avería", "daño", "roto", "descompuesto",
            "mal funcionamiento", "error", "problema"
        ]

        conteo = defaultdict(int)
        for tarea in self.sistema.tareas:
            if tarea.tipo == TipoMantenimiento.CORRECTIVO and tarea.observaciones:
                observacion = tarea.observaciones.lower()
                for palabra in palabras_clave:
                    if palabra in observacion:
                        equipo_nombre = tarea.equipo.nombre
                        conteo[equipo_nombre] += 1
                        break

        return dict(conteo)

    def tiempo_promedio_mantenimiento(self) -> float:
        tareas_completadas = [
            t for t in self.sistema.tareas
            if t.estado == EstadoTarea.COMPLETADA and t.duracion_minutos
        ]

        if not tareas_completadas:
            return 0.0

        total = sum(t.duracion_minutos for t in tareas_completadas)
        return total / len(tareas_completadas)

    def mantenimientos_por_tipo(self) -> Dict[str, int]:
        conteo = {
            "PREVENTIVO": 0,
            "CORRECTIVO": 0
        }

        for tarea in self.sistema.tareas:
            conteo[tarea.tipo.name] += 1

        return conteo
