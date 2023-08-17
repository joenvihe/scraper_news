import sys
import requests
from bs4 import BeautifulSoup
import csv
import requests
import psycopg2
import os
import json
from psycopg2 import sql
import random
from googleapiclient.discovery import build

# Reemplaza con tu propia clave de API
API_KEY = os.environ["API_KEY_YOUTUBE_DATA"]
# Crea una instancia del servicio de YouTube Data API

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    ]
    
    return random.choice(user_agents)


def update_db(periodico,id,contenido):
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

    # Definir la consulta SQL de actualización
    update_query = """
        UPDATE public.noticias
        SET contenido = '{}'
        WHERE periodico = '{}' and _id = '{}';
    """.format(contenido.replace("'", "''"),periodico,id)

    # Ejecutar la consulta de actualización
    cursor.execute(update_query)

    # Confirmar los cambios en la base de datos
    conn.commit()

    # Cerrar el cursor y la conexión
    cursor.close()
    conn.close()

    return ""

def update_elcomercio(fila):
    #('larepublica', '2Q2K7XOXCFEU3IEHS5NGEKX2NM', '/economia/2021/04/10/expectativas-de-inflacion-se-mantienen-en-el-rango-meta/')
    url = "https://elcomercio.pe{}".format(fila[2])
    print(url)

    user_agent = get_random_user_agent()
    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "es,es-ES;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Cookie": "_tfpvi=NDgxYjg2ZGQtYWE1Ny00MDYyLTk5OGQtNTkzYmZiZjYzMDhjIzgtNA%3D%3D; __AP_SESSION__=134ca4a3-5d3a-491d-a523-08985428362f; ___nrbi=%7B%22firstVisit%22%3A1691902055%2C%22userId%22%3A%22a32a0723-0896-4e5b-b0df-32e785142c6f%22%2C%22userVars%22%3A%5B%5D%2C%22futurePreviousVisit%22%3A1691902055%2C%22timesVisited%22%3A1%7D; compass_uid=a32a0723-0896-4e5b-b0df-32e785142c6f; __qca=P0-854938016-1691902056641; _gid=GA1.2.1692692428.1691902057; _cc_id=68aee879e13885ef4f30f9d599aafebb; panoramaId_expiry=1691988460480; panoramaId=06e11c145f156512a7fac596616da9fb927a1827211ef3382209e54034793228; panoramaIdType=panoDevice; cto_bundle=hUyqO18zekJlWUgzVlhTVU4lMkJ6S0dpcUQ5Q1JHa2VGN3BWVldJOU1XSklCeTNoUWpRdXU5UDd4JTJGbmZsUmV1M3UzQnRtWXdGMnd0c1FqTWt3NjNqNFZMUHp0aFJaNjYyV3BCaTZCeVpKSkZpaiUyRkw2SkJvZXlONDRhQTd2UExzUmxISFB1NTVGOFQ3aFBoNWZXZjU1NHg4Q3pNQXclM0QlM0Q; __gads=ID=a16992f89fbf6d0a:T=1691902062:RT=1691902062:S=ALNI_MaJzT67vWrxffnxAkZ-KYEYR7gU4Q; __gpi=UID=000009fa85e2cd40:T=1691902062:RT=1691902062:S=ALNI_MZvHm-kYPkUvg1tE8fiYYjWhF6jIw; TAPAD=%7B%22id%22%3A%22b51f3542-b673-43a8-8250-5b74cf37a8fa%22%7D; _pbjs_userid_consent_data=3524755945110770; ___nrbic=%7B%22previousVisit%22%3A1691902055%2C%22currentVisitStarted%22%3A1691902055%2C%22sessionId%22%3A%221b08d98d-a6a6-445a-8ff6-8cf6e59a8f92%22%2C%22sessionVars%22%3A%5B%5D%2C%22visitedInThisSession%22%3Atrue%2C%22pagesViewed%22%3A2%2C%22landingPage%22%3A%22https%3A//larepublica.pe/politica/actualidad/2023/08/12/pedro-castillo-extienden-investigacion-por-rebelion-hasta-abril-del-2024-838416%22%2C%22referrer%22%3A%22%22%7D; _ga_65B0HP0E17=GS1.1.1691902056.1.1.1691902074.0.0.0; _ga=GA1.1.715588297.1691902057; _ga_K5929ZXSSV=GS1.1.1691902056.1.1.1691902078.38.0.0",
        "If-None-Match": "\"w0v0ao6lnl5msk\"",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"99\", \"Microsoft Edge\";v=\"115\", \"Chromium\";v=\"115\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        # Añade más encabezados aquí si es necesario
    }
    html_code = ""
    try:
        response = requests.get(url, headers=headers) 
        if response.status_code == 200:
            html_code = response.text
        else:
            print("Error al obtener la página:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error de conexión:", e)

    if len(html_code)>0: 
        soup = BeautifulSoup(html_code, 'html.parser')
        article_tag = soup.find('div',class_='st-sidebar__main')
        # Verificar si se encontró el tag <article>
        if article_tag:
            # Obtener el texto del tag <article>
            article_text = article_tag.get_text()
            # Imprimir el contenido del texto del tag <article>
            if len(article_text)>0:
                update_db(fila[0],fila[1],article_text)
        
    return ""


