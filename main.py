import customtkinter as c
from modules.window import App
import json


color = ('#11001C', '#F6C0D0')
color2 = ('#fff', '#11001C')


def main():
    """Función principal que contiene toda la lógica del programa."""

    # Creación de bases de datos

    # Configuración de la ventana customtkinter
    c.deactivate_automatic_dpi_awareness()
    c.set_appearance_mode('light')
    c.set_default_color_theme('blue')
    root = App()
    root.mainloop()


if __name__ == '__main__':
    main()
