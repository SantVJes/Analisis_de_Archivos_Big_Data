#Created by:Jesus Santiago Velasco  29/04/2024
#Email: Sanjesvel@outlook.com

#importamos los datos del fichero "ENCalG_22Jul_Nacional.csv" y los guardamos en un objeto que llamamos 
#"enc_Guarderias_csv"
enc_Guarderias_csv <- read.csv("/Users/santiago/Documents/GitHub/Analisis_de_Archivos_Big_Data/Analisis_de_Guardaria_2022_CVC_Con_R/ENCalG_22Jul_Nacional.csv")

#Observamos el archivo cvs importado
View(enc_Guarderias_csv)

#limpiamos datos de columnas Completamente Vacias


# Seleccionar las columnas no vacías
columnas_con_datos <- which(colMeans(is.na(enc_Guarderias_csv)) != 1)

# Crear un nuevo dataframe sin las columnas vacías
enc_Guarderias_csv_sin_nulos <- enc_Guarderias_csv[, columnas_con_datos]

# Mostrar el  nuevo dataframe
View(enc_Guarderias_csv_sin_nulos)