def update_larepublica(fila):
    #('larepublica', '2Q2K7XOXCFEU3IEHS5NGEKX2NM', '/economia/2021/04/10/expectativas-de-inflacion-se-mantienen-en-el-rango-meta/')
    url = "https://larepublica.pe{}".format(fila[2])
    print(url)
    user_agent = get_random_user_agent()
    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "es,es-ES;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Cookie": "_tfpvi=NDgxYjg2ZGQtYWE1Ny00MDYyLTk5OGQtNTkzYmZiZjYzMDhjIzgtNA%3D%3D; __AP_SESSION__=134ca4a3-5d3a-491d-a523-08985428362f; ___nrbi=%7B%22firstVisit%22%3A1691902055%2C%22userId%22%3A%22a32a0723-0896-4e5b-b0df-32e785142c6f%22%2C%22userVars%22%3A%5B%5D%2C%22futurePreviousVisit%22%3A1691902055%2C%22timesVisited%22%3A1%7D; compass_uid=a32a0723-0896-4e5b-b0df-32e785142c6f; __qca=P0-854938016-1691902056641; _gid=GA1.2.1692692428.1691902057; _cc_id=68aee879e13885ef4f30f9d599aafebb; panoramaId_expiry=1691988460480; panoramaId=06e11c145f156512a7fac596616da9fb927a1827211ef3382209e54034793228; panoramaIdType=panoDevice; cto_bundle=hUyqO18zekJlWUgzVlhTVU4lMkJ6S0dpcUQ5Q1JHa2VGN3BWVldJOU1XSklCeTNoUWpRdXU5UDd4JTJGbmZsUmV1M3UzQnRtWXdGMnd0c1FqTWt3NjNqNFZMUHp0aFJaNjYyV3BCaTZCeVpKSkZpaiUyRkw2SkJvZXlONDRhQTd2UExzUmxISFB1NTVGOFQ3aFBoNWZXZjU1NHg4Q3pNQXclM0QlM0Q; __gads=ID=a16992f89fbf6d0a:T=1691902062:RT=1691902062:S=ALNI_MaJzT67vWrxffnxAkZ-KYEYR7gU4Q; __gpi=UID=000009fa85e2cd40:T=1691902062:RT=1691902062:S=ALNI_MZvHm-kYPkUvg1tE8fiYYjWhF6jIw; TAPAD=%7B%22id%22%3A%22b51f3542-b673-43a8-8250-5b74cf37a8fa%22%7D; _pbjs_userid_consent_data=3524755945110770; ___nrbic=%7B%22previousVisit%22%3A1691902055%2C%22currentVisitStarted%22%3A1691902055%2C%22sessionId%22%3A%221b08d98d-a6a6-445a-8ff6-8cf6e59a8f92%22%2C%22sessionVars%22%3A%5B%5D%2C%22visitedInThisSession%22%3Atrue%2C%22pagesViewed%22%3A2%2C%22landingPage%22%3A%22https%3A//larepublica.pe/politica/actualidad/2023/08/12/pedro-castillo-extienden-investigacion-por-rebelion-hasta-abril-del-2024-838416%22%2C%22referrer%22%3A%22%22%7D; _ga_65B0HP0E17=GS1.1.1691902056.1.1.1691902074.0.0.0; _ga=GA1.1.715588297.1691902057; _ga_K5929ZXSSV=GS1.1.1691902056.1.1.1691902078.38.0.0",
        "If-None-Match": "\"w0v0ao6lnl5msk\"",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"99\", \"Microsoft Edge\";v=\"115\", \"Chromium\";v=\"115\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        # Añade más encabezados aquí si es necesario
    }
    html_code = ""
    try:
        response = requests.get(url, headers=headers) 
        if response.status_code == 200:
            html_code = response.text
        else:
            print("Error al obtener la página:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error de conexión:", e)

    if len(html_code)>0: 
        soup = BeautifulSoup(html_code, 'html.parser')
        article_tag = soup.find('article')
        # Verificar si se encontró el tag <article>
        if article_tag:
            # Obtener el texto del tag <article>
            article_text = article_tag.get_text()
            # Imprimir el contenido del texto del tag <article>
            #print(article_text)
            update_db(fila[0],fila[1],article_text)
        
    return ""

