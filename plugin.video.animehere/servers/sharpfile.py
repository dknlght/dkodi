# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para sharpfile
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    logger.info("[sharpfile.py] test_video_exists(page_url='%s')" % page_url)

    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[sharpfile.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    #http://www.sharpfile.com/8fgbj6dtq4xc/house.05x19.pionnerdj.avi.html
    patronvideos = "http://(www.sharpfile.com/.*?\.html)"
    logger.info("[sharpfile.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    for match in matches:
        titulo = "[sharpfile]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'sharpfile' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
