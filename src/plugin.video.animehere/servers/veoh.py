# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para Veoh
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import os
import urlparse,urllib2,urllib,re

from core import scrapertools
from core import logger
from core import config

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[veoh.py] get_video_url(page_url='%s')" % page_url)

    video_urls = []

    # Lo extrae a partir de flashvideodownloader.org
    if page_url.startswith("http://"):
        url = 'http://www.flashvideodownloader.org/download.php?u='+page_url
    else:
        url = 'http://www.flashvideodownloader.org/download.php?u=http://www.veoh.com/watch/'+page_url
    logger.info("[veoh.py] url="+url)
    data = scrapertools.cachePage(url)
    
    # Extrae el vídeo
    patronvideos  = '<a href="(http://content.veoh.com.*?)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    if len(matches)>0:
        video_urls.append( ["[veoh]",matches[0]] )
    
    for video_url in video_urls:
        logger.info("[veoh.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos  = '"http://www.veoh.com/.*?permalinkId=([^"]+)"'
    logger.info("[veoh.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[veoh]"
        if match.count("&")>0:
            primera = match.find("&")
            url = match[:primera]
        else:
            url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'veoh' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos = 'var embed_code[^>]+>   <param name="movie" value="http://www.veoh.com/static/swf/webplayer/WebPlayer.swf.*?permalinkId=(.*?)&player=videodetailsembedded&videoAutoPlay=0&id=anonymous"></param>'
    logger.info("[veoh.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[veoh]"
        if match.count("&")>0:
            primera = match.find("&")
            url = match[:primera]
        else:
            url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'veoh' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
