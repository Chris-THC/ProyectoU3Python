from datetime import datetime
from typing import List

from modelo.entidades import SistemaMantenimiento, Equipo, Ubicacion, Tecnico, TareaMantenimiento, TipoMantenimiento, \
    EstadoTarea


class GestorMantenimiento:
    def __init__(self, sistema: SistemaMantenimiento):
        self.sistema = sistema

    def registrar_equipo(self, id: str, nombre: str, ubicacion: Ubicacion,
                         fecha_instalacion: datetime, horas_uso: int = 0) -> Equipo:
        equipo = Equipo(id, nombre, ubicacion, fecha_instalacion, horas_uso)
        self.sistema.agregar_equipo(equipo)
        return equipo

    def registrar_tecnico(self, id: str, nombre: str, especialidad: str) -> Tecnico:
        tecnico = Tecnico(id, nombre, especialidad)
        self.sistema.agregar_tecnico(tecnico)
        return tecnico

    def registrar_ubicacion(self, id: str, nombre: str, descripcion: str = "") -> Ubicacion:
        ubicacion = Ubicacion(id, nombre, descripcion)
        self.sistema.agregar_ubicacion(ubicacion)
        return ubicacion

    def planificar_mantenimiento_preventivo(self, equipo_id: str, tecnico_id: str,
                                            fecha_programada: datetime) -> TareaMantenimiento:
        equipo = next(e for e in self.sistema.equipos if e.id == equipo_id)
        tecnico = next(t for t in self.sistema.tecnicos if t.id == tecnico_id)

        tarea = TareaMantenimiento(
            id=f"TAR-{datetime.now().timestamp()}",
            tipo=TipoMantenimiento.PREVENTIVO,
            equipo=equipo,
            tecnico_asignado=tecnico,
            fecha_programada=fecha_programada
        )

        self.sistema.agregar_tarea(tarea)
        return tarea

    def registrar_mantenimiento_correctivo(self, equipo_id: str, tecnico_id: str,
                                           observaciones: str) -> TareaMantenimiento:
        equipo = next(e for e in self.sistema.equipos if e.id == equipo_id)
        tecnico = next(t for t in self.sistema.tecnicos if t.id == tecnico_id)

        tarea = TareaMantenimiento(
            id=f"TAR-{datetime.now().timestamp()}",
            tipo=TipoMantenimiento.CORRECTIVO,
            equipo=equipo,
            tecnico_asignado=tecnico,
            fecha_programada=datetime.now(),
            estado=EstadoTarea.COMPLETADA,
            observaciones=observaciones,
            fecha_realizacion=datetime.now()
        )

        self.sistema.agregar_tarea(tarea)
        return tarea

    def ejecutar_tarea(self, tarea_id: str, duracion_minutos: int, observaciones: str = "") -> bool:
        tarea = next((t for t in self.sistema.tareas if t.id == tarea_id), None)
        if tarea and tarea.estado == EstadoTarea.PENDIENTE:
            tarea.estado = EstadoTarea.COMPLETADA
            tarea.fecha_realizacion = datetime.now()
            tarea.duracion_minutos = duracion_minutos
            tarea.observaciones = observaciones
            return True
        return False

    def obtener_tareas_pendientes(self) -> List[TareaMantenimiento]:
        return [t for t in self.sistema.tareas if t.estado == EstadoTarea.PENDIENTE]

    def obtener_tareas_por_equipo(self, equipo_id: str) -> List[TareaMantenimiento]:
        return [t for t in self.sistema.tareas if t.equipo.id == equipo_id]

    def obtener_tareas_por_tecnico(self, tecnico_id: str) -> List[TareaMantenimiento]:
        return [t for t in self.sistema.tareas if t.tecnico_asignado.id == tecnico_id]

    def verificar_alertas_mantenimiento(self) -> List[Equipo]:
        alertas = []
        hoy = datetime.now()

        for equipo in self.sistema.equipos:
            # Alertas por horas de uso
            if equipo.horas_uso >= equipo.horas_mantenimiento:
                alertas.append(equipo)
                continue

            # Alertas por falta de mantenimiento preventivo
            tareas = [t for t in self.sistema.tareas
                      if t.equipo.id == equipo.id and t.tipo == TipoMantenimiento.PREVENTIVO]

            if tareas:
                ultima_tarea = max(tareas, key=lambda t: t.fecha_programada)
                if (hoy - ultima_tarea.fecha_programada).days > 180:  # 6 meses
                    alertas.append(equipo)
            else:
                # Nunca se ha hecho mantenimiento
                if (hoy - equipo.fecha_instalacion).days > 180:
                    alertas.append(equipo)

        return alertas
