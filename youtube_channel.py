import sys
import os
from googleapiclient.discovery import build

# Reemplaza con tu propia clave de API
API_KEY = os.environ["API_KEY_YOUTUBE_DATA"]

# Crea una instancia del servicio de YouTube Data API
youtube = build('youtube', 'v3', developerKey=API_KEY)

if __name__ == '__main__':
    if len(sys.argv) == 2: 
        # Extraer el ID del canal de la URL
        channel_id = sys.argv[1] # ejem. @exitosape en 'https://www.youtube.com/@exitosape/videos'

        # Realizar la solicitud para obtener la metadata del canal
        response = youtube.channels().list(
            part='snippet,contentDetails,statistics',
            id=channel_id
        ).execute()

        # Extraer la información relevante de la respuesta
        print("################################3")
        print(response)
        print("################################3")