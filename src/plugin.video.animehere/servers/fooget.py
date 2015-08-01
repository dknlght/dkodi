# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para fooget
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    logger.info("[fooget.py] test_video_exists(page_url='%s')" % page_url)
    
    # Existe: http://www.fooget.com/s3k5gbuvfqel.html
    # No existe: 
    data = scrapertools.cache_page(page_url)
    patron  = '<img src="http://fooget.com/images2/download-arrow.jpg"[^>]+>[^<]+'
    patron += '<span[^>]+>([^<]+)</span>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    if len(matches)>0:
        return True,""
    else:
        patron  = '<h2>(File Not Found)</h2>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if len(matches)>0:
            return False,"El archivo ya no está disponible<br/>en fooget o ha sido borrado"
    
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[fooget.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://www.filejungle.com/f/3Q7apX
    patronvideos  = '(http://www.fooget.com/[a-z0-9]+.html)'
    logger.info("[fooget.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[fooget]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'fooget' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
