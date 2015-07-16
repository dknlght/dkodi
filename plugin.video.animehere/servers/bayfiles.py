# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para bayfiles
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    logger.info("[bayfiles.py] test_video_exists(page_url='%s')" % page_url)

    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[bayfiles.py] get_video_url("+page_url+")")
    from servers import servertools
    video_urls = []

    data = scrapertools.cache_page(page_url)
    try:
        vfid = re.compile('var vfid = ([^;]+);').findall(data)[0]
    except:
        logger.info("[bayfiles.py] Error no encontro vfid")
        return ''
    try:
        delay = re.compile('var delay = ([^;]+);').findall(data)[0]
        delay = int(delay)
    except:
        delay = 300

    logger.info("[bayfiles.py] vfid="+vfid)
    logger.info("[bayfiles.py] delay="+str(delay))

    from platformcode.xbmc import xbmctools
 
    t = millis()
    #http://bayfiles.com/ajax_download?_=1336330599281&action=startTimer&vfid=2174049
    url_token = "http://bayfiles.com/ajax_download?_=%s&action=startTimer&vfid=%s"%(t,vfid)
    data = scrapertools.cache_page(url_token)
    logger.info("data="+data)
    datajson = load_json(data)

    if datajson['set']==True:
        token=datajson['token']
        resultado = xbmctools.handle_wait(delay,"Progreso","Conectando con servidor BayFiles (Free)")
        #if resultado == False:
            
        url_ajax = 'http://bayfiles.com/ajax_download'
        post = "action=getLink&vfid=%s&token=%s" %(vfid,token)
        data = scrapertools.cache_page( url_ajax , post=post, headers=[['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'],['Referer',page_url]] )
    
        # Extrae la url del video
        patron = 'onclick="javascript:window.location.href = \'(.+?)\''
        matches = re.compile(patron,re.DOTALL).findall(data)
        #scrapertools.printMatches(matches)
        
        if len(matches)>0:
            mediaurl = matches[0]
            try:
                location = scrapertools.getLocationHeaderFromResponse(mediaurl)
                if location:
                    mediaurl = location
            except:
                logger.info("Error al redireccionar")
            mediaurl = mediaurl + "|Referer="+urllib.quote(page_url)
            video_urls.append( ["."+mediaurl.rsplit('.',1)[1]+" [bayfiles]",mediaurl,60])

    for video_url in video_urls:
        logger.info("[bayfiles.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://bayfiles.com/file/3R2P/8QqLEo/A.Gifted.Man.S01E15.HDTV.XviD-2HD.mp4
    # http://www.bayfiles.com/file/3yUL/NQ6Kl0/hu60.mp4
    # linkto?url=http://bayfiles.com/file/4pMd/Mhu9Ht/Megamente.720p-Latino.mp4?cid=3154&ctipo=pelicula&cdef=720

    patronvideos  = '(bayfiles.com/file/[a-zA-Z0-9]+/[a-zA-Z0-9]+/[^&^"^\'^<\?]+)'
    logger.info("[bayfiles.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[bayfiles]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'bayfiles' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            

    return devuelve

def load_json(data):
    # callback to transform json string values to utf8
    def to_utf8(dct):
        rdct = {}
        for k, v in dct.items() :
            if isinstance(v, (str, unicode)) :
                rdct[k] = v.encode('utf8', 'ignore')
            else :
                rdct[k] = v
        return rdct
    try :        
        from lib import simplejson
        json_data = simplejson.loads(data, object_hook=to_utf8)
        return json_data
    except:
        try:
            import json
            json_data = json.loads(data, object_hook=to_utf8)
            return json_data
        except:
            import sys
            for line in sys.exc_info():
                logger.error("%s" % line)
    return None

def millis():
    import time as time_ #make sure we don't override time
    return int(round(time_.time() * 1000))
    