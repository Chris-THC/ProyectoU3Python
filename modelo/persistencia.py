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

        try:
            with open(self.archivo, 'r') as f:
                datos = json.load(f)
        except json.JSONDecodeError:
            return SistemaMantenimiento()

        sistema = SistemaMantenimiento()

        # 1. Cargar ubicaciones
        ubicaciones = {u['id']: Ubicacion(**u) for u in datos.get('ubicaciones', [])}
        for ub in ubicaciones.values():
            sistema.agregar_ubicacion(ub)

        # 2. Cargar equipos
        equipos = {}
        for eq in datos.get('equipos', []):
            try:
                eq_data = eq.copy()
                eq_data['id'] = eq_data.pop('_id')  # Convertir _id a id
                eq_data['ubicacion'] = ubicaciones[eq_data['ubicacion_id']]
                del eq_data['ubicacion_id']

                # Convertir string a datetime
                eq_data['fecha_instalacion'] = datetime.fromisoformat(eq_data['fecha_instalacion'])

                equipo = Equipo(**eq_data)
                equipos[equipo.id] = equipo
                sistema.agregar_equipo(equipo)
            except KeyError as e:
                print(f"Error cargando equipo {eq.get('id')}: {str(e)}")
            except ValueError as e:
                print(f"Error en formato de fecha para equipo {eq.get('id')}: {str(e)}")

        # 3. Cargar técnicos
        tecnicos = {}
        for tec in datos.get('tecnicos', []):
            try:
                tec_data = tec.copy()
                tec_data['id'] = tec_data.pop('_id')  # Convertir _id a id

                tecnico = Tecnico(**tec_data)
                tecnicos[tecnico.id] = tecnico
                sistema.agregar_tecnico(tecnico)
            except KeyError as e:
                print(f"Error cargando técnico {tec.get('id')}: {str(e)}")

        # 4. Cargar tareas (¡esta es la parte crítica!)
        for ta in datos.get('tareas', []):
            try:
                ta_data = ta.copy()

                # Convertir IDs a objetos
                ta_data['equipo'] = equipos[ta_data['equipo_id']]
                ta_data['tecnico_asignado'] = tecnicos[ta_data['tecnico_id']]
                del ta_data['equipo_id']
                del ta_data['tecnico_id']

                # Convertir enums
                ta_data['tipo'] = TipoMantenimiento[ta_data['tipo']]
                ta_data['estado'] = EstadoTarea[ta_data['estado']]

                # Convertir fechas
                if ta_data['fecha_realizacion']:
                    ta_data['fecha_realizacion'] = datetime.fromisoformat(ta_data['fecha_realizacion'])
                ta_data['fecha_programada'] = datetime.fromisoformat(ta_data['fecha_programada'])

                sistema.agregar_tarea(TareaMantenimiento(**ta_data))
            except Exception as e:
                print(f"Error cargando tarea {ta.get('id')}: {str(e)}")

        return sistema

    def _serializar_fecha(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Tipo {type(obj)} no serializable")

    def _equipo_a_dict(self, equipo: Equipo) -> dict:
        d = equipo.__dict__.copy()
        d['id'] = d.pop('_id')  # Cambiar _id a id
        d['ubicacion_id'] = d['ubicacion'].id
        del d['ubicacion']
        return d

    def _tecnico_a_dict(self, tecnico: Tecnico) -> dict:
        d = tecnico.__dict__.copy()
        d['id'] = d.pop('_id')  # Cambiar _id a id
        return d

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
