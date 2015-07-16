# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para royalvids
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[royalvids.py] url="+page_url)
    
    # http://www.royalvids.eu/e.php?id=4f1ce3fe5305f&width=670&height=400
    page_url = 'http://www.royalvids.eu/e.php?id='+page_url+'&width=670&height=400'
    # Lo pide una vez
    data = scrapertools.cache_page( page_url)
    

    # Extrae el trozo cifrado
   
    patron ='<param name="flashvars" value="file=(.+?)&'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    data = ""
    if len(matches)>0:
        logger.info("[royalvids.py] flashvars=")
    else:
        logger.info("[royalvids.py] no encuentra flashvars=")

        return []
    
    
    video_urls = []
    
    url = matches[0]+"?start=0"
    video_urls.append( ["."+matches[0].rsplit('.',1)[1]+" [royalvids]",url])

    for video_url in video_urls:
        logger.info("[royalvids.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://www.peliculasaudiolatino.com/show/royalvids.php?url=4f1ce3fe5305f
    patronvideos  = 'royalvids\.php\?url=([A-Z0-9a-z]+)'
    logger.info("[royalvids.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[royalvids]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'royalvids' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    # http://www.royalvids.eu/e.php?id=4f1ce3fe5305f&width=670&height=400
    patronvideos  = 'http://www.royalvids.eu/e.php\?id=([A-Z0-9a-z]+)'
    logger.info("[royalvids.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[royalvids]"
        url = "http://www.royalvids.com/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'royalvids' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
