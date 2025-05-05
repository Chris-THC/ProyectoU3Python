"""
Módulo principal del sistema de gestión de mantenimiento industrial.

Este módulo inicializa los componentes principales del sistema, carga los datos
existentes desde el almacenamiento, y lanza la interfaz gráfica para la interacción
con el usuario. Al finalizar, guarda los datos actualizados.
"""
from control.gestor_mantenimiento import GestorMantenimiento
from control.reportes import GeneradorReportes
from modelo.persistencia import PersistenciaJSON
from vista.main_window import MainWindow


def main():
    """
       Función principal del sistema.

       Realiza las siguientes operaciones:
       - Carga los datos existentes desde un archivo de persistencia.
       - Inicializa los componentes del sistema, como el gestor de mantenimiento y el generador de reportes.
       - Crea y ejecuta la interfaz gráfica principal.
       - Guarda los datos actualizados al salir del sistema.
    """
    # Cargar datos existentes
    persistencia = PersistenciaJSON()
    sistema = persistencia.cargar()

    # Inicializar componentes del sistema
    gestor = GestorMantenimiento(sistema)
    generador_reportes = GeneradorReportes(sistema)

    # Crear y mostrar la interfaz gráfica
    app = MainWindow(gestor, generador_reportes)
    app.ejecutar()

    # Guardar datos al salir
    persistencia.guardar(sistema)


if __name__ == "__main__":
    main()