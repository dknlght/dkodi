# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para Rapidtube
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="" , video_password="" ):
    logger.info("[rapidtube.py] get_video_url(page_url='%s')" % page_url)

    video_urls = []

    # Descarga la página
    headers = [ ['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'],['Referer','http://www.rapidtube.com/'] ]
    data = scrapertools.cache_page(page_url , headers = headers)
    data = data.replace('"',"'")
    print data

    # Extrae el vídeo
    patronvideos  = "file: '([^']+)'"
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)

    for match in matches:
        video_urls.append( [ "."+match.rsplit('.',1)[1]+" [rapidtube]" , match+"?start=0" ] )

    for video_url in video_urls:
        logger.info("[rapidtube.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos  = '(http://(?:\w+\.)?rapidtube.com/[a-zA-Z0-9]+)'
    logger.info("[rapidtube.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[rapidtube]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'rapidtube' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


    return devuelve