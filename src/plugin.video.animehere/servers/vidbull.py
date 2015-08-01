# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para vidbull
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import unpackerjs
import time

def test_video_exists( page_url ):
    logger.info("[vidbull.py] test_video_exists(page_url='%s')" % page_url)
    
    data = scrapertools.cache_page( page_url )
    if "The file was removed by administrator" in data:
        return False,"El archivo ya no está disponible<br/>en vidbull (ha sido borrado)"
    else:
        return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[vidbull.py] url="+page_url)
        
    data = scrapertools.cache_page( page_url , headers=[['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14']] )
    logger.info("data="+data)

    # Extrae el trozo cifrado
    '''
    <script type='text/javascript'>eval(function(p,a,c,k,e,d){while(c--)if(k[c])p=p.replace(new RegExp('\\b'+c.toString(a)+'\\b','g'),k[c]);return p}('2j 2=2i 2h(\'6://8.5/b/b.2g\',\'b\',\'2f\',\'2e\',\'9\');2.g(\'2d\',\'k\');2.g(\'2c\',\'2b\');2.g(\'2a\',\'29\');2.4(\'28\',\'../b/27.26\');2.4(\'25\',\'24\');2.4(\'l\',\'6://n.8.5:23/d/21/20.1z\');2.4(\'1y\',\'6://n.8.5/i/1x/e.1w\');2.4(\'1v\',\'6\');2.4(\'1u.j\',\'1t\');2.4(\'1s\',\'1r\');2.4(\'1q\',\'f-3\');2.4(\'f.h\',\'6://8.5/e\');2.4(\'f.1p\',\'%1o%1n%1m%1l%1k%1j%1i.5%1h-e-1g.1f%22%1e%c%1d%c%1c%c%1b%1a%19%18%17%16%m%14%13%m\');2.4(\'a.l\',\'6://8.5/12/11.10\');2.4(\'a.z\',\'k\');2.4(\'a.y\',\'15\');2.4(\'a.x\',\'1\');2.4(\'a.w\',\'0.7\');2.4(\'a.j\',\'v-u\');2.4(\'a.h\',\'6://8.5\');2.4(\'t\',\'s r\');2.4(\'q\',\'6://8.5\');2.p(\'o\');',36,92,'||s1||addVariable|com|http||vidbull||logo|player|3D0||erk3r6bpfyxy|sharing|addParam|link||position|true|file|3E|fs11|flvplayer|write|aboutlink|dlf|VidBull|abouttext|right|top|out|over|timeout|hide|png|vidbull_playerlogo|images|2FIFRAME|3C||3D338|20HEIGHT|3D640|20WIDTH|3DNO|20SCROLLING|20MARGINHEIGHT|20MARGINWIDTH|20FRAMEBORDER|html|640x318|2Fembed|2Fvidbull|2F|3A|22http|3D|20SRC|3CIFRAME|code|plugins|uniform|stretching|left|dock|provider|jpg|00031|image|flv|video|45sbu63kljrwuxim7e6xp2koxj4sxpaxyivgkrzwu27ggj5rdrrayurf||182|2606|duration|zip|modieus1|skin|opaque|wmode|always|allowscriptaccess|allowfullscreen|318|640|swf|SWFObject|new|var'.split('|')))
    '''
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
    
    # Extrae la URL
    media_url = scrapertools.get_match(descifrado,"addVariable\('file','([^']+)'")
    
    video_urls = []
    
    if len(matches)>0:
        video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [vidbull]",media_url])

    for video_url in video_urls:
        logger.info("[vidbull.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://www.vidbull.com/3360qika02mo
    # http://vidbull.com/6efa0ns1dpxc.html
    patronvideos  = 'vidbull.com/([A-Z0-9a-z\-\.]+)'
    logger.info("[vidbull.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[vidbull]"
        url = "http://vidbull.com/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'vidbull' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
