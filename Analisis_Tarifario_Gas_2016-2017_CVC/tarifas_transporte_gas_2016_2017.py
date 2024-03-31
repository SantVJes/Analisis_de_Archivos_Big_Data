#Created by:Jesus Santiago Velasco  20/03/2024
#Email: Sanjesvel@outlook.com
'''Librerias'''
import pandas as pd
import matplotlib.pyplot as plt
import waterfall_chart
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
 
#Funcion para mostrar las opciones a realizar 
def mostrar_menu():
    print("1. Promedio del costo a la tarifa de gas para los años 2016 y 2017")
    print("2. Variación del precio del gas natural a lo largo de dos años")
    print("3. Demanda promedio del gas natural para 2016")
    print("4. Demanda promedio del gas natural para 2017")
    print("5. Tarifas máximas por año")
    print("6. Salir")
 
  
#Declaramos la funcion para validar datos(Columnas a promediar y promediar las columnas de datos tarifarios
def promedio_costo_gas_2016_2017(datos_csv):
    '''Variables'''
    zona_A_analizar = None
    columnas_selec = []
    promedio_columnas = []
    iterador1= 0
    zona_A_analizar , columnas_selec =  seleccion_zona_y_columnas(datos_csv) #extraemos las columanas y la zona analizar
    while iterador1 < len(columnas_selec) : #while donde sacamos el promedio con el metodo mean
        promedio_columnas.append(zona_A_analizar[columnas_selec[iterador1]].mean())
        iterador1 +=1
    #graficamos los datos obtenidos 
    graficar_barras(f"Promedio del costo del transporte del gas 2016-2017 de la zona{zona_A_analizar["zona"].unique()} ","Columnas analizadas del archivo csv","Promedio de Pesos por Gigajoule",columnas_selec,promedio_columnas)
    
     
            
#Declaramos Fucion que calcule la variacion porcentual del precio de gas alo largo de los 2 años
def variacion_porcentual_precio_gas_2016_2017(datos_csv):
    '''Variables'''
    zona_A_analizar = None
    columnas_selec_variacion = []
    variacion_porcentual_columnas = []
    iterador1= 0
    zona_A_analizar, columnas_selec_variacion = seleccion_zona_y_columnas(datos_csv)
    while iterador1 < len(columnas_selec_variacion):# while Precios del gas natural al inicio y al final de los dos años de una misma columna donde lo multiplacamos por 100 para tener el porcentaje de la variacion 
        variacion_porcentual_columnas.append( ((zona_A_analizar[columnas_selec_variacion[iterador1]].iloc[-1] - zona_A_analizar[columnas_selec_variacion[iterador1]].iloc[0]) / zona_A_analizar[columnas_selec_variacion[iterador1]].iloc[0])* 100 ) 
        iterador1 += 1
    #graficamos los datos obtenidos 
    graficar_barras(f"Variacion del costo del transporte del gas 2016-2017 de la zona {zona_A_analizar["zona"].unique()}","Columnas analizadas del archivo csv","Variacion porcentual entre 2016-2017",columnas_selec_variacion,variacion_porcentual_columnas)
  
#Declaramos la funcion para la demanda promedio pues es la unica que es posible calcular con esste archivo del precio del gas año 2016

def demanda_promedio_gas(datos_csv,fecha):
    '''Variables'''
    zona_A_analizar = None
    columnas_selec = []
    iterador1 = 0
    demanda_promedio = []
    demanda_total = None
    # Calculamos el número de días en 2016
    dias_del_ano = pd.to_datetime(f'{fecha}-12-31') - pd.to_datetime(f'{fecha}-01-01')
    dias_del_ano = dias_del_ano.days + 1
    #Conviertimos las columnas de fecha a tipo datetime y la mandamos ala funcion de seleccion de zona y columna
    datos_csv['fecha_inicio'] = pd.to_datetime(datos_csv['fecha_inicio'])
    zona_A_analizar, columnas_selec = seleccion_zona_y_columnas(datos_csv[datos_csv['fecha_inicio'].dt.year == fecha]) 
    while iterador1 < len(columnas_selec) :#while para la demanda de las columans para sacar el porcentaje de demanda promedio
        # Calculamos la demanda total para 2016 para cada columna selecionada '
        demanda_total = zona_A_analizar[columnas_selec[iterador1]].sum()
        demanda_promedio.append((demanda_total / dias_del_ano)* 100)
        iterador1 += 1 
    #graficamos los datos obtenidos    
    graficar_barras(f"Demanda del costo del transporte del gas {fecha} de la zona {zona_A_analizar["zona"].unique()}","Columnas analizadas del archivo csv",f"Demanda promedio del año {fecha}",columnas_selec,demanda_promedio)
    
