# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para allmyvideos
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import unpackerjs,unpackerjs3

def test_video_exists( page_url ):
    logger.info("[allmyvideos.py] test_video_exists(page_url='%s')" % page_url)

    # No existe / borrado: http://allmyvideos.net/8jcgbrzhujri
    data = scrapertools.cache_page(page_url)
    #logger.info("data="+data)
    if "<b>File Not Found</b>" in data or "<b>Archivo no encontrado</b>" in data or '<b class="err">Deleted' in data or '<b class="err">Removed' in data or '<font class="err">No such' in data:
        return False,"No existe o ha sido borrado de allmyvideos"
    else:
        # Existe: http://allmyvideos.net/6ltw8v1zaa7o
        patron  = '<META NAME="description" CONTENT="(Archivo para descargar[^"]+)">'
        matches = re.compile(patron,re.DOTALL).findall(data)
        
        if len(matches)>0:
            return True,""
    
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[allmyvideos.py] url="+page_url)
    
    # Lo pide una vez
    headers = [['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14']]
    data = scrapertools.cache_page( page_url , headers=headers )
    logger.info("data="+data)
    
    try:
        '''
        <input type="hidden" name="op" value="download1">
        <input type="hidden" name="usr_login" value="">
        <input type="hidden" name="id" value="d6fefkzvjc1z">
        <input type="hidden" name="fname" value="coriolanus.dvdr.mp4">
        <input type="hidden" name="referer" value="">
        <input type="hidden" name="method_free" value="1">
        <input type="image"  id="submitButton" src="/images/continue-to-video.png" value="method_free" />
        '''
        op = scrapertools.get_match(data,'<input type="hidden" name="op" value="([^"]+)"')
        usr_login = ""
        id = scrapertools.get_match(data,'<input type="hidden" name="id" value="([^"]+)"')
        fname = scrapertools.get_match(data,'<input type="hidden" name="fname" value="([^"]+)"')
        referer = scrapertools.get_match(data,'<input type="hidden" name="referer" value="([^"]*)"')
        method_free = scrapertools.get_match(data,'<input type="hidden" name="method_free" value="([^"]*)"')
        submitbutton = scrapertools.get_match(data,'<input type="image"  id="submitButton".*?value="([^"]+)"').replace(" ","+")
        
        import time
        time.sleep(10)
        
        # Lo pide una segunda vez, como si hubieras hecho click en el banner
        #op=download1&usr_login=&id=d6fefkzvjc1z&fname=coriolanus.dvdr.mp4&referer=&method_free=1&x=109&y=17
        post = "op="+op+"&usr_login="+usr_login+"&id="+id+"&fname="+fname+"&referer="+referer+"&method_free="+method_free+"&x=109&y=17"
        headers.append(["Referer",page_url])
        data = scrapertools.cache_page( page_url , post=post, headers=headers )
        logger.info("data="+data)
    except:
        pass
    
    # Extrae la URL
    media_url = scrapertools.get_match( data , '"file"\s*\:\s*"([^"]+)"' )+"?start=0"
    
    video_urls = []
    video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [allmyvideos]",media_url])

    for video_url in video_urls:
        logger.info("[allmyvideos.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://allmyvideos.net/embed-d6fefkzvjc1z.html 
    patronvideos  = 'allmyvideos.net/embed-([a-z0-9]+)'
    logger.info("[allmyvideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[allmyvideos]"
        url = "http://allmyvideos.net/"+match
        if url not in encontrados and url!="http://allmyvideos.net/embed":
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'allmyvideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://allmyvideos.net/6lgjjav5cymi
    patronvideos  = 'allmyvideos.net/([a-z0-9]+)'
    logger.info("[allmyvideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[allmyvideos]"
        url = "http://allmyvideos.net/"+match
        if url not in encontrados and not url.startswith("embed"):
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'allmyvideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://www.cinetux.org/video/allmyvideos.php?id=gntpo9m3mifj
    patronvideos  = 'allmyvideos.php\?id\=([a-z0-9]+)'
    logger.info("[allmyvideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[allmyvideos]"
        url = "http://allmyvideos.net/"+match
        if url not in encontrados and not url.startswith("embed"):
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'allmyvideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


    return devuelve

def test():

    video_urls = get_video_url("http://allmyvideos.net/6lgjjav5cymi")

    return len(video_urls)>0