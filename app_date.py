
import psycopg2
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.retrievers import SVMRetriever
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import CallbackManager
import json

retriever_type = "SIMILARITY SEARCH"
# Use RecursiveCharacterTextSplitter as the default and only text splitter
splitter_type = "RecursiveCharacterTextSplitter"


def es_json(texto):
    try:
        json.loads(texto)
        return True
    except ValueError:
        return False


def update_db(periodico,id_registro,nuevo_valor_json):
    # Establecer la conexión a la base de datos
    conexion = psycopg2.connect(
        dbname= os.environ["HEROKU_DATABASE"],
        user= os.environ["HEROKU_USER"],
        password= os.environ["HEROKU_PASSWORD"],
        host= os.environ["HEROKU_HOST"],  # o la dirección del servidor
        port="5432"  # el puerto de PostgreSQL
    )

    # Consulta de actualización
    consulta = """
        UPDATE public.noticias
        SET noticias_json = %s
        WHERE periodico = %s and _id = %s
    """

    # Ejecutar la consulta
    try:
        with conexion.cursor() as cursor:
            cursor.execute(consulta, (json.dumps(nuevo_valor_json), periodico, id_registro))
            conexion.commit()
            print("Actualización exitosa")
    except psycopg2.Error as e:
        print("Error al actualizar:", e)
    finally:
        conexion.close()
    return ""

def create_retriever(_embeddings, splits, retriever_type):
    if retriever_type == "SIMILARITY SEARCH":
        try:
            vectorstore = FAISS.from_texts(splits, _embeddings)
        except (IndexError, ValueError) as e:
            print(f"Error creating vectorstore: {e}")
            return
        retriever = vectorstore.as_retriever(k=5)
    elif retriever_type == "SUPPORT VECTOR MACHINES":
        retriever = SVMRetriever.from_texts(splits, _embeddings)

    return retriever

def split_texts(text, chunk_size, overlap, split_method):

    # Split texts
    # IN: text, chunk size, overlap, split_method
    # OUT: list of str splits

    split_method = "RecursiveTextSplitter"
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=overlap)

    splits = text_splitter.split_text(text)
    if not splits:
        print("Failed to split document")

    return splits

# selecciona las noticias por la BD
def get_noticias():
    # Establecer la conexión a la base de datos
    conn = psycopg2.connect(
        dbname= os.environ["HEROKU_DATABASE"],
        user= os.environ["HEROKU_USER"],
        password= os.environ["HEROKU_PASSWORD"],
        host= os.environ["HEROKU_HOST"],  # o la dirección del servidor
        port="5432"  # el puerto de PostgreSQL
    )

    # Crear un cursor
    cursor = conn.cursor()

    # Definir la consulta SQL
    query = """
    SELECT DISTINCT periodico,_id,contenido  
    FROM public.noticias 
    WHERE contenido IS NOT NULL and noticias_json IS NULL
    AND EXTRACT(YEAR FROM TO_DATE(display_date, 'YYYY-MM-dd')) = 2023
    AND EXTRACT(MONTH FROM TO_DATE(display_date, 'YYYY-MM-dd')) = 8
    limit 700
    """

    # Ejecutar la consulta
    cursor.execute(query)

    # Obtener los resultados en una lista de arreglos
    resultados = cursor.fetchall()

    # Cerrar el cursor y la conexión
    cursor.close()
    conn.close()
    
    return resultados

def generate_json(contenido):
    os.environ["OPENAI_API_KEY"] = os.environ["TOKEN_OPENAI_CHATGPT"]
    # Load and process the uploaded PDF or TXT files.
    with open("prompt.txt", "r") as archivo:
        user_question = archivo.read()
    loaded_text = contenido
            
    # Split the document into chunks
    splits = split_texts(loaded_text, chunk_size=1000,
                        overlap=0, split_method=splitter_type)

    embeddings = OpenAIEmbeddings()
    retriever = create_retriever(embeddings, splits, retriever_type)
    # Initialize the RetrievalQA chain with streaming output
    callback_handler = StreamingStdOutCallbackHandler()
    callback_manager = CallbackManager([callback_handler])

    chat_openai = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        streaming=True, callback_manager=callback_manager, verbose=True, temperature=0)
    qa = RetrievalQA.from_chain_type(llm=chat_openai, retriever=retriever, chain_type="stuff", verbose=True)
    
    answer = qa.run(user_question)

    return answer

#####################################################################################
# MAIN PRINCIPAL
#####################################################################################
if __name__ == '__main__':
    lista_noticias = get_noticias()
    for noticia in lista_noticias:
        periodico = noticia[0]
        id = noticia[1]
        contenido = noticia[2]
        resultado = generate_json(contenido)
        if es_json(resultado):
            update_db(periodico,id,resultado)
        else:
            print("ERROOOOOOOOOOOOOOOOOOORRRRRRRRRRR")
            print(resultado)

# generar langchain
# guardar la data actualizada

