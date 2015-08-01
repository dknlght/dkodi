# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para allbox4
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import unpackerjs

def test_video_exists( page_url ):
    logger.info("[allbox4.py] test_video_exists(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)
    
    if ">Descarga lenta</a>" in data:
        return False,"El esquema de descarga no es compatible con pelisalacarta"
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[allbox4.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []

    # Descarga
    data = scrapertools.cache_page( page_url )

    try:
        paramstext = scrapertools.get_match( data , '<param name="flashvars" value="([^"]+)"')
        params = paramstext.split("&")

        file=""
        token=""
        start=""
        for param in params:
            if param.startswith("file="):
               file=param[5:] 
            if param.startswith("token="):
               token=param[6:] 
            if param.startswith("start="):
               start=param[6:] 
        
        media_url = file+"?"+start+"&"+token
    except:
        packed = scrapertools.get_match(data,"<div id=\"player_coded\">(<script type='text/javascript'>eval\(function\(p,a,c,k,e,d.*?</script>)</div>")
        from core import unpackerjs
        unpacked = unpackerjs.unpackjs(packed)
        logger.info("unpacked="+unpacked)
        media_url = scrapertools.get_match(unpacked,'<embed id="np_vid"type="video/divx"src="([^"]+)"')

    video_urls = []
    video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:] + " [allbox4]",media_url ] )

    for video_url in video_urls:
        logger.info("[allbox4.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://www.allbox4.com/embed-6szcvf0tv0s3.html
    patronvideos  = 'allbox4.com/([a-z0-9\-\.]+)'
    logger.info("[allbox4.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[allbox4]"

        url = "http://www.allbox4.com/"+match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'allbox4' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve