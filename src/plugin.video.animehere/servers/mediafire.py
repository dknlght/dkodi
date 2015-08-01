# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para mediafire
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[mediafire.py] get_video_url(page_url='%s')" % page_url)
    video_urls=[]
    
    data = scrapertools.cache_page(page_url)

    # Espera un segundo y vuelve a cargar
    logger.info("[mediafire.py] waiting 1 secs")
    import time
    time.sleep(1)

    data = scrapertools.cache_page(page_url)
    patron = 'kNO \= "([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        video_urls.append( [matches[0][-4:]+" [mediafire]",matches[0] ] )

    for video_url in video_urls:
        logger.info("[mediafire.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls        

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    #<a href="http://www.mediafire.com/download.php?pkpnzadbp2qp893" target="_blank">[Natgeo] Huesos con Historia 08 - Los Esqueletos de Windy Pits</a><br />
    patronvideos  = '<a href=".*?mediafire.com/download.php\?([a-z0-9]+)"[^>]+>([^<]+)</a>'
    logger.info("[mediafire.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match,title in matches:
        titulo = title+" [mediafire]"
        url = 'http://www.mediafire.com/?'+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'mediafire' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://www.mediafire.com/download.php?pkpnzadbp2qp893
    patronvideos  = 'mediafire.com/download.php\?([a-z0-9]+)'
    logger.info("[mediafire.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mediafire]"
        url = 'http://www.mediafire.com/?'+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'mediafire' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://www.mediafire.com/?4ckgjozbfid
    patronvideos  = 'http://www.mediafire.com/\?([a-z0-9]+)'
    logger.info("[mediafire.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mediafire]"
        url = 'http://www.mediafire.com/?'+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'mediafire' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://www.mediafire.com/file/c0ama0jzxk6pbjl
    patronvideos  = 'http://www.mediafire.com/file/([a-z0-9]+)'
    logger.info("[mediafire.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mediafire]"
        url = 'http://www.mediafire.com/?'+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'mediafire' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # Encontrado en animeflv
    #s=mediafire.com%2F%3F7fsmmq2144fx6t4|-|wupload.com%2Ffile%2F2653904582
    patronvideos  = 'mediafire.com\%2F\%3F([a-z0-9]+)'
    logger.info("[mediafire.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[mediafire]"
        url = "http://www.mediafire.com/?"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'mediafire' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
