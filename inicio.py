# Andrés Cortez, Fernando Lavarreda, Valeria Paiz, Alejandro Ortega
# Universidad del Valle, Programacion Orientada a Objetos

import tkinter as tk
import tkinter.font as tf
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import preguntas as pg

# Ventana de inicio de la aplicacion toma como argumentos un objeto LecuraArchivos
# Punto de partida para el usuario


class App(tk.Tk):
    def __init__(self, lectura):
        super().__init__()
        self.lectura = lectura
        font = tf.Font(size=3)
        self.geometry("230x260")
        self.iconbitmap("resources/meditation.ico")
        self.config(bg="#5a84cd")
        self.title("Mindfulness")
        img = ImageTk.PhotoImage(Image.open("resources/mindfulness.png").resize((190, 190)))
        self.canvas_main_logo = tk.Canvas(self, width=200, height=200, bg="teal")
        self.canvas_main_logo.create_image(102, 100, anchor=tk.CENTER, image=img)
        self.canvas_main_logo.image = img
        self.canvas_main_logo.grid(row=1, column=1, columnspan=10)

        self.info = ttk.Button(self, text="Información", command=self.instruct).grid(row=3, column=5)
        self.cuestionario = ttk.Button(self, text="Cuestionario", command=self.preguntas).grid(row=3, column=6)

        self.lb = tk.Label(self, text="     ", bg="#5a84cd", font=font).grid(row=0, column=0)
        self.lb1 = tk.Label(self, text="     ", bg="#5a84cd", font=font).grid(row=2, column=0)

    def instruct(self):
        """Mostrar instrucciones a pantalla"""
        inst = Instructions()

    def preguntas(self):
        """Generar GUI con el cuestionario, pasando objeto LecturaArchivos"""
        preguntas = pg.MyApp(self.lectura)


class Instructions(tk.Toplevel):
    def __init__(self):
        """Inicializar objeto que muestra las instrucciones del programa"""
        super().__init__()
        self.grab_set()
        self.geometry("345x300")
        self.iconbitmap("resources/meditation.ico")
        self.txt = tk.Text(self, width=250, height=260)
        self.txt.pack()
        self.description = """
Bienveni@ a Mindullness GT
----------------------------

Acerca de nosotros.......
Nuestro propósito........

Instrucciones:
    1. Llenar Cuestionario
    2. Hacer diagnóstico
    3. Obtener Resultados
    4. Realizar Tratamiento

¿Cómo llenar el Cuestionario?
    -Lee cada uno de los ítems atentamente 
    e indica cuánto le ha afectado 
    en la última semana. 
    (0 siendo nada - 3 siendo extremo)       
        """
        self.fill_it()

    def fill_it(self):
        """Proveer del texto a las instrucciones"""
        self.txt.insert(tk.END, self.description)


if __name__ == "__main__":
    app = App()
    app.mainloop()
