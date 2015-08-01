# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para nosvideo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    logger.info("[nosvideo.py] test_video_exists(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)
    
    if "The file is being converted" in data:
        return False,"El fichero está en proceso"

    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[nosvideo.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    
    # Lee la URL
    data = scrapertools.cache_page( page_url )
    bloque = scrapertools.get_match(data,'<Form method="POST"(.*)</.orm>')
    #logger.info("bloque="+bloque)
    op = scrapertools.get_match(bloque,'<input type="hidden" name="op" value="([^"]+)"')
    id = scrapertools.get_match(bloque,'<input type="hidden" name="id" value="([^"]+)"')
    rand = scrapertools.get_match(bloque,'<input type="hidden" name="rand" value="([^"]*)"')
    referer = scrapertools.get_match(bloque,'<input type="hidden" name="referer" value="([^"]*)"')
    usr_login = scrapertools.get_match(bloque,'<input type="hidden" name="usr_login" value="([^"]*)"')
    fname = scrapertools.get_match(bloque,'<input type="hidden" name="fname" value="([^"]+)"')
    method_free = scrapertools.get_match(bloque,'<input type="[^"]+" name="method_free" value="([^"]*)"')
    method_premium = scrapertools.get_match(bloque,'<input type="[^"]+" name="method_premium" value="([^"]*)"')

    # Simula el botón
    #op=download1&id=iij5rw25kh4c&rand=&referer=&usr_login=&fname=TED-TS-Screener.Castellano.Ro_dri.avi&method_free=&method_premium=&down_script=1&method_free=Continue+to+Video
    post = "op="+op+"&id="+id+"&rand="+rand+"&referer="+referer+"&usr_login="+usr_login+"&fname="+fname+"&method_free=&method_premium="+method_premium+"&down_script=1&method_free="+method_free
    data = scrapertools.cache_page( page_url , post=post )
    #logger.info("data="+data)

    # Saca el bloque packed y lo descifra
    packed = scrapertools.get_match(data,"(<script type='text/javascript'>eval\(function\(p,a,c,k,e,d\).*?</script>)")
    from core import unpackerjs
    unpacked = unpackerjs.unpackjs(packed)
    logger.info("unpacked="+unpacked)
    
    # Extrae el descriptor
    playlist = scrapertools.get_match(unpacked,"playlist\=(.*?\.xml)")
    data = scrapertools.cache_page( playlist )
    location = scrapertools.get_match(data,"<file>([^<]+)</file>")
    
    video_urls.append( [ scrapertools.get_filename_from_url(location)[-4:] + " [nosvideo]",location ] )

    for video_url in video_urls:
        logger.info("[nosvideo.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    #http://nosvideo.com/?v=iij5rw25kh4c
    patronvideos  = '(nosvideo.com/\?v\=[a-z0-9]+)'
    logger.info("[nosvideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[nosvideo]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'nosvideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://nosupload.com/?v=iij5rw25kh4c
    patronvideos  = 'nosupload.com(/\?v\=[a-z0-9]+)'
    logger.info("[nosvideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[nosvideo]"
        url = "http://nosvideo.com"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'nosvideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve


def test():

    video_urls = get_video_url("http://nosvideo.com/?v=zuxl97lozqmp")

    return len(video_urls)>0