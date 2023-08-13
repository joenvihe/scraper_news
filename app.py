import sys
import requests
from bs4 import BeautifulSoup
import csv

#ur de 100 en 100....
url_comercio = "https://elcomercio.pe/pf/api/v3/content/fetch/story-feed-by-section"
params_comercio = {
    "query": '''{"feedOffset":500,
                  "includedFields":"&_sourceInclude=websites.elcomercio.website_url,_id,headlines.basic,subheadlines.basic,display_date,content_restrictions.content_code,credits.by._id,credits.by.name,credits.by.url,credits.by.type,credits.by.image.url,websites.elcomercio.website_section.path,websites.elcomercio.website_section.name,taxonomy.sections.path,taxonomy.sections._id,taxonomy.sections.name,promo_items.basic.type,promo_items.basic.url,promo_items.basic.width,promo_items.basic.height,promo_items.basic.resized_urls,promo_items.basic_video.promo_items.basic.url,promo_items.basic_video.promo_items.basic.type,promo_items.basic_video.promo_items.basic.resized_urls,promo_items.basic_gallery.promo_items.basic.url,promo_items.basic_gallery.promo_items.basic.type,promo_items.basic_gallery.promo_items.basic.resized_urls,promo_items.youtube_id.content,promo_items.basic_html,promo_items.basic_jwplayer.type,promo_items.basic_jwplayer.subtype,promo_items.basic_jwplayer.embed,promo_items.basic_jwplayer.embed.config,promo_items.basic_jwplayer.embed.config.thumbnail_url,promo_items.basic_jwplayer.embed.config.resized_urls,promo_items.basic_jwplayer.embed.config.key,promo_items.basic_html.content",
                  "presets":"landscape_s:234x161,landscape_xs:118x72",
                  "section":"/politica",
                  "stories_qty":100}''',
    "filter": '{"content_elements":{"_id":1,"content_restrictions":{"content_code":1},"credits":{"by":{"image":{"url":1},"name":1,"type":1,"url":1}},"display_date":1,"headlines":{"basic":1},"promo_items":{"basic":{"resized_urls":{"landscape_s":1,"landscape_xs":1,"lazy_default":1},"type":1,"url":1},"basic_gallery":{"promo_items":{"basic":{"resized_urls":{"landscape_s":1,"landscape_xs":1,"lazy_default":1},"type":1,"url":1}}},"basic_html":{"content":1},"basic_jwplayer":{"embed":{"config":{"resized_urls":{"landscape_s":1,"landscape_xs":1,"lazy_default":1},"thumbnail_url":1}},"subtype":1,"type":1},"basic_video":{"promo_items":{"basic":{"resized_urls":{"landscape_s":1,"landscape_xs":1,"lazy_default":1},"type":1,"url":1}}},"youtube_id":{"content":1}},"subheadlines":{"basic":1},"taxonomy":{"sections":{"name":1,"path":1}},"website_url":1,"websites":{"elcomercio":{"website_section":{"name":1,"path":1},"website_url":1}}},"next":1}',
    "d": "2831",
    "_website": "elcomercio"
}

headers_comercio = {
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



def scrape_website(website_code):
    if website_code == 'el_comercio':
        response = requests.get(url_comercio, params=params_comercio, headers=headers_comercio)
    elif website_code == 'b':
        url = 'https://www.csd.es'
    else:
        print('Código de sitio web no válido')
        return

    if response.status_code == 200:
        data = response.json()
        print('Datos extraídos y guardados en datos_extraidos.csv')
        print(data)
    else:
        print('La solicitud no fue exitosa. Código de estado:', response.status_code)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Uso: python script.py <código_del_sitio_web>')
    else:
        website_code = sys.argv[1]
        scrape_website(website_code)
