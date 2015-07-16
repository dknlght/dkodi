# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para gigabyteupload
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re

from core import scrapertools
from core import logger
from core import config
from core import unpackerjs2

import os

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[gigabyteupload.py] get_video_url(page_url='%s')" % page_url)

    video_urls = []

    # Lo pide una vez
    data = scrapertools.cache_page( page_url , headers=[['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14']] )
    
    # Extrae los parámetros
    patron = 'http\:\/\/www\.gigabyteupload\.com/download\-([a-z0-9]+)'
    matches = re.compile(patron,re.DOTALL).findall(page_url)
    id = matches[0]
    logger.info("[gigabyteupload.py] id="+id)

    patron  = '<form method="post" action="([^"]+)">[^<]+<input type="hidden" name="security_key" value="([^"]+)" \/>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    security_key=matches[0][1]
    logger.info("[gigabyteupload.py] security_key="+security_key)

    url2 = matches[0][0]
    logger.info("[gigabyteupload.py] url2="+url2)

    # Carga el descriptor
    #post = "op=download&usr_login=&id="+id+"&security_key="+security_key+"&submit="+submit+"&aff=&came_from=referer=&method_free=Free+Stream"
    post = "security_key="+security_key+"&submit=Watch+Online"
    data = scrapertools.cache_page( url2 , post=post, headers=[['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14']] )
    #logger.info(data)
    
    # Extrae el trozo cifrado
    patron = '<div id="player">.*?<script type="text/javascript">(eval.*?)</script>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    data = ""
    if len(matches)>0:
        data = matches[0]
        logger.info("[Gigabyteupload.py] bloque packed="+data)
    else:
        return ""
    
    # Lo descifra
    descifrado = unpackerjs2.unpackjs(data)
    logger.info("descifrado="+descifrado)
    
    # Extrae la URL del vídeo
    # so.addVariable(\'file\',\'http://B.gigabyteupload.com/files/9333438c9df831298d484459278b6938/4e4bc759/gigabyteupload/7ba04b5fb538223.flv\')
    descifrado = descifrado.replace("\\","")
    logger.info("descifrado="+descifrado)
    # so.addVariable('file','http://B.gigabyteupload.com/files/9333438c9df831298d484459278b6938/4e4bc759/gigabyteupload/7ba04b5fb538223.flv')
    patron = "so.addVariable\('file','([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(descifrado)
    scrapertools.printMatches(matches)
    
    url = ""
    
    try:
        video_urls.append( [ "[gigabyteupload]" , matches[0].replace("B.gigabyteupload.com","ggu4.gigabyteupload.com")+"?start=0" ] )
    except:
        pass

    for video_url in video_urls:
        logger.info("[gigabyteupload.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls


# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos = '<a href="(http://www.gigabyteupload.com/[^"]+)"'
    logger.info("[gigabyteupload.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[gigabyteupload]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'gigabyteupload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve