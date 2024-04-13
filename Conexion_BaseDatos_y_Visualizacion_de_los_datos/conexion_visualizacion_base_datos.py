#Created by:Jesus Santiago Velasco  12/04/2024
#Email: Sanjesvel@outlook.com
'''Librerias'''
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import os
'''Variables'''
datos_csv = None
'''Funciones'''
#Declaramos una funcion donde el usuario ingrese el la ruta del archivo csv
def validar_archivo_csv():

    while True:
        ruta_archivo = input("Ingrese la ruta del archivo CSV: ")
        if ruta_archivo: # Validamos si la ruta es valida
            try: # validamos si es un archivo cvs
                datos_csv = pd.read_csv(ruta_archivo)
                print("Archivo CSV seleccionado Correctamente \n")  
                return datos_csv
            except Exception as e:
                print("Error al abrir el archivo asegurese si es una archivo CSV", e)
        else:
            print("La ruta ingresada no es válida.")

# Declaramos la funcion para Selecionar la zona y columnas del Archivo CVS para analizar
def seleccion_zona_y_columnas(datos_csv):
    '''Variables'''
    columnas_a_analizar =[]
    zonas = None
    selec_zona = None
    columnas = None
    num_columnas = None
    
    while True: # bucle por si el usuario selecione una zona invalida 
        zonas = datos_csv["zona"].unique() 
        print("Zonas del archivo CSV:") 
        for i in range(len(zonas)): # Muestra las zonas disponibles
            print(f"{i+1}.{zonas[i]}")
        
        selec_zona = input("\nPor favor, Ingresa el nombre de la zona que desea analizar: ")
        if selec_zona in zonas: # Verifica si la zona eliguida es valida 
            print(f"\nHas seleccionado la zona '{selec_zona}' para analizar.")
            selec_zona = datos_csv[datos_csv["zona"]== selec_zona] 
            # Selección de columnas
            while True: # bucle por si el usuario selecione una columna o una cantidad de columnas a analizar invalida
                columnas = datos_csv.select_dtypes(include='float').columns
                print("\nColumnas disponibles a analizar:")
                for i in range(len(columnas)): # Muestra las columnas Disponibles
                    print(f"{i+1}.{columnas[i]}")
                print(f"{len(columnas) + 1}.Ingresa el numero 7 para Analizar todas")
                # El try son por el motivo si el usario mete un dato erronio pueda continuar el progrmas sin fallar
                num_columnas = input("\nPor favor, ingrese cuantas columnas desea analizar: ")
                try: # Verifica si el dato es entero
                    num_columnas = int(num_columnas)
                except ValueError:
                    os.system('clear')
                    print("Error: Debe ingresar un número entero.")
                    continue
                # Verifica si el numero de columnas para analisar esta dentro del rango invalido
                if num_columnas <= 0 or num_columnas > len(columnas): 
                    os.system('clear') # Limpia la consola
                    print("Error: El numero de columnas a analizar no es valido.")
                if num_columnas == len(columnas) :
                    columnas_a_analizar= columnas
                else:
                    print("\nPor favor, ingrese el nombre de las columnas a analizar:")
                    for k in range(num_columnas): #
                      while True:
                        print("\nColumnas disponibles a analizar:")
                        for i in range(len(columnas)): # Muestra las columnas disponibles para seleccionar
                            print(f"{i+1}.{columnas[i]}")
                       
                        nombre_columna = input(f"\ningrese el nombre de la columna {k+1} eligida a analizar: ")
                        if nombre_columna in columnas: # Verifica si la columna ingresada es valida
                            columnas_a_analizar.append(nombre_columna)
                            break
                        else:
                            os.system('clear') # Limpia la consola
                            print(f"Error: La columna '{nombre_columna}' no existe en el archivo CSV.")    
                break  # Salir del bucle while de selección de columnas
            return selec_zona, columnas_a_analizar
        else:
            os.system('clear') # Limpia la consola
            print("\nLa zona seleccionada no es válida. Por favor, intente nuevamente.\n")
 
