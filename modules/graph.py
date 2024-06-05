class VisualizeWindow(CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure((0,1,2,3), weight=1, uniform='a')
        self.grid_columnconfigure((0,1,2,3), weight=1, uniform='a')
        CTkLabel(self, text='Visualizar').grid(row=0, column=1, columnspan=2)