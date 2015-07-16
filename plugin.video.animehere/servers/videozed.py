# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videozed
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import unpackerjs

def test_video_exists( page_url ):
    logger.info("[videozed.py] test_video_exists(page_url='%s')" % page_url)

    data = scrapertools.cache_page( url = page_url )
    if "<h1>File Not Found</h1>" in data:
        return False,"El archivo no existe<br/>en videozed o ha sido borrado."
    else:
        return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[videozed.py] url="+page_url)
    
    # Lo pide una vez
    headers = [['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14']]
    data = scrapertools.cache_page( page_url , headers=headers )
    logger.info("data="+data)
    
    '''
    <input type="hidden" name="op" value="download1">
    <input type="hidden" name="usr_login" value="">
    <input type="hidden" name="id" value="t9pxgc69j56f">
    <input type="hidden" name="fname" value="Hobbit.DVDS.900.RD.avi">
    <input type="hidden" name="referer" value="">
    <input type="submit" name="method_free"  value="Continue to Video">
    '''
    op = scrapertools.get_match(data,'<input type="hidden" name="op" value="([^"]+)"')
    usr_login = ""
    id = scrapertools.get_match(data,'<input type="hidden" name="id" value="([^"]+)"')
    fname = scrapertools.get_match(data,'<input type="hidden" name="fname" value="([^"]+)"')
    referer = scrapertools.get_match(data,'<input type="hidden" name="referer" value="([^"]*)"')
    method_free = scrapertools.get_match(data,'<input type="submit" name="method_free"\s+value="([^"]*)"')
    
    import time
    time.sleep(10)
    
    # Lo pide una segunda vez, como si hubieras hecho click en el banner
    #op=download1&usr_login=&id=d6fefkzvjc1z&fname=coriolanus.dvdr.mp4&referer=&method_free=1&x=109&y=17
    post = "op="+op+"&usr_login="+usr_login+"&id="+id+"&fname="+fname+"&referer="+referer+"&method_free="+method_free+"&x=109&y=17"
    headers.append(["Referer",page_url])
    data = scrapertools.cache_page( page_url , post=post, headers=headers )
    logger.info("data="+data)
    
    # Extrae la URL
    media_url = scrapertools.get_match( data , '"file"\s*\:\s*"([^"]+)"' )+"?start=0"
    
    video_urls = []
    video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [videozed]",media_url])

    for video_url in video_urls:
        logger.info("[videozed.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://videozed.net/t9pxgc69j56f
    patronvideos  = '(videozed.net/[a-z0-9]+)'
    logger.info("[videozed.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[videozed]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'videozed' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

def test():
    video_urls = get_video_url("http://videozed.net/t9pxgc69j56f")

    return len(video_urls)>0