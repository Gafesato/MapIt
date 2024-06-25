from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkEntry
from ddbb import addIdeaRelevance
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import matplotlib.pyplot as plt
#from modules.manage import relevance_up_to_date
from ddbb import getTopicList


class RelateWindow(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # TODO: VERIFICAR SI HAY RELEVANCIA AL DÍA
        self.grid_columnconfigure((0), weight=1, uniform='a')
        self.grid_rowconfigure((0,1), weight=1, uniform='a')
        self.main_button = CTkButton(self, text='Realizar conexiones', border_color='#753742', 
                  border_width=3, fg_color='#554640',
                  hover_color='#AA5042', corner_radius=20, state='disabled')
        #, command=self.create_connections)
        self.status_message = CTkLabel(self, text='Status Operaciones', fg_color='#f56')

        self.main_button.grid(row=0, sticky='s')
        self.status_message.grid(row=1, sticky='swe', padx=100)

        # ! Contenedores principales ocultos
        self.preview_cont = CTkFrame(self, corner_radius=0)
        self.rel_cont = CTkFrame(self, corner_radius=0)
        self.preview_cont.grid_rowconfigure((0,1,2,3,4), weight=1, uniform='a')
        self.preview_cont.grid_columnconfigure((0,1), weight=1, uniform='a')

        self.rel_cont.grid_rowconfigure((0,1,2,3,4,5), weight=1, uniform='a')
        self.rel_cont.grid_columnconfigure((0,1,2,3), weight=1, uniform='a')
        
        #if relevance_up_to_date():
            # Si la relevancia está al día se pueden hacer las conexiones
        self.main_button.configure(state='normal')
        self.status_message.configure(text='Está al día. Puede relacionar!')
        self.main_button.configure(command=lambda: self.create_connections(first=True))
        #else:
            # De lo contrario, el botón está desactivado
            #self.main_button.configure(state='disabled')
            #self.status_message.configure(text='Tiene temas por relacionar todavía!')

        # Obtener la lista de temas que se van a pasar por el proceso del mini grafo
        self.CONTADOR = 0
        try:
            self.topic_list = getTopicList()[2]
        except IndexError:
            self.status_message.configure(text='No tiene temas todavía!')


    def create_connections(self, first=False, success=False):
        if first:
            self.main_button.grid_forget()
            self.status_message.grid_remove()
            self.preview_cont.grid(row=0, column=0, sticky='news')
            self.rel_cont.grid(row=1, column=0, sticky='news')

            self.status_message = CTkLabel(self.rel_cont, fg_color='#f56')
            self.status_message.grid(row=5, column=0, columnspan=4, sticky='news')
        if success:
            self.status_message.configure(text='')

        try:
            topic1, topic2 = self.topic_list[self.CONTADOR], self.topic_list[self.CONTADOR+1]
            title_topics = CTkLabel(self.rel_cont, text=f'¿Cómo se relacionan los temas {topic1} y {topic2}?', wraplength=300)
            reltype_entry = CTkEntry(self.rel_cont, placeholder_text='Tipo de relación')
            label_entry = CTkEntry(self.rel_cont, placeholder_text='Label')

            # Estos datos de aquí se deben obtener desde la DB
            option_menu_topic1 = 'relevante'
            option_menu_topic2 = 'detalle'
            # ---------------------------------------------------

            send_info_btn = CTkButton(self.rel_cont, text='Enviar Info', fg_color='#456',
                                    command=lambda: self.verify_input(label_entry, reltype_entry, option_menu_topic1, option_menu_topic2, topic1, topic2))
        
            question_option = CTkLabel(self.rel_cont, 
                                        text='''
    Las relaciones disponibles son:
    Causal (c) | Consecuencia (cs)
    Estrechamente relacionadas (er)
    Sin relación (sr)
            ''')
        
            title_topics.grid(row=0, column=0, columnspan=2, rowspan=3, sticky='news')
            reltype_entry.grid(row=3, column=0, sticky='we', padx=(10,5))
            label_entry.grid(row=3, column=1, sticky='we', padx=(5,10))
            send_info_btn.grid(row=4, column=0, columnspan=2, sticky='we', padx=20)
            question_option.grid(row=0, rowspan=5, column=2, columnspan=2, sticky='news')

            rel_title = CTkLabel(self.preview_cont, text='Vista Previa de la Relación', fg_color='#045', pady=10)
            box = CTkFrame(self.preview_cont, fg_color='yellow',)
            rel_title.grid(row=0, column=0, columnspan=2, sticky='news')
            box.grid(row=1, rowspan=3, column=0, columnspan=2, sticky='news')


            # Agregar a la DB la relacion, label, relevancia
            accept_graph_btn = CTkButton(self.preview_cont, text='¿Aceptar Previsualización?', command=lambda: self.accept_graph_funct(reltype_entry, label_entry, topic1, topic2, self.topic_list, self.CONTADOR))
            accept_graph_btn.grid(row=4, column=0, columnspan=2)
        except IndexError:
            self.status_message.configure(text='¡Conexiones realizadas con éxito!')



    def verify_input(self, label_entry, reltype_entry, option_menu_topic1, option_menu_topic2, topic1, topic2):
        """Verifica los campos requeridos y envía información para pre visualizar"""

        if not reltype_entry.get() or not label_entry.get():
            self.status_message.configure(text='Falta algún o los dos campos requeridos!')
        elif reltype_entry.get() not in ['cs', 'er', 'c', 'sr']:
            self.status_message.configure(text='Agregue una relación válida')
        elif reltype_entry.get() and label_entry.get():
            self.status_message.configure(text='Mostrando relación con éxito...')
            self.relation_preview(label_entry, reltype_entry, option_menu_topic1, option_menu_topic2, topic1, topic2)


    def relation_preview(self, label_entry, reltype_entry, option_menu_topic1, option_menu_topic2, topic1, topic2):
        """Presenta la visualización de los dos temas que se están relacionando."""

        plt.close() # Eliminar la ventana actual de matplotlib para evitar saturación
        fig, ax = plt.subplots(figsize=(1,1))
        canvas = FigureCanvasTkAgg(fig, master=self.preview_cont)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=1, column=0, columnspan=2, rowspan=3, sticky='news')
        

        G = nx.DiGraph()
        G.add_node(topic1)
        G.add_node(topic2)

        relation_options = ['cs', 'c', 'er']
        if reltype_entry.get() == 'er':
            G.add_edges_from([(topic1, topic2), (topic2, topic1)])
        if reltype_entry.get() in relation_options:
            G.add_edge(topic1, topic2, label=f'{label_entry.get()}')

        pos = nx.spring_layout(G)
        ax.clear()

        # Determinar Tamaño y Color de los nodos
        sizes = {
            'relevante': ['yellow', 1500],
            'detalle': ['skyblue', 800]
        }
        nx.draw(G, pos, ax=ax, with_labels=True, node_size=[sizes[option_menu_topic1][1], sizes[option_menu_topic2][1]],
                node_color=[sizes[option_menu_topic1][0], sizes[option_menu_topic2][0]])
        
        if reltype_entry.get() in relation_options:
            edge_labels = nx.get_edge_attributes(G, 'label')
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.5, font_size=10)
        
        plt.margins(0.2)
        canvas.draw()


    def accept_graph_funct(self, reltype_entry, label_entry, topic1, topic1_to_rel, topic_list, CONTADOR):
        """Agrega los nuevos valores a la DB."""

        if addIdeaRelevance(reltype_entry, label_entry, topic1, topic1_to_rel):
            if CONTADOR + 2 <= len(topic_list):
                # Como se le ha dado enviar al botón, ahora cambia los temas a preguntar por la relacion
                self.CONTADOR += 1
                self.status_message.configure(text='Añadida la idea y la conexión con éxito.')
                return self.create_connections(self)
            else:
                self.preview_cont.destroy()
                self.rel_cont.destroy()
                #CTkLabel("Ahora puede visualizar el grafo").pack(fill='both', expand=True)

        else:
            self.status_message.configure(text='Error al añadir a la base de Datos')