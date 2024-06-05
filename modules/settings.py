from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkSlider
import customtkinter as ctk

class SettingsWindow(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure((0,1,2,3,4), weight=1, uniform='a')
        self.grid_columnconfigure((0,1,2,3), weight=1, uniform='a')
        CTkLabel(self, text='Configuración General', font=('Arial', 25)).grid(row=0, rowspan=2, column=1, columnspan=2)
        CTkLabel(self, text='Configurar tema ventana').grid(row=2, column=0)
        CTkButton(self, text='Cambiar Tema', command=self.toggle_dark_light).grid(row=2, column=1)

        CTkLabel(self, text='Escoger tamaño ventana').grid(row=3, column=0)
        self.scale_slider= CTkSlider(self, from_=0.8, to=1.2, number_of_steps=20, command=self.set_scale)
        self.scale_slider.set(1)
        self.scale_slider_count = CTkLabel(self, text=f'Porcentaje: {self.scale_slider.get()}')
        
        self.scale_slider.grid(row=3, column=1)
        self.scale_slider_count.grid(row=3, column=2)

        CTkLabel(self, text='Otra configuración aquí ()').grid(row=4, column=0)


    def toggle_dark_light(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")


    def set_scale(self, value):
        ctk.set_widget_scaling(value)
        self.scale_slider_count.configure(text=f'Porcentaje: {value}')