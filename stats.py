# Modulo para crear archivos de excel y manipular la informacion de la base de datos
# Agregado el 19/09/2020 Fernando Lavarreda
import os
import socket
import gspread as gs
import openpyxl as xl

class ManejoInfo:
    def __init__(self, ruta_json):
        self.route = ruta_json

    def descargar_info(self, ubicacion, nombre):
        if self.check_connection():
            try:
                client = gs.service_account(self.route)
                sheet = client.open("Mindfulness").sheet1
            except Exception as e:
                with open("resources/error.txt") as error:
                    error.write(e)
            else:
                vals1 = sheet.col_values(1)
                vals2 = sheet.col_values(2)
                wb = xl.Workbook()
                wksheet = wb.active
                for value in range(len(vals1)):
                    wksheet.cell(row=value+1, column=1).value = vals1[value]
                    wksheet.cell(row=value+1, column=2).value = vals2[value]
                wb.save(ubicacion+nombre+".xlsx")
                os.startfile(ubicacion+nombre+".xlsx")


    
    def check_connection(self):
        """Vericar conneccion a Internet, retorna bool"""
        try:
            socket.getaddrinfo("google.com", "321")
        except socket.gaierror:
            connection = False
        else:
            connection = True
        return connection

if __name__ == "__main__":
    test = ManejoInfo("resources/creds.json")
    test.descargar_info("c:/users/ferna/", "please")