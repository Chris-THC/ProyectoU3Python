import tkinter as tk
from tkinter import ttk


class ReportesView:
    def __init__(self, parent, generador_reportes):
        self.generador = generador_reportes

        self.window = tk.Toplevel(parent)
        self.window.title("Reportes de Mantenimiento")
        self.window.geometry("800x600")

        self._crear_interfaz()
        self._cargar_reportes()

    def _crear_interfaz(self):
        # Notebook para los diferentes reportes
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True)

        # Pestaña 1: Equipos con más mantenimientos
        frame_equipos = ttk.Frame(notebook)
        self.tree_equipos = ttk.Treeview(frame_equipos, columns=('equipo', 'mantenimientos'), show='headings')
        self.tree_equipos.heading('equipo', text='Equipo')
        self.tree_equipos.heading('mantenimientos', text='N° Mantenimientos')
        self.tree_equipos.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        notebook.add(frame_equipos, text='Equipos con más mantenimientos')

        # Pestaña 2: Técnicos más activos
        frame_tecnicos = ttk.Frame(notebook)
        self.tree_tecnicos = ttk.Treeview(frame_tecnicos, columns=('tecnico', 'tareas'), show='headings')
        self.tree_tecnicos.heading('tecnico', text='Técnico')
        self.tree_tecnicos.heading('tareas', text='Tareas Completadas')
        self.tree_tecnicos.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        notebook.add(frame_tecnicos, text='Técnicos más activos')

        # Pestaña 3: Fallas recurrentes
        frame_fallas = ttk.Frame(notebook)
        self.tree_fallas = ttk.Treeview(frame_fallas, columns=('equipo', 'fallas'), show='headings')
        self.tree_fallas.heading('equipo', text='Equipo')
        self.tree_fallas.heading('fallas', text='N° Fallas Reportadas')
        self.tree_fallas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        notebook.add(frame_fallas, text='Fallas recurrentes')

        # Pestaña 4: Estadísticas generales
        frame_stats = ttk.Frame(notebook)

        # Tiempo promedio
        ttk.Label(frame_stats, text="Tiempo promedio de mantenimiento:").pack(anchor=tk.W, pady=5)
        self.tiempo_promedio_var = tk.StringVar()
        ttk.Label(frame_stats, textvariable=self.tiempo_promedio_var, font=('Arial', 12)).pack(anchor=tk.W)

        # Mantenimientos por tipo
        ttk.Label(frame_stats, text="Distribución por tipo:").pack(anchor=tk.W, pady=5)
        self.tipo_frame = ttk.Frame(frame_stats)
        self.tipo_frame.pack(fill=tk.X, pady=5)

        notebook.add(frame_stats, text='Estadísticas')

    def _cargar_reportes(self):
        # Equipos con más mantenimientos
        equipos_top = self.generador.equipos_con_mas_mantenimientos()
        for equipo, count in equipos_top:
            self.tree_equipos.insert('', 'end', values=(equipo.nombre, count))

        # Técnicos más activos
        tecnicos_top = self.generador.tecnicos_mas_activos()
        for tecnico, count in tecnicos_top:
            self.tree_tecnicos.insert('', 'end', values=(tecnico.nombre, count))

        # Fallas recurrentes
        fallas = self.generador.fallas_recurrentes()
        for equipo, count in fallas.items():
            self.tree_fallas.insert('', 'end', values=(equipo, count))

        # Estadísticas generales
        tiempo_prom = self.generador.tiempo_promedio_mantenimiento()
        self.tiempo_promedio_var.set(f"{tiempo_prom:.1f} minutos")

        tipos = self.generador.mantenimientos_por_tipo()
        for tipo, count in tipos.items():
            frame = ttk.Frame(self.tipo_frame)
            frame.pack(fill=tk.X, pady=2)

            ttk.Label(frame, text=tipo, width=15).pack(side=tk.LEFT)
            ttk.Progressbar(frame, value=count, maximum=max(tipos.values() or 1)).pack(side=tk.LEFT, expand=True,
                                                                                       fill=tk.X, padx=5)
            ttk.Label(frame, text=str(count)).pack(side=tk.LEFT)
