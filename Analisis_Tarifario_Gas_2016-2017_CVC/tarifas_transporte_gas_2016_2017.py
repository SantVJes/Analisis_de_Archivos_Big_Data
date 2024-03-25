#Created by:Jesus Santiago Velasco  20/03/2024
#Email: Sanjesvel@outlook.com
'''Librerias'''
import pandas as pd
import matplotlib.pyplot as plt
import waterfall_chart

'''Variables'''
datos_cvs = None
columnas_prom = []

'''Funciones'''

#Declaramos una funcion donde el usuario ingrese el la ruta del archivo csv
def validar_archivo_csv():
     while True:
        ruta_archivo = input("Ingrese la ruta del archivo CSV: ")
        if ruta_archivo: #Validamos si la ruta es valida
            try: #validamos si es un archivo cvs
                datos_cvs = pd.read_csv(ruta_archivo)
                print("Archivo CSV seleccionado Correctamente \n")  
                return datos_cvs
            except Exception as e:
                print("Error al abrir el archivo asegurese si es una archivo CVS", e)
        else:
            print("La ruta ingresada no es válida.")



'''Codijo_Principal'''

datos_cvs = validar_archivo_csv()





