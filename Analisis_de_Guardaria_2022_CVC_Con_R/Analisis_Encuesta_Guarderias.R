#Created by:Jesus Santiago Velasco  29/04/2024
#Email: Sanjesvel@outlook.com

#importamos los datos del fichero "ENCalG_22Jul_Nacional.csv" y los guardamos en un objeto que llamamos 
#"enc_Guarderias_csv"
enc_Guarderias_csv <- read.csv("/Users/santiago/Documents/GitHub/Analisis_de_Archivos_Big_Data/Analisis_de_Guardaria_2022_CVC_Con_R/ENCalG_22Jul_Nacional.csv")

#Observamos el archivo cvs importado
View(enc_Guarderias_csv)

#Llamamos ala funcion limpiar_cvs_de_columans_vacias
enc_Guarderias_csv  <- limpiar_cvs_de_columans_vacias(enc_Guarderias_csv)

#llamamos ala funcion contabilizar_delagaciones
localidades_conM_participacion <- contabilizar_delegaciones(enc_Guarderias_csv$Delegación)

# Graficar un dataframe df como gráfico de barras con título y ejes personalizados
graficar_datos(localidades_conM_participacion$Participaciones.Freq, "barra", main = "Las delegaciones con más Localidades participantes en la encuesta", 
               xlab = "Delegaciones", ylab = "Numero de Participantes",col = rainbow(20), 
               names.arg = localidades_conM_participacion$Participaciones.delegaciones,cex.names = 0.5, mgp = c(3, -0.3, 1))


#llamamos ala funcion para sacar el porcentaje de participacion por delegacion
porcentaje_partipor_delegacion <- porcentaje_participacion_por_delegacion(unique(enc_Guarderias_csv$Delegación),enc_Guarderias_csv[,2:137])

# Graficar un dataframe df como gráfico de puntos con etiquetas personalizadas
graficar_datos(porcentaje_partipor_delegacion$porcentaje_participacion, "puntos",main = "Porcentaje de participacion por delegacion", 
               xlab = "Delegaciones", ylab = "Porcentaje de participacion", col = sample(colors()), pch = 16, cex = 2)

# Agregar etiquetas a los puntos
text(porcentaje_partipor_delegacion$porcentaje_participacion, labels = porcentaje_partipor_delegacion$delegacion, pos = 3, cex = 0.8, col = "black", offset = 0.5)


#llama ala funcion preguntas menos respondidas
pregunas_Men_respondidads <- preguntas_menos_respondidas(enc_Guarderias_csv[,13:137])

# Graficar un dataframe df como gráfico de barras con título y ejes personalizados
graficar_datos(pregunas_Men_respondidads$personas_q_no_respo_pregunta, "barra", horiz = TRUE, main = " Preguntas menos respondidas", 
               xlab = "Personas que no respondieron", ylab = "Preguntas",col = rainbow(20), 
               names.arg = pregunas_Men_respondidads$pregunta , las = 1,cex.names = 0.6, mgp = c(3, -0.3, 1))



#llama ala funcion de porcentaje de preguntas contextadas al 100%
porcentaje_preguntas_contextadas_100_pordelegacion <- porcentaje_preguntas_contestadas_por_localidad(unique(enc_Guarderias_csv$Delegación),enc_Guarderias_csv[,2:137])

# Graficar un dataframe df como gráfico de puntos con etiquetas personalizadas
graficar_datos(porcentaje_preguntas_contextadas_100_pordelegacion$porcentaje_participacion, "puntos",main = "porcentaje de preguntas contextadas al 100% por delegacion", 
               xlab = "Delegaciones", ylab = "Porcentaje de preguntas contextadas al 100%", col = sample(colors()), pch = 16, cex = 2)

# Agregar etiquetas a los puntos
text(porcentaje_preguntas_contextadas_100_pordelegacion$porcentaje_participacion, labels = porcentaje_preguntas_contextadas_100_pordelegacion$delegacion,, pos = 3, cex = 0.6, col = "black", offset = 0.5 ,srt = 20)


#----------Funciones del Programa para Analizar los datos---------------------

# Función para seleccionar las columnas no vacías de un dataframe
limpiar_cvs_de_columans_vacias <- function(datos) {
  # Seleccionar las columnas que no tienen valores NA (vacíos)
  columnas_con_datos <- which(colMeans(is.na(datos)) != 1)
  
  # Crear un nuevo dataframe sin las columnas vacías
  datos_sin_nulos <- datos[, columnas_con_datos]
  
  return(datos_sin_nulos)
}


# Función para encontrar las delegaciones con más localidades participantes en una encuesta
contabilizar_delegaciones <- function(delegaciones) { #tiene como parametro la columna delagaciones 

  # Encontrar cuantas veces se repite una localidad con un diccionario por el metodo table 
  conteo_Localidades_participantes <- table(delegaciones)
  
  # Encontrar el máximo número de participaciones
  max_participaciones <- mean(conteo_Localidades_participantes)
  
  # Seleccionar las delegaciones que tienen el máximo número de participaciones
  delegaciones_max_participaciones <- names(conteo_Localidades_participantes)[conteo_Localidades_participantes >= max_participaciones]
  
  # Crear un dataframe con las delegaciones que tienen el máximo número de participaciones
  df_max_participaciones <- data.frame(Participaciones = conteo_Localidades_participantes[delegaciones_max_participaciones])
  
  # Retornar el dataframe
  return(df_max_participaciones)
}


