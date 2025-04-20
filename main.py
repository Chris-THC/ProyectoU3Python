from control.gestor_mantenimiento import GestorMantenimiento
from control.reportes import GeneradorReportes
from modelo.persistencia import PersistenciaJSON
from vista.main_window import MainWindow


def main():
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