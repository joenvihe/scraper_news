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
        Listado de varias noticias ordenados por bloques:

        bloque = 1
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

        bloque = 2
        periodico = 'elcomercio'
        url = '/politica/pedro-castillo-abogado-benji-espinoza-recomienda-al-presidente-no-recibir-a-la-comision-de-fiscalizacion-este-lunes-27-de-junio-fiscalia-de-la-nacion-bruno-pacheco-rmmn-noticia/'
        fecha = '2022-06-27T03:46:28.325Z'
        contenido = '
        Pedro Castillo debe decidir si recibirá mañana a la comisión de fiscalización. (Foto: archivo Presidencia) Redacción EC26/06/2022 22H46Benji Espinoza, abogado de Pedro Castillo, le ha recomendado que no reciba mañana, lunes 27 de junio, a la Comisión de Fiscalización en Palacio de Gobierno. Además, considera que se trataría de una persecución múltiple contra el presidente.“He recomendado, como abogado del presidente, que no la reciba (a la Comisión de Fiscalización), porque una declaración debe ser la concreción del derecho a ser escuchado con objetividad, con parcialidad y con el debido proceso. Cuando eso no existe, la declaración es una mera formalidad”, señaló en entrevista con Punto Final.MIRA AQUÍ | Pedro Castillo: Comisión de Fiscalización asistirá este lunes a Palacio de Gobierno para tomar declaración de presidenteEn ese sentido, dijo que espera que Castillo haga caso a la sugerencia. Pero en caso, decidiera declarar a la comisión, el abogado estaría ejerciendo su defensa técnica.Cabe mencionar que la Constitución no obliga al Presidente a comparecer a este tipo de comisiones. Incluso, la Comisión de Constitución lo ha manifestado en dos opiniones consultivas.Benji Espinoza espera que Pedro Castillo haga caso a su pedido y no brinde las declaraciones el día de mañana. Además, porque considera que hay una persecución por parte de la Fiscalía de la Nación.LEE MÁS | Pedro Castillo: “Me pondré a disposición de las rondas campesinas si les consta que he robado un centavo”“Yo creo que va a ser atendido mi pedido, el presidente escucha recomendaciones de su defensa. Hay que ser claros, el presidente ya está sometido a una investigación y la propia comisión cuando lo cita dice que estos hechos ya los conoce la Fiscalía de la Nación, en otras palabras, hay una persecución múltiple”, finalizó.TAGSBenji EspinozaPedro CastilloComisión de FiscalizaciónVIDEO RECOMENDADOPedro Castillo sobre los medios de comunicación. TE PUEDE INTERESARPedro Castillo: presidente de Comisión de Fiscalización espera que sesión en Palacio sea públicaPedro Castillo: “Ratifico que hemos llegado a dirigir los destinos del país sin robar un centavo al Perú”Abogado de Pedro Castillo apelará rechazo a anular investigación de Fiscalía de la NaciónCritican proyecto de ley que busca sancionar difusión de información reservadaDimitri Senmache: presentan moción de censura contra ministro del InteriorLas más leídas1“El juego del calamar 2″: Fecha de estreno y sinopsis de la nueva temporada en Netflix 2Alumnos del colegio Leoncio Prado obligados a formar desnudos y descalzos: todo lo que se sabe3“No sé en manos de quién se está quedando Alianza, no los conozco” | ENTREVISTA	
        ' 	
	
        bloque = 3
        periodico = 'larepublica'
        url = '/politica/pedro-castillo/2023/06/11/jose-gavidia-exministro-de-pedro-castillo-pide-millonaria-indemnizacion-en-libras-esterlinas-773377'
        fecha = '2023-06-11 21:08:58'
        contenido = '
        Política11 Jun 2023 | 21:08 hExministro José Gavidia pide millonaria indemnización al Estado por ser retirado de cargo en LondresMás de 3 millones de soles equivalen a lo que pide el exministro de Defensa ante un juzgado de Piura. Únete al canal de Whatsapp de La RepúblicaCésar Pérez, a quien Fiscalía halló S/360.000 en su casa, se encargará de la alcaldía del CallaoPedro Castillo: extienden investigación por rebelión hasta abril del 2024José Gavidia fue nombrado representante en Londres por Pedro Castillo luego de renunciar a su cargo en el Mindef. Foto: composición LR/Alvaro Lozano/ Mindef/ PresidenciaJessica ArceSiguenos en Google News José Luis Gavidia, quien fue titular del Ministerio de Defensa (Mindef) entre febrero y agosto del 2022 durante el gobierno del hoy vacado Pedro Castillo y, tras ello, designado representante del Perú ante la Organización Marítima Internacional de la ONU en la ciudad de Londres, acudió a un juzgado de trabajo en Piura para exigir al Estado 681.626,80 libras esterlinas (moneda oficial de Reino Unido), que en soles suman más de 3 millones. El dominical de Panorama tuvo acceso al documento de Procuraduría del Ministerio de Defensa en el que se constata que el exministro de Castillo Terrones está exigiendo al Estado el mencionado monto por un periodo de dos daños, que corresponderían a presuntos perjuicios por haber cortado su designación el 1 de marzo del 2023. El medio de comunicación se comunicó con el extitular de Defensa, pero este aseguró no conocer nada sobre ello. PUEDES VER: José Luis Gavidia renunció al Ministerio de Defensa “por motivos personales” Gavidia fue nombrado por Pedro Castillo Cuando Gavidia renunció en agosto del año pasado a su cargo de ministro de Defensa, en medio de la controversia por contratos otorgados a su familia, expresó ante la prensa que estaba afectado emocionalmente. Ante ello, el entonces presiente Pedro Castillo le otorgó el puesto como representante permanente alterno del Perú ante la Organización Marítima Internacional, cargo por el que el Estado gastó alrededor de medio millón de soles contando asignaciones mensuales, pasajes y maletas que Gavidia llevó a este país. A pesar de la salida del poder de Castillo en diciembre del 2022, el exministro continuaba asumiendo el puesto hasta marzo del 2023, cuando fue relevado del cargo por el que ahora pide una millonaria indemnización. Ministerio de DefensaPedro Castillo TerronesPedro CastilloONUÚNETE AL CANAL DE WHATSAPP DE LRRECIBE LAS NOTICIAS EN GOOGLE NEWSOFERTAS DE HOYCargando MgId...	
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


