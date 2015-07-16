# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para watchfreeinhd
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[watchfreeinhd.py] get_video_url(page_url='%s')" % page_url)

    video_urls = []
    
    # Descarga la página, el usuario tiene dos botones de "Descargar" o "Ver"
    data = scrapertools.cache_page(page_url)
    
    # La descarga de nuevo como si hubiera pulsado el botón "Ver"
    # http://srv.hdplay.org/storage/flv/xGylz8.flv?token=703acade4b51aa6b26ad264327c4a4cf
    data = scrapertools.cache_page(page_url,post="agree=")
    patron = '<div id="playerHolder">[^<]+'
    patron += '<a href="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        video_urls.append( ["[watchfreeinhd]",matches[0] ] )

    for video_url in video_urls:
        logger.info("[watchfreeinhd.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://www.watchfreeinhd.com/r0GUbN
    patronvideos  = '(http://www.watchfreeinhd.com/[A-Za-z0-9]+)'
    logger.info("[watchfreeinhd.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[watchfreeinhd]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'watchfreeinhd' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
