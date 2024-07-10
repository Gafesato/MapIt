from customtkinter import CTk, CTkToplevel, CTkTabview, CTkFrame, CTkButton, CTkLabel, CTkOptionMenu, CTkEntry, CTkInputDialog, CTkTextbox, CTkSlider
import tkinter as tk
from tkinter import ttk
from json_db import change_db, read_db
from ddbb import getTopicList, addTopic, checkTopic, deleteTopic, updateTopic, addIdea, openDB, addIdeaRelevance


color = ('#11001C', '#F6C0D0')
color2 = ('#fff', '#11001C')



class MessageError(CTkToplevel):
    def __init__(self, master, message):
        super().__init__(master)
        self.state('zoomed')
        self.title("Ventana informativa")
        self.geometry("400x100")

        label = CTkLabel(self, text=message)
        label.pack(pady=20)

        button = CTkButton(self, text="OK", command=self.destroy)
        button.pack(pady=10)


class Subject:
    def __init__(self, parent, tab_name, tab_view):
        self.parent = parent
        self.tab_name = tab_name
        self.subject_tabview = tab_view

            
        self.parent.grid_columnconfigure((0,1,2), weight=1, uniform='a')
        self.parent.grid_rowconfigure((0,1,2,3,4,5), weight=1, uniform='a')

        subject_title = CTkLabel(self.parent, text=f"Lista de Temas")
        subject_title.grid(row=0, column=0)

        self.update_button = CTkButton(self.parent, text='Actualizar nombre', command=self.updateSubject)
        self.update_button.grid(row=0, column=1)

        self.delete_button = CTkButton(self.parent, text='Eliminar tema', command=self.deleteSubject)
        self.delete_button.grid(row=0, column=2)

        # Funcionalidad de añadir temas
        self.topic_entry = CTkEntry(self.parent)
        self.topic_entry.grid(row=5, column=0)
        self.topic_add_btn = CTkButton(self.parent, text='Añadir Tema', command=self.createTopic)
        self.topic_add_btn.grid(row=5, column=1)

        # Create a table in the tab
        self.tree = ttk.Treeview(self.parent)

        # Define the columns
        column1, column2, column3 = "Tema", "Idea", "Importancia"
        self.tree["columns"] = (column1, column2, column3)

        # Format the columns
        self.tree.column("#0", width=0, stretch=tk.NO)  # The ghost column, not used
        self.tree.column(column1, anchor=tk.W, width=100)
        self.tree.column(column2, anchor=tk.W, width=100)
        self.tree.column(column3, anchor=tk.W, width=100)

        # Create the column headings
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading(column1, text=column1, anchor=tk.W)
        self.tree.heading(column2, text=column2, anchor=tk.W)
        self.tree.heading(column3, text=column3, anchor=tk.W)


        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.parent, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        # Position the table and scrollbar in the window
        self.tree.grid(row=1, column=0, rowspan=3, columnspan=2, sticky='nsew')
        scrollbar.grid(row=4, column=2, rowspan=2, sticky='ns')

        # Add data to the table
        self.data = self.get_topics_from_db(self.tab_name)[1]
        for row in self.data:
            self.tree.insert("", tk.END, values=row)


    def get_topics_from_db(self, subject_name):
        """Get the subject data from the json file. """

        db = read_db()
        topics = db["subjects"].get(subject_name, [])

        # 0 -> Get the list
        # 1 -> Insert in the table
        return [topics, [(topic, "", "") for topic in topics]]
    

    def create_delete_button(self, iid):
        # Create a button for deleting a row
        button = CTkButton(self.parent, text="Delete", command=lambda: self.delete_row(iid))
        return button


    def delete_row(self, iid):
        self.tree.delete(iid)


    def createTopic(self):
        """Add the topic tot the table and to JSON file."""
        entry = self.topic_entry.get()
        db = read_db()

        if entry in [' ', ''] or len(entry) < 4:
            MessageError(self.parent, "¡Entrada inválida o muy corta!")
        else:
            data = self.get_topics_from_db(self.tab_name)[0]
            if entry in data:
                MessageError(self.parent, f"El tema {entry} ya existe!")
            if entry not in data:
                # Cambios en JSON
                db["subjects"][self.tab_name].append(entry)
                change_db(db)

                # Cambios en la tabla y el Entry
                self.tree.insert("", tk.END, values=(entry, "", ""))
                self.topic_entry.delete(0, tk.END)


    def updateSubject(self):
        """Update a topic in the JSON file."""

        dialog = CTkInputDialog(text="Ingresar nombre nuevo del tema: ", title="Editar")
        new = dialog.get_input()
        subject_name = self.subject_tabview.get()
        db = read_db()
        if new not in db["subjects"].keys() and new not in [' ', '']:
            if subject_name in db["subjects"]:
                db["subjects"][new] = db["subjects"].pop(subject_name)
                change_db(db)
                self.subject_tabview.rename(subject_name, new)
                self.subject_tabview.set(new)
        else:
            MessageError(self, f"La materia {new} ya existe o error!")


    def deleteSubject(self):
        """Delete a topic from the JSON file and the tabview."""

        db = read_db()
        subject_name = self.subject_tabview.get()
        if subject_name in db["subjects"]:
            del db["subjects"][subject_name]
            change_db(db)
            self.subject_tabview.delete(subject_name)
            self.subject_tabview.set('General')




class ManageWindow(CTkFrame):
    def __init__(self, master):
            super().__init__(master)

            #? Agregar materias
            self.grid_rowconfigure((0,1,2,3), weight=1, uniform='a')
            self.grid_columnconfigure(0, weight=1, uniform='a')
            
            self.subject_tabview = CTkTabview(self)
            self.subject_tabview.grid(row=0, column=0, rowspan=3, sticky='news')
            self.subject_tabview.add('General')
            self.subject_tabview.set('General')

            # Add the existent subjects as Tabs
            db = read_db()
            for subject_name in db["subjects"].keys():
                self.subject_tabview.add(subject_name)
                Subject(self.subject_tabview.tab(subject_name), subject_name, self.subject_tabview)

            self.home_view = self.subject_tabview.tab('General')
            self.home_view.grid_columnconfigure((0,1,2), weight=1)
            self.home_view.grid_rowconfigure((0,1,2), weight=1)

            CTkLabel(self.home_view, text='Lista de Materias').grid(row=0, column=0, sticky='news')
            CTkButton(self.home_view, text='Añadir materia', command=self.addSubject).grid(row=1, column=0)
            self.subject_entry = CTkEntry(self.home_view)
            self.subject_entry.grid(row=1, column=1)
            CTkTextbox(self.home_view).grid(column=0, row=2, sticky='news')



    def addSubject(self):
        """Add the subject to the JSON file."""

        subject = self.subject_entry.get()
        db = read_db()
        total_subjects = len(db["subjects"])
        if subject in db["subjects"].keys():
            MessageError(self, f"La materia {subject} ya existe!")
        elif subject not in [' ', ''] and total_subjects < 6:
            db["subjects"][subject] = []
            change_db(db)
            self.subject_tabview.add(subject)
            Subject(self.subject_tabview.tab(subject), subject, self.subject_tabview)
        else:
            MessageError(self, "No se pueden añadir más de 6 materias o campo incompleto!")
        self.subject_entry.delete(0, tk.END)





