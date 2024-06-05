from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel, CTkOptionMenu, CTkEntry, CTkInputDialog, CTkTextbox, CTkSlider
import tkinter as tk
import customtkinter as c
from ddbb import getTopicList, createDB, addTopic, checkTopic, deleteTopic, updateTopic, addIdea, check_user_db, openDB, addIdeaRelevance
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import matplotlib.pyplot as plt

from ddbb import createDB, check_user_db
from modules.window import App

color = ('#11001C', '#F6C0D0')
color2 = ('#fff', '#11001C')


def main():
    """Función principal que contiene toda la lógica del programa."""

    # Creación de bases de datos
    createDB()
    check_user_db()

    # Configuración de la ventana customtkinter
    c.deactivate_automatic_dpi_awareness()
    c.set_appearance_mode('light')
    c.set_default_color_theme('blue')
    root = App()
    root.mainloop()


if __name__ == '__main__':
    main()