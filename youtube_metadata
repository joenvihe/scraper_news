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
        video_id = sys.argv[1] # ejem. @exitosape en 'https://www.youtube.com/@exitosape/videos'

        # Realizar la solicitud para obtener la metadata del video
        response = youtube.videos().list(
            part='snippet,statistics',
            id=video_id
        ).execute()

        # Extraer la información relevante de la respuesta
        video_info = response['items'][0]
        video_title = video_info['snippet']['title']
        video_description = video_info['snippet']['description']
        view_count = video_info['statistics']['viewCount']
        like_count = video_info['statistics']['likeCount']
        dislike_count = video_info['statistics']['dislikeCount']
        comment_count = video_info['statistics']['commentCount']

        # Imprimir la metadata del video
        print(f'Título del video: {video_title}')
        print(f'Descripción del video: {video_description}')
        print(f'Vistas: {view_count}')
        print(f'Likes: {like_count}')
        print(f'Dislikes: {dislike_count}')
        print(f'Comentarios: {comment_count}')
