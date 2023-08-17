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

        # Inicializar la lista para almacenar los videos
        videos = []

        # Definir el token de paginación inicial
        next_page_token = None

        # Ciclo para obtener todos los videos del canal
        while True:
            # Realizar la solicitud para obtener la lista de videos del canal
            response = youtube.search().list(
                part='id',
                channelId=channel_id,
                maxResults=50,  # Puedes ajustar la cantidad de videos por solicitud
                order='date',  # Ordenar por fecha
                pageToken=next_page_token
            ).execute()

            # Agregar los IDs de video a la lista
            for item in response['items']:
                videos.append(item['id']['videoId'])

            # Verificar si hay más páginas de resultados
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

        # Imprimir la lista de IDs de video
        print(f'Total de videos encontrados: {len(videos)}')
        print('Lista de IDs de video:')
        for video_id in videos:
            print(video_id)

#UCxgO_rak_BKZP8VNVmYqbWg  id de canal de exitosa
#UC5j8-2FT0ZMMBkmK72R4aeA  id de canal de rpp