# Función para  encontrar el  porcentaje de participación por delegación.
porcentaje_participacion_por_delegacion <- function(delegaciones,colum_preguntas)
{
  #separamos las delegaciones 
  delegaciones_existentes <- unique(colum_preguntas$deleg)
  
  # Crear una lista para almacenar los dataframes de cada delegación
  dataframes_delegaciones <- list()
  
  # Crear un dataframe vacío para almacenar los resultados
  porcentaje_participacion_df <- data.frame(delegacion = integer(), porcentaje_participacion = numeric())
  
  # Iterar sobre cada delegación y crear un dataframe correspondiente
  for (i  in delegaciones_existentes) {
    
    #selecionamos la  delegacion 
    delegacion <- delegaciones_existentes[i]
    
    
    
    # Filtrar el dataframe original por la delegación actual
    dataframe_delegacion <- subset(colum_preguntas, deleg == delegacion)
    # Añadir el dataframe filtrado a la lista
    dataframes_delegaciones[[as.character(delegacion)]] <- dataframe_delegacion
    
    #Quitamos las primeras Columnas por motivos que son datos sin importacia ,de hora y fecha etc.
    
    # Contar las filas con valores NA en las columnas donde el usuario no participó en la pregunta
    filas_na <- apply(dataframe_delegacion[, -c(1, 12)], 1, function(x) sum(is.na(x)))
    
    # Contar las filas donde el usuario  participó en la pregunta
    filas_par <- apply(dataframe_delegacion[, -c(1, 12)], 1, function(x) sum(!is.na(x)))
  
    # Calcular el porcentaje de participación utilizando la fórmula proporcionada
    porcentaje_participacion <- (sum(filas_par) * 100) / (sum(filas_par) + sum(filas_na))
    
    
    
    
    # Agregar la delegación y el porcentaje de participación al dataframe
   porcentaje_participacion_df <- rbind(porcentaje_participacion_df, 
                                                data.frame(delegacion = delegaciones[i], 
                                                           porcentaje_participacion = porcentaje_participacion))
  }
  
  #returnamos dataframe 
  return(porcentaje_participacion_df)
  
  }
  
  

# Funcion para indiquar las preguntas menos respondidas en relación con el resto 
preguntas_menos_respondidas <- function(columnas_preguntas)
{
  
  # Calcular el número de NA en cada columna que indica que no las usuario no respondieron
  na_por_columna <- colSums(is.na(columnas_preguntas))

  # Calcular el promedio de NA en todas las columnas para sacar las preguntas menos respondidas
  promedio_na <- mean(na_por_columna)
  
  # Seleccionar las columnas que tienen más NA que el promedio que indica las preguntas menos respondidas
  columnas_seleccionadas <- columnas_preguntas[, na_por_columna > promedio_na]
  
  #Crear un dataframe con el nombre de las columnas y la cantidad de NA en cada columna
  preguntas_Me_respondidas <- data.frame(pregunta = names(columnas_seleccionadas), personas_q_no_respo_pregunta  = colSums(is.na(columnas_seleccionadas)) )
  
  # Retornar las columnas seleccionadas
  return( preguntas_Me_respondidas)
  
}

#función que muestra los porcentajes de preguntas contestadas  al 100% por delegacion.

porcentaje_preguntas_contestadas_por_localidad <- function(delegaciones,colum_preguntas)
{
 
  #separamos las delegaciones 
  delegaciones_existentes <- unique(colum_preguntas$deleg)
  
  # Crear una lista para almacenar los dataframes de cada delegación
  dataframes_delegaciones <- list()
  
  # Crear un dataframe vacío para almacenar los resultados
  porcentaje_participacion_df <- data.frame(delegacion = integer(), porcentaje_de_preguntas_respondidas = numeric())
  
  
  # Iterar sobre cada delegación y crear un dataframe correspondiente
  
  for (i  in delegaciones_existentes) 
    {
    
    #selecionamos la  delegacion 
    delegacion <- delegaciones_existentes[i]
    
    # Filtrar el dataframe original por la delegación actual
    dataframe_delegacion <- subset(colum_preguntas, deleg == delegacion)
    # Añadir el dataframe filtrado a la lista
    dataframes_delegaciones[[as.character(delegacion)]] <- dataframe_delegacion
    
    # Filtrar las columnas que no contienen valores NA en ninguna fila
    columnas_sin_na <- colum_preguntas[, !apply(is.na(dataframe_delegacion), 2, any)]
    
    # Calcular el porcentaje de preguntas contextadas al 100% utilizando la fórmula proporcionada9
    porcentaje_participacion <- (ncol(columnas_sin_na) * 100) / (ncol(columnas_sin_na) + ncol(dataframe_delegacion) )
    
    # Agregar la delegación y el porcentaje de participación al dataframe
    porcentaje_participacion_df <- rbind(porcentaje_participacion_df, 
                                         data.frame(delegacion = delegaciones[i], 
                                                    porcentaje_participacion = porcentaje_participacion))
  }
  #returnamos dataframe 
  return(porcentaje_participacion_df)
  
  
}



#Funcion para graficar los datos 
graficar_datos <- function(datos, tipo_grafica, ...) {
  # Verificar el tipo de gráfico y realizar la gráfica correspondiente
  switch(tipo_grafica,
         
         "barra" = barplot(datos, ...),
         
         "lineales" = plot(datos, type = "s", ...),
         
         "puntos" = plot(datos, type = "b", ...),
         
         "circulares" = pie(datos, ...),
         
         print("Tipo de gráfico no válido. Por favor, elige entre 'barra', 'lineales', 'puntos' o 'circulares'."))
}

  
  
  


  











