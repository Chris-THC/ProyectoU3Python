from collections import defaultdict
from typing import List, Dict, Tuple

from modelo.Entidades.Equipo import Equipo
from modelo.Entidades.EstadoTarea import EstadoTarea
from modelo.Entidades.Tecnico import Tecnico
from modelo.Entidades.TipoMantenimiento import TipoMantenimiento
from modelo.SistemaMantenimiento import SistemaMantenimiento


class GeneradorReportes:
    """
        Clase que genera reportes basados en los datos del sistema de mantenimiento.
    """

    def __init__(self, sistema: SistemaMantenimiento):
        """
        Inicializador de la clase GeneradorReportes.

        :param sistema: Instancia del sistema de mantenimiento.
        """
        self.sistema = sistema

    def equipos_con_mas_mantenimientos(self, top_n: int = 5) -> List[Tuple[Equipo, int]]:
        """
                Obtiene los equipos con mayor cantidad de mantenimientos realizados.

                :param top_n: Número máximo de equipos a incluir en el reporte.
                :return: Lista de tuplas con los equipos y la cantidad de mantenimientos realizados.
        """
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
        """
                Obtiene los técnicos con mayor cantidad de tareas completadas.

                :param top_n: Número máximo de técnicos a incluir en el reporte.
                :return: Lista de tuplas con los técnicos y la cantidad de tareas completadas.
        """
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
        """
                Identifica las fallas más recurrentes en los equipos basándose en las observaciones.

                :return: Diccionario con los nombres de los equipos y la cantidad de fallas registradas.
        """
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
        """
                Calcula el tiempo promedio de duración de las tareas de mantenimiento completadas.

                :return: Tiempo promedio en minutos. Devuelve 0.0 si no hay tareas completadas.
        """
        tareas_completadas = [
            t for t in self.sistema.tareas
            if t.estado == EstadoTarea.COMPLETADA and t.duracion_minutos
        ]

        if not tareas_completadas:
            return 0.0

        total = sum(t.duracion_minutos for t in tareas_completadas)
        return total / len(tareas_completadas)

    def mantenimientos_por_tipo(self) -> Dict[str, int]:
        """
                Genera un conteo de las tareas de mantenimiento por tipo (PREVENTIVO o CORRECTIVO).

                :return: Diccionario con el tipo de mantenimiento como clave y la cantidad como valor.
        """
        conteo = {
            "PREVENTIVO": 0,
            "CORRECTIVO": 0
        }

        for tarea in self.sistema.tareas:
            conteo[tarea.tipo.name] += 1

        return conteo
