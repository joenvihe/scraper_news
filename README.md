# scraper_news
Escrapeo de periodicos peruanos

# enlaces
- https://python.langchain.com/docs/use_cases/extraction
- https://github.com/amrrs/csvchat-langchain/blob/main/Chat_with_CSV_%26_Excel_using_LangChain_and_OpenAI.ipynb
- https://github.com/openai/openai-cookbook/blob/main/examples/Whisper_processing_guide.ipynb


# ejecuciones

```
> python3 app.py UCxgO_rak_BKZP8VNVmYqbWg you_exitosa
> python3 app.py UC5j8-2FT0ZMMBkmK72R4aeA you_rpp
> python3 app.py contenido 1
> python3 app.py elcomercio 0
> python3 app.py larepublica 0
> python3 scraper_news/test_langchain.py textos/q.txt textos/c20.txt
```

# Estructura de youtube
```
{'kind': 'youtube#video', 
  'etag': 'Fj1_UNe9n-Tet9hskB7-l_k_VYI', 
  'id': 'COFWlKLu45E', 
  'snippet': {
            'publishedAt': '2023-03-07T00:50:03Z', 
            'channelId': 'UCxgO_rak_BKZP8VNVmYqbWg', 
            'title': 'Samuel Canaza: Habla el padre que falleció ahogado en río Ilave. "A la fuerza los ha hecho cruzar"', 
            'description': 'A través de un ....', 
            'thumbnails': {
                'default': {'url': 'https://i.ytimg.com/vi/COFWlKLu45E/default.jpg', 'width': 120, 'height': 90}, 
                'medium': {'url': 'https://i.ytimg.com/vi/COFWlKLu45E/mqdefault.jpg', 'width': 320, 'height': 180}, 
                'high': {'url': 'https://i.ytimg.com/vi/COFWlKLu45E/hqdefault.jpg', 'width': 480, 'height': 360}, 
                'standard': {'url': 'https://i.ytimg.com/vi/COFWlKLu45E/sddefault.jpg', 'width': 640, 'height': 480}, 
                'maxres': {'url': 'https://i.ytimg.com/vi/COFWlKLu45E/maxresdefault.jpg', 'width': 1280, 'height': 720}
            }, 
            'channelTitle': 'Exitosa Noticias', 
            'tags': ['exitosa noticias', 'Noticias Perú'], 
            'categoryId': '25', 
            'liveBroadcastContent': 'none', 
            'localized': {
                'title': 'Samuel...', 
                'description': 'A trav..'
                }, 
            'defaultAudioLanguage': 'es-419'
        }, 
    'statistics': {
        'viewCount': '20101', 
        'likeCount': '155', 
        'favoriteCount': '0', 
        'commentCount': '120'}
}
```

# Codigo de conversación de whatsapp con langchain

```
import logging
import langchain
import weaviate
import pywhatkit

# Configuración del logger
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
)

# Importar los datos
with open("data.json", "r") as f:
    data = json.load(f)

# Crear una conexión a Weaviate
client = weaviate.Client(host="localhost", port=8080)

# Crear una colección en Weaviate
collection = client.create_collection("citas")

# Importar los datos a Weaviate
for cita in data:
    collection.create_document(cita)

# Crear una instancia de ChatGPT
chatgpt = langchain.ChatGPT(api_key="YOUR_API_KEY")

# Establecer el tema del chatbot
chatgpt.set_topic("asistente virtual de clinica")

# Establecer la temperatura de ChatGPT a cero
chatgpt.temperature = 0

# Crear una instancia de ChatSession
session = chatgpt.ChatSession()

# Obtener el ID del chat de WhatsApp
chat_id = pywhatkit.get_my_whatsapp_id()

# Cargar la conversación del archivo JSON
with open("chat_log.json", "r") as f:
    messages = json.load(f)

# Actualizar la sesión con la conversación
session.messages = messages

# Iniciar la conversación
while True:
    # Obtener el mensaje de WhatsApp
    message = pywhatkit.get_message_from_whatsapp(chat_id)

    # Procesar el mensaje de WhatsApp
    response = chatgpt.generate_response(message)

    # Guardar la conversación en la sesión
    session.store_message(message, response)

    # Enviar la respuesta a WhatsApp
    pywhatkit.sendwhatsapp_message(chat_id, response)

    # Detectar errores
    if not response:
        logging.error("No se pudo generar una respuesta")
        break

    # Detectar finalización de la conversación
    if "Gracias" in response or "Adiós" in response:
        break

# Guardar la conversación en el archivo JSON
with open("chat_log.json", "w") as f:
    f.write(json.dumps(session.messages))

# Obtener el nombre del cliente
name = session.get_user_name()

# Saludar al cliente
if name:
    greeting = f"Hola {name}, ¿en qué te puedo ayudar?"
else:
    greeting = "Hola, ¿en qué te puedo ayudar?"

# Imprimir el saludo
print(greeting)

# Obtener la última conversación del cliente
last_conversation = session.get_last_conversation()

# Mostrar la última conversación al cliente
if last_conversation:
    print(f"En nuestra última conversación, hablamos sobre {last_conversation}")
    
```

# Estructura de Vector BD
```
{
  "especialidad": "Cardiología",
  "médico": "Dr. Juan Pérez",
  "horario": "Lunes a viernes de 8:00 a 12:00 horas y de 14:00 a 18:00 horas",
  "citas": [
    {
      "cliente": "María López",
      "fecha": "2023-08-25",
      "hora": "9:00 horas"
    },
    {
      "cliente": "Juan Pérez",
      "fecha": "2023-08-26",
      "hora": "10:00 horas"
    }
  ]
}
{
  "cliente": {
    "nombre": "María López",
    "apellidos": "Pérez",
    "edad": 35,
    "sexo": "Femenino",
    "dirección": "Calle 123, 4567, Ciudad de México"
  },
  "especialidad": "Cardiología"
}
```
