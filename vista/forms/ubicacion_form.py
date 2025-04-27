import tkinter as tk
from random import randint
from tkinter import ttk, messagebox
from typing import Callable


class UbicacionForm:
    """
    Clase que representa el formulario para registrar una nueva ubicación en el sistema.

    Permite al usuario ingresar los datos necesarios para registrar una ubicación,
    como el nombre y una descripción opcional.
    """

    def __init__(self, parent, gestor, callback_actualizar: Callable):
        """
        Inicializa el formulario de registro de ubicación.

        :param parent: Ventana padre donde se abrirá el formulario.
        :param gestor: Objeto gestor que maneja la lógica del sistema.
        :param callback_actualizar: Función de callback para actualizar la vista principal tras registrar una ubicación.
        """
        self.gestor = gestor
        self.callback_actualizar = callback_actualizar

        self.window = tk.Toplevel(parent)
        self.window.title("Registrar Nueva Ubicación")
        self.window.geometry("400x200")

        self._crear_formulario()

    def _crear_formulario(self):
        """
        Crea y organiza los elementos del formulario de registro de ubicación.
        """
        frame = ttk.Frame(self.window, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Campos del formulario
        ttk.Label(frame, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.nombre_entry = ttk.Entry(frame)
        self.nombre_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)

        ttk.Label(frame, text="Descripción (opcional):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.desc_entry = ttk.Entry(frame)
        self.desc_entry.grid(row=2, column=1, sticky=tk.EW, pady=5)

        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Guardar", command=self._guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.window.destroy).pack(side=tk.LEFT, padx=5)

        frame.columnconfigure(1, weight=1)

    def _guardar(self):
        """
        Guarda los datos de la ubicación ingresados en el formulario.

        Realiza validaciones básicas y registra la ubicación en el sistema.
        Muestra mensajes de éxito o error según el resultado.
        """
        try:
            ubicacion = self.gestor.registrar_ubicacion(
                id=self._id_aleatorio(),
                nombre=self.nombre_entry.get().strip(),
                descripcion=self.desc_entry.get().strip()
            )
            messagebox.showinfo("Éxito", "Ubicación registrada correctamente")
            self.callback_actualizar()
            self.window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}")

    def _id_aleatorio(self):
        """
        Genera un ID aleatorio para la ubicación.

        :return: Id aleatorio como cadena.
        """
        return str(randint(100000, 999999))
