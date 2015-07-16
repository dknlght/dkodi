# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para stagevu
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[stagevu.py] get_video_url(page_url='%s')" % page_url)

    video_urls = []

    # Descarga la página del vídeo
    data = scrapertools.cache_page( page_url )

    # Busca el vídeo de dos formas distintas
    patronvideos  = '<param name="src" value="([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    if len(matches) > 0:
        video_urls = [[ "[stagevu]" , matches[0] ]]
    else:
        patronvideos = 'src="([^"]+stagevu.com/[^i][^"]+)"' #Forma src="XXXstagevu.com/ y algo distinto de i para evitar images e includes
        matches = re.findall(patronvideos,data)
        if len(matches)>0:
            video_urls = [[ "[stagevu]" , matches[0] ]]

    for video_url in video_urls:
        logger.info("[stagevu.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos  = '(http://stagevu.com/video/[A-Z0-9a-z]+)'
    logger.info("[stagevu.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[stagevu]"
        url = match
    
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'stagevu' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos  = 'http://stagevu.com.*?uid\=([A-Z0-9a-z]+)'
    logger.info("[stagevu.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[stagevu]"
        url = "http://stagevu.com/video/"+match
    
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'stagevu' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos  = 'http://[^\.]+\.stagevu.com/v/[^/]+/(.*?).avi'
    logger.info("[stagevu.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos).findall(data)

    for match in matches:
        titulo = "[stagevu]"
        url = "http://stagevu.com/video/"+match
    
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'stagevu' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
