# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para hdplay
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[hdplay.py] get_video_url(page_url='%s')" % page_url)

    video_urls = []
    
    # Descarga la página, el usuario tiene dos botones de "Descargar" o "Ver"
    data = scrapertools.cache_page(page_url)
    
    # La descarga de nuevo como si hubiera pulsado el botón "Ver"
    data = scrapertools.cache_page(page_url,post="agree=")

    #var movieURL  = "http://srv.hdplay.org:81/storage/flv/JOUhxy.mp4?key=3e518187037720b4ef1a210df2c92162";
    #var fileName = "JOUhxy.mp4";
    patron = 'var movieURL  \= "([^"]+)"\;\W+'
    patron += 'var fileName \= "([^"]+)"\;'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
         
        # La URL es http://srv.hdplay.org:81/storage/flv/JOUhxy.mp4?key=3e518187037720b4ef1a210df2c92162
        url = matches[0][0] #+"?file="+matches[0][1]+"&start=0"
        video_urls.append( ["[hdplay]",url ] )

    for video_url in video_urls:
        logger.info("[hdplay.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://www.hdplay.org/xGylz8
    patronvideos  = '(http://www.hdplay.org/[A-Za-z0-9]+)'
    logger.info("[hdplay.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[hdplay]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'hdplay' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
