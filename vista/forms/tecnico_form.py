import tkinter as tk
from random import randint
from tkinter import ttk, messagebox
from typing import Callable


class TecnicoForm:
    """
    Clase que representa el formulario para registrar un nuevo técnico en el sistema.

    Permite al usuario ingresar los datos necesarios para registrar un técnico,
    como nombre, especialidad y estado activo.
    """

    def __init__(self, parent, gestor, callback_actualizar: Callable):
        """
        Inicializa el formulario de registro de técnico.

        :param parent: Ventana padre donde se abrirá el formulario.
        :param gestor: Objeto gestor que maneja la lógica del sistema.
        :param callback_actualizar: Función de callback para actualizar la vista principal tras registrar un técnico.
        """
        self.gestor = gestor
        self.callback_actualizar = callback_actualizar

        self.window = tk.Toplevel(parent)
        self.window.title("Registrar Nuevo Técnico")
        self.window.geometry("400x200")

        self._crear_formulario()

    def _crear_formulario(self):
        """
        Crea y organiza los elementos del formulario de registro de técnico.
        """
        # Frame principal
        frame = ttk.Frame(self.window, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Campos del formulario
        ttk.Label(frame, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.nombre_entry = ttk.Entry(frame)
        self.nombre_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)

        ttk.Label(frame, text="Especialidad:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.especialidad_entry = ttk.Entry(frame)
        self.especialidad_entry.grid(row=2, column=1, sticky=tk.EW, pady=5)

        # Checkbox para estado activo
        self.activo_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            frame,
            text="Técnico activo",
            variable=self.activo_var
        ).grid(row=3, column=0, columnspan=2, pady=5, sticky=tk.W)

        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Guardar", command=self._guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.window.destroy).pack(side=tk.LEFT, padx=5)

        # Configurar expansión
        frame.columnconfigure(1, weight=1)

    def _guardar(self):
        """
        Guarda los datos del técnico ingresados en el formulario.

        Realiza validaciones básicas y registra el técnico en el sistema.
        Muestra mensajes de éxito o error según el resultado.
        """
        try:
            # Obtener valores del formulario
            id_tecnico = self._id_aleatorio()
            nombre = self.nombre_entry.get().strip()
            especialidad = self.especialidad_entry.get().strip()
            activo = self.activo_var.get()

            # Validaciones básicas
            if not id_tecnico or not nombre or not especialidad:
                raise ValueError("Todos los campos son obligatorios")

            # Registrar el técnico
            self.gestor.registrar_tecnico(
                id=id_tecnico,
                nombre=nombre,
                especialidad=especialidad
            ).activo = activo

            messagebox.showinfo("Éxito", "Técnico registrado correctamente")
            self.callback_actualizar()
            self.window.destroy()

        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el técnico: {e}")

    def _id_aleatorio(self):
        """
        Genera un ID aleatorio para el técnico.

        :return: ID aleatorio como cadena.
        """
        return str(randint(100000, 999999))
