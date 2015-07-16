# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para upafile
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import unpackerjs

def test_video_exists( page_url ):
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[upafile.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []

    data = scrapertools.cache_page(page_url)
    #<script type='text/javascript'>eval(function(p,a,c,k,e,d){while(c--)if(k[c])p=p.replace(new RegExp('\\b'+c.toString(a)+'\\b','g'),k[c]);return p}('11 0=10 z(\'2://4.3/6/6.y\',\'6\',\'x\',\'w\',\'9\');0.5(\'v\',\'u\');0.5(\'t\',\'s\');0.5(\'r\',\'q\');0.1(\'p\',\'\');0.1(\'o\',\'2://a.4.3:n/d/m/8.l\');0.1(\'k\',\'2://a.4.3/i/j/h.g\');0.1(\'7\',\'8\');0.1(\'7\',\'2\');0.1(\'2.f\',\'e\');0.c(\'b\');',36,38,'s1|addVariable|http|com|upafile|addParam|player|provider|video||s82|flvplayer|write||start|startparam|jpg|idyoybh552bf||00024|image|mp4|k65ufdsgg7pvam5r5o22urriqvsqzkkf4cu3biws2xwxsvgmrfmjyfbz|182|file|duration|opaque|wmode|always|allowscriptaccess|true|allowfullscreen|400|500|swf|SWFObject|new|var'.split('|')))
    patron = "<script type='text/javascript'>(eval\(function\(p,a,c,k,e,d\).*?)</script>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    cifrado=""
    for match in matches:
        logger.info("match="+match)
        if "mp4" in match or "flv" in match or "video" in match:
            cifrado = match
            break
    
    # Extrae la URL del vídeo
    logger.info("cifrado="+cifrado)
    descifrado = unpackerjs.unpackjs(cifrado)
    descifrado = descifrado.replace("\\","")
    logger.info("descifrado="+descifrado)

    #s1.addVariable('file','http://s82.upafile.com:182/d/k65ufdsgg7pvam5r5o22urriqvsqzkkf4cu3biws2xwxsvgmrfkxwzx4/video.mp4')
    media_url = scrapertools.get_match(descifrado,"addVariable\('file','([^']+)'")
    
    if len(matches)>0:
        video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [upafile]",media_url])

    for video_url in video_urls:
        logger.info("[upafile.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    #http://upafile.com/idyoybh552bf
    data = urllib.unquote(data)
    patronvideos  = '(upafile.com/[a-z0-9]+)'
    logger.info("[upafile.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[upafile]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'upafile' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
