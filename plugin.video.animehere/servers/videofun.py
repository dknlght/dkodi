# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para allmyvideos
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import unpackerjs,unpackerjs3

def test_video_exists( page_url ):
    logger.info("[videofun.py] test_video_exists(page_url='%s')" % page_url)

    # No existe / borrado: http://allmyvideos.net/8jcgbrzhujri
    data = scrapertools.cache_page(page_url)
    #logger.info("data="+data)
    if "<b>File Not Found</b>" in data or "<b>Archivo no encontrado</b>" in data or '<b class="err">Deleted' in data or '<b class="err">Removed' in data or '<font class="err">No such' in data:
        return False,"No existe o ha sido borrado de allmyvideos"
    else:
        # Existe: http://allmyvideos.net/6ltw8v1zaa7o
        patron  = '<META NAME="description" CONTENT="(Archivo para descargar[^"]+)">'
        matches = re.compile(patron,re.DOTALL).findall(data)
        
        if len(matches)>0:
            return True,""
    
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[videofun.py] url="+page_url)
    
    # Lo pide una vez
    headers = [['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14']]
    data = scrapertools.cache_page( page_url , headers=headers )
    data=''.join(data.splitlines()).replace('\'','"')
    media_url= ""
    op = scrapertools.get_match(data,'playlist:\s*\[(.+?)\]')
    urls=op.split("{")
    for rows in urls:
        if(rows.find("url") > -1):
             murl= scrapertools.get_match(rows,'url:\s*"(.+?)"')
             media_url=urllib.unquote_plus(murl)
    video_urls = []
    video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [videofun]",media_url])

    for video_url in video_urls:
        logger.info("[allmyvideos.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

def test():

    video_urls = get_video_url("http://allmyvideos.net/6lgjjav5cymi")

    return len(video_urls)>0