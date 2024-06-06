from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkOptionMenu, CTkEntry, CTkInputDialog, CTkTextbox, CTkSlider
import tkinter as tk
from ddbb import getTopicList, addTopic, checkTopic, deleteTopic, updateTopic, addIdea, openDB, addIdeaRelevance
#from modules.functions import db_total_rel_topics, update_root_screen, relevance_status, db_topics, db_total_topics

db_topics, db_total_topics = None, None
db_total_rel_topics = int

relevance_status = False

color = ('#11001C', '#F6C0D0')
color2 = ('#fff', '#11001C')

def update_root_screen(process=1, relevance_status=False):
    global db_topics
    global db_total_topics
    global db_total_rel_topics

    db_topics, db_total_topics = getTopicList()
    if process == 1:
        try:
            if db_total_topics > 5:
                db_total_rel_topics = 6
            else:
                db_total_rel_topics = db_total_topics
        except TypeError:
            pass
    
    


def relevance_up_to_date():
    # Especificar relevancia al día
    try:
        cursor, con = openDB('db/user.db')
        cursor.execute('UPDATE user_info SET relevancia = ? WHERE id = ?', (relevance_status, 1,))
        con.commit()
        con.close()
        return True
    except Exception:
        return False


class ManageWindow(CTkFrame):
    """Página con gestión de temas."""

    def __init__(self, master):
        super().__init__(master)

        #! Contenedores de main
        self.grid_columnconfigure((0,1), weight=1, uniform='a')
        self.grid_rowconfigure(0, weight=1, uniform='a')

        self.topics_cont = CTkFrame(self, corner_radius=0)
        self.topics_cont.grid(row=0, column=0, sticky='news')
        self.topics_cont.grid_columnconfigure((0,1,2,3), weight=1, uniform = 'a')
        self.topics_cont.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=1, uniform = 'a')


        self.info_cont = CTkFrame(self, corner_radius=0)
        self.info_cont.grid(row=0, column=1, sticky='news')
        self.info_cont.grid_columnconfigure((0,1), weight=1, uniform = 'a')
        self.info_cont.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=1, uniform = 'a')
        

        #! Lado izquierdo
        topic_title = CTkLabel(self.topics_cont, text="Lista de Temas: ", fg_color='#191919', text_color='#fff')
        self.topic_list = tk.Listbox(self.topics_cont, borderwidth=0, activestyle=tk.DOTBOX, selectborderwidth=2,
                                     selectbackground='#191919', selectforeground='#fff')
        self.topic_add_entry = CTkEntry(self.topics_cont)
        topic_add_btn = CTkButton(self.topics_cont, text='+', font=('Arial', 30), command=self.topic_add_funct)
        topic_detele_btn = CTkButton(self.topics_cont, text='-', font=('Arial', 30), command=self.topic_delete_funct)
        self.status_message = CTkLabel(self.topics_cont, text='Status Operaciones', 
                                       fg_color='#191919', text_color='#fff')

        #? Posición lado izquierdo
        topic_title.grid(row=0, column=0, columnspan=4, sticky='news')

        self.topic_list.grid(row=1, rowspan=3, column=0, columnspan=4, padx=20, sticky='news')
        self.topic_list.bind("<Double-1>", lambda event: self.topic_update_funct(self))

        topic_add_btn.grid(row=4, column=0, sticky='news', padx=10, pady=(10,5))
        self.topic_add_entry.grid(row=4, column=1, sticky='news', pady=10, padx=(0, 10), columnspan=3)
        topic_detele_btn.grid(row=5, column=0, sticky='news', padx=10, pady=(5,10))
        self.status_message.grid(row=7, column=0, columnspan=4, sticky='news')


        #! Lado derecho
        self.introduction_message = CTkLabel(self.info_cont, text='''
1. Tras una clase, agregue 
todos los temas nuevos aprendidos.
                                             
2. Seleccione cuáles son relevantes y 
cuáles son detalles.
                                             
3. Agregue oraciones que describan 
el nuevo tema.
                                             
4. Agregue, elimine o edite temas de 
acuerdo a su preferencia.
                                             
5. Si existen más de 10 temas, 
se recomienda RELACIONAR los temas.
                                             
''')
        self.start_relevance_btn = CTkButton(self.info_cont, text='Empezar relevancia', text_color=color, fg_color=color2,
                                             state='disabled', corner_radius=20, command=lambda: self.add_relevance_funct(delete_flag=True))
        self.introduction_message2 = CTkLabel(self.info_cont, text='''
1. Deben haber más de 5 temas para 
que el botón se habilite.
                                              
2. Proceda a agregar la idea y qué 
tipo de relevancia es para cada tema.
''')
        
        #? Posición lado derecho
        self.introduction_message.grid(row=0, column=0, columnspan=2, rowspan=4, sticky='news')
        self.start_relevance_btn.grid(row=4, column=0, columnspan=2, sticky='news', pady=10, padx=40)
        self.introduction_message2.grid(row=5, column=0, columnspan=2, rowspan=2, sticky='news')

    

        #! LADO DERECHO: Elementos del paso 2
        update_root_screen()
        self.start_relevance_title = CTkLabel(self.info_cont, text=f'Total de temas: {db_total_topics}')
        self.start_relevance_count = CTkLabel(self.info_cont, text=f'Quedan {db_total_rel_topics} temas relevantes')
        self.start_option_title = CTkLabel(self.info_cont, text='', wraplength=150)
        self.start_option_menu = CTkOptionMenu(self.info_cont, corner_radius=20,
                            values=['relevante','detalle'], anchor='center')
        self.start_option_menu.set('')
        self.start_idea_entry = CTkTextbox(self.info_cont, corner_radius=20, fg_color=color2)
        self.start_send_info = CTkButton(self.info_cont, text='Enviar Información', command=self.relevance_send_funct)
        
        self.topic_setup(update_flag=True)
        self.rel_topic_iterator = 0
        self.rel_topic_decrement_iterator = 1
        
        #self.add_idea_message = CTkLabel(self.topics_cont, text='Presione enter para guardar la idea | Edite sobre el texto para guardar', wraplength=150)
        #delete_funct = lambda: self.topic_detele_funct(self.topic_delete_entry, self.topic_list, self.status_message)

        

    def add_relevance_funct(self, delete_flag=False, delete_flag2=False):
        """Itera sobre los temas que no tienen relevancia y pregunta sobre ellos."""

        # Eliminar los elementos del paso 1 del lado derecho y crea los del segundo paso
        if delete_flag:
            self.start_relevance_btn.grid_remove()
            self.introduction_message.grid_remove()
            self.introduction_message2.grid_remove()

            self.start_relevance_title.grid(row=0, column=0, columnspan=2,sticky='news')
            self.start_relevance_count.grid(row=1, column=0, columnspan=2,sticky='news')
            self.start_option_title.grid(row=2, column=0, sticky='news')
            self.start_option_menu.grid(row=2, column=1, sticky='we')
            self.start_idea_entry.grid(row=3, rowspan=3, column=0, columnspan=2, sticky='news')
            self.start_send_info.grid(row=6, column=0, columnspan=2, sticky='news')

            self.relevance_send_funct(first=True)
        
            # Aquí llamar a la función que destruye todos
            # Tener desactivado el botón hasta que se agreguen 3 temás más
            # Repetir el proceso
        if delete_flag2:
            self.introduction_message.grid(row=0, column=0, columnspan=2, rowspan=4, sticky='news')
            self.start_relevance_btn.grid(row=4, column=0, columnspan=2, sticky='news', pady=10, padx=40)
            self.introduction_message2.grid(row=5, column=0, columnspan=2, rowspan=2, sticky='news')
            self.start_relevance_title.grid_remove()
            self.start_relevance_count.grid_remove()
            self.start_option_title.grid_remove()
            self.start_option_menu.grid_remove()
            self.start_idea_entry.grid_remove()
            self.start_send_info.grid_remove()
            self.start_send_info.grid_remove()


    def relevance_send_funct(self, first=False):
        """Verifica que todos los campos de start relevance estén y agrega a la DB."""

        global db_total_rel_topics
        # Actualizar el tema a preguntar por la relevancia


        if self.rel_topic_iterator < db_total_topics:

            update_root_screen()
            topic = db_topics[self.rel_topic_iterator]
            self.start_option_title.configure(text = f'Escoger la relevancia para el tema {topic}')
            self.start_relevance_count.configure(text=f'Quedan {db_total_rel_topics-self.rel_topic_decrement_iterator} temas relevantes')
            self.start_relevance_title.configure(text=f'Total de temas: {db_total_topics}')

            option_entry = self.start_option_menu.get()
            idea_entry = self.start_idea_entry.get('0.0', 'end')

            check_relevant_flag = False
            if option_entry and len(idea_entry) >= 5:
                if option_entry == 'relevante' and self.rel_topic_decrement_iterator < db_total_rel_topics:
                    print(f'TOTAL DB REL TOPICS {db_total_rel_topics}')
                    self.rel_topic_decrement_iterator += 1
                    check_relevant_flag = True
                elif option_entry == 'relevante' and self.rel_topic_decrement_iterator == db_total_rel_topics:
                    self.status_message.configure(text='No quedan temas relevantes!')

                if option_entry == 'detalle' or check_relevant_flag:
                    addIdea(topic=(db_topics[self.rel_topic_iterator]), 
                            relevance=option_entry, idea=idea_entry)
                    self.status_message.configure(text='Añadida la idea y la relevancia con éxito!')

                
                self.start_option_menu.set('')
                self.start_idea_entry.delete('0.0', 'end')
                self.rel_topic_iterator += 1
                self.after(1500, self.relevance_send_funct())
            else:
                if first:
                    self.status_message.configure(text='Agregue las ideas y la relevancia!')
                else:
                    self.status_message.configure(text='Faltan algún o ambos de los campos!')

        else:
            # Volver al paso 1
            self.status_message.configure(text='Ha terminado de agregar las ideas y la relevancia!')
            update_root_screen(relevance_status=True)
            #self.topic_setup()
            self.rel_topic_iterator = 0
            self.rel_topic_decrement_iterator = 0
            self.after(3000, lambda: self.add_relevance_funct(delete_flag2=True))


    def topic_setup(self, update_flag=False):
        """Agrega los temas de la db al listbox y configura el botón de relevancia."""

        if update_flag == True:
            if db_topics != None:
                for topic in db_topics:
                    self.topic_list.insert(tk.END, topic)
            elif db_topics == None:
                self.status_message.configure(text="STATUS --> No hay Temas")

        if db_total_topics != None:
            if db_total_topics >= 5 and relevance_status == False:
                if self.start_relevance_btn.cget('state') == 'disabled':
                    self.start_relevance_btn.configure(state='normal')
            elif relevance_status:
                # Si se está al día con la relevancia, se desactiva el botón
                self.start_relevance_btn.configure(state='disabled')
            else:
                # Con que un solo widget exista, los cierra todos
                if self.start_idea_entry.winfo_exists():
                    self.status_message.configure(text='Ahora tiene menos de 5 temas!')
                    self.add_relevance_funct(delete_flag2=True)

                self.start_relevance_btn.configure(state='disabled')


    def topic_add_funct(self, control_relevance_flag=False):
        """Añade al listbox y a la db el tema."""

        #create_idea = False
        topic_new = self.topic_add_entry.get()
        if checkTopic(topic_new):
            s = f'El tema {topic_new} ya existe.'
        elif topic_new:
            s = 'Error al añadir en la base de datos.'
            if addTopic(topic_new):
                # Modificar Tkinter
                self.topic_list.insert(tk.END, topic_new)
                self.topic_add_entry.delete(0, tk.END)
                s = f'{topic_new} agregado con éxito.'

                # Se indica que es falso porque se ha añadido un nuevo tema, 
                # por lo que se activa el botón de relacionar
                update_root_screen(relevance_status=False)
                self.start_relevance_title.configure(text=f'Total de temas: {db_total_topics}')
                self.start_relevance_count.configure(text=f'Quedan {db_total_rel_topics} temas relevantes')
                self.topic_setup()
                
                #create_idea = True
                #self.after(1, self.get_topic_count())
        else:
            s = 'Error al añadir.'

        self.status_message.configure(text=s)


    def topic_delete_funct(self):
        """Elimina del listbox y la db el tema."""

        try:
            topic_pos = self.topic_list.curselection()[0]
            topic_to_delete = self.topic_list.get(topic_pos)
            if deleteTopic(topic_to_delete):
                self.topic_list.delete(topic_pos)
                s = f"{topic_to_delete} eliminado con éxito."
                update_root_screen()
                self.start_relevance_title.configure(text=f'Total de temas: {db_total_topics}')
                self.start_relevance_count.configure(text=f'Quedan {db_total_rel_topics} temas relevantes')
                self.topic_setup()
                topic = db_topics[self.rel_topic_iterator]
                self.start_option_title.configure(text = f'Escoger la relevancia para el tema {topic}')
        except IndexError:
            s = "Seleccione un tema para eliminar!"
        self.status_message.configure(text=s)


    def topic_update_funct(event, self):
        """Actualiza el tema al dar doble click sobre él."""

        try:
            topic_pos = self.topic_list.curselection()[0]
            topic_before = self.topic_list.get(topic_pos)
            dialog = CTkInputDialog(text=f'Cambiando {topic_before} por:', title=f'Editando...')

            topic_update = dialog.get_input()
            if checkTopic(topic_update):
                s = f'El tema {topic_update} ya existe.'
            elif topic_update:
                updateTopic(topic_before, topic_update)
                s = f"|{topic_before}| se actualizó por |{topic_update}| con éxito."
                # Editar Tkinter
                self.topic_list.delete(topic_pos)
                self.topic_list.insert(topic_pos, topic_update)
            else:
                s = 'Error al actualizar.'
        except IndexError:
            s = 'Agregue un tema!'

        self.status_message.configure(text=s)

    """
    def get_topic_count(self, update_flag=False):
        ""Actualiza el root y la cuenta sobre el total de temas.""

        get_const()
        
        # Actualiza el total de temas en el paso 2
        self.start_relevance_title.configure(text=f'Total de temas: {db_total_topics}')
        self.start_relevance_count.configure(text=f'Quedan {TOTAL_REL_TOPIC_COUNT} temas relevantes')


        if self.db_topics[0] != None and update_flag:
            for topic in self.db_topics[0]:
                self.topic_list.insert(tk.END, topic)
        elif self.db_topics[0] == None and update_flag:
            self.status_message.configure(text="STATUS --> No hay Temas")

        if db_total_topics >= 5:
            self.start_relevance_btn.configure(state='normal', require_redraw=True)
        elif TOTAL_REL_TOPIC_COUNT < 5:
            self.start_relevance_btn.configure(state='disabled', require_redraw=True)
    """