# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para twitvid
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[twitvid.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    
    # Lee la página del player
    data = scrapertools.cache_page(page_url)
    logger.info("data="+data)
    url = scrapertools.get_match(data,'video_path="([^"]+)"')
    logger.info("url="+url)
    import urlparse
    url = urlparse.urljoin( page_url, url )
    location = scrapertools.get_header_from_response(url,header_to_get="location")
    
    video_urls.append( [ scrapertools.get_filename_from_url(location)[-4:]+" [twitvid]",location ] )
    
    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    #http://www.twitvid.com/embed.php?guid=ILHLI
    patronvideos  = 'twitvid.com/embed.php\?guid=([A-Z0-9]+)'
    logger.info("[twitvid.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[twitvid]"
        url = "http://www.telly.com/"+match+"?fromtwitvid=1"
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'twitvid' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

def test():
    video_urls = get_video_url("http://www.telly.com/0DN7PH?fromtwitvid=1")

    return len(video_urls)>0