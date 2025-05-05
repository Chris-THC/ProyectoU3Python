class Persona:
    """
    Clase base que representa a una persona con un identificador y un nombre.
    """

    def __init__(self, id: str, nombre: str):
        """
        Inicializador de la clase Persona.

        :param id: Identificador único de la persona.
        :param nombre: Nombre de la persona.
        """
        self._id = id
        self.nombre = nombre

    @property
    def id(self) -> str:
        """
        Devuelve el identificador único de la persona.
        """
        return self._id
