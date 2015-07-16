# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videos externos de veevr
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    logger.info("[veevr.py] test_video_exists(page_url='%s')" % page_url)
    
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[veevr.py] get_video_url(page_url='%s')" % page_url)

    video_urls = []

    for video_url in video_urls:
        logger.info("[veevr.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []
    
    # veevr http://veevr.com/videos/kgDAMC4Btp"
    patronvideos  = 'http://veevr.[\w]+/videos/([\w]+)'
    logger.info("[veevr.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[veevr]"
        url = "http://veevr.com/videos/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'veevr' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
    
    # veevr http://veevr.com/embed/kgDAMC4Btp"
    patronvideos  = 'http://veevr.[\w]+/embed/([\w]+)'
    logger.info("[veevr.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[veevr]"
        url = "http://veevr.com/videos/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'veevr' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
            
    return devuelve
