import os
import shutil
from datetime import datetime

def copiar_archivos_despues_de(fuente, destino, fecha_limite):
    # Comprueba si la carpeta de destino existe, si no, la crea
    if not os.path.exists(destino):
        os.makedirs(destino)

    for root, _, files in os.walk(fuente):
        for file in files:
            ruta_completa = os.path.join(root, file)
            # Obtiene la fecha de modificación del archivo
            fecha_modificacion = datetime.fromtimestamp(os.path.getmtime(ruta_completa))
            # Compara la fecha de modificación con la fecha límite
            if fecha_modificacion > fecha_limite:
                # Copia el archivo al destino
                shutil.copy2(ruta_completa, destino)
                print(f"Copiado {file} a {destino}")

if __name__ == "__main__":
    # Carpeta de origen y destino
    carpeta_origen = "D:/fotos-Andres"
    carpeta_destino = "C:/Users/lopez/Desktop/fotos-despues-8-enero"
    # Fecha límite (8 de enero de 2024)
    fecha_limite = datetime(2024, 1, 8)
    copiar_archivos_despues_de(carpeta_origen, carpeta_destino, fecha_limite)