#Declaramos la Funcion para la conexion con la base  de datos 
def conexion_basedatos():
    try:
        # Conexión a la base de datos
        myconexion = pymysql.connect(
            host= 'localhost',
            user= 'root',
            passwd= '',
            db= 'Conexion_Big_data'
        )
        print("Conexión exitosa a la base de datos.")
        return myconexion

    except pymysql.Error as e:
        print(f"No se puede conectar a la base de datos: {e}")
        return None

#Declaramos la funcion para crear la tabla en la base de datos 
def crear_tabla_variacion_gas():
    try:
        # Conexión a la base de datos
        myconexion = conexion_basedatos()
        if myconexion:
            # Crear un cursor para ejecutar consultas
            mycursor = myconexion.cursor()

            # Consulta para crear la tabla
            mycursor.execute("""CREATE TABLE IF NOT EXISTS Variacion_del_costo_del_transporte_del_gas_2016_2017(
             zona VARCHAR(50) ,
             capacidad_base_firme DOUBLE NOT NULL,
             uso_base_firme DOUBLE NOT NULL,
             capacidad_base_temporal DOUBLE NOT NULL,
             uso_base_temporal DOUBLE NOT NULL,
             maxima_base_interrumpible DOUBLE NOT NULL,
             minima_base_interrumpible DOUBLE NOT NULL,
             volumetrica DOUBLE NOT NULL
             );""")
            #confirmamos la transaccion
            myconexion.commit()
            print("Tabla creada exitosamente.")
            
            # Cerrar el cursor
            mycursor.close()
            
    except pymysql.Error as e:
        print(f"Error al crear la tabla: {e}")

    finally:
        # Cerrar la conexión
        if myconexion:
            myconexion.close() 


