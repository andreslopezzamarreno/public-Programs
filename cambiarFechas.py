import os
from PyPDF2 import PdfReader
from datetime import datetime
import pywintypes
import win32file
import win32con
import re
# Ruta de la carpeta que contiene los archivos PDF
carpeta_pdf = r'C:\Users\lopez\Documents\libro-de-los-bautizados'

# Itera a través de los archivos PDF en la carpeta
for filename in os.listdir(carpeta_pdf):
    if filename.endswith('.pdf'):
        file_path = os.path.join(carpeta_pdf, filename)
        print(file_path)
        # Abre el archivo PDF
        pdf_reader = PdfReader(file_path)

        match = re.search(r'\d+', filename)

        if match:
            numero = match.group()  # Obtiene la secuencia de dígitos encontrada
            libro = numero[:3]
            parte_restante = numero[3:]
            longitud_restante = len(parte_restante)
            mitad1 = parte_restante[:longitud_restante // 2]
            mitad2 = parte_restante[longitud_restante // 2:]

            nombrenuevo = libro+"-"+mitad1+"-"+mitad2+".pdf"

            nueva_ruta = os.path.join(os.path.dirname(file_path), nombrenuevo)

# Cambia el nombre del archivo
            os.rename(file_path, nueva_ruta)
        else:
            # No se encontraron dígitos en el nombre de archivo
            print("No se encontraron dígitos en el nombre de archivo.")


        """ # Busca el texto "fue BAUTIZADO el día:" y extrae la fecha
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            
            if "fue BAUTIZADO el día:" in page_text:
                start_index = page_text.find("fue BAUTIZADO el día:") + len("fue BAUTIZADO el día: ")
                date_str = page_text[start_index:start_index + 11]  # Suponiendo que la fecha tiene el formato "dd/MM/yyyy"
                if date_str[0] == " ":
                    date_str = date_str.replace(' ', '')
                if date_str[len(date_str)-1] == ",":
                    date_str = date_str.replace(',', '')

                fecha_obj = datetime.strptime(date_str, "%d/%m/%Y")    

                marca_de_tiempo = fecha_obj.timestamp()

                os.utime(file_path, (marca_de_tiempo, marca_de_tiempo)) """

print("Fechas de modificación actualizadas.")
