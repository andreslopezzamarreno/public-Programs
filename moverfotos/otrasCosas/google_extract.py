import os
from datetime import datetime
import argparse
import shutil
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
import win32file
import win32con
import pywintypes
import pickle

# Define los scopes
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

def get_credentials(client_secret_path):
    pickle_path = client_secret_path+'/token.pickle'
    client_secret_path+='/client_secret.json'
    creds = None
    if os.path.exists(pickle_path):
        with open(pickle_path, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(pickle_path, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def download_photos(service, folder_path, start_date, end_date):
    # Convierte las fechas de cadena a datetime
    start_date = datetime.strptime(start_date, '%Y-%m-%d')  # Año, Mes, Día
    end_date = datetime.strptime(end_date, '%Y-%m-%d')  # Año, Mes, Día
    filters = {
        'dateFilter': {
            'ranges': [
                {
                    'startDate': {
                        'year': start_date.year,
                        'month': start_date.month,
                        'day': start_date.day
                    },
                    'endDate': {
                        'year': end_date.year,
                        'month': end_date.month,
                        'day': end_date.day
                    }
                }
            ]
        }
    }
    request = service.mediaItems().search(body={'filters': filters, 'pageSize': 100})
    while request is not None:
        results = request.execute()
        items = results.get('mediaItems', [])
        if not items:
            print('No se encontraron fotos.')
            return
        print('Descargando fotos...')
        for item in items:
            response = requests.get(item['baseUrl'] + '=d', stream=True)
            file_path = os.path.join(folder_path, item['filename'])
            with open(file_path, 'wb') as out_file:
                out_file.write(response.content)
            creation_time = datetime.strptime(item['mediaMetadata']['creationTime'], '%Y-%m-%dT%H:%M:%S%z')
            win_time = pywintypes.Time(creation_time)
            win32file.SetFileTime(win32file.CreateFile(file_path, win32con.GENERIC_WRITE, 0, None, win32con.OPEN_EXISTING, win32con.FILE_ATTRIBUTE_NORMAL, None), win_time, win_time, win_time)
        print('Las fotos se han descargado correctamente.')
        request = service.mediaItems().search_next(previous_request=request, previous_response=results)

def copy_videos(folder_path, video_path):
    print('Copiando videos...')
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.mov') or file_name.endswith('.mp4'):
            print(file_name)
            source_file = os.path.join(video_path, file_name)
            destination_file = os.path.join(folder_path, file_name)
            if os.path.exists(destination_file):
                shutil.copyfile(source_file, destination_file)
                
def main(client_secret_path,folder_path, video_path, start_date, end_date):

    creds = get_credentials(client_secret_path)
    service = build('photoslibrary', 'v1', credentials=creds, static_discovery=False)
    download_photos(service, folder_path, start_date, end_date)
    copy_videos(folder_path, video_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Descarga fotos de Google Photos a una carpeta específica y copia videos con el mismo nombre desde otra carpeta.')
    parser.add_argument('client_secret_path', type=str, help='La ruta de la carpeta donde se guarda el client_secret')
    parser.add_argument('folder_path', type=str, help='La ruta de la carpeta donde se guardarán las fotos.')
    parser.add_argument('video_path', type=str, help='La ruta de la carpeta donde los videos están correctamente descargados.')
    parser.add_argument('start_date', type=str, help='La fecha de inicio en formato YYYY-MM-DD.')
    parser.add_argument('end_date', type=str, help='La fecha de fin en formato YYYY-MM-DD.')
    args = parser.parse_args()
    main(args.client_secret_path,args.folder_path, args.video_path, args.start_date, args.end_date)