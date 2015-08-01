# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para jumbofiles
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[jumbofiles.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []

    data = scrapertools.cache_page(page_url)
    
    # op=download2&id=oiyetnk5vwzf&rand=m2080mem&referer=&method_free=&method_premium=&down_direct=1&x=64&y=5
    op = scrapertools.get_match(data,'<input type="hidden" name="op" value="([^"]+)">')
    id = scrapertools.get_match(data,'<input type="hidden" name="id" value="([^"]+)">')
    random_number = scrapertools.get_match(data,'<input type="hidden" name="rand" value="([^"]+)">')
    down_direct = scrapertools.get_match(data,'<input type="hidden" name="down_direct" value="([^"]+)">')

    post = "op=%s&id=%s&rand=%s&referer=&method_free=&method_premium=&down_direct=%s&x=64&y=5" % (op,id,random_number,down_direct)
    data = scrapertools.cache_page(page_url,post=post)
    #logger.info("data="+data)

    #<FORM METHOD="LINK" ACTION="http://www96.jumbofiles.com:443/d/jbswjaebcr4eam62sd6ue2bb47yo6ldj5pcbc6wed6qteh73vjzcu/ORNE.avi">
    video_url = scrapertools.get_match(data,'<FORM METHOD="LINK" ACTION="([^"]+)">')
    video_urls.append( [ video_url[-4:]+" [jumbofiles]" , video_url ] )

    for video_url in video_urls:
        logger.info("[jumbofiles.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://jumbofiles.com/oiyetnk5vwzf
    patronvideos  = '(http://jumbofiles.com/[0-9a-z]+)'
    logger.info("[jumbofiles.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[jumbofiles]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'jumbofiles' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
