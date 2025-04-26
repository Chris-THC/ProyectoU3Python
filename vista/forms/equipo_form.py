import tkinter as tk
from datetime import datetime
from random import randint
from tkinter import ttk, messagebox
from typing import Callable


class EquipoForm:
    def __init__(self, parent, gestor, callback_actualizar: Callable):
        self.gestor = gestor
        self.callback_actualizar = callback_actualizar

        self.window = tk.Toplevel(parent)
        self.window.title("Registrar Nuevo Equipo")
        self.window.geometry("400x300")

        self._crear_formulario()

    def _crear_formulario(self):
        # Frame principal
        frame = ttk.Frame(self.window, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.nombre_entry = ttk.Entry(frame)
        self.nombre_entry.grid(row=1, column=1, sticky=tk.EW, pady=5)

        ttk.Label(frame, text="Ubicación:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.ubicacion_combobox = ttk.Combobox(frame, state="readonly")
        self.ubicacion_combobox.grid(row=2, column=1, sticky=tk.EW, pady=5)
        self._cargar_ubicaciones()

        ttk.Label(frame, text="Fecha de Instalación:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.fecha_entry = ttk.Entry(frame)
        self.fecha_entry.grid(row=3, column=1, sticky=tk.EW, pady=5)
        self.fecha_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ttk.Label(frame, text="Horas de Uso:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.horas_entry = ttk.Spinbox(frame, from_=0, to=100000)
        self.horas_entry.grid(row=4, column=1, sticky=tk.EW, pady=5)
        self.horas_entry.set(0)

        ttk.Label(frame, text="Horas entre Mantenimientos:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.horas_mant_entry = ttk.Spinbox(frame, from_=10, to=1000)
        self.horas_mant_entry.grid(row=5, column=1, sticky=tk.EW, pady=5)
        self.horas_mant_entry.set(100)

        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Guardar", command=self._guardar).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancelar", command=self.window.destroy).pack(side=tk.LEFT, padx=5)

        # Configurar expansión
        frame.columnconfigure(1, weight=1)

    def _cargar_ubicaciones(self):
        ubicaciones = [(u.id, u.nombre) for u in self.gestor.sistema.ubicaciones]
        if not ubicaciones:
            # Deshabilitar el formulario y mostrar mensaje
            self.ubicacion_combobox['values'] = ["⚠️ Registre una ubicación primero"]
            self.ubicacion_combobox.set("⚠️ Registre una ubicación primero")
            self.ubicacion_combobox['state'] = 'disabled'

            # Bloquear botón de guardado
            self.btn_guardar['state'] = 'disabled'

            # Añadir botón para redirigir a registro de ubicación
            btn_redirigir = ttk.Button(
                self.window,
                text="Ir a Registrar Ubicación",
                command=self._abrir_form_ubicacion
            )
            btn_redirigir.pack(pady=10)
        else:
            self.ubicacion_combobox['values'] = [f"{id} - {nombre}" for id, nombre in ubicaciones]
            self.ubicacion_combobox.current(0)

    def _abrir_form_ubicacion(self):
        from .ubicacion_form import UbicacionForm  # Importación local para evitar circular
        UbicacionForm(self.window, self.gestor, self._actualizar_combobox)

    def _actualizar_combobox(self):
        self._cargar_ubicaciones()
        if self.gestor.sistema.ubicaciones:
            self.btn_guardar['state'] = 'normal'

    def _id_aleatorio(self):
        return str(randint(100000, 999999))  # Genera un número entero de 6 dígitos

    def _guardar(self):
        try:
            # Obtener valores del formulario
            id_equipo = self._id_aleatorio()
            nombre = self.nombre_entry.get().strip()
            ubicacion_str = self.ubicacion_combobox.get()
            fecha_instalacion = datetime.strptime(self.fecha_entry.get(), "%Y-%m-%d")
            horas_uso = int(self.horas_entry.get())
            horas_mantenimiento = int(self.horas_mant_entry.get())

            # Validaciones básicas
            if not id_equipo or not nombre or not ubicacion_str:
                raise ValueError("Todos los campos son obligatorios")

            # Obtener ubicación seleccionada
            ubicacion_id = ubicacion_str.split(" - ")[0]
            ubicacion = next(u for u in self.gestor.sistema.ubicaciones if u.id == ubicacion_id)

            # Registrar el equipo
            equipo = self.gestor.registrar_equipo(
                id=id_equipo,
                nombre=nombre,
                ubicacion=ubicacion,
                fecha_instalacion=fecha_instalacion,
                horas_uso=horas_uso
            )
            equipo.horas_mantenimiento = horas_mantenimiento

            messagebox.showinfo("Éxito", "Equipo registrado correctamente")
            self.callback_actualizar()
            self.window.destroy()

        except ValueError as e:
            messagebox.showerror("Error", f"Datos inválidos: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el equipo: {e}")
