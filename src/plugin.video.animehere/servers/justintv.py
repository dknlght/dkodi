# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para justintv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
try:
    import json
except:
    import simplejson as json

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[justintv.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    
    channelname = scrapertools.get_match(page_url,"justin.tv/([_a-z0-9]+)")
    logger.info("channelname="+channelname)

    video_url = ""
    
    if page_url.startswith('rtmp'):
        video_url = page_url
    else:
        headers=[ ["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:14.0) Gecko/20100101 Firefox/14.0.1"] ]
        data = scrapertools.cache_page(page_url,headers=headers)
        logger.info("data="+data)
        match = re.compile('swfobject.embedSWF\("(.+?)"').findall(data)
        swf = ' swfUrl='+str(match[0])
        
        headers.append( ["Referer","http://justin.tv"] )
        data = scrapertools.cache_page('http://usher.justin.tv/find/'+channelname+'.json?type=live')
        logger.info("data="+data)
        datadict = json.loads(data)
        for entry in datadict:
            logger.info("entry="+str(entry))

        try:
            token = ' jtv='+datadict[0]["token"].replace('\\','\\5c').replace('"','\\22').replace(' ','\\20')
            connect = datadict[0]["connect"]+'/'+datadict[0]["play"]
            Pageurl = ' Pageurl=http://www.justin.tv/'+channelname
            video_url = connect+token+swf+Pageurl
        except:
            video_url=""

    logger.info("video_url="+video_url)

    if video_url!="":
        video_urls.append( [ "[justintv]" , video_url ] )

    for video_url in video_urls:
        logger.info("[justintv.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://www.justin.tv/cineplanet82
    patronvideos  = '(justin.tv/[_0-9a-z]+)'
    logger.info("[justintv.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        if match!="justin.tv/widgets":
            titulo = "[justintv]"
            url = "http://www."+match
            if url not in encontrados:
                logger.info("  url="+url)
                devuelve.append( [ titulo , url , 'justintv' ] )
                encontrados.add(url)
            else:
                logger.info("  url duplicada="+url)

    return devuelve
