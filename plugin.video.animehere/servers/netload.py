# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para netload
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[netload.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://netload.in/dateiroqHV0QNJg/Salmon.Fishing.in.the.Yemen.2012.720p.UNSOLOCLIC.INFO.mkv.htm
    patronvideos  = '(netload.in/[a-zA-Z0-9]+/.*?.htm)'
    logger.info("[netload.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data+'"')

    for match in matches:
        titulo = "[netload]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'netload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://netload.in/datei2OuYAjcVGq.htm
    patronvideos  = '(netload.in/[a-zA-Z0-9]+.htm)'
    logger.info("[netload.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data+'"')

    for match in matches:
        titulo = "[netload]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'netload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
