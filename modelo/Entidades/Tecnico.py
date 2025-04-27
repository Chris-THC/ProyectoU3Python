from modelo.Entidades.Persona import Persona


class Tecnico(Persona):
    """
        Clase que representa a un técnico encargado de realizar mantenimientos.
    """

    def __init__(self, id: str, nombre: str, especialidad: str, activo: bool = True):
        """
                Inicializador de la clase Técnico.

                :param id: Identificador único del técnico.
                :param nombre: Nombre del técnico.
                :param especialidad: Especialidad del técnico.
                :param activo: Indica si el técnico está activo.
        """
        super().__init__(id, nombre)
        self.especialidad = especialidad
        self.activo = activo
