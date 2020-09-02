# Andrés Cortez, Fernando Lavarreda, Valeria Paiz, Alejandro Ortega
# Universidad del Valle, Programacion Orientada a Objetos
import socket
import gspread as gs
from datetime import datetime

# Clase que almacena multiples Enfermedades y provee de un diagnostico
# Determina si las enfermedades se padecen o no al introducirle datos


class Diagnostico:
    def __init__(self):
        """Inicializar objeto Diagnostico, que contiene multiples Enfermedades"""
        self.enfermedades = []

    def add_enfermedad(self, nombre, umbral):
        """Agregar objeto Enfermedad al Diagnostico"""
        self.enfermedades.append(Enfermedad(nombre, umbral))

    def aumento_enfermedad(self, cantidad, nombre):
        """Incrementar el valor actual de una enfermedad en base a su nombre"""
        for enfermedad in self.enfermedades:
            if enfermedad.nombre == nombre:
                enfermedad.incrementar(cantidad)

    def ver_diagnostico(self):
        """Obtener listado de las enfermedades que dieron positivo"""
        positivos = []
        for enfermedad in self.enfermedades:
            if enfermedad.diagnostico():
                positivos.append(enfermedad.nombre)
        return positivos

    def eliminar_enfermedad(self, nombre):
        """Eliminar une enfermedad de la lista de enfermedades actuales"""
        indexes = []
        counter = 0
        for enfermedad in self.enfermedades:
            if enfermedad.get_nombre() == nombre:
                indexes.append(counter)
            counter += 1
        for index in indexes:
            self.enfermedades.pop(index)

    def clear(self):
        """Cambiar los valores actuales de las enfermedades a cero"""
        for enfermedad in self.enfermedades:
            enfermedad.valorActual = 0

# Clase que modela una enfermedad mental
# Toma como parametros su nombre y el umbral que indica se se padece o no


class Enfermedad:
    def __init__(self, nombre, umbral):
        """Creacion de un objeto que representa una enfermedad mental"""
        self.nombre = ""
        self.umbral = 0
        self.valorActual = 0
        self.set_nombre(nombre)
        self.set_umbral(umbral)

    def diagnostico(self):
        """Metodo para determinar si una enfermedad ha dado positivo o no"""
        if self.umbral <= self.valorActual:
            return True
        else:
            return False

    def incrementar(self, cantidad):
        """Aumental el valor actual de una enfermedad"""
        self.valorActual += cantidad

    def set_nombre(self, nombre):
        """Cambiar el nombre de la enfermedad"""
        self.nombre = nombre

    def set_umbral(self, umbral):
        """Cambiar umbral para la enfermedad"""
        self.umbral = umbral

    def set_valorActual(self, cantidad):
        self.valorActual = cantidad

    def get_nombre(self):
        """Visualizar el nombre de la enfermedad"""
        return self.nombre

    def get_umbral(self):
        """Visualizar umbral de la enfermedad"""
        return self.umbral

    def get_valor_actual(self):
        """Visualizar el valor actual de la enfermedad"""
        return self.valorActual


# Lectura de archivos de texto para crear preguntas y un Diagnostico
# Los archivos de texto contienen en un encabezado la descripcion de las enfermedades
# El encodicicamiento de cada una de ellas sigue el patron Nombre,identificador,umbral;Nombre2,...
# Luego las preguntas siguen el patron: identificadorPreguntaGenerica

class LecturaArchivos:
    def __init__(self):
        """Crear objeto LecturaArchivos para manejar logica de la aplicacion"""
        self.preguntas = {}
        self.respuestas = {}
        self.diagnosis = Diagnostico()
        pass

    def leer_preguntas(self, ruta):
        """Leer preguntas de un archivo de texto"""
        with open(ruta, "r") as fl:
            descripcion = fl.readline().split(";")
            for enf in descripcion:
                enfermedad = enf.split(",")
                self.preguntas[enfermedad[0]] = [enfermedad[1][0], int(enfermedad[2][0:2])]
            preguntas = fl.readlines()
            for pregunta in preguntas:
                for key, value in self.preguntas.items():
                    if pregunta[0] in value[0]:
                        self.preguntas[key].append(pregunta[1:len(pregunta)-1])
        self.actualizar_diagnostico()

    def ver_preg(self):
        """Obtener informacion acerca de las enfermedades y el encodificamiento de la informacion"""
        print(self.preguntas)

    def ver_preguntas(self):
        """Ver preguntas de la aplicacion"""
        preguntas = []
        for value in self.preguntas.values():
            preguntas += value[2:]
        return preguntas

    def clamp_respuestas(self, listado_respuestas):
        """Juntar las preguntas para determinar un diagnóstico"""
        i = 0
        for key in self.preguntas.keys():
            self.respuestas[key] = sum(listado_respuestas[i:len(self.preguntas[key])-2+i])
            i += len(self.preguntas[key])-2
        self.actualizar_diagnostico(False)

    def actualizar_diagnostico(self, enfermedades=True):
        """Actualizar objeto Diagnostico 'self.diagnosis' en base a lectura de archivos de texto """
        if enfermedades:
            for key, value in self.preguntas.items():
                self.diagnosis.add_enfermedad(key, value[1])
        else:
            for key, value in self.respuestas.items():
                self.diagnosis.aumento_enfermedad(value, key)

    def ver_diagnostico(self, conoce=False, enfermedad=""):
        """Obtener diagnostico del usuario"""
        informacion = {}
        if not conoce:
            positivos = self.diagnosis.ver_diagnostico()
        else:
            positivos = [enfermedad]
        if positivos:
            for positivo in positivos:
                with open("resources/"+positivo + ".txt", "r") as fd:
                    descripcion = fd.readlines()
                    informacion[positivo] = [d[:-2] for d in descripcion]
        else:
            informacion["No se Diagnostico nada"] = [""]*22
        return informacion

    def set_to_zero(self):
        """Resetear los valores actuales de las enfermedades"""
        self.diagnosis.clear()

    def grabar_info(self, info, path, wks):
        """Grabar informacion obtenida a Drive, parametros: informacion, direccion credenciales y nombre de archivo"""
        if self.check_connection():
            try:
                cliente = self.access(path)
                sheet = cliente.open(wks).sheet1
                diagnosticos = sheet.col_values(1)
                fechas = sheet.col_values(2)
                sheet.update_cell(row=len(diagnosticos)+1, col=1, value=info)
                sheet.update_cell(row=len(fechas)+1, col=2, value=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            except Exception:
                pass

    def check_connection(self):
        """Vericar conneccion a Internet, retorna bool"""
        try:
            socket.getaddrinfo("google.com", "321")
        except socket.gaierror:
            connection = False
        else:
            connection = True
        return connection

    def access(self, json_description):
        """Proveer Json file path de GoogleCredentials"""
        client = gs.service_account(filename=json_description)
        return client


if __name__ == "__main__":
    prueba = LecturaArchivos()
    prueba.leer_preguntas("resources/prueba1.txt")
    prueba.ver_preg()
    print(prueba.ver_preguntas())
