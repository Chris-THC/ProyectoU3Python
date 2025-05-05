from datetime import datetime
from typing import List

from modelo.Entidades.Equipo import Equipo
from modelo.Entidades.EstadoTarea import EstadoTarea
from modelo.Entidades.TareaMantenimiento import TareaMantenimiento
from modelo.Entidades.Tecnico import Tecnico
from modelo.Entidades.TipoMantenimiento import TipoMantenimiento
from modelo.Entidades.Ubicacion import Ubicacion
from modelo.SistemaMantenimiento import SistemaMantenimiento


class GestorMantenimiento:
    """
    Clase que gestiona las operaciones relacionadas con el mantenimiento de equipos,
    técnicos, ubicaciones y tareas en el sistema.
    """

    def __init__(self, sistema: SistemaMantenimiento):
        """
        Inicializador de la clase GestorMantenimiento.

        :param sistema: Instancia del sistema de mantenimiento.
        """
        self.sistema = sistema

    def registrar_equipo(self, id: str, nombre: str, ubicacion: Ubicacion,
                         fecha_instalacion: datetime, horas_uso: int = 0) -> Equipo:
        """
        Registra un nuevo equipo en el sistema.

        :param id: Identificador único del equipo.
        :param nombre: Nombre del equipo.
        :param ubicacion: Ubicación del equipo.
        :param fecha_instalacion: Fecha de instalación del equipo.
        :param horas_uso: Horas de uso iniciales del equipo.
        :return: Instancia del equipo registrado.
        """
        equipo = Equipo(id, nombre, ubicacion, fecha_instalacion, horas_uso)
        self.sistema.agregar_equipo(equipo)
        return equipo

    def registrar_tecnico(self, id: str, nombre: str, especialidad: str) -> Tecnico:
        """
        Registra un nuevo técnico en el sistema.

        :param id: Identificador único del técnico.
        :param nombre: Nombre del técnico.
        :param especialidad: Especialidad del técnico.
        :return: Instancia del técnico registrado.
        """
        tecnico = Tecnico(id, nombre, especialidad)
        self.sistema.agregar_tecnico(tecnico)
        return tecnico

    def registrar_ubicacion(self, id: str, nombre: str, descripcion: str = "") -> Ubicacion:
        """
        Registra una nueva ubicación en el sistema.

        :param id: Identificador único de la ubicación.
        :param nombre: Nombre de la ubicación.
        :param descripcion: Descripción opcional de la ubicación.
        :return: Instancia de la ubicación registrada.
        """
        if not id or not nombre:
            raise ValueError("ID y nombre son obligatorios")
        ubicacion = Ubicacion(id=id, nombre=nombre, descripcion=descripcion)
        self.sistema.agregar_ubicacion(ubicacion)
        return ubicacion

    def planificar_mantenimiento_preventivo(self, equipo_id: str, tecnico_id: str,
                                            fecha_programada: datetime) -> TareaMantenimiento:
        """
        Planifica una tarea de mantenimiento preventivo para un equipo.

        :param equipo_id: Identificador del equipo.
        :param tecnico_id: Identificador del técnico asignado.
        :param fecha_programada: Fecha programada para el mantenimiento.
        :return: Instancia de la tarea de mantenimiento creada.
        """
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
        """
        Registra una tarea de mantenimiento correctivo para un equipo.

        :param equipo_id: Identificador del equipo.
        :param tecnico_id: Identificador del técnico asignado.
        :param observaciones: Observaciones sobre el mantenimiento.
        :return: Instancia de la tarea de mantenimiento creada.
        """
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
        """
        Ejecuta una tarea de mantenimiento pendiente.

        :param tarea_id: Identificador de la tarea.
        :param duracion_minutos: Duración de la tarea en minutos.
        :param observaciones: Observaciones adicionales sobre la tarea.
        :return: True si la tarea fue ejecutada exitosamente, False en caso contrario.
        """
        tarea = next((t for t in self.sistema.tareas if t.id == tarea_id), None)
        if tarea and tarea.estado == EstadoTarea.PENDIENTE:
            tarea.estado = EstadoTarea.COMPLETADA
            tarea.fecha_realizacion = datetime.now()
            tarea.duracion_minutos = duracion_minutos
            tarea.observaciones = observaciones
            return True
        return False

    def obtener_tareas_pendientes(self) -> List[TareaMantenimiento]:
        """
        Obtiene todas las tareas de mantenimiento pendientes.

        :return: Lista de tareas pendientes.
        """
        return [t for t in self.sistema.tareas if t.estado == EstadoTarea.PENDIENTE]

    def obtener_tareas_por_equipo(self, equipo_id: str) -> List[TareaMantenimiento]:
        """
        Obtiene todas las tareas asociadas a un equipo específico.

        :param equipo_id: Identificador del equipo.
        :return: Lista de tareas asociadas al equipo.
        """
        return [t for t in self.sistema.tareas if t.equipo.id == equipo_id]

    def obtener_tareas_por_tecnico(self, tecnico_id: str) -> List[TareaMantenimiento]:
        """
        Obtiene todas las tareas asignadas a un técnico específico.

        :param tecnico_id: Identificador del técnico.
        :return: Lista de tareas asignadas al técnico.
        """
        return [t for t in self.sistema.tareas if t.tecnico_asignado.id == tecnico_id]

    def verificar_alertas_mantenimiento(self) -> List[Equipo]:
        """
        Verifica alertas de mantenimiento para los equipos.

        :return: Lista de equipos que requieren atención de mantenimiento.
        """
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
                if (hoy - ultima_tarea.fecha_programada).days > 3:
                    alertas.append(equipo)
            else:
                # Nunca se ha hecho mantenimiento
                if (hoy - equipo.fecha_instalacion).days > 3:
                    alertas.append(equipo)

        return alertas
