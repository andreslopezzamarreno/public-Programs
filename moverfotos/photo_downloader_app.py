"""
Este programa proporciona una interfaz gráfica para descargar fotos de Google Fotos y copiar videos de una carpeta de origen a una carpeta de destino.

El programa consta de varias funciones que realizan tareas específicas, como obtener credenciales de autorización, descargar fotos desde Google Fotos,
copiar videos, y guardar y cargar datos de configuración.

Funciones:
- get_credentials(client_secret_path): Obtiene las credenciales de autorización para acceder a la API de Google.
- download_photos(service, folder_path, start_date, end_date): Descarga fotos desde Google Fotos entre un rango de fechas especificado.
- copy_videos(folder_path, video_path): Copia archivos de video desde una carpeta de origen a una carpeta de destino.
- browse_cfg(): Abre un cuadro de diálogo para seleccionar la carpeta que contiene el archivo de configuración y token.
- browse_folder(): Abre un cuadro de diálogo para seleccionar la carpeta de destino donde se guardarán las fotos descargadas.
- browse_video(): Abre un cuadro de diálogo para seleccionar la carpeta de origen que contiene los videos a copiar.
- run_app(): Ejecuta la aplicación para descargar fotos y copiar videos, y guarda los datos de configuración.
- save_data(): Guarda los datos de configuración en un archivo JSON.
- load_data(): Carga los datos de configuración desde un archivo JSON si existe.

El programa utiliza la biblioteca Tkinter para crear una interfaz gráfica simple que permite al usuario interactuar con las funciones mencionadas anteriormente.

Para utilizar este programa, el usuario debe proporcionar la ruta de la carpeta que contiene el archivo de configuración y token de acceso,
la carpeta de destino para las fotos descargadas, la carpeta de origen que contiene los videos a copiar, y seleccionar un rango de fechas para descargar las fotos.

Una vez que se han proporcionado todas las configuraciones necesarias, el usuario puede hacer clic en el botón "Descargar" para ejecutar la aplicación y 
realizar las tareas de descarga de fotos y copia de videos.

Autor: Andrés López Zamarreño
Fecha: 9/5/2024
"""
import os
import json
import shutil
from datetime import datetime
import time
import tkinter as tk
from tkinter import filedialog
import pickle
import requests
from tkcalendar import DateEntry
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import win32file
import win32con
import pywintypes

root = tk.Tk()

# etiqueta para los mensajes
download_label = tk.Label(root, bg='mint cream')
download_label.grid(row=9, column=0, columnspan=4, padx=30, pady=5)

# Define los scopes para conectarte a la api
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']


