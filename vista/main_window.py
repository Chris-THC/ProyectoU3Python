import tkinter as tk
from tkinter import ttk, messagebox

from control.gestor_mantenimiento import GestorMantenimiento
from control.reportes import GeneradorReportes
from modelo.entidades import EstadoTarea
from modelo.persistencia import PersistenciaJSON
from vista.forms.equipo_form import EquipoForm
from vista.forms.tarea_form import TareaForm
from vista.forms.tecnico_form import TecnicoForm
from vista.forms.ubicacion_form import UbicacionForm
from vista.reportes_view import ReportesView


class MainWindow:
    def __init__(self, gestor: GestorMantenimiento, generador_reportes: GeneradorReportes):
        self.gestor = gestor
        self.generador_reportes = generador_reportes

        self.root = tk.Tk()
        self.root.title("Sistema de Gestión de Mantenimiento Industrial")
        self.root.geometry("1100x500")

        self._crear_menu()
        self._crear_boton_ubicacion()
        self._crear_interfaz()

        self.actualizar_listados()

    def _crear_menu(self):
        menubar = tk.Menu(self.root)

        # Menú Archivo
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menu_archivo.add_command(label="Salir", command=self.root.quit)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)

        # Menú Registros
        menu_registros = tk.Menu(menubar, tearoff=0)
        menu_registros.add_command(label="Nuevo Equipo", command=self.abrir_form_equipo)
        menu_registros.add_command(label="Nuevo Técnico", command=self.abrir_form_tecnico)
        menu_registros.add_command(label="Nueva Tarea", command=self.abrir_form_tarea)
        menubar.add_cascade(label="Registros", menu=menu_registros)

        # Menú Reportes
        menu_reportes = tk.Menu(menubar, tearoff=0)
        menu_reportes.add_command(label="Ver Reportes", command=self.mostrar_reportes)
        menubar.add_cascade(label="Reportes", menu=menu_reportes)

        self.root.config(menu=menubar)

    def _crear_interfaz(self):
        # Panel principal
        panel_principal = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        panel_principal.pack(fill=tk.BOTH, expand=True)

        # Panel izquierdo (listados)
        panel_izquierdo = ttk.Frame(panel_principal, width=300)
        panel_principal.add(panel_izquierdo)

        # Notebook para los listados
        notebook = ttk.Notebook(panel_izquierdo)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Pestaña de equipos
        frame_equipos = ttk.Frame(notebook)
        self.tree_equipos = ttk.Treeview(frame_equipos, columns=('nombre', 'ubicacion'), show='headings')
        self.tree_equipos.heading('nombre', text='Nombre')
        self.tree_equipos.heading('ubicacion', text='Ubicación')
        self.tree_equipos.pack(fill=tk.BOTH, expand=True)

        # Botón de eliminación de equipos
        btn_eliminar_equipo = ttk.Button(frame_equipos, text="Eliminar Equipo", command=self.eliminar_equipo)
        btn_eliminar_equipo.pack(pady=5, side=tk.LEFT)

        notebook.add(frame_equipos, text='Equipos')

        # Pestaña de técnicos
        frame_tecnicos = ttk.Frame(notebook)
        self.tree_tecnicos = ttk.Treeview(frame_tecnicos, columns=('nombre', 'especialidad'), show='headings')
        self.tree_tecnicos.heading('nombre', text='Nombre')
        self.tree_tecnicos.heading('especialidad', text='Especialidad')
        self.tree_tecnicos.pack(fill=tk.BOTH, expand=True)

        # Botón de eliminación de técnicos
        btn_eliminar_tecnico = ttk.Button(frame_tecnicos, text="Eliminar Técnico", command=self.eliminar_tecnico)
        btn_eliminar_tecnico.pack(pady=5, side=tk.LEFT)

        notebook.add(frame_tecnicos, text='Técnicos')

        # Pestaña de tareas
        frame_tareas = ttk.Frame(notebook)
        self.tree_tareas = ttk.Treeview(frame_tareas, columns=('id', 'equipo', 'tipo', 'estado'), show='headings')
        self.tree_tareas.heading('id', text='ID')
        self.tree_tareas.heading('equipo', text='Equipo')
        self.tree_tareas.heading('tipo', text='Tipo')
        self.tree_tareas.heading('estado', text='Estado')
        self.tree_tareas.pack(fill=tk.BOTH, expand=True)

        # Botones específicos para la pestaña de tareas
        btn_cambiar_estado = ttk.Button(frame_tareas, text="Cambiar Estado", command=self.cambiar_estado_tarea)
        btn_cambiar_estado.pack(pady=5, side=tk.LEFT)

        btn_eliminar_tarea = ttk.Button(frame_tareas, text="Eliminar Tarea", command=self.eliminar_tarea)
        btn_eliminar_tarea.pack(pady=5, side=tk.LEFT)

        notebook.add(frame_tareas, text='Tareas')

        # Panel derecho (detalles)
        panel_derecho = ttk.Frame(panel_principal)
        panel_principal.add(panel_derecho)

        # Área de alertas
        frame_alertas = ttk.LabelFrame(panel_derecho, text="Alertas de Mantenimiento", padding=10)
        frame_alertas.pack(fill=tk.X, padx=5, pady=5)

        self.lista_alertas = tk.Listbox(frame_alertas)
        self.lista_alertas.pack(fill=tk.BOTH, expand=True)

    def actualizar_listados(self):
        # Actualizar listado de equipos
        self.tree_equipos.delete(*self.tree_equipos.get_children())
        for equipo in self.gestor.sistema.equipos:
            self.tree_equipos.insert('', 'end', values=(equipo.nombre, equipo.ubicacion.nombre))

        # Actualizar listado de técnicos
        self.tree_tecnicos.delete(*self.tree_tecnicos.get_children())
        for tecnico in self.gestor.sistema.tecnicos:
            self.tree_tecnicos.insert('', 'end', values=(tecnico.nombre, tecnico.especialidad))

        # Actualizar listado de tareas
        self.tree_tareas.delete(*self.tree_tareas.get_children())
        for tarea in self.gestor.sistema.tareas:
            self.tree_tareas.insert('', 'end', values=(
                tarea.id,  # Incluye el ID como primer valor
                tarea.equipo.nombre,
                tarea.tipo.name,
                tarea.estado.name
            ))

        # Actualizar alertas
        self.lista_alertas.delete(0, tk.END)
        alertas = self.gestor.verificar_alertas_mantenimiento()
        for equipo in alertas:
            self.lista_alertas.insert(tk.END, f"{equipo.nombre} necesita mantenimiento")

    def cambiar_estado_tarea(self):
        # Obtener tarea seleccionada
        selected_item = self.tree_tareas.selection()
        if not selected_item:
            return  # No hay tarea seleccionada

        # Acceder al ID de la tarea desde el primer valor
        tarea_id = self.tree_tareas.item(selected_item, 'values')[0]

        tarea = next((t for t in self.gestor.sistema.tareas if t.id == tarea_id), None)

        if tarea:
            # Alternar estado
            if tarea.estado == EstadoTarea.PENDIENTE:
                tarea.estado = EstadoTarea.COMPLETADA
            elif tarea.estado == EstadoTarea.COMPLETADA:
                tarea.estado = EstadoTarea.PENDIENTE
            messagebox.showinfo("Éxito", f"Nuevo Estado: '{tarea.estado.name}'")

            # Actualizar Treeview
            self.actualizar_listados()

            # Guardar cambios en el archivo JSON
            persistencia = PersistenciaJSON()
            persistencia.guardar(self.gestor.sistema)

    def _crear_boton_ubicacion(self):
        # Frame para el botón en la parte superior
        self.frame_botones = ttk.Frame(self.root)
        self.frame_botones.pack(fill=tk.X, padx=5, pady=5)

        # Botón destacado para ubicaciones
        btn_ubicacion = ttk.Button(
            self.frame_botones,
            text="➕ Registrar Ubicación",
            command=self.abrir_form_ubicacion,
            style='Accent.TButton'  # Estilo destacado (requiere tema 'azure' o similar)
        )
        btn_ubicacion.pack(side=tk.LEFT, padx=5)

    def eliminar_tarea(self):
        # Obtener tarea seleccionada
        selected_item = self.tree_tareas.selection()
        if not selected_item:
            print("No hay tarea seleccionada")  # Depuración
            return

        # Obtener el ID de la tarea seleccionada
        tarea_id = self.tree_tareas.item(selected_item, 'values')[0]
        print("ID de tarea seleccionada para eliminar:", tarea_id)  # Depuración

        # Buscar y eliminar la tarea del sistema
        tarea = next((t for t in self.gestor.sistema.tareas if t.id == tarea_id), None)
        if tarea:
            self.gestor.sistema.tareas.remove(tarea)
            print(f"Tarea {tarea_id} eliminada del sistema")  # Depuración

            # Guardar cambios en el archivo JSON
            persistencia = PersistenciaJSON()
            persistencia.guardar(self.gestor.sistema)

            # Actualizar la tabla de tareas
            self.actualizar_listados()
        else:
            print(f"Tarea {tarea_id} no encontrada")  # Depuración

    def eliminar_equipo(self):
        selected_item = self.tree_equipos.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "No hay equipo seleccionado")
            return

        equipo_id = self.tree_equipos.item(selected_item, 'values')[0]
        equipo = next((e for e in self.gestor.sistema.equipos if e.nombre == equipo_id), None)

        if equipo and not self.gestor.obtener_tareas_por_equipo(equipo.id):
            self.gestor.sistema.equipos.remove(equipo)
            messagebox.showinfo("Éxito", f"Equipo '{equipo.nombre}' eliminado correctamente")
            PersistenciaJSON().guardar(self.gestor.sistema)
            self.actualizar_listados()
        else:
            messagebox.showerror("Error", "No se puede eliminar el equipo porque tiene tareas asociadas")

    def eliminar_tecnico(self):
        selected_item = self.tree_tecnicos.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "No hay técnico seleccionado")
            return

        tecnico_id = self.tree_tecnicos.item(selected_item, 'values')[0]
        tecnico = next((t for t in self.gestor.sistema.tecnicos if t.nombre == tecnico_id), None)

        if tecnico and not self.gestor.obtener_tareas_por_tecnico(tecnico.id):
            self.gestor.sistema.tecnicos.remove(tecnico)
            messagebox.showinfo("Éxito", f"Técnico '{tecnico.nombre}' eliminado correctamente")
            PersistenciaJSON().guardar(self.gestor.sistema)
            self.actualizar_listados()
        else:
            messagebox.showerror("Error", "No se puede eliminar el técnico porque tiene tareas asociadas")

    def abrir_form_equipo(self):
        EquipoForm(self.root, self.gestor, self.actualizar_listados)

    def abrir_form_tecnico(self):
        TecnicoForm(self.root, self.gestor, self.actualizar_listados)

    def abrir_form_tarea(self):
        TareaForm(self.root, self.gestor, self.actualizar_listados)

    def mostrar_reportes(self):
        ReportesView(self.root, self.generador_reportes)

    def abrir_form_ubicacion(self):
        # Método para abrir el formulario de ubicación
        UbicacionForm(self.root, self.gestor, self.actualizar_listados)

    def ejecutar(self):
        self.root.mainloop()
