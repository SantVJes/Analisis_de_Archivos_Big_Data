En este repositorio, encontrarás archivos CSV que están siendo analizados utilizando tecnologías de Big Data con el lenguaje de programación Python, específicamente en la versión 3.12.2 


Descripción de la primera  carpeta "Análisis de archivo de gas natural 2016-2017" :

1.Análisis de archivo de gas natural 2016-2017:
En esta carpeta encontrarás un análisis de un archivo CSV donde se extraen datos para ser graficados, permitiendo así interpretar los datos contenidos en dicho archivo.


Descripción de la primera  carpeta "Conexion_BaseDatos_y_Visualizacion_de_los_datos" :
 tiene como objetivo conectar una base de datos MySQL, cargar datos desde un archivo CSV a dicha base de datos y realizar visualizaciones de los datos utilizando la librería Matplotlib.

Contenido del Script:

Librerías: Importa las librerías necesarias para el proyecto, como pymysql para la conexión a la base de datos, pandas para la manipulación de datos y matplotlib para la visualización.
Variables: Define algunas variables necesarias para el funcionamiento del script.
Funciones:
validar_archivo_csv(): Solicita al usuario la ruta de un archivo CSV, valida si es un archivo CSV válido y lo carga utilizando pandas.
seleccion_zona_y_columnas(): Permite al usuario seleccionar una zona y las columnas a analizar desde el archivo CSV.
conexion_basedatos(): Establece la conexión con la base de datos MySQL.
crear_tabla_variacion_gas(): Crea una tabla en la base de datos para almacenar los datos de variación de costo de transporte de gas.
insertar_datos_variacion_gas(): Inserta los datos de variación de costo de transporte de gas en la tabla de la base de datos.
variacion_porcentual_precio_gas_2016_2017(): Calcula la variación porcentual del precio de gas entre 2016 y 2017 y almacena los resultados en la base de datos.
preguntar_graficar(): Pregunta al usuario si desea graficar los datos y, en caso afirmativo, permite seleccionar el tipo de gráfico.
Funciones de graficación: graficar_barras(), graficar_lineas(), graficar_scatter(), graficar_pie(), que utilizan Matplotlib para crear diferentes tipos de gráficos.
Programa Principal: Solicita al usuario la ruta del archivo CSV, valida el archivo, calcula la variación porcentual del precio del gas y ofrece la opción de graficar los resultados.
Importancia de la Visualización de Datos:

La visualización de datos es crucial en cualquier análisis o investigación por varias razones:

Comprensión Rápida: Las visualizaciones permiten comprender rápidamente los patrones, tendencias y relaciones en los datos.
Comunicación Efectiva: Las visualizaciones son una forma efectiva de comunicar hallazgos y resultados a una audiencia no técnica.
Identificación de Anomalías: Las visualizaciones pueden ayudar a identificar anomalías o valores atípicos en los datos.
Toma de Decisiones Informada: Al visualizar los datos de manera clara y concisa, se facilita la toma de decisiones informada.
Propuesta de Visualización:

Para visualizar la variación porcentual del costo del transporte del gas a lo largo de los años, se puede utilizar un gráfico de línea. Este gráfico mostrará la tendencia general de la variación porcentual a lo largo del tiempo. Además, se puede utilizar un gráfico de barras para comparar la variación porcentual entre diferentes zonas. Cada barra representará la variación porcentual de una zona específica, facilitando la comparación entre ellas

