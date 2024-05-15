import argparse
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle

# Define los scopes
SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

def main(client_file_path, token_file_name):
    
        creds = None
        client_file = os.path.join(client_file_path, 'client_secret2.json')
        token_file = f'{token_file_name}.pickle'
        # El archivo token.pickle almacena las credenciales del usuario
        # Comprueba si existe antes de solicitar nuevas credenciales
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        # Si no hay credenciales válidas, solicita al usuario que inicie sesión.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(client_file, SCOPES)
                creds = flow.run_local_server(port=0)
            # Guarda las credenciales para la próxima ejecución
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Google Photos API')
    parser.add_argument('--client_file_path', type=str, help='Ruta del archivo JSON del cliente')
    parser.add_argument('--token_file_name', type=str, help='Nombre del archivo pickle del token sin la extensión')
    args = parser.parse_args()
    main(args.client_file_path, args.token_file_name)
