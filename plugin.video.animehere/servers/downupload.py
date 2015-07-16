# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videos externos de downupload
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import unpackerjs

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[downupload.py] get_video_url(page_url='%s')" % page_url)

    page_url = page_url.replace("amp;","")
    data = scrapertools.cache_page(page_url)
    
    video_urls = []

    # s1.addVariable('file','http://78.140.181.136:182/d/kka3sx52abiuphevyzfirfaqtihgyq5xlvblnetok2mj4llocdeturoy/video.mp4');
    # http://downupload.com:182/d/k2a3kxf2abiuphevyzfirgajremkk3if57xcpelwboz4hbzjnfsvbit6/video.mp4
    patron  = "(http://[\S]+\.mp4)" 
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    if len(matches)>0:
        scrapertools.printMatches(matches)
        for match in matches:
            videourl = match
            videourl = videourl.replace('%5C','')
            videourl = urllib.unquote(videourl)
            video_urls.append( [ ".mp4 [Downupload]" , videourl ] )
            
    else:
        # Si es un enlace de Descarga se busca el archivo
        patron  = '<div id="player_code">.*?value[\W]name[\W]param[\W]com[\W]http[\W]false[\W](.*?)[\W]divx[\W]previewImage[\W].*?[\W]custommode[\W](.*?)[\W](.*?)[\W](.*?)[\W]src'
        matches = re.compile(patron,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)
        for match in matches:
            videourl = "http://"+match[0]+".com:"+match[3]+"/d/"+match[2]+"/video."+match[1]
            videourl = videourl.replace('|','.')
            videourl = urllib.unquote(videourl)
            video_urls.append( [ "."+match[1]+" [Downupload]" , videourl ] )
            
        # Localiza enlaces con IP
        if len(matches)==0:
            patron  = '<div id="player_code">.*?value[\W]name[\W]param[\W]http[\W]false[\W](.*?)[\W](.*?)[\W](.*?)[\W](.*?)[\W]divx[\W]previewImage[\W].*?[\W]custommode[\W](.*?)[\W](.*?)[\W](.*?)[\W]src'
            matches = re.compile(patron,re.DOTALL).findall(data)
            scrapertools.printMatches(matches)
            for match in matches:
                videourl = "http://"+match[3]+"."+match[2]+"."+match[1]+"."+match[0]+":"+match[6]+"/d/"+match[5]+"/video."+match[4]
                videourl = videourl.replace('|','')
                videourl = urllib.unquote(videourl)
                video_urls.append( [ "."+match[4]+" [Downupload]" , videourl ] )
            # Otro metodo de busqueda
            if len(matches)==0:
                url = unpackerjs.unpackjs(data)
                logger.info("[unpackerjs.py] "+url)
                patron = 'src"value="([^"]+)"'
                matches = re.compile(patron,re.DOTALL).findall(url)
                for match in matches:                  
                    videourl = match
                    videourl = videourl.replace('|','')
                    videourl = urllib.unquote(videourl)
                    video_urls.append( [ "."+videourl.rsplit('.',1)[1]+" [Downupload]" , videourl ] )                  
                    
                

    for video_url in video_urls:
        logger.info("[downupload.py] %s - %s" % (video_url[0],video_url[1]))
        
    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # Downupload http://www.downupload.com/embed-p9oenzlz6xhu.html
    patronvideos  = '(downupload.com/embed-.*?\.html)'
    logger.info("[downupload.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Downupload]"
        url = "http://www."+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'downupload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # Enlaces de Descarga
    if len(matches)==0:
        patronvideos  = '(downupload.com/[\w]+)'
        logger.info("[downupload.py] find_videos #"+patronvideos+"#")
        matches = re.compile(patronvideos,re.DOTALL).findall(data)

        for match in matches:
            titulo = "[Downupload]"
            url = match.replace("downupload.com/","http://www.downupload.com/embed-")
            url = url+".html"
            if url not in encontrados:
                logger.info("  url="+url)
                devuelve.append( [ titulo , url , 'downupload' ] )
                encontrados.add(url)
            else:
                logger.info("  url duplicada="+url)    
            
    return devuelve
