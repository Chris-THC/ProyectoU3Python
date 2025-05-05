import tkinter as tk
from datetime import datetime, timedelta
from tkinter import ttk, messagebox
from typing import Callable


class TareaForm:
    """
    Clase que representa el formulario para registrar una nueva tarea de mantenimiento.

    Permite al usuario planificar tareas de mantenimiento preventivo o registrar tareas de mantenimiento correctivo.
    """

    def __init__(self, parent, gestor, callback_actualizar: Callable):
        """
        Inicializa el formulario de registro de tareas de mantenimiento.

        :param parent: Ventana padre donde se abrirá el formulario.
        :param gestor: Objeto gestor que maneja la lógica del sistema.
        :param callback_actualizar: Función de callback para actualizar la vista principal tras registrar una tarea.
        """
        self.gestor = gestor
        self.callback_actualizar = callback_actualizar

        self.window = tk.Toplevel(parent)
        self.window.title("Registrar Nueva Tarea de Mantenimiento")
        self.window.geometry("500x400")

        self._crear_formulario()

    def _crear_formulario(self):
        """
        Crea y organiza los elementos del formulario de registro de tareas de mantenimiento.
        """
        # Frame principal
        frame = ttk.Frame(self.window, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Tipo de mantenimiento
        ttk.Label(frame, text="Tipo de Mantenimiento:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.tipo_var = tk.StringVar(value="PREVENTIVO")
        tipo_frame = ttk.Frame(frame)
        tipo_frame.grid(row=0, column=1, sticky=tk.EW, pady=5)

        ttk.Radiobutton(
            tipo_frame,
            text="Preventivo",
            variable=self.tipo_var,
            value="PREVENTIVO",
            command=self._toggle_tipo
        ).pack(side=tk.LEFT)

        ttk.Radiobutton(
            tipo_frame,
            text="Correctivo",
            variable=self.tipo_var,
            value="CORRECTIVO",
            command=self._toggle_tipo
        ).pack(side=tk.LEFT)

        # Equipo
        ttk.Label(frame, text="Equipo:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.equipo_combobox = ttk.Combobox(frame, state="readonly")
        self.equipo_combobox.grid(row=1, column=1, sticky=tk.EW, pady=5)
        self._cargar_equipos()

        # Técnico
        ttk.Label(frame, text="Técnico Asignado:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.tecnico_combobox = ttk.Combobox(frame, state="readonly")
        self.tecnico_combobox.grid(row=2, column=1, sticky=tk.EW, pady=5)
        self._cargar_tecnicos()

        # Fecha programada (solo para preventivo)
        self.fecha_frame = ttk.Frame(frame)
        self.fecha_frame.grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=5)

        ttk.Label(self.fecha_frame, text="Fecha Programada:").pack(side=tk.LEFT)
        self.fecha_entry = ttk.Entry(self.fecha_frame)
        self.fecha_entry.pack(side=tk.LEFT, padx=5)
        self.fecha_entry.insert(0, (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"))

        # Observaciones (solo para correctivo)
        self.obs_frame = ttk.Frame(frame)

        ttk.Label(self.obs_frame, text="Observaciones:").pack(anchor=tk.W)
        self.obs_text = tk.Text(self.obs_frame, height=5, width=40)
        self.obs_text.pack(fill=tk.BOTH, expand=True)

        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Guardar", command=self._guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.window.destroy).pack(side=tk.LEFT, padx=5)

        # Configurar expansión
        frame.columnconfigure(1, weight=1)
        self._toggle_tipo()

    def _cargar_equipos(self):
        """
        Carga los equipos disponibles en el sistema y los muestra en el combobox.

        Si no hay equipos registrados, el combobox permanecerá vacío.
        """
        equipos = [(e.id, e.nombre) for e in self.gestor.sistema.equipos]
        self.equipo_combobox['values'] = [f"{id} - {nombre}" for id, nombre in equipos]
        if equipos:
            self.equipo_combobox.current(0)

    def _cargar_tecnicos(self):
        """
        Carga los técnicos activos en el sistema y los muestra en el combobox.

        Si no hay técnicos activos, el combobox permanecerá vacío.
        """
        tecnicos = [(t.id, t.nombre) for t in self.gestor.sistema.tecnicos if t.activo]
        self.tecnico_combobox['values'] = [f"{id} - {nombre}" for id, nombre in tecnicos]
        if tecnicos:
            self.tecnico_combobox.current(0)

    def _toggle_tipo(self):
        """
        Alterna entre los campos de entrada según el tipo de mantenimiento seleccionado.

        Muestra el campo de fecha programada para mantenimiento preventivo y
        el campo de observaciones para mantenimiento correctivo.
        """
        if self.tipo_var.get() == "PREVENTIVO":
            self.fecha_frame.grid()
            self.obs_frame.grid_forget()
        else:
            self.fecha_frame.grid_forget()
            self.obs_frame.grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=5)

    def _guardar(self):
        """
        Guarda los datos de la tarea ingresados en el formulario.

        Realiza validaciones básicas y registra la tarea en el sistema.
        Muestra mensajes de éxito o error según el resultado.
        """
        try:
            # Obtener valores comunes
            tipo = self.tipo_var.get()
            equipo_str = self.equipo_combobox.get()
            tecnico_str = self.tecnico_combobox.get()

            # Validaciones básicas
            if not equipo_str or not tecnico_str:
                raise ValueError("Debe seleccionar equipo y técnico")

            # Obtener IDs
            equipo_id = equipo_str.split(" - ")[0]
            tecnico_id = tecnico_str.split(" - ")[0]

            if tipo == "PREVENTIVO":
                # Registrar mantenimiento preventivo
                fecha_programada = datetime.strptime(self.fecha_entry.get(), "%Y-%m-%d")
                tarea = self.gestor.planificar_mantenimiento_preventivo(
                    equipo_id=equipo_id,
                    tecnico_id=tecnico_id,
                    fecha_programada=fecha_programada
                )
                mensaje = "Mantenimiento preventivo planificado correctamente"
            else:
                # Registrar mantenimiento correctivo
                observaciones = self.obs_text.get("1.0", tk.END).strip()
                if not observaciones:
                    raise ValueError("Las observaciones son obligatorias para mantenimiento correctivo")

                tarea = self.gestor.registrar_mantenimiento_correctivo(
                    equipo_id=equipo_id,
                    tecnico_id=tecnico_id,
                    observaciones=observaciones
                )
                mensaje = "Mantenimiento correctivo registrado correctamente"

            messagebox.showinfo("Éxito", mensaje)
            self.callback_actualizar()
            self.window.destroy()

        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la tarea: {e}")