# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para rapidvideo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:18.0) Gecko/20100101 Firefox/18.0"

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[rapidvideo.py] url="+page_url)
    video_urls=[]

    data = scrapertools.cache_page(page_url)
    data = scrapertools.get_match(data,'<div style="text-align:center; font-family: arial; font-size:11px; line-height:20px; border-bottom:1px solid #333; color:#FFF;">Quality<br/></div>(.*?)</div></div>')

    patron  = "<div.*?jw_set\('([^']+)'[^>]+>(.*?)<br/></div>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)==0: return []

    for url,quality in matches:
        video_urls.append( [ scrapertools.get_filename_from_url(url)[-4:]+" ["+scrapertools.htmlclean(quality).strip()+"][rapidvideo]",url+"?start=0"] )

    for video_url in video_urls:
        logger.info("[rapidvideo.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []
            
    # http://www.rapidvideo.com/embed/sy6wen17
    patronvideos  = 'rapidvideo.com/embed/([A-Za-z0-9]+)'
    logger.info("[rapidvideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[rapidvideo]"
        url = "http://www.rapidvideo.com/view/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'rapidvideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://www.rapidvideo.com/view/YK7A0L7FU3A
    patronvideos  = 'rapidvideo.com/view/([A-Za-z0-9]+)'
    logger.info("[rapidvideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[rapidvideo]"
        url = "http://www.rapidvideo.com/view/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'rapidvideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


    return devuelve

def test():

    video_urls = get_video_url("http://www.rapidvideo.com/embed/sy6wen17")

    return len(video_urls)>0