# 6000 tiene solo titulares

def select_db():
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
    query = "select periodico,_id,canonical_url FROM public.noticias where contenido is null and seccion='politica' order by display_date desc  LImit 30000"

    # Ejecutar la consulta
    cursor.execute(query)

    # Obtener los resultados en una lista de arreglos
    resultados = cursor.fetchall()

    # Cerrar el cursor y la conexión
    cursor.close()
    conn.close()

    # Imprimir los resultados
    for fila in resultados:
        if fila[0]=="larepublica":
            update_larepublica(fila)
        elif fila[0]=="elcomercio":
            update_elcomercio(fila)


 

#####################################################################################
# CODIGO PARA INSERTA A LA BD
#####################################################################################
def add_db(json_list):
    try:
        db_params = {
            "host": os.environ["HEROKU_HOST"],
            "database": os.environ["HEROKU_DATABASE"],
            "user": os.environ["HEROKU_USER"],
            "password": os.environ["HEROKU_PASSWORD"]
        }
        # Establecer conexión a la base de datos
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Preparar la consulta de inserción
        insert_query = """
            INSERT INTO public.noticias (
                periodico,
                seccion,
                _id,
                canonical_url,
                display_date,
                headlines_basic,
                subheadlines_basic,
                taxonomy_seo_keywords,
                taxonomy_tags,
                _type
            ) VALUES (
                %(periodico)s,
                %(seccion)s,
                %(_id)s,
                %(canonical_url)s,
                %(display_date)s,
                %(headlines_basic)s,
                %(subheadlines_basic)s,
                %(taxonomy_seo_keywords)s,
                %(taxonomy_tags)s,
                %(_type)s
            )
        """
        # Insertar los datos de manera masiva 
        cursor.executemany(insert_query, json_list)
        # Confirmar y cerrar la conexión 
        connection.commit() 
        cursor.close() 
        connection.close()
    except Exception as e:
        print(e)

#####################################################################################
# CODIGO DE SCRAPEO E INSERT A LA BD
#####################################################################################

