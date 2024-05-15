import os
import shutil
from datetime import datetime
# Nombre del archivo de texto
nombre_archivo = "C:/Users/lopez/Desktop/nombrefotosjunio.txt"

# Carpeta de origen y destino
carpeta_origen = "C:/Users/lopez/Desktop/Photos_from_2021"
carpeta_destino = "C:/Users/lopez/Desktop/fotosjunio"
# Abrir el archivo en modo lectura
with open(nombre_archivo, "r") as archivo:
    # Leer cada línea del archivo
    for linea in archivo:
        # Dividir la línea en dos partes usando la coma como separador
        partes = linea.strip().split(", ")

        # Separar el nombre y la fecha de creación
        nombre = partes[0].split(": ")[1]
        fecha_creacion_str = partes[1].split(": ")[1]

        # Convertir la fecha de creación a un objeto datetime
        fecha_creacion = datetime.strptime(fecha_creacion_str, "%Y-%m-%dT%H:%M:%SZ")

        # Construir la ruta completa del archivo en la carpeta de origen
        ruta_archivo_origen = os.path.join(carpeta_origen, nombre)

        # Verificar si el archivo existe en la carpeta de origen
        if os.path.exists(ruta_archivo_origen):
            # Construir la ruta completa del archivo en la carpeta de destino
            ruta_archivo_destino = os.path.join(carpeta_destino, nombre)

            # Copiar el archivo de la carpeta de origen a la carpeta de destino
            shutil.copy2(ruta_archivo_origen, ruta_archivo_destino)

            # Establecer la fecha de creación y modificación del archivo en la carpeta de destino
            os.utime(ruta_archivo_destino, (fecha_creacion.timestamp(), fecha_creacion.timestamp()))
            print(f"Archivo {nombre} copiado a {carpeta_destino} con fecha de creación y modificación actualizadas")
        else:
            print(f"El archivo {nombre} no existe en la carpeta de origen.")


# Llama a la función con el nombre del archivo, la carpeta de origen y la carpeta de destino
#encontrar_archivo('C:/Users/lopez/Desktop/nombrefotosjunio.txt', 'C:/Users/lopez/Desktop/Photos_from_2021', 'C:/Users/lopez/Desktop/fotosjunio')
