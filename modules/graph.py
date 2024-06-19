from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkTabview, CTkEntry, CTkInputDialog, CTkTextbox, CTkSlider
import tkinter as tk
from ddbb import getTopicList, createSubjectDB, getSubjectList, addTopic, checkTopic, deleteTopic, updateTopic, addIdea, openDB, addIdeaRelevance
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import matplotlib.pyplot as plt


class GraphWindow(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure((0,1,2,3), weight=1, uniform='a')
        self.grid_columnconfigure((0,1,2,3), weight=1, uniform='a')
        self.tabview = CTkTabview(self)
        self.tabview.grid(row=0, rowspan=3, column=0, columnspan=4, sticky='news')
        self.tab_actual = 'General'

        # Mostrar las materias actuales en la vista TabView
        #createSubjectDB()
        materias = getSubjectList()
        for materia in materias:
            self.tabview.add(materia)

        self.tabview.add(self.tab_actual)
        self.tabview.set(self.tab_actual)


        # Mostrar el grafo para la materia de Fundamentos
        plt.close() # Eliminar la ventana actual de matplotlib para evitar saturación
        fig, ax = plt.subplots(figsize=(1,1))
        canvas = FigureCanvasTkAgg(fig, master=self.tabview.tab('Fundamentos'))
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill='both', expand=True)
        

        G = nx.DiGraph()

        cursor, con = openDB('db/temas1.db')
        # CAMBIAR LA COLUMNA GRUPO_GRAFO POR TIPO RELACION
        cursor.execute('SELECT temas, importancia, grupo_grafo, conexiones FROM grafo WHERE importancia IS NOT " "')
        results = cursor.fetchall()
        topic_list = [query[0] for query in results]
        relevance_list = [query[1] for query in results]
        relation_list = [query[2] for query in results]
        conexion_list = [query[3] for query in results]
        con.close()


        # Agregar temas -> NODOS
        G.add_nodes_from(topic_list)

        # Agregar aristas -> EDGES
        print(relation_list)
        print(conexion_list)

        


        # Dotar tamaño-color de acuerdo a la relevancia
        sizes = {
            'relevante': ['yellow', 1500],
            'detalle': ['skyblue', 800]
        }
        node_color_list = [sizes[relevance][0] for relevance in relevance_list]
        node_size_list = [sizes[relevance][1] for relevance in relevance_list]

        

        # Graficar
        pos = nx.spring_layout(G)
        ax.clear()

        nx.draw_networkx_nodes(G, pos, node_size=node_size_list, node_color=node_color_list)
        nx.draw(G, pos, ax=ax, with_labels=True)
        plt.margins(0.2)
        canvas.draw()

