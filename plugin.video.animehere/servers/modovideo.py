# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para modovideo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re, urlparse, urllib, urllib2
import os

from core import scrapertools
from core import logger
from core import config

#Location: http://www.modovideo.com/MakeLightBox.php?retURL=&h1=Video Has been removed&p=

def test_video_exists( page_url ):
    if not page_url.startswith("http://"):
        page_url = 'http://www.modovideo.com/frame.php?v='+page_url

    logger.info("[modovideo.py] test_video_exists(page_url='%s')" % page_url)
    
    # Vídeo borrado: http://www.modovideo.com/frame.php?v=teml3hpu3141n0lam2a04iufcsz7q7pt
    location = scrapertools.get_header_from_response( url = page_url , header_to_get = "location")
    if location=="":
        return True,""
    #Location: http://www.modovideo.com/MakeLightBox.php?retURL=&h1=Video Has been removed&p=
    elif "Video Has been removed" in location:
        return False,"El archivo ya no está disponible<br/>en modovideo (ha sido borrado)"
    else:
        return True,""

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[modovideo.py] get_video_url(page_url='%s')" % page_url)

    video_urls = []
    
    # Descarga la página
    headers = []
    headers.append(["User-Agent","Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10"])
    scrapertools.cache_page(page_url,headers=headers)

    # Descarga el iframe
    headers.append(["Referer",page_url])
    code = scrapertools.get_match(page_url,"http://www.modovideo.com/video\?v\=([a-zA-Z0-9]+)")
    #http://www.modovideo.com/frame.php?v=teml3hpu3141n0lam2a04iufcsz7q7pt
    data = scrapertools.cachePage("http://www.modovideo.com/frame.php?v="+code , headers=headers)

    # Extrae la URL real
    #<video id='player' src=http://s07.modovideo.com:80/vid/8734f19b6ec156e285a0e526fdc79566/508ea846/flv/0c4lymiwtfe2m9tdr2fp8dzxmbe3csv3.mp4 style=' width: 100%; height: 75%'  type='video/mp4' poster='' controls='controls' ></video></div>
    patronvideos  = "<video id='player' src=(.*?) "
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    
    video_urls = []
    for match in matches:
        video_urls.append(["[modovideo]",match])

    for video_url in video_urls:
        logger.info("[modovideo.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []
    #http://www.modovideo.com/video?v=7050wk9aa66xr579rtyyjm3fhbq45k4d
    #http://www.modovideo.com/frame.php?v=qzyrxqsxacbq3q43ssyghxzqkp35t8rh
    patronvideos  = 'modovideo.com/(?:frame\.php|video\.php|video)\?v=([a-zA-Z0-9]+)' 
    logger.info("[modovideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Modovideo]"
        url = "http://www.modovideo.com/video?v="+match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'modovideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #logger.info("1) Modovideo formato Peliculasaudiolatino") #http://www.peliculasaudiolatino.com/show/modovideo.php?url=qzyrxqsxacbq3q43ssyghxzqkp35t8rh
    patronvideos  = "modovideo.php\?url=([a-zA-Z0-9]+)"
    logger.info("[modovideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Modovideo]"
        url = "http://www.modovideo.com/video?v="+match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'modovideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve