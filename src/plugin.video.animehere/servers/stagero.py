# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para stagero
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[stagero.py] get_video_url(page_url='%s')" % page_url)
    
    data = scrapertools.cache_page( page_url )
    patron = 'flashvars.filekey="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    key = matches[0]
    logger.info("key="+key)
    key = key.replace(".","%2E").replace("-","%2D")
    #83%2E39%2E140%2E15%2D3d72dd9c74a6df9dc282e10ae8817313
    logger.info("key="+key)
    
    patron = 'http://www.stagero.eu/video/([0-9a-z]+)'
    matches = re.compile(patron,re.DOTALL).findall(page_url)
    code = matches[0]
    logger.info("code="+code)
    
    url = "http://www.stagero.eu/api/player.api.php?file="+code+"&codes=1&pass=undefined&user=undefined&key="+key
    data = scrapertools.cache_page( url )
    logger.info("data="+data)
    
    #url=http://f41.stagero.eu/dl/efdaa7087c9b948dcc082c228f0a959d/4f24137f/ff4e38fd834627d5cc0739beec8d80a847.flv&title=Il.Sentiero.2010.iTALiAN.MD.DVDRip.XviDTNZ.avi%26asdasdas&site_url=http://www.stagero.eu/video/dfb39de9eaf03&seekparm=&enablelimit=0
    patron = 'url\=([^\&]+)\&'
    matches = re.compile(patron,re.DOTALL).findall(data)
    media_url = matches[0]+"?client=FLASH"
    logger.info("media_url="+media_url)
    #http://f43.stagero.eu/dl/3fed06657028c2c0c957e1afce521a29/4f2412f3/ff4e38fd834627d5cc0739beec8d80a847.flv?client=FLASH


    video_urls = []
    video_urls.append( [ "[stagero]" , media_url ] )

    for video_url in video_urls:
        logger.info("[stagero.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://www.stagero.eu/video/dfb39de9eaf03
    patronvideos  = '(http://www.stagero.eu/video/[0-9a-z]+)'
    logger.info("[stagero.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[stagero]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'stagero' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
