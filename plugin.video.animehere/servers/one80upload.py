# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para 180upload
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    
    data = scrapertools.cache_page(page_url)
    
    if "<b>File Not Found" in data:
        return False,"El fichero ha sido borrado"
    
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[one80upload.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []

    data = scrapertools.cache_page(page_url)

    #op=download2&id=yz6lx411cshb&rand=3wqqg6mjw3nxu254dfw4icuxknqfkzdjnbluhty&referer=&method_free=&method_premium=&down_direct=1
    codigo = scrapertools.get_match(data,'<input type="hidden" name="id" value="([^"]+)">[^<]+')
    rand = scrapertools.get_match(data,'<input type="hidden" name="rand" value="([^"]+)">')
    post = "op=download2&id="+codigo+"&rand="+rand+"&referer=&method_free=&method_premium=&down_direct=1"

    data = scrapertools.cache_page( page_url , post=post, headers=[['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'],['Referer',page_url]] )
    #logger.info("data="+data)

    # Busca el video online o archivo de descarga
    patron = 'href="([^"]+)" target="_parent"><span class="style1">Download'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)

    if len(matches)>0:
        logger.info("[180upload.py] encuentra archivo de descarga="+matches[0])
    else:
        logger.info("[180upload.py] buscando video para ver online")
        patron = "this\.play\('([^']+)'"
        matches = re.compile(patron,re.DOTALL).findall(data)
        

    if len(matches)>0:
        video_urls.append( ["."+matches[0].rsplit('.',1)[1]+" [180upload]",matches[0]])

    for video_url in video_urls:
        logger.info("[180upload.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    #http://180upload.com/embed-6z7cwbswemsv.html
    data = urllib.unquote(data)
    patronvideos  = '180upload.com/embed-([a-z0-9]+)\.html'
    logger.info("[one80upload.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[180upload]"
        url = "http://180upload.com/"+match
        if url not in encontrados and match!="embed":
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'one80upload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://180upload.com/rtp8y30mlfj0
    #http%3A%2F%2F180upload.com%2F5k344aiotajv
    data = urllib.unquote(data)
    patronvideos  = '180upload.com/([a-z0-9]+)'
    logger.info("[one80upload.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[180upload]"
        url = "http://180upload.com/"+match
        if url not in encontrados and match!="embed":
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'one80upload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

def test():
    video_urls = get_video_url("http://180upload.com/98bpne5grck6")

    return len(video_urls)>0