def tarifas_maximas_por_ano(datos_csv,anos):
    '''Variables'''
    zona_A_analizar = None
    columnas_selec=[]
    iterador1=0
    valores_maximos= []
    # Convertir la columna de fechas a tipo datetime si no está en ese formato
    datos_csv['fecha_inicio'] = pd.to_datetime(datos_csv['fecha_inicio'])
    # Filtrar los datos por año
    for ano in anos:
        datos_ano = datos_csv[datos_csv['fecha_inicio'].dt.year == ano]  #filtramos datos por el año
        print(f"Seleccione los datos de los que desea sacar el máximo histórico del año {ano}")
        zona_A_analizar, columnas_selec = seleccion_zona_y_columnas(datos_ano)
        iterador1=0 #limpiamos el iterador
        while iterador1 < len(columnas_selec) :#while donde seleciona los valores maximos de cada columna
             valores_maximos.append(zona_A_analizar[columnas_selec[iterador1]].max())
             iterador1 += 1
        #graficamos los valores maximos de cada año
        graficar_barras(f"\nValores maximos del costo del gas {ano} de la zona {zona_A_analizar["zona"].unique()}","Columnas analizadas del archivo csv",f"valores maximos del {ano}",columnas_selec,valores_maximos)
        valores_maximos.clear()#Limpiamos el array para obtener los proximos valores maximos del otro años
    
#funcion que pregunta al usuario si desea graficar los datos
def preguntar_graficar():
    respuesta = input("¿Deseas graficar los datos? (s/n): ")
    return respuesta.lower() == 's'
           
#funcion para graficar los datos que queremos 
def graficar_barras(titulografic,nombre_eje_x,nombre_eje_y,columnas_selec,valores_a_graficar):
    if preguntar_graficar():
       fig ,ax = plt.subplots(figsize=(20, 8))  # Crear la figura y los ejes 
       """Creamos Las Graficas En forma de Barras de las Zonas """
       plt.suptitle(f"{titulografic} ", fontsize=16, fontweight="bold") #Titulo de la hoja de las Graficas
       """Graficamos Las 2 Primeras Columnas de la zona"""
       ax.bar(columnas_selec,valores_a_graficar,  color = 'tab:purple' )  #Graficamos el Precio por capacidad base firme ("Asignamos el rango Y Enbellecimietno ")
       ax.set_ylabel(f"{nombre_eje_y}" , ) #Asignamos Nombre al Eje y
       ax.set_title(f'{titulografic}', loc = "left", fontdict = {'fontsize':14, 'fontweight':'bold', 'color':'tab:purple'}) #Asignamos un Titulo Ala grafica
       ax.set_xticklabels(columnas_selec,rotation=10, fontdict = { 'fontsize':8,'fontweight':'bold','color':'tab:blue'})  # Acomodamos los rangos del eje x s
       ax.set_xlabel(f"{nombre_eje_x}",rotation = 0 ,fontdict = { 'fontsize':14, 'fontweight':'bold', 'color':'tab:purple'}) #Asignamos Titulo al Eje X 
       plt.show()
    else:
        print("Nose grafico ningun datos")

'''Codijo_Principal'''
print("Bienvenidos AL Programa Para Analizar Su Archivo CSV")
datos_csv = validar_archivo_csv()

while True:
        print("Menu de Analisis del Archivo CSV ")
        mostrar_menu()
        opcion = input("Seleccione una opción analizar y graficar: ")
        if opcion == "1":
           promedio_costo_gas_2016_2017(datos_csv) 
        elif opcion == "2":
           variacion_porcentual_precio_gas_2016_2017(datos_csv)
        elif opcion == "3":
           demanda_promedio_gas(datos_csv,2016)
        elif opcion == "4":
           demanda_promedio_gas(datos_csv,2017)
        elif opcion == "5":
           tarifas_maximas_por_ano(datos_csv,[2016,2017])
        elif opcion == "6":
            print("Saliendo del programa...")
            break
        else:
            os.system('clear')
            print("Opción no válida. Por favor, seleccione una opción válida.")


