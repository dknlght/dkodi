# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para extabit.com
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    logger.info("[extabit.py] test_video_exists(page_url='%s')" % page_url)
    
    # Vídeo borrado: uploaded.to/file/q4rkg1rw -> Redirige a otra página uploaded.to/410/q4rkg1rw
    # Video erróneo: uploaded.to/file/q4rkg1rx -> Redirige a otra página uploaded.to/404
    location = scrapertools.get_header_from_response( url = page_url , header_to_get = "location")
    if location=="":
        return True,""
    elif "410" in location:
        return False,"El archivo ya no está disponible<br/>en extabit.com (ha sido borrado)"
    elif "404" in location:
        return False,"El archivo no existe<br/>en extabit.com (enlace no válido)"
    else:
        return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[extabit.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://uploaded.to/file/1haty8nt
    patronvideos  = '(extabit.com/file/[a-zA-Z0-9]+)'
    logger.info("[extabit.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[extabit.com]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'extabit' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    

    return devuelve
