# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para moevideos
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import unpackerjs

def test_video_exists( page_url ):
    logger.info("[moevideos.py] test_video_exists(page_url='%s')" % page_url)

    # Si es el código embed directamente, no se puede comprobar
    if "video.php" in page_url:
        return True,""

    # No existe / borrado: http://www.moevideos.net/online/27991
    data = scrapertools.cache_page(page_url)
    #logger.info("data="+data)
    if "<span class='tabular'>No existe</span>" in data:
        return False,"No existe o ha sido borrado de moevideos"
    else:
        # Existe: http://www.moevideos.net/online/18998
        patron  = "<span class='tabular'>([^>]+)</span>"
        matches = re.compile(patron,re.DOTALL).findall(data)
        
        if len(matches)>0:
            return True,""
    
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[moevideos.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []

    if page_url.startswith("http://www.moevideos.net/online"):
        headers = []
        headers.append(['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'])
        data = scrapertools.cache_page( page_url , headers=headers )
            
        # Descarga el script (no sirve para nada, excepto las cookies)
        headers.append(['Referer',page_url])
        post = "id=1&enviar2=ver+video"
        data = scrapertools.cache_page( page_url , post=post, headers=headers )
        code = scrapertools.get_match(data,'flashvars\="file\=([^"]+)"')
        logger.info("code="+code)
    else:
        #http://moevideo.net/?page=video&uid=81492.8c7b6086f4942341aa1b78fb92df
        code = scrapertools.get_match(page_url,"uid=([a-z0-9\.]+)")

    # API de letitbit
    headers2 = []
    headers2.append(['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'])
    #url = "http://api.letitbit.net"
    url = "http://api.moevideo.net"
    #post = "r=%5B%22tVL0gjqo5%22%2C%5B%22preview%2Fflv%5Fimage%22%2C%7B%22uid%22%3A%2272871%2E71f6541e64b0eda8da727a79424d%22%7D%5D%2C%5B%22preview%2Fflv%5Flink%22%2C%7B%22uid%22%3A%2272871%2E71f6541e64b0eda8da727a79424d%22%7D%5D%5D"
    #post = "r=%5B%22tVL0gjqo5%22%2C%5B%22preview%2Fflv%5Fimage%22%2C%7B%22uid%22%3A%2212110%2E1424270cc192f8856e07d5ba179d%22%7D%5D%2C%5B%22preview%2Fflv%5Flink%22%2C%7B%22uid%22%3A%2212110%2E1424270cc192f8856e07d5ba179d%22%7D%5D%5D
    #post = "r=%5B%22tVL0gjqo5%22%2C%5B%22preview%2Fflv%5Fimage%22%2C%7B%22uid%22%3A%2268653%2E669cbb12a3b9ebee43ce14425d9e%22%7D%5D%2C%5B%22preview%2Fflv%5Flink%22%2C%7B%22uid%22%3A%2268653%2E669cbb12a3b9ebee43ce14425d9e%22%7D%5D%5D"
    post = 'r=["tVL0gjqo5",["preview/flv_image",{"uid":"'+code+'"}],["preview/flv_link",{"uid":"'+code+'"}]]'
    data = scrapertools.cache_page(url,headers=headers2,post=post)
    logger.info("data="+data)
    if ',"not_found"' in data:
        return []
    data = data.replace("\\","")
    logger.info("data="+data)
    patron = '"link"\:"([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    video_url = matches[0]+"?ref=www.moevideos.net|User-Agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:15.0) Gecko/20100101 Firefox/15.0.1&Range=bytes:0-"
    logger.info("[moevideos.py] video_url="+video_url)

    video_urls = []
    video_urls.append( [ scrapertools.get_filename_from_url(video_url)[-4:] + " [moevideos]",video_url ] )

    for video_url in video_urls:
        logger.info("[moevideos.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://www.moevideos.net/online/18998
    patronvideos  = 'moevideos.net/online/(\d+)'
    logger.info("[moevideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[moevideos]"
        url = "http://www.moevideos.net/online/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'moevideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://www.moevideos.net/view/30086
    patronvideos  = 'moevideos.net/view/(\d+)'
    logger.info("[moevideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[moevideos]"
        url = "http://www.moevideos.net/online/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'moevideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://moevideo.net/video.php?file=71845.7a9a6d72d6133bb7860375b63f0e&width=600&height=450
    patronvideos  = 'moevideo.net/video.php\?file\=([a-z0-9\.]+)'
    logger.info("[moevideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[moevideos]"
        url = "http://moevideo.net/?page=video&uid="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'moevideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://www2.cinetux.org/moevideo.php?id=20671.29b19bfe3cfcf1c203816a78d1e8
    patronvideos  = 'cinetux.org/moevideo.php\?id\=([a-z0-9\.]+)'
    logger.info("[moevideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[moevideos]"
        url = "http://moevideo.net/?page=video&uid="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'moevideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    #http://moevideo.net/?page=video&uid=81492.8c7b6086f4942341aa1b78fb92df
    patronvideos  = 'moevideo.net/\?page\=video\&uid=([a-z0-9\.]+)'
    logger.info("[moevideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[moevideos]"
        url = "http://moevideo.net/?page=video&uid="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'moevideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://moevideo.net/framevideo/95250.9c5a5f9faea7207a842d609e4913
    patronvideos  = 'moevideo.net/framevideo/([a-z0-9\.]+)'
    logger.info("[moevideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[moevideos]"
        url = "http://moevideo.net/?page=video&uid="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'moevideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


    #http://moevideo.net/swf/letplayerflx3.swf?file=23885.2b0a98945f7aa37acd1d6a0e9713
    patronvideos  = 'moevideo.net/swf/letplayerflx3.swf\?file\=([a-z0-9\.]+)'
    logger.info("[moevideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[moevideos]"
        url = "http://moevideo.net/?page=video&uid="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'moevideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

def test():
    video_urls = get_video_url("http://www.moevideos.net/online/164016")
    video_urls = get_video_url("http://moevideo.net/?page=video&uid=60823.6717786f74cd87a6cbeeb8c9e48d")

    return len(video_urls)>0