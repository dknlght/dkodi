# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para bliptv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import re
import urllib

from core import scrapertools
from core import logger

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="" , video_password="" ):
    logger.info("[bliptv.py] get_video_url(page_url='%s')" % page_url)

    video_urls = []

    if page_url.startswith("http://blip.tv/play"):    
        redirect = scrapertools.get_header_from_response(page_url,header_to_get="location")
        logger.info("[bliptv.py] redirect="+redirect)
        
        patron='file\=(.*?)$'
        matches = re.compile(patron).findall(redirect)
        logger.info("[bliptv.py] matches1=%d" % len(matches))
        
        if len(matches)==0:
            patron='file\=([^\&]+)\&'
            matches = re.compile(patron).findall(redirect)
            logger.info("[bliptv.py] matches2=%d" % len(matches))
        
        if len(matches)>0:
            url = matches[0]
            logger.info("[bliptv.py] url="+url)
            url = urllib.unquote(url)
            logger.info("[bliptv.py] url="+url)

            data = scrapertools.cache_page(url)
            logger.info(data)
            patron = '<media\:content url\="([^"]+)" blip\:role="([^"]+)".*?type="([^"]+)"[^>]+>'
            matches = re.compile(patron).findall(data)
            scrapertools.printMatches(matches)

            for match in matches:
                video_url = ["%s [blip.tv]" % match[1] , match[0]]
                video_urls.append( video_url )

    for video_url in video_urls:
        logger.info("[bliptv.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # Código embed de Blip.tv
    patronvideos  = '(http://blip.tv/play/[A-Z0-9a-z]+.html)'
    logger.info("[bliptv.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[blip.tv]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'bliptv' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve