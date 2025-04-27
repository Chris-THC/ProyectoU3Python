# Sistema de Gestión de Mantenimiento Industrial

## Autor
- [@Cristofer Amador Hernandez](https://github.com/Chris-THC)

## Descripción del Proyecto

Este proyecto es un sistema de gestión de mantenimiento industrial que permite registrar, planificar y gestionar tareas de mantenimiento preventivo y correctivo para equipos industriales. Además, incluye funcionalidades para administrar técnicos, ubicaciones y generar reportes detallados sobre el estado de los equipos y las tareas realizadas.

### Características principales:
- Registro de equipos, técnicos y ubicaciones.
- Planificación de tareas de mantenimiento preventivo.
- Registro de tareas de mantenimiento correctivo.
- Alertas automáticas para equipos que requieren mantenimiento.
- Generación de reportes sobre equipos, técnicos y estadísticas de mantenimiento.
- Interfaz gráfica desarrollada con `Tkinter`.

## Requisitos del Sistema

- Python 3.8 o superior.
- Sistema operativo Windows.
- Paquetes especificados en `requirements.txt`.

## Instalación y Ejecución

Sigue los pasos a continuación para configurar y ejecutar el proyecto en un entorno Windows:

### 1. Clonar el repositorio
Clona este repositorio en tu máquina local:
```bash
  git clone https://github.com/Chris-THC/ProyectoU3Python.git
```
Accede a la carpeta del proyecto:
```bash
  cd ProyectoU3Python
```
⚠️ **Nota Importante:** Asegúrate de seguir las instrucciones antes de proceder.

Sí accedes al proyecto desde un archivo comprimido, descomprime el archivo y navega a la carpeta del proyecto.
Y puesdes omitir el paso de clonar el repositorio.

### 2. Crear un entorno virtual
Crea un entorno virtual para aislar las dependencias del proyecto:
```bash
   python -m venv venv
```

### 3. Activar el entorno virtual
Activa el entorno virtual:
```bash
  venv\Scripts\activate
```

### 4. Instalar las dependencias
Instala los paquetes necesarios desde el archivo `requirements.txt`:
```bash
  pip install -r requirements.txt
```

### 5. Ejecutar el proyecto
Ejecuta el archivo principal para iniciar la aplicación:
```bash
  python main.py
```

## Estructura del Proyecto

- `control/`: Contiene la lógica de negocio y controladores del sistema.
- `modelo/`: Define las entidades principales y la persistencia de datos.
- `vista/`: Implementa la interfaz gráfica del usuario (GUI) con `Tkinter`.
- `datos/`: Almacena los datos persistentes en formato JSON.
- `main.py`: Punto de entrada principal del sistema.

## Uso del Sistema

1. **Registrar Ubicaciones**: Antes de registrar equipos, asegúrate de registrar las ubicaciones donde estarán asignados.
2. **Registrar Equipos y Técnicos**: Agrega los equipos y técnicos necesarios para gestionar las tareas de mantenimiento.
3. **Planificar Tareas**: Crea tareas de mantenimiento preventivo o correctivo según sea necesario.
4. **Generar Reportes**: Consulta reportes sobre equipos, técnicos y estadísticas generales.

## Notas Adicionales

- Los datos se almacenan en el archivo `datos/mantenimiento.json`. Asegúrate de no eliminar este archivo para mantener la persistencia de los datos.
- Si deseas restablecer los datos, simplemente elimina el archivo JSON y se generará uno nuevo vacío al iniciar el sistema.

## Créditos

Este proyecto fue desarrollado como una solución para la gestión de mantenimiento industrial, integrando una interfaz gráfica amigable y funcionalidades avanzadas de reportes.