from customtkinter import CTk, CTkFrame, CTkButton, CTkLabel
from modules.settings import SettingsWindow
from modules.manage import ManageWindow
from modules.relate import RelateWindow
from modules.graph import GraphWindow

color = ('#11001C', '#F6C0D0')
color2 = ('#fff', '#11001C')

class MainWindow(CTkFrame):
    """Frame que tiene la información de inicio."""

    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure((0,1,2,3,4,5), weight=1, uniform='a')
        self.grid_columnconfigure((0,1,2,3), weight=1, uniform='a')

        CTkLabel(self, text='Bienvenido a Map It', font=('Arial', 30)).grid(row=0, column=1, columnspan=2, pady=(20,0))
        CTkLabel(self, text="""
Le ayudaremos a crear conexiones duraderas con todos los temas 
                 que está aprendiendo.


    1. Gestión de Temas: Podrá ver, añadir, actualizar, 
                 eliminar sus temas.

    2. Relacionar Temas: Podrá especificar la relevancia del tema y 
                 las conexiones per se.

    3. Visualizar Grafo: Escoga cuál grafo visualizar.
""", 
        font=('Arial', 18), padx=15).grid(row=1, column=0, columnspan=4, rowspan=4, sticky='news')
        CTkLabel(self, text='Gracias por confiar en nososotros. @ Todos los derechos reservados.', 
                 font=('Arial', 16), fg_color=('#000807', '#FBF9FF'), text_color=color2).grid(row=5, column=0, columnspan=4, sticky='news')


class App(CTk):
    """Es el root principal e única instancia de CTk que se llama."""

    def __init__(self):
        super().__init__()
        self.iconbitmap('./img/logo.ico')
        self.geometry('800x500+10+10')
        self.minsize(800, 500)
        self.title('Map It')

        self.option_menu = CTkFrame(self, fg_color=('#F6C0D0','#11001C'), corner_radius=0)
        self.option_menu.place(x=0, y=0, relwidth=0.2, relheight=1)
        CTkLabel(self, text='Bienvenido', font=('Arial', 40)).place(relx=0.4, relwidth=0.4, rely=0.4)
        
        self.option_menu.grid_rowconfigure((0,1,2,3,4,5), weight=1, uniform='a')
        self.option_menu.grid_columnconfigure((0), weight=1, uniform='a')

        self.option_menu_title = CTkLabel(self.option_menu, text='Map It', font=('Arial', 25))
        self.option_menu_main = CTkButton(self.option_menu, fg_color=color, text_color=color2, text='¿Cómo funciona?', command=lambda: self.set_home())
        self.option_menu_manage = CTkButton(self.option_menu, fg_color=color, text_color=color2, text='Gestionar Temas', command=lambda: self.set_home('manage'))
        self.option_menu_relate = CTkButton(self.option_menu, fg_color=color, text_color=color2, text='Relacionar Temas', command=lambda: self.set_home('relate'))
        self.option_menu_visualize = CTkButton(self.option_menu, fg_color=color, text_color=color2, text='Visualizar Grafos', command=lambda: self.set_home('visualize'))
        self.option_menu_settings = CTkButton(self.option_menu, fg_color=color, text_color=color2, text='Configuración', command=lambda: self.set_home('settings'))


        self.option_menu_title.grid(column=0, row=0, sticky='news', pady=(10,0), padx=20)
        self.option_menu_main.grid(column=0, row=1, sticky='we', pady=(10,0), padx=20)
        self.option_menu_manage.grid(column=0, row=2, sticky='we', pady=(10,0), padx=20)
        self.option_menu_relate.grid(column=0, row=3, sticky='we', pady=(10,0), padx=20)
        self.option_menu_visualize.grid(column=0, row=4, sticky='we', pady=(10,0), padx=20)
        self.option_menu_settings.grid(column=0, row=5, sticky='we', pady=(10,0), padx=20)
        


    def set_home(self, option='main'):
        # Cada vez que se llama volver a crear las instancias de los Frames

        if option == "main": frame = MainWindow(self)
        if option == 'manage': frame = ManageWindow(self)
        if option == 'visualize': frame = ManageWindow(self)
        if option == 'relate': frame = ManageWindow(self)
        if option == 'settings': frame = SettingsWindow(self)
        frame.place(relx=0.2, y=0, relwidth=0.8, relheight=1)