def scrape_website(website_code,v_cantidad):
    if website_code == 'elcomercio':
        #ur de hice 0,100, 500....VAL_STRING_CANTIDAD
        url_elcomercio = "https://elcomercio.pe/pf/api/v3/content/fetch/story-feed-by-section"
        params_elcomercio = {
            "query": '''{"feedOffset":VAL_STRING_CANTIDAD,
                        "includedFields":"&_sourceInclude=websites.elcomercio.website_url,_id,headlines.basic,subheadlines.basic,display_date,content_restrictions.content_code,credits.by._id,credits.by.name,credits.by.url,credits.by.type,credits.by.image.url,websites.elcomercio.website_section.path,websites.elcomercio.website_section.name,taxonomy.sections.path,taxonomy.sections._id,taxonomy.sections.name,promo_items.basic.type,promo_items.basic.url,promo_items.basic.width,promo_items.basic.height,promo_items.basic.resized_urls,promo_items.basic_video.promo_items.basic.url,promo_items.basic_video.promo_items.basic.type,promo_items.basic_video.promo_items.basic.resized_urls,promo_items.basic_gallery.promo_items.basic.url,promo_items.basic_gallery.promo_items.basic.type,promo_items.basic_gallery.promo_items.basic.resized_urls,promo_items.youtube_id.content,promo_items.basic_html,promo_items.basic_jwplayer.type,promo_items.basic_jwplayer.subtype,promo_items.basic_jwplayer.embed,promo_items.basic_jwplayer.embed.config,promo_items.basic_jwplayer.embed.config.thumbnail_url,promo_items.basic_jwplayer.embed.config.resized_urls,promo_items.basic_jwplayer.embed.config.key,promo_items.basic_html.content",
                        "presets":"landscape_s:234x161,landscape_xs:118x72",
                        "section":"/politica",
                        "stories_qty":100}''',
            "filter": '{"content_elements":{"_id":1,"content_restrictions":{"content_code":1},"credits":{"by":{"image":{"url":1},"name":1,"type":1,"url":1}},"display_date":1,"headlines":{"basic":1},"promo_items":{"basic":{"resized_urls":{"landscape_s":1,"landscape_xs":1,"lazy_default":1},"type":1,"url":1},"basic_gallery":{"promo_items":{"basic":{"resized_urls":{"landscape_s":1,"landscape_xs":1,"lazy_default":1},"type":1,"url":1}}},"basic_html":{"content":1},"basic_jwplayer":{"embed":{"config":{"resized_urls":{"landscape_s":1,"landscape_xs":1,"lazy_default":1},"thumbnail_url":1}},"subtype":1,"type":1},"basic_video":{"promo_items":{"basic":{"resized_urls":{"landscape_s":1,"landscape_xs":1,"lazy_default":1},"type":1,"url":1}}},"youtube_id":{"content":1}},"subheadlines":{"basic":1},"taxonomy":{"sections":{"name":1,"path":1}},"website_url":1,"websites":{"elcomercio":{"website_section":{"name":1,"path":1},"website_url":1}}},"next":1}',
            "d": "2831",
            "_website": "elcomercio"
        }

        user_agent = get_random_user_agent()

        headers_elcomercio = {
            "User-Agent": user_agent,
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "es-ES,es;q=0.9",
            "Referer": "https://elcomercio.pe/archivo/politica/",
            "Sec-Ch-Ua": '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            "Sec-Ch-Ua-Mobile": "?1",
            "Sec-Ch-Ua-Platform": "\"Android\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            # Agrega otras cabeceras si es necesario
        }

        params_elcomercio["query"] =  params_elcomercio["query"].replace("VAL_STRING_CANTIDAD",str(v_cantidad))
        response = requests.get(url_elcomercio, params=params_elcomercio, headers=headers_elcomercio)
        data = response.json()
        json_list = []
        for valores in data["content_elements"]:
            json_result = {
            "periodico": "elcomercio",
            "seccion": "politica",
            "_id": valores["_id"],
            "canonical_url": valores["websites"]["elcomercio"]["website_url"],
            "display_date": valores["display_date"],
            "headlines_basic": str(valores["headlines"]["basic"]),
            "subheadlines_basic": str(valores["subheadlines"]["basic"]),
            "taxonomy_seo_keywords": str(valores["taxonomy"]),
            "taxonomy_tags": str(valores["taxonomy"]["sections"][0]["path"]),
            "_type": str(valores["taxonomy"]["sections"][0]["name"])
            }
            json_list.append(json_result)
    elif website_code == 'larepublica':
        url_larepublica = "https://larepublica.pe/api/search/articles?category_slug=politica&limit=100&page=VALOR_LAREPUBLICA&order_by=update_date"
        
        user_agent = get_random_user_agent()

        headers_larepublica = {
            "User-Agent": user_agent,
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "es-ES,es;q=0.9",
            "Cache-Control": "max-age=0",
            #"Cookie": "_tfpvi=OGE4MjI0M2ItOGFiZi00MDQ3LWIxNDAtMWUwZGYwYjcwOGRiIy05LTc%3D; compass_uid=ad62f089-b4a2-44ff-80b4-ebb56974379e; _cc_id=d749f8aef1f17c3fbaedf2bc39992bb3; __qca=P0-1464962464-1691765168006; truvid_protected={\"val\":\"c\",\"level\":2,\"geo\":\"PE\",\"timestamp\":1691765494}; _ga_DY52VFJQZF=GS1.1.1691781334.1.1.1691781834.0.0.0; clever-last-tracker-45756=1; ___nrbi=%7B%22firstVisit%22%3A1689030202%2C%22userId%22%3A%22ad62f089-b4a2-44ff-80b4-ebb56974379e%22%2C%22userVars%22%3A%5B%5D%2C%22futurePreviousVisit%22%3A1691897369%2C%22timesVisited%22%3A5%7D; _gid=GA1.2.489052991.1691897373; panoramaId_expiry=1691983777480; panoramaId=7e9777a17041e418bc1b41876b8ba9fb927a4fe7365716de8bb596d29972c7d6; panoramaIdType=panoDevice; _pbjs_userid_consent_data=6683316680106290; cto_bidid=uYTRXF9WdmtjcSUyRnUwemhuVjRWSGkyOVkxTnQ3aWJmQ29lQ29hanRvZmxmZnpkU0ZObEY0cERsWWtDJTJCNDhuVFFxdDRiNUJFWlc3N2Q3WmQ2T3M3SiUyRnZoUks4NW5DR2RXVVRsRm1FUFc4eGYlMkZ2MmZJMnQ4WiUyQllGM29CRDYzRklzOUZ4WWQ; __AP_SESSION__=7779e931-5eb7-474a-8ef3-96accf327a6a; ___nrbic=%7B%22previousVisit%22%3A1691765166%2C%22currentVisitStarted%22%3A1691897369%2C%22sessionId%22%3A%224fc53c8b-3b7d-4910-97dd-f72c6b3405f3%22%2C%22sessionVars%22%3A%5B%5D%2C%22visitedInThisSession%22%3Atrue%2C%22pagesViewed%22%3A9%2C%22landingPage%22%3A%22https%3A//larepublica.pe/%22%2C%22referrer%22%3A%22https%3A//larepublica.pe/mundo/2023/08/09/encuestas-ecuador-2023-quienes-son-los-candidatos-con-mayor-intencion-de-voto-para-las-elecciones-encuestas-presidenciales-ecuador-2023-cedatos-lista-de-candidatos-inscritos-elecciones-2023-candidatos-presidenciales-ecuador-elecciones-2023-ecuador-504720%22%7D; _ga=GA1.1.74485386.1689030204; cto_bundle=ULgvq19LRG4yZEd0QjRyeHpycDdTbUVGdTAyUWFEQ0llVnZWaVA1VEglMkJLSUpOeTJqQ0xLV2VJbWZvVFNlJTJGJTJCWWxXMyUyRmtqQlZ0dXVzZ0lYJTJCdll4M0VNaUVydzVuY3FZdjJ6b3I4NlJqcnlNeCUyQmh1N2o1SFROVzglMkZvNjdaMVZibXBtbkQ2MlM0Q2I4TXpnSDk4WGJuQW5leGw3USUzRCUzRA; __gads=ID=6c962fda630b6090:T=1689030206:RT=1691902498:S=ALNI_MZUMRgo6RL3gKwSZMSJwqAWRVjAMg; __gpi=UID=000009f7bc070f7e:T=1689030206:RT=1691902498:S=ALNI_MbJsUucFZSpXqCQQ0IMFY70sMP0HQ; _ga_65B0HP0E17=GS1.1.1691902027.6.1.1691902739.0.0.0; _ga_K5929ZXSSV=GS1.1.1691902027.8.1.1691902739.60.0.0; MgidStorage=%7B%220%22%3A%7B%22svspr%22%3A%22https%3A%2F%2Flarepublica.pe%2Fpolitica%22%2C%22svsds%22%3A7%7D%2C%22C1446817%22%3A%7B%22page%22%3A3%2C%22time%22%3A%221691902739883%22%7D%2C%22C1467861%22%3A%7B%22page%22%3A1%7D%7D",
            "Referer": "https://larepublica.pe/politica",
            "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"99\", \"Google Chrome\";v=\"115\", \"Chromium\";v=\"115\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }
        url_larepublica = url_larepublica.replace("VALOR_LAREPUBLICA",str(v_cantidad))
        #print(url_larepublica)
        response = requests.get(url_larepublica, headers=headers_larepublica)
        #print(response.json()["articles"]["data"][0])
        data = response.json()
        json_list = []
        for valores in data["articles"]["data"]:
            try:
                val_sh = str(valores["data"]["teaser"])
            except Exception as e:
                val_sh = str(valores["title"])
                print(e)
            try:
                val_t = str(valores["data"]["tags"][0]["name"])
            except Exception as e:
                val_t = str(valores["data"])
                print(e)
            json_result = {
            "periodico": "larepublica",
            "seccion": "politica",
            "_id": valores["_id"],
            "canonical_url": valores["slug"],
            "display_date": valores["update_date"],
            "headlines_basic": str(valores["title"]),
            "subheadlines_basic": val_sh,
            "taxonomy_seo_keywords": val_t,
            "taxonomy_tags": str(valores["data"]),
            "_type": str(valores["type"])
            }
            json_list.append(json_result)

    else:
        print('Código de sitio web no válido')
        return

    if response.status_code == 200:
        add_db(json_list)
    else:
        print('La solicitud no fue exitosa. Código de estado:', response.status_code)

def get_video_list_channel(channel_id):
    # Inicializar la lista para almacenar los videos
    videos = []
    youtube = build('youtube', 'v3', developerKey=API_KEY)
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
    #videos = validar_no_repetir()
    return videos

def get_metadata(video_id,nom_channel):
    # Extraer el ID del canal de la URL
    # Realizar la solicitud para obtener la metadata del video
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    response = youtube.videos().list(
        part='snippet,statistics',
        id=video_id
    ).execute()
    # Extraer la información relevante de la respuesta
    video_info = response['items'][0]
    try:
        tsk = str(video_info["statistics"]["viewCount"])
    except Exceiption as e:
        tsk=""
    try:
        tt = str(video_info["statistics"]["commentCount"])
    except Exceiption as e:
        tt=""
    try:
        _t = str(video_info["statistics"]["viewCount"])
    except Exceiption as e:
        _t=""

    resultado = {
        "periodico": str(nom_channel),
        "seccion": video_info["snippet"]["categoryId"],
        "_id": video_info["id"],
        "canonical_url": video_info["id"],
        "display_date": video_info["snippet"]["publishedAt"],
        "headlines_basic": str(video_info["snippet"]["title"]),
        "subheadlines_basic": str(video_info["snippet"]["description"]),
        "taxonomy_seo_keywords": str(tsk),
        "taxonomy_tags": str(tt),
        "_type": str(_t)
    }
    return resultado

def scrape_youtube(id_channel,nom_channel):
    # en el caso de youtube el website_code es el ID_CHANNEL
    lista_videos = get_video_list_channel(id_channel)
    l_videos = []
    for video in lista_videos:
        metadata=get_metadata(video,nom_channel) # video es el id del video debe ser un json
        l_videos.append(metadata)

    if len(l_videos)>0:
        add_db(l_videos)

#####################################################################################
# MAIN PRINCIPAL
#####################################################################################
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Uso: python script.py <código_del_sitio_web>')
    else:
        website_code = sys.argv[1]
        v_cantidad = sys.argv[2]
        if website_code == "contenido":
            select_db()
        if v_cantidad[:3] == "you":
            #s= "you_EXITOSA"
            #print(s[:3]) #you
            #print(s[4:]) #EXITOSA
            #website_Code es el id_channel
            scrape_youtube(website_code,v_cantidad[4:])
        else:
            scrape_website(website_code,v_cantidad)