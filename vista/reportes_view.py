"""
Módulo que define la vista de reportes del sistema de gestión de mantenimiento industrial.

Proporciona una interfaz gráfica para visualizar reportes relacionados con equipos,
técnicos, fallas recurrentes y estadísticas generales, además de generar reportes en formato PDF.
"""
import os
import tkinter as tk
from io import BytesIO
from tkinter import ttk, filedialog, messagebox

from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph


class ReportesView:
    """
       Clase que representa la vista de reportes del sistema.

       Permite visualizar reportes de equipos con más mantenimientos, técnicos más activos,
       fallas recurrentes y estadísticas generales. También permite generar y descargar
       reportes en formato PDF.
    """

    def __init__(self, parent, generador_reportes):
        """
                Inicializa la vista de reportes.

                :param parent: Ventana padre donde se abrirá la vista de reportes.
                :param generador_reportes: Objeto encargado de generar los reportes del sistema.
        """
        self.generador = generador_reportes

        self.window = tk.Toplevel(parent)
        self.window.title("Reportes de Mantenimiento")
        self.window.geometry("800x600")

        self._crear_interfaz()
        self._cargar_reportes()

    def _crear_interfaz(self):
        """
                Crea y organiza los elementos de la interfaz gráfica para la vista de reportes.

                Incluye pestañas para visualizar diferentes reportes y un botón para descargar
                reportes en formato PDF.
        """
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

        # Mantenimientos por tipo
        ttk.Label(frame_stats, text="Distribución por tipo:").pack(anchor=tk.W, pady=5)
        self.tipo_frame = ttk.Frame(frame_stats)
        self.tipo_frame.pack(fill=tk.X, pady=5)

        # Reporte de mantenimiento
        ttk.Label(frame_stats, text="Descargar reporte de mantenimiento:").pack(anchor=tk.W, pady=5)
        ttk.Button(frame_stats, text="Descargar PDF", command=self._descargar_pdf).pack(pady=10)

        notebook.add(frame_stats, text='Estadísticas')

    def _cargar_reportes(self):
        """
                Carga los datos de los reportes en las tablas correspondientes.

                Los reportes incluyen:
                - Equipos con más mantenimientos.
                - Técnicos más activos.
                - Fallas recurrentes.
                - Estadísticas generales.
        """
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

        tipos = self.generador.mantenimientos_por_tipo()
        for tipo, count in tipos.items():
            frame = ttk.Frame(self.tipo_frame)
            frame.pack(fill=tk.X, pady=2)

            ttk.Label(frame, text=tipo, width=15).pack(side=tk.LEFT)
            ttk.Progressbar(frame, value=count, maximum=max(tipos.values() or 1)).pack(side=tk.LEFT, expand=True,
                                                                                       fill=tk.X, padx=5)
            ttk.Label(frame, text=str(count)).pack(side=tk.LEFT)

    def _generar_pdf(self):
        """
                Genera un reporte en formato PDF y lo abre directamente desde la memoria.

                Muestra un mensaje de error si ocurre algún problema durante la generación.
        """
        try:
            pdf_buffer = BytesIO()
            self._crear_pdf(pdf_buffer)
            pdf_buffer.seek(0)
            os.startfile(pdf_buffer, 'open')  # Abre el PDF desde memoria
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF: {e}")

    def _descargar_pdf(self):
        """
               Descarga el reporte en formato PDF y lo guarda en el sistema de archivos.

               Muestra un cuadro de diálogo para seleccionar la ubicación y el nombre del archivo.
        """
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("Archivos PDF", "*.pdf")],
                title="Guardar reporte como"
            )
            if file_path:
                with open(file_path, "wb") as f:
                    pdf_buffer = BytesIO()
                    self._crear_pdf(pdf_buffer)
                    f.write(pdf_buffer.getvalue())
                messagebox.showinfo("Éxito", "Reporte guardado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el PDF: {e}")

    def _crear_pdf(self, buffer):
        """
                Crea el contenido del reporte en formato PDF.

                Incluye tablas de equipos, técnicos, ubicaciones y estadísticas gráficas.

                :param buffer: Objeto de tipo BytesIO donde se generará el contenido del PDF.
        """

        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()

        # Título
        elements.append(Paragraph("Reporte de Mantenimiento", styles['Title']))

        # Tabla de equipos
        equipos = [["ID", "Nombre", "Ubicación", "Horas de Uso"]]
        for equipo in self.generador.sistema.equipos:
            equipos.append([equipo.id, equipo.nombre, equipo.ubicacion.nombre, equipo.horas_uso])
        table_equipos = Table(equipos)
        table_equipos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(Paragraph("Equipos registrados", styles['Heading2']))
        elements.append(table_equipos)

        # Tabla de técnicos
        tecnicos = [["ID", "Nombre", "Especialidad", "Activo"]]
        for tecnico in self.generador.sistema.tecnicos:
            tecnicos.append([tecnico.id, tecnico.nombre, tecnico.especialidad, "Sí" if tecnico.activo else "No"])
        table_tecnicos = Table(tecnicos)
        table_tecnicos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(Paragraph("Técnicos registrados:", styles['Heading2']))
        elements.append(table_tecnicos)

        # Tabla de ubicaciones
        ubicaciones = [["ID", "Nombre", "Descripción"]]
        for ubicacion in self.generador.sistema.ubicaciones:
            ubicaciones.append([ubicacion.id, ubicacion.nombre, ubicacion.descripcion])
        table_ubicaciones = Table(ubicaciones)
        table_ubicaciones.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(Paragraph("Ubicaciones regitrados", styles['Heading2']))
        elements.append(table_ubicaciones)

        # Gráfica de estadísticas
        drawing = Drawing(400, 200)
        chart = VerticalBarChart()
        chart.x = 50
        chart.y = 50
        chart.height = 125
        chart.width = 300

        # Datos de la gráfica
        data = [list(self.generador.mantenimientos_por_tipo().values())]
        chart.data = data
        chart.categoryAxis.categoryNames = list(self.generador.mantenimientos_por_tipo().keys())
        chart.bars[0].fillColor = colors.blue

        # Configuración del eje Y
        chart.valueAxis.valueMin = 0
        chart.valueAxis.valueMax = max(max(data)) + 1  # Ajusta el máximo según los datos
        chart.valueAxis.valueStep = 1  # Escala de 1 en 1

        drawing.add(chart)
        elements.append(drawing)
        elements.append(Paragraph("Estadísticas de Mantenimiento", styles['Heading2']))

        # Construir el PDF
        doc.build(elements)
