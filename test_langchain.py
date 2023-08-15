import sys
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.retrievers import SVMRetriever
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import CallbackManager

retriever_type = "SIMILARITY SEARCH"
# Use RecursiveCharacterTextSplitter as the default and only text splitter
splitter_type = "RecursiveCharacterTextSplitter"

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

if __name__ == '__main__':
    if len(sys.argv) == 2:
        os.environ["OPENAI_API_KEY"] = os.environ["TOKEN_OPENAI_CHATGPT"]
        user_question = sys.argv[1]
        # Load and process the uploaded PDF or TXT files.
        loaded_text = """
        periodico = 'elcomercio'
        url = '/politica/benji-espinoza-abogado-de-pedro-castillo-no-se-puede-revisar-camaras-de-palacio-ahi-el-presidente-tiene-secretos-de-estado-rmmn-noticia/'
        fecha = '2022-08-12T21:57:27.423Z'
        contenido = '
        Abogado de Pedro Castillo, Benji Espinoza, niega 
        que se vayan a entregar cámaras de seguridad | Foto: 
        El Comercio Redacción EC12/08/2022 16H57Benji Espinoza, 
        abogado del presidente Pedro Castillo, descartó que se vayan
        a entregar los videos de las cámaras de seguridad de Palacio de Gobierno para descartar que Yenifer Paredes haya podido esconderse en estos espacios para evitar su detención.“No estamos hablando de la casa de cualquier persona, hablamos de Palacio de Gobierno y en palacio hay secretos de Estado. No es que los fiscales tienen derecho a conocer. Si lo hacen, cometen delito grave y pueden acabar destituidos”, manifestó este viernes a Canal N.MÁS INFORMACIÓN | “Castillo es un actor consciente de los hechos de corrupción”Según Benji Espinoza, las veces que los fiscales y policías pudieron ingresar a los espacios de Palacio de Gobierno durante diligencias se debió a que fueron “permisivos”.“Que hayan sido permisivos con revisar la residencia no significa que se puedan conocer aspectos de Palacio de Gobierno porque, quien lo pide y quien lo autoriza, podría estar prevaricando [¿Van a entregar los videos?] ¿Cree que pueden revisarse las cámaras de Palacio? No se puede porque no es una casa, no es una vivienda cualquiera. Ahí el presidente tiene secretos de Estado, ¿cómo es eso que la fiscalía va a conocer secretos de Estado?”, agregó para luego persistir en que la casa de Gobierno es “inviolable”.Benji Espinoza negó que se puedan entregar los videos de las cámaras de seguridad de Palacio de Gobierno. (Canal N) La cuñada de Pedro Castillo y criada como su hija, Yenifer Paredes, no fue ubicada en la residencia presidencial luego que se impidiera por más de una hora el ingreso de los fiscales y la policía el pasado martes.REVISA AQUÍ | Ministro Geiner Alvarado remite escrito a fiscal de la Nación y reitera disposición para cooperar con investigacionesTras 24 horas en la clandestinidad, Paredes se entregó ante el Ministerio Público para que se cumpla su detención preliminar aprobada por el Poder Judicial por un plazo de 10 días.Al respecto, Benji Espinoza negó que se haya obstaculizado la labor de búsqueda de la investigada en la residencia presidencial al bloquear su ingreso hasta que él como abogado estuviera presente, al destacar que Palacio de Gobierno no es la casa de Yenifer Paredes, sino de sus defendidos, Pedro Castillo y Lilia Paredes.MIRA TAMBIÉN | Bloque Magisterial dice que hay “judicialización de la política” en el caso de Yenifer Paredes“[¿Se demoró el ingreso para que saquen a Yenifer Paredes?] Esa es una discusión perfecta para escribir una novela, una ficción. En los hechos, se revisó toda la residencia. Se cumplió estrictamente con el mandato judicial y hubo colaboración de la primera dama y el presidente”, manifestó.TAGSBenji EspinozaPedro CastilloYenifer ParedesPalacio de GobiernoVIDEO RECOMENDADODurante una reunión con dirigentes de organizaciones sociales en el Palacio de Gobierno, Pedro Castillo y el presidente del Consejo de Ministros, Aníbal Torres, anunciaron que habrán movilizaciones e invocaron a traer más personas para marchar en contra de los que considera "Golpistas". (Fuente: América TV) TE PUEDE INTERESARAníbal Torres: “El pueblo dice: ‘cierren el Congreso’, ¿le voy a tapar la boca al pueblo?”Lady Camones rechaza “incitación a la violencia” de Aníbal TorresVladimir Cerrón: juez rechaza pronunciarse sobre su pedido para declarar extinta su inhabilitaciónPedro Castillo: ¿Cómo opera la presunta red criminal que lideraría? | PODCASTLas más leídas1“El juego del calamar 2″: Cuál es la fecha de estreno de la nueva temporada en Netflix 2Alumnos del colegio Leoncio Prado obligados a formar desnudos y descalzos: todo lo que se sabe3“No sé en manos de quién se está quedando Alianza, no los conozco” | ENTREVISTA	
        '
        """
        # Split the document into chunks
        splits = split_texts(loaded_text, chunk_size=1000,
                            overlap=0, split_method=splitter_type)


        embeddings = OpenAIEmbeddings()
        retriever = create_retriever(embeddings, splits, retriever_type)
        # Initialize the RetrievalQA chain with streaming output
        callback_handler = StreamingStdOutCallbackHandler()
        callback_manager = CallbackManager([callback_handler])

        chat_openai = ChatOpenAI(
            streaming=True, callback_manager=callback_manager, verbose=True, temperature=0)
        qa = RetrievalQA.from_chain_type(llm=chat_openai, retriever=retriever, chain_type="stuff", verbose=True)
        
        answer = qa.run(user_question)
        print("Answer:", answer)


