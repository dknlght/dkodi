# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para rapidshare
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[rapidshare.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # https://rapidshare.com/files/3346009389/_BiW__Last_Exile_Ginyoku_no_Fam_-_Episodio_09__A68583B1_.mkv
    # "https://rapidshare.com/files/3346009389/_BiW__Last_Exile_Ginyoku_no_Fam_-_Episodio_09__A68583B1_.mkv"
    # http://rapidshare.com/files/2327495081/Camino.Sangriento.4.HDR.Proper.200Ro.dri.part5.rar
    # https://rapidshare.com/files/715435909/Salmon.Fishing.in.the.Yemen.2012.720p.UNSOLOCLIC.INFO.mkv
    patronvideos  = '(rapidshare.com/files/[0-9]+/.*?)["|<]'
    logger.info("[rapidshare.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data+'"')

    for match in matches:
        titulo = "[rapidshare]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'rapidshare' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
