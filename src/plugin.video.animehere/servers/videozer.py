# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videozer
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import os,re
import base64

from core import scrapertools
from core import logger
from core import config

HOSTER_KEY="MjE1Njc4"

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[videozer.py] get_video_url(page_url='%s')" % page_url)

    video_urls = []

    # Espera un poco como hace el player flash
    logger.info("[videobb.py] waiting 3 secs")
    import time
    time.sleep(3)

    # Obtiene el id
    code = Extract_id(page_url)
    if code == "":
        return []

    # Descarga el json con los detalles del vídeo
    controluri = "http://videozer.com/player_control/settings.php?v=%s&fv=v1.1.03"  %code
    datajson = scrapertools.cachePage(controluri)
    logger.info("response="+datajson);

    # Convierte el json en un diccionario
    datajson = datajson.replace("false","False").replace("true","True")
    datajson = datajson.replace("null","None")
    datadict = eval("("+datajson+")")
    
    # Formatos
    formatos = datadict["cfg"]["quality"]

    for formato in formatos:
        uri = base64.decodestring(formato["u"])

        import videobb
        video_url = videobb.build_url(uri,HOSTER_KEY,datajson)
        resolucion = formato["l"]
        video_urls.append( ["%s [videozer]" % resolucion , video_url , 5 ])

    for video_url in video_urls:
        logger.info("[videozer.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Extract video id from URL
def Extract_id(url):
    _VALID_URL = r'^((?:http://)?(?:\w+\.)?videozer\.com/(?:(?:e/|embed/|video/)|(?:(?:flash/|f/)))?)?([0-9A-Za-z_-]+)(?(1).+)?$'
    mobj = re.match(_VALID_URL, url)
    if mobj is None:
        logger.info('ERROR: URL invalida: %s' % url)
        
        return ""
    id = mobj.group(2)
    return id

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos  = "(http\:\/\/(?:www\.)?videozer.com\/(?:(?:e/|embed/|flash/)|(?:(?:video/|f/)))?[a-zA-Z0-9]{4,8})"
    logger.info("[videozer.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    #print data
    for match in matches:
        titulo = "[videozer]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'videozer' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve