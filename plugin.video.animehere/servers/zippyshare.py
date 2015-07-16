# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para zippyshare
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
    logger.info("[zippyshare.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []

    headers=[]
    headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:19.0) Gecko/20100101 Firefox/19.0"])

    data = scrapertools.cache_page(page_url,headers=headers)

    location = scrapertools.get_match(data,"var submitCaptcha.*?document.location \= '([^']+)'")
    mediaurl = urlparse.urljoin(page_url,location)+"|"+urllib.urlencode({'Referer' : page_url})

    extension = scrapertools.get_filename_from_url(mediaurl)[-4:]
    
    video_urls.append( [ extension + " [zippyshare]",mediaurl ] )

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    #http://www5.zippyshare.com/v/11178679/file.html
    patronvideos  = '([a-z0-9]+\.zippyshare.com/v/\d+/file.html)'
    logger.info("[zippyshare.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[zippyshare]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'zippyshare' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

def test():
    video_urls = get_video_url("http://www5.zippyshare.com/v/11178679/file.html")
    return len(video_urls)>0