import customtkinter as CTk
from tkinter import simpledialog

class ManageWindow(CTk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        

root = CTk.CTk()
root.geometry("400x300")

manage_window = ManageWindow(root)
manage_window.grid(row=0, column=0, sticky="nsew")

root.mainloop()