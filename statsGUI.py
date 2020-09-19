# Modulo para interactuar de manera grafica con la informacion de los usuarios
# Agregado por Fernando Lavarreda 
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tf
import tkinter.filedialog as fd


class VerInfo(tk.Tk):
    def __init__(self, ManejoEstadisticas):
        super().__init__()
        self.manejo = ManejoEstadisticas
        self.geometry("370x120")
        self.title("Estadisticas MindfulnessGT")
        self.iconbitmap("resources/bar-chart.ico")
        self.config(bg="#74bce3")

        font = tf.Font(size=18, family="Verdana", weight="bold")
        self.titulo = tk.Label(self, bg="#74bce3", font=font, text="Estadísticas MindfulnessGT", foreground="#009c53")
        descarga = ttk.Button(self, text="Descargar informacion", command=self.download)
        self.excel = ttk.Button(self, text="Enviar a Excel", command=self.create, state=tk.DISABLED)
        self.graphs = ttk.Button(self, text="Grafico de Barras", command=self.graphicate, state=tk.DISABLED)

        self.archivo = tk.StringVar()
        ingresar_archivo = tk.Entry(self, textvariable=self.archivo)
        self.lb = tk.Label(self, bg="#74bce3", foreground="#aded3e", text="")

        self.titulo.grid(row=0, column=0, columnspan=4)
        descarga.grid(row=1, column=0, sticky=tk.W+tk.E, padx=5)
        ingresar_archivo.grid(row=2, column=1, columnspan=3, sticky=tk.W+tk.E, padx=10)
        self.lb.grid(row=1, column=1, columnspan=3,  sticky=tk.W+tk.E)
        self.excel.grid(row=2, column=0, sticky=tk.W+tk.E, padx=5)
        self.graphs.grid(row=3, column=0, sticky=tk.W+tk.E, padx=5)

    
    def download(self):
        self.manejo.descargar_info()
        if self.manejo.downloaded:
            self.lb.config(text="Se ha descargado la información")
            self.excel.config(state=tk.ACTIVE)
            self.graphs.config(state=tk.ACTIVE)
        else:
            self.lb.config(text="No se ha podido descargar la información")

    def create(self):
        direc = fd.askdirectory(title="Seleccionar Carpeta")
        if direc:
            if self.archivo.get() != "":
                self.manejo.crear_excel(direc+"/", self.archivo.get())
            else:
                self.manejo.crear_excel(direc, "default_name")
            self.lb.config(text="Se ha creado el archivo")

    def graphicate(self):
        self.manejo.bar_graph()



if __name__ == "__main__":
    vv = VerInfo("")
    vv.mainloop()
