# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para streamcloud
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import unpackerjs

def test_video_exists( page_url ):
    logger.info("[streamcloud.py] test_video_exists(page_url='%s')" % page_url)

    data = scrapertools.cache_page( url = page_url )
    if "<h1>File Not Found</h1>" in data:
        return False,"El archivo no existe<br/>en streamcloud o ha sido borrado."
    else:
        return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[streamcloud.py] url="+page_url)
    
    # Lo pide una vez
    headers = [['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14']]
    data = scrapertools.cache_page( page_url , headers=headers )
    #logger.info("data="+data)

    logger.info("[streamcloud.py] Esperando 10 segundos...")

    '''
    Esto cuelga XBMC en algunos casos?
    try:
        from platformcode.xbmc import xbmctools
        xbmctools.handle_wait(12,"streamcloud",'')
    except:
    '''
    import time
    time.sleep(12)

    logger.info("[streamcloud.py] Espera concluida")
    
    try:
        media_url = scrapertools.get_match( data , 'file\: "([^"]+)"' )+"?start=0"
    except:
        op = scrapertools.get_match(data,'<input type="hidden" name="op" value="([^"]+)"')
        usr_login = ""
        id = scrapertools.get_match(data,'<input type="hidden" name="id" value="([^"]+)"')
        fname = scrapertools.get_match(data,'<input type="hidden" name="fname" value="([^"]+)"')
        referer = scrapertools.get_match(data,'<input type="hidden" name="referer" value="([^"]*)"')
        hashstring = scrapertools.get_match(data,'<input type="hidden" name="hash" value="([^"]*)"')
        imhuman = scrapertools.get_match(data,'<input type="submit" name="imhuman".*?value="([^"]+)">').replace(" ","+")
        
        post = "op="+op+"&usr_login="+usr_login+"&id="+id+"&fname="+fname+"&referer="+referer+"&hash="+hashstring+"&imhuman="+imhuman
        headers.append(["Referer",page_url])
        data = scrapertools.cache_page( page_url , post=post, headers=headers )

        if 'id="justanotice"' in data:
            logger.info("[streamcloud.py] data="+data)
            logger.info("[streamcloud.py] Ha saltado el detector de adblock")
            return []

        # Extrae la URL
        media_url = scrapertools.get_match( data , 'file\: "([^"]+)"' )+"?start=0"
        
    video_urls = []
    video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [streamcloud]",media_url])

    for video_url in video_urls:
        logger.info("[streamcloud.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://streamcloud.eu/cwvhcluep67i
    patronvideos  = '(streamcloud.eu/[a-z0-9]+)'
    logger.info("[streamcloud.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[streamcloud]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'streamcloud' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

if __name__ == "__main__":
    import getopt
    import sys
    options, arguments = getopt.getopt(sys.argv[1:], "", ["video_url=","login=","password="])
    
    video_url = ""
    login = ""
    password = ""
    
    logger.info("%s %s" % (str(options),str(arguments)))
    
    for option, argument in options:
        print option,argument
        if option == "--video_url":
            video_url = argument
        elif option == "--login":
            login = argument
        elif option == "--password":
            password = argument
        else:
            assert False, "Opcion desconocida"

    if video_url=="":
        print "ejemplo de invocacion"
        print "streamcloud --video_url http://xxx --login usuario --password secreto"
    else:
        
        if login!="":
            premium=True
        else:
            premium=False
        
        print get_video_url(video_url,premium,login,password)

def test():
    video_urls = get_video_url("http://streamcloud.eu/132qd8f6gaj2")

    return len(video_urls)>0