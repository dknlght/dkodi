# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videoweed
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import re, urlparse, urllib, urllib2
import os

from core import scrapertools
from core import logger
from core import config

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="" , video_password="" ):
    logger.info("[videoweed.py] get_video_url(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)
    patron = 'flashvars.file="(.*?)";'
    matches = re.compile(patron).findall(data)
    for match in matches:
        logger.info("File = "+match)
    flashvarsfile = match
    patron = 'flashvars.filekey="(.*?)";'
    matches = re.compile(patron).findall(data)
    for match in matches:
        logger.info("Key = "+match)
    flashvarsfilekey = match
    post="key="+flashvarsfilekey+"&user=undefined&codes=1&pass=undefined&file="+flashvarsfile
    url = "http://www.videoweed.es/api/player.api.php?"+post
    data = scrapertools.cache_page(url, post=post)
    logger.info(data)
    patron = 'url=(.*?)&title='
    matches = re.compile(patron).findall(data)
    scrapertools.printMatches(matches)
    
    video_urls = []
    logger.info(matches[0])
    video_urls.append( [".flv [videoweed]",matches[0]])
    
    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos  = '(http://www.videoweed.[a-z]+/file/[a-zA-Z0-9]+)'
    logger.info("[videoweed.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[videoweed]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'videoweed' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #logger.info("1) Videoweed formato islapeliculas") #http://embed.videoweed.com/embed.php?v=h56ts9bh1vat8
    patronvideos  = "(http://embed.videoweed.*?)&"
    logger.info("[videoweed.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[videoweed]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'videoweed' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    #rep="/rep2.php?vw=wuogenrzatq40&t=18&c=13"
    patronvideos  = 'src="" rep="([^"]+)" width="([^"]+)" height="([^"]+)"'
    logger.info("[videoweed.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[videoweed]"
        url = match[0]
        url = url.replace("/rep2.php?vw=","http://www.videoweed.es/file/")
        
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'videoweed' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

def test_video_exists(page_url):
    video_urls = get_video_url(page_url)
    if len(video_urls)>0:
        return True,""
    else:
        return False,""

    return len(video_urls)>0