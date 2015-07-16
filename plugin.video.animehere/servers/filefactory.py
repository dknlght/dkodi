# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para filefactory
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    logger.info("[filefactory.py] test_video_exists(page_url='%s')" % page_url)

    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[filefactory.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    #http://www.filefactory.com/file/35ip193vzp1f/n/HMD-5x19-ESP.avi
    patronvideos = "(www.filefactory.com/file.*?\.avi)"
    logger.info("[filefactory.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    for match in matches:
        titulo = "[filefactory]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'filefactory' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
