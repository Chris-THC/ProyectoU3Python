class Ubicacion:
    """
    Clase que representa una ubicación dentro del sistema.
    """

    def __init__(self, id: str, nombre: str, descripcion: str = ""):
        """
            Inicializador de la clase Ubicación.

            :param id: Identificador único de la ubicación.
            :param nombre: Nombre de la ubicación.
            :param descripcion: Descripción opcional de la ubicación.
        """
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