def get_credentials(client_secret_path):
    """
    Obtiene las credenciales de autorización para acceder a la API de Google.

    Parámetros:
        client_secret_path (str): La ruta al archivo 'client_secret.json' y la carpeta
                                  donde se almacenará el token de acceso ('token.pickle').

    Devoluciones:
        google.auth.credentials.Credentials: Las credenciales de autorización para acceder
                                              a la API de Google.
        None: Si ocurre un error durante el proceso de obtención de credenciales.

    Excepciones:
        FileNotFoundError: Si el archivo 'client_secret.json' no se encuentra en la ruta
                           especificada.
        Exception: Si ocurre un error durante el proceso de autenticación.
    """
    try:
        pickle_path = client_secret_path + '/token.pickle'
        client_secret_path += '/client_secret.json'
        creds = None
        if os.path.exists(pickle_path):
            with open(pickle_path, 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    client_secret_path, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(pickle_path, 'wb') as token:
                pickle.dump(creds, token)
        return creds
    except FileNotFoundError:
        download_label.config(
            text="Error: No se encontró el archivo 'client_secret.json'. Por favor, verifica la ruta.")
        root.update()
        return None
    except pickle.PickleError as e:
        download_label.config(
            text=f"Error: Ocurrió un problema durante la manipulación del archivo 'token.pickle'. Detalles: {str(e)}")
        root.update()
        return None



def download_photos(service, folder_path, start_date, end_date):
    """
    Descarga fotos desde Google Fotos entre un rango de fechas especificado.

    Parámetros:
        service (googleapiclient.discovery.Resource): El servicio de Google Fotos para realizar la búsqueda y descarga de fotos.
        folder_path (str): La ruta de la carpeta donde se guardarán las fotos descargadas.
        start_date (str): La fecha de inicio del rango de búsqueda en formato 'YYYY-MM-DD'.
        end_date (str): La fecha de fin del rango de búsqueda en formato 'YYYY-MM-DD'.

    Devoluciones:
        None

    Excepciones:
        Exception: Si ocurre un error durante la búsqueda o descarga de fotos.
    """
    try:
            # Convierte las fechas de cadena a datetime
        start_date_dt = datetime.strptime(
            start_date, '%Y-%m-%d')  # Año, Mes, Día
        end_date_dt = datetime.strptime(end_date, '%Y-%m-%d')  # Año, Mes, Día
        filters = {
            'dateFilter': {
                'ranges': [
                    {
                        'startDate': {
                            'year': start_date_dt.year,
                            'month': start_date_dt.month,
                            'day': start_date_dt.day
                        },
                        'endDate': {
                            'year': end_date_dt.year,
                            'month': end_date_dt.month,
                            'day': end_date_dt.day
                        }
                    }
                ]
            }
        }
        request = service.mediaItems().search(
            body={'filters': filters, 'pageSize': 100})
        while request is not None:
            results = request.execute()
            items = results.get('mediaItems', [])
            if not items:
                print('No se encontraron fotos.')
                return
            for item in items:
                response = requests.get(item['baseUrl'] + '=d', stream=True)
                file_path = folder_path + '/' + item['filename']
                with open(file_path, 'wb') as out_file:
                    out_file.write(response.content)
                creation_time_str = item['mediaMetadata']['creationTime']
                if creation_time_str.endswith('Z'):
                    creation_time_str = creation_time_str[:-1] + '+00:00'
                creation_time = datetime.strptime(
                    creation_time_str, '%Y-%m-%dT%H:%M:%S%z')
                win_time = pywintypes.Time(creation_time)
                win32file.SetFileTime(win32file.CreateFile(file_path, win32con.GENERIC_WRITE, 0, None,
                                                        win32con.OPEN_EXISTING, win32con.FILE_ATTRIBUTE_NORMAL, None), win_time, win_time, win_time)
            print('Las fotos se han descargado correctamente.')
            request = service.mediaItems().search_next(
                previous_request=request, previous_response=results)
    except (IOError, OSError, requests.RequestException, ValueError) as e:
        download_label.config(
            text=f"Error: Ocurrió un problema durante la descarga de las fotos. Detalles: {str(e)}")
        root.update()


def copy_videos(folder_path, video_path):
    """
    Copia archivos de video desde una carpeta de origen a una carpeta de destino.

    Parámetros:
        folder_path (str): La ruta de la carpeta de destino donde se copiarán los videos.
        video_path (str): La ruta de la carpeta de origen que contiene los videos a copiar.

    Devoluciones:
        None

    Excepciones:
        FileNotFoundError: Si no se encuentra el archivo de video en la ruta especificada.
        Exception: Si ocurre un error durante la copia de los videos.
    """
    try:
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.MOV') or file_name.endswith('.mp4'):
                source_file = os.path.join(video_path, file_name)
                destination_file = os.path.join(folder_path, file_name)

                fecha_modificacion = os.path.getmtime(destination_file)

                if os.path.exists(source_file):
                    if os.path.exists(destination_file):
                        print(file_name)
                        shutil.copyfile(source_file, destination_file)
                        os.utime(destination_file,
                                 (fecha_modificacion, fecha_modificacion))
    except FileNotFoundError:
        download_label.config(
            text="Error: No se encontró el archivo de video. Por favor, verifica la ruta.")
        root.update()
    except (OSError, IOError) as e:
        download_label.config(
            text=f"Error: Ocurrió un problema durante la copia de los videos. Detalles: {str(e)}")
        root.update()


def browse_cfg():
    """
    Open a file dialog to select a configuration file (cfg) path and set it using the 'cfg_path' variable.

    Parameters:
        None

    Returns:
        None
    """
    cfg_path.set(filedialog.askdirectory())


def browse_folder():
    """
    Open a file dialog to select a folder path and set it using the 'folder_path' variable.

    Parameters:
        None

    Returns:
        None
    """
    folder_path.set(filedialog.askdirectory())


def browse_video():
    """
    Open a file dialog to select a video file path and set it using the 'video_path' variable.

    Parameters:
        None

    Returns:
        None
    """
    video_path.set(filedialog.askdirectory())


def run_app():
    """
    Run the application to download photos and videos.

    This function updates the UI to display a "Downloading..." message, then executes the application to:
    1. Retrieve credentials based on the provided configuration file path.
    2. Build a Google Photos service using the retrieved credentials.
    3. Download photos within the specified date range to the selected folder path.
    4. Copy videos from the selected folder to the specified video path.
    5. Save the downloaded data.

    After completion, it updates the UI to display "Photos downloaded successfully..." message,
    waits for 2 seconds, then removes the "Downloading..." message.

    Parameters:
        None

    Returns:
        None
    """
    # Mostrar el mensaje de "Descargando..."
    download_label.config(text="Descargando...")
    root.update()  # Actualizar la ventana para mostrar el mensaje

    # Ejecutar la aplicación y guardar los datos
    creds = get_credentials(cfg_path.get())
    service = build('photoslibrary', 'v1', credentials=creds,
                    static_discovery=False)
    download_photos(service, folder_path.get(), str(
        start_date.get_date()), str(end_date.get_date()))
    copy_videos(folder_path.get(), video_path.get())
    save_data()

    download_label.config(text="Fotos Descargadas correctamente...")
    root.update()
    time.sleep(2)
    # Eliminar el mensaje de "Descargando..."
    download_label.grid_forget()


def save_data():
    """
    Guarda los datos de configuración en un archivo JSON.

    Devoluciones:
        None
    """
    data = {
        'cfg_path': cfg_path.get(),
        'folder_path': folder_path.get(),
        'video_path': video_path.get(),
        'start_date': start_date.get_date().strftime('%d/%m/%Y'),  # Formato 'dd/mm/yyyy'
        'end_date': end_date.get_date().strftime('%d/%m/%Y')  # Formato 'dd/mm/yyyy'
    }
    with open('cfg/data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f)


def load_data():
    """
    Carga los datos de configuración desde un archivo JSON si existe.

    Devoluciones:
        None
    """
    if os.path.exists('cfg/data.json'):
        with open('cfg/data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        cfg_path.set(data['cfg_path'])
        folder_path.set(data['folder_path'])
        video_path.set(data['video_path'])
        start_date.set_date(datetime.strptime(
            data['start_date'], '%d/%m/%Y').date())
        end_date.set_date(datetime.strptime(
            data['end_date'], '%d/%m/%Y').date())


# Establece el tamaño de la ventana
root.geometry("500x450")  # Ancho x Alto
root.title("Descarga de fotos de Google")
root.configure(bg='mint cream')  # Cambia el color de fondo a blanco roto

cfg_path = tk.StringVar()
folder_path = tk.StringVar()
video_path = tk.StringVar()
start_date = DateEntry(root, date_pattern='dd/mm/yyyy')
end_date = DateEntry(root, date_pattern='dd/mm/yyyy')

# Cargar los datos después de definir las variables
load_data()

cfg_label = tk.Label(
    root, text="Carpeta de token y configuracion", bg='mint cream')
cfg_label.grid(row=0, column=0, columnspan=3, padx=50, pady=10)
cfg_entry = tk.Entry(root, textvariable=cfg_path)
cfg_entry.grid(row=1, column=0, columnspan=2,
               sticky='we', padx=(50, 10), pady=10)
cfg_button = tk.Button(root, text="Buscar carpeta", command=browse_cfg, relief='flat', bg='powder blue',
                       activebackground="light blue")  # Quita la sombra y cambia el color a gris claro
cfg_button.grid(row=1, column=2, sticky='w', padx=(10, 50), pady=10)

folder_label = tk.Label(
    root, text="Carpeta donde se guardaran las fotos", bg='mint cream')
folder_label.grid(row=2, column=0, columnspan=3, padx=50, pady=10)
folder_entry = tk.Entry(root, textvariable=folder_path)
folder_entry.grid(row=3, column=0, columnspan=2,
                  sticky='we', padx=(50, 10), pady=10)
folder_button = tk.Button(root, text="Buscar carpeta", command=browse_folder, relief='flat',
                          bg='powder blue', activebackground="light blue")  # Quita la sombra y cambia el color a gris claro
folder_button.grid(row=3, column=2, sticky='w', padx=(10, 50), pady=10)

video_label = tk.Label(
    root, text="Carpeta checkout correspondiente a las fechas", bg='mint cream')
video_label.grid(row=4, column=0, columnspan=3, padx=50, pady=10)
video_entry = tk.Entry(root, textvariable=video_path)
video_entry.grid(row=5, column=0, columnspan=2,
                 sticky='we', padx=(50, 10), pady=10)
video_button = tk.Button(root, text="Buscar carpeta", command=browse_video, relief='flat',
                         bg='powder blue', activebackground="light blue")  # Quita la sombra y cambia el color a gris claro
video_button.grid(row=5, column=2, sticky='w', padx=(10, 50), pady=10)

start_date_label = tk.Label(root, text="Fecha de inicio", bg='mint cream')
start_date_label.grid(row=6, column=0, columnspan=2, padx=(30, 10), pady=10)

end_date_label = tk.Label(root, text="Fecha de fin", bg='mint cream')
end_date_label.grid(row=6, column=1, columnspan=2, padx=(10, 30), pady=10)

start_date.grid(row=7, column=0, columnspan=2, padx=(30, 10), pady=10)
end_date.grid(row=7, column=1, columnspan=2, padx=(10, 30), pady=10)

# Crear un Frame para contener el botón
button_frame = tk.Frame(root, bg='mint cream')
button_frame.grid(row=8, column=0, columnspan=4,
                  padx=30, pady=(10, 0), sticky='we')

# Crear el botón dentro del Frame
run_button = tk.Button(button_frame, text="Descargar", command=run_app, relief='flat', bg='powder blue',
                       activebackground="light blue")  # Quita la sombra y cambia el color a gris claro
run_button.pack(side='left', expand=True, fill='x')

root.columnconfigure(0, weight=6)  # 60% del espacio para Entry
root.columnconfigure(1, weight=3)  # 30% del espacio para Button
root.columnconfigure(2, weight=1)  # 10% del espacio restante

root.mainloop()
