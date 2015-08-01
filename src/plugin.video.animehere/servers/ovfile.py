# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para ovfile
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import unpackerjs

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[ovfile.py] url="+page_url)

    if page_url.startswith('http'):
        page_url = extract_id(page_url)
        if page_url=="":return []

    page_url = 'http://ovfile.com/embed-'+page_url+'-600x340.html'
    # Lo pide una vez
    data = scrapertools.cache_page( page_url)
    

    # Extrae el trozo cifrado
    patron = "src='http://ovfile.com/player/swfobject.js'></script>[^<]+"
    patron +="<script type='text/javascript'>(.*?)</script>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    data = ""
    if len(matches)>0:
        data = matches[0]
        logger.info("[ovfile.py] bloque packed="+data)
    else:
        logger.info("[ovfile.py] no encuentra bloque packed="+data)

        return ""
    
    # Lo descifra
    descifrado = unpackerjs.unpackjs(data)
    descifrado = descifrado.replace("\\'","'")
    # Extrae la URL del vídeo
    logger.info("descifrado="+descifrado)
    # Extrae la URL
    patron = "'file','([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(descifrado)
    scrapertools.printMatches(matches)
    
    video_urls = []
    
    if len(matches)>0:
        url = "%s?file=%s" %(matches[0],matches[0])
        video_urls.append( ["."+matches[0].rsplit('.',1)[1]+" [ovfile]",url])

    for video_url in video_urls:
        logger.info("[ovfile.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://www.peliculasaudiolatino.com/show/ovfile.php?url=3nzfd2cny8c1
    patronvideos  = 'ovfile\.php\?url=([A-Z0-9a-z]+)'
    logger.info("[ovfile.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[ovfile]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'ovfile' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    # http://www.ovfile.com/qya0qmf3k502
    patronvideos  = 'http://www.ovfile.com/([\w]+)'
    logger.info("[ovfile.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[ovfile]"
        url = "http://www.ovfile.com/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'ovfile' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://ovfile.com/embed-ijohcc1dvs5m-600x340.html
    patronvideos  = 'http://ovfile.com/embed-([\w]+)-600x340.html'
    logger.info("[ovfile.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[ovfile]"
        url = "http://www.ovfile.com/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'ovfile' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

def extract_id(url):
    return get_match(url, 'ovfile\.com/([\w]+)')

def get_match(data, regex) :
    match = "";
    m = re.search(regex, data)
    if m != None :
        match = m.group(1)
    return match