def insertar_datos_variacion_gas(zona,variacion_porcentual_columnas):
    try:
        # Conexión a la base de datos
        myconexion = conexion_basedatos()
        # Creamos la tabla si no existe 
        crear_tabla_variacion_gas()
        if myconexion:
            # Crear un cursor para ejecutar consultas
            mycursor = myconexion.cursor()
         
            mycursor.execute("""INSERT INTO Variacion_del_costo_del_transporte_del_gas_2016_2017(
                zona, 
                capacidad_base_firme, uso_base_firme, 
                capacidad_base_temporal, 
                uso_base_temporal, maxima_base_interrumpible,
                minima_base_interrumpible,
                volumetrica )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (zona,
             variacion_porcentual_columnas[0],
             variacion_porcentual_columnas[1],
             variacion_porcentual_columnas[2], 
             variacion_porcentual_columnas[3], 
             variacion_porcentual_columnas[4],
             variacion_porcentual_columnas[5],
             variacion_porcentual_columnas[6]))
            # Confirmar la transacción
            myconexion.commit()

            print("Datos insertados correctamente.")

            # Cerrar el cursor
            mycursor.close()

    except pymysql.Error as e:
        print(f"Error al insertar datos en la tabla: {e}")

    finally:
        # Cerrar la conexión
        if myconexion:
            myconexion.close()

#Declaramos Fucion que calcule la variacion porcentual del precio de gas alo largo de los 2 años
def variacion_porcentual_precio_gas_2016_2017(datos_csv):
    '''Variables'''
    zona_A_analizar = None
    columnas_selec_variacion = []
    variacion_porcentual_columnas  = []
    iterador1= 0
    zona_A_analizar, columnas_selec_variacion = seleccion_zona_y_columnas(datos_csv)
    while iterador1 < len(columnas_selec_variacion):# while Precios del gas natural al inicio y al final de los dos años de una misma columna donde lo multiplacamos por 100 para tener el porcentaje de la variacion 
        variacion_porcentual_columnas.append( ((zona_A_analizar[columnas_selec_variacion[iterador1]].iloc[-1] - zona_A_analizar[columnas_selec_variacion[iterador1]].iloc[0]) / zona_A_analizar[columnas_selec_variacion[iterador1]].iloc[0])* 100 ) 
        iterador1 += 1  
    #Insertamos los datos Obtenidos en la base de datos 
    insertar_datos_variacion_gas(zona_A_analizar["zona"].unique(),variacion_porcentual_columnas)
    preguntar_graficar(f"Variacion del costo del transporte del gas 2016-2017 de la zona {zona_A_analizar["zona"].unique()}","Columnas analizadas del archivo csv","Variacion porcentual entre 2016-2017",columnas_selec_variacion,variacion_porcentual_columnas)

    
#funcion que pregunta al usuario si desea graficar los datos
def preguntar_graficar(titulografic,nombre_eje_x,nombre_eje_y,columnas_selec,valores_a_graficar):
    respuesta = input("¿Deseas graficar los datos? (s/n): ")
    if respuesta.lower() == 's':
        tipo_grafica = int(input("Selecciona el tipo de gráfica que deseas realizar:\n1. Gráfico de líneas\n2. Gráfico de barras\n3. Gráfico de dispersión\n4. Gráfico de pastel\n\nIngrese el número correspondiente a tu elección: ") ) 
         # Realizar la gráfica según la elección del usuario
        if tipo_grafica == 1:
          graficar_linias(titulografic,nombre_eje_x,nombre_eje_y,columnas_selec,valores_a_graficar)
        elif tipo_grafica == 2:
          graficar_barras(titulografic,nombre_eje_x,nombre_eje_y,columnas_selec,valores_a_graficar)
        elif tipo_grafica == 3:
          graficar_scatter(titulografic,nombre_eje_x,nombre_eje_y,columnas_selec,valores_a_graficar)
        elif tipo_grafica == 4:
          graficar_pie(titulografic,nombre_eje_x,nombre_eje_y,columnas_selec,valores_a_graficar)
        else:
          print("No se graficaron datos.")
    
#funciones para grafiacar las diferesntes tipo de visualizacion de los datos 
def graficar_barras(titulografic,nombre_eje_x,nombre_eje_y,columnas_selec,valores_a_graficar):
   
       fig ,ax = plt.subplots(figsize=(20, 8))  # Crear la figura y los ejes 
       """Creamos Las Graficas En forma de lineas de las Zonas """
       plt.suptitle(f"{titulografic} ", fontsize=16, fontweight="bold") #Titulo de la hoja de las Graficas
       """Graficamos Las 2 Primeras Columnas de la zona"""
       ax.bar(columnas_selec,valores_a_graficar,  color = 'tab:purple' )  #Graficamos el Precio por capacidad base firme ("Asignamos el rango Y Enbellecimietno ")
       ax.set_ylabel(f"{nombre_eje_y}" , ) #Asignamos Nombre al Eje y
       ax.set_title(f'{titulografic}', loc = "left", fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:purple'}) #Asignamos un Titulo Ala grafica
       ax.set_xticklabels(columnas_selec,rotation=10, fontdict = { 'fontsize':8,'fontweight':'bold','color':'tab:blue'})  # Acomodamos los rangos del eje x s
       ax.set_xlabel(f"{nombre_eje_x}",rotation = 0 ,fontdict = { 'fontsize':14, 'fontweight':'bold', 'color':'tab:purple'}) #Asignamos Titulo al Eje X 
       plt.show()
  

def graficar_linias(titulografic,nombre_eje_x,nombre_eje_y,columnas_selec,valores_a_graficar):
    
       fig ,ax = plt.subplots(figsize=(20, 8))  # Crear la figura y los ejes 
       """Creamos Las Graficas En forma de Barras de las Zonas """
       plt.suptitle(f"{titulografic} ", fontsize=16, fontweight="bold") #Titulo de la hoja de las Graficas
       """Graficamos Las 2 Primeras Columnas de la zona"""
       ax.plot(columnas_selec,valores_a_graficar,  color = 'tab:purple' )  #Graficamos el Precio por capacidad base firme ("Asignamos el rango Y Enbellecimietno ")
       ax.set_ylabel(f"{nombre_eje_y}" , ) #Asignamos Nombre al Eje y
       ax.set_title(f'{titulografic}', loc = "left", fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:purple'}) #Asignamos un Titulo Ala grafica
       ax.set_xticklabels(columnas_selec,rotation=10, fontdict = { 'fontsize':8,'fontweight':'bold','color':'tab:blue'})  # Acomodamos los rangos del eje x s
       ax.set_xlabel(f"{nombre_eje_x}",rotation = 0 ,fontdict = { 'fontsize':14, 'fontweight':'bold', 'color':'tab:purple'}) #Asignamos Titulo al Eje X 
       plt.show()
    
def graficar_scatter(titulografic,nombre_eje_x,nombre_eje_y,columnas_selec,valores_a_graficar):
 
       fig ,ax = plt.subplots(figsize=(20, 8))  # Crear la figura y los ejes 
       """Creamos Las Graficas En forma de  dispercion de las Zonas """
       plt.suptitle(f"{titulografic} ", fontsize=16, fontweight="bold") #Titulo de la hoja de las Graficas
       """Graficamos Las 2 Primeras Columnas de la zona"""
       ax.scatter(columnas_selec,valores_a_graficar,  color = 'tab:purple' )  #Graficamos el Precio por capacidad base firme ("Asignamos el rango Y Enbellecimietno ")
       ax.set_ylabel(f"{nombre_eje_y}" , ) #Asignamos Nombre al Eje y
       ax.set_title(f'{titulografic}', loc = "left", fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:purple'}) #Asignamos un Titulo Ala grafica
       ax.set_xticklabels(columnas_selec,rotation=10, fontdict = { 'fontsize':8,'fontweight':'bold','color':'tab:blue'})  # Acomodamos los rangos del eje x s
       ax.set_xlabel(f"{nombre_eje_x}",rotation = 0 ,fontdict = { 'fontsize':14, 'fontweight':'bold', 'color':'tab:purple'}) #Asignamos Titulo al Eje X 
       plt.show()
  
def graficar_pie(titulografic,nombre_eje_x,nombre_eje_y,columnas_selec,valores_a_graficar):

       fig ,ax = plt.subplots(figsize=(20, 8))  # Crear la figura y los ejes 
       """Creamos Las Graficas En forma de pastel de las Zonas """
       plt.suptitle(f"{titulografic} ", fontsize=16, fontweight="bold") #Titulo de la hoja de las Graficas
       """Graficamos Las 2 Primeras Columnas de la zona"""
       ax.pie(columnas_selec,valores_a_graficar,  color = 'tab:purple' )  #Graficamos el Precio por capacidad base firme ("Asignamos el rango Y Enbellecimietno ")
       ax.set_ylabel(f"{nombre_eje_y}" , ) #Asignamos Nombre al Eje y
       ax.set_title(f'{titulografic}', loc = "left", fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:purple'}) #Asignamos un Titulo Ala grafica
       ax.set_xticklabels(columnas_selec,rotation=10, fontdict = { 'fontsize':8,'fontweight':'bold','color':'tab:blue'})  # Acomodamos los rangos del eje x s
       ax.set_xlabel(f"{nombre_eje_x}",rotation = 0 ,fontdict = { 'fontsize':14, 'fontweight':'bold', 'color':'tab:purple'}) #Asignamos Titulo al Eje X 
       plt.show()
   
'''Programa Principal'''

print('Bienvenidos A Carga de datos de un Archivo csv en Una base de datos  e visualizacion de este ')

#Validamos el archivo  csv
datos_csv = validar_archivo_csv()
variacion_porcentual_precio_gas_2016_2017(datos_csv)