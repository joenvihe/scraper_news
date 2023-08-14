import sys
import requests
from bs4 import BeautifulSoup
import csv
import requests
import psycopg2
import os
import json


# 6000 tiene solo titulares
########################################################################################
# PARAMETROS DE LAS URLS A SCRAPEAR
########################################################################################
url_larepublica = "https://larepublica.pe/api/search/articles?category_slug=politica&limit=100&page={}&order_by=update_date"

headers_larepublica = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
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

headers_elcomercio = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36",
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
        print(url_larepublica)
        url_larepublica = url_larepublica.format(str(v_cantidad))
        response = requests.get(url_larepublica, headers=headers_larepublica)
        print(response.json())
    else:
        print('Código de sitio web no válido')
        return

    if response.status_code == 200:
        add_db(json_list)
    else:
        print('La solicitud no fue exitosa. Código de estado:', response.status_code)

#####################################################################################
# MAIN PRINCIPAL
#####################################################################################


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Uso: python script.py <código_del_sitio_web>')
    else:
        website_code = sys.argv[1]
        v_cantidad = sys.argv[2]
        scrape_website(website_code,v_cantidad)
