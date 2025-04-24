import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable


class TecnicoForm:
    def __init__(self, parent, gestor, callback_actualizar: Callable):
        self.gestor = gestor
        self.callback_actualizar = callback_actualizar

        self.window = tk.Toplevel(parent)
        self.window.title("Registrar Nuevo Técnico")
        self.window.geometry("400x200")

        self._crear_formulario()

    def _crear_formulario(self):
        # Frame principal
        frame = ttk.Frame(self.window, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        # Campos del formulario
        ttk.Label(frame, text="ID del Técnico:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.id_entry = ttk.Entry(frame)
        self.id_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)

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
        try:
            # Obtener valores del formulario
            id_tecnico = self.id_entry.get().strip()
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
