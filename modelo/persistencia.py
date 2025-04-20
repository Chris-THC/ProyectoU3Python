import json
from datetime import datetime
from pathlib import Path

from modelo.entidades import SistemaMantenimiento, Ubicacion, Equipo, Tecnico, TareaMantenimiento, TipoMantenimiento, \
    EstadoTarea


class PersistenciaJSON:
    def __init__(self, archivo: str = "datos/mantenimiento.json"):
        self.archivo = Path(archivo)
        self.archivo.parent.mkdir(exist_ok=True)

    def guardar(self, sistema: SistemaMantenimiento):
        datos = {
            "equipos": [self._equipo_a_dict(e) for e in sistema.equipos],
            "tecnicos": [self._tecnico_a_dict(t) for t in sistema.tecnicos],
            "tareas": [self._tarea_a_dict(t) for t in sistema.tareas],
            "ubicaciones": [self._ubicacion_a_dict(u) for u in sistema.ubicaciones]
        }

        with open(self.archivo, 'w') as f:
            json.dump(datos, f, indent=4, default=self._serializar_fecha)

    def cargar(self) -> SistemaMantenimiento:
        if not self.archivo.exists():
            return SistemaMantenimiento()

        with open(self.archivo, 'r') as f:
            datos = json.load(f)

        sistema = SistemaMantenimiento()

        # Reconstruir objetos desde el JSON
        ubicaciones = {u['id']: Ubicacion(**u) for u in datos['ubicaciones']}

        for eq in datos['equipos']:
            eq['ubicacion'] = ubicaciones[eq['ubicacion_id']]
            sistema.agregar_equipo(Equipo(**eq))

        for tec in datos['tecnicos']:
            sistema.agregar_tecnico(Tecnico(**tec))

        for ta in datos['tareas']:
            ta['tipo'] = TipoMantenimiento[ta['tipo']]
            ta['estado'] = EstadoTarea[ta['estado']]
            ta['equipo'] = next(e for e in sistema.equipos if e.id == ta['equipo_id'])
            ta['tecnico_asignado'] = next(t for t in sistema.tecnicos if t.id == ta['tecnico_id'])
            if ta['fecha_realizacion']:
                ta['fecha_realizacion'] = datetime.fromisoformat(ta['fecha_realizacion'])
            ta['fecha_programada'] = datetime.fromisoformat(ta['fecha_programada'])
            sistema.agregar_tarea(TareaMantenimiento(**ta))

        for ub in datos['ubicaciones']:
            sistema.agregar_ubicacion(Ubicacion(**ub))

        return sistema

    def _serializar_fecha(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Tipo {type(obj)} no serializable")

    def _equipo_a_dict(self, equipo: Equipo) -> dict:
        d = equipo.__dict__.copy()
        d['ubicacion_id'] = d['ubicacion'].id
        del d['ubicacion']
        return d

    def _tecnico_a_dict(self, tecnico: Tecnico) -> dict:
        return tecnico.__dict__.copy()

    def _tarea_a_dict(self, tarea: TareaMantenimiento) -> dict:
        d = tarea.__dict__.copy()
        d['tipo'] = d['tipo'].name
        d['estado'] = d['estado'].name
        d['equipo_id'] = d['equipo'].id
        d['tecnico_id'] = d['tecnico_asignado'].id
        del d['equipo']
        del d['tecnico_asignado']
        return d

    def _ubicacion_a_dict(self, ubicacion: Ubicacion) -> dict:
        return ubicacion.__dict__.copy()
