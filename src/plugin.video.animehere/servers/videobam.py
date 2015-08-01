# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videos externos de videobam
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    logger.info("[videobam.py] test_video_exists(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)
    
    if "Video is processing" in data:
        return False,"El fichero está en proceso"

    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[videobam.py] get_video_url(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)

    video_urls = []
    
    patronSD= " low: '([^']+)'" 
    matches = re.compile(patronSD,re.DOTALL).findall(data)
    for match in matches:
        videourl = match
        video_urls.append( [ "LQ [videobam]" , videourl ] )
        
    patronHD = " high: '([^']+)'"
    matches = re.compile(patronHD,re.DOTALL).findall(data)
    for match in matches:
        videourl = match
        video_urls.append( [ "HQ [videobam]" , videourl ] )

    if len(matches)==0:
        # "scaling":"fit","url":"http:\/\/f10.videobam.com\/storage\/11\/videos\/a\/aa\/AaUsV\/encoded.mp4
        
        patron = '[\W]scaling[\W]:[\W]fit[\W],[\W]url"\:"([^"]+)"'
        matches = re.compile(patron,re.DOTALL).findall(data)
        for match in matches:
            videourl = match.replace('\/','/')
            videourl = urllib.unquote(videourl)
            video_urls.append( [ ".mp4 [videobam]" , videourl ] )
        

    for video_url in video_urls:
        logger.info("[videobam.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # VideoBam para AnimeID    src="http://videobam.com/widget/USezW"
    # VideoBam custom    src="http://videobam.com/widget/USezW/custom/568"
    patronvideos  = 'http://videobam.com/widget/([\w]+)'
    logger.info("[videobam.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[videobam]"
        url = "http://videobam.com/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'videobam' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://videobam.com/fsgUt
    patronvideos  = 'http://videobam.com/([\w]+)'
    logger.info("[videobam.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[videobam]"
        url = "http://videobam.com/"+match
        if not match.startswith("videos"):
            if url not in encontrados and url!="http://videobam.com/widget":
                logger.info("  url="+url)
                devuelve.append( [ titulo , url , 'videobam' ] )
                encontrados.add(url)
            else:
                logger.info("  url duplicada="+url)

    return devuelve

def test():
    video_urls = get_video_url("http://videobam.com/enant")

    return len(video_urls)>0