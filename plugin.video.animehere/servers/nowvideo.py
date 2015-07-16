# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para nowvideo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

USER_AGENT="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:20.0) Gecko/20100101 Firefox/20.0"

def test_video_exists( page_url ):
    logger.info("[nowvideo.py] test_video_exists(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)
    
    if "The file is being converted" in data:
        return False,"El fichero está en proceso"

    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[nowvideo.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    
    if premium:
        # Lee la página de login
        login_url = "http://www.nowvideo.eu/login.php"
        data = scrapertools.cache_page( login_url )

        # Hace el login
        login_url = "http://www.nowvideo.eu/login.php?return="
        post = "user="+user+"&pass="+password+"&register=Login"
        headers=[]
        headers.append(["User-Agent",USER_AGENT])
        headers.append(["Referer","http://www.nowvideo.eu/login.php"])
        data = scrapertools.cache_page( login_url , post=post, headers=headers )

        # Descarga la página del vídeo 
        data = scrapertools.cache_page( page_url )
        logger.debug("data:" + data)
        
        # URL a invocar: http://www.nowvideo.eu/api/player.api.php?user=aaa&file=rxnwy9ku2nwx7&pass=bbb&cid=1&cid2=undefined&key=83%2E46%2E246%2E226%2Dc7e707c6e20a730c563e349d2333e788&cid3=undefined
        # En la página:
        '''
        flashvars.domain="http://www.nowvideo.eu";
        flashvars.file="rxnwy9ku2nwx7";
        flashvars.filekey="83.46.246.226-c7e707c6e20a730c563e349d2333e788";
        flashvars.advURL="0";
        flashvars.autoplay="false";
        flashvars.cid="1";
        flashvars.user="aaa";
        flashvars.key="bbb";
        flashvars.type="1";
        '''
        flashvar_file = scrapertools.get_match(data,'flashvars.file="([^"]+)"')
        flashvar_filekey = scrapertools.get_match(data,'flashvars.filekey="([^"]+)"')
        flashvar_user = scrapertools.get_match(data,'flashvars.user="([^"]+)"')
        flashvar_key = scrapertools.get_match(data,'flashvars.key="([^"]+)"')
        flashvar_type = scrapertools.get_match(data,'flashvars.type="([^"]+)"')

        #http://www.nowvideo.eu/api/player.api.php?user=aaa&file=rxnwy9ku2nwx7&pass=bbb&cid=1&cid2=undefined&key=83%2E46%2E246%2E226%2Dc7e707c6e20a730c563e349d2333e788&cid3=undefined
        url = "http://www.nowvideo.eu/api/player.api.php?user="+flashvar_user+"&file="+flashvar_file+"&pass="+flashvar_key+"&cid=1&cid2=undefined&key="+flashvar_filekey.replace(".","%2E").replace("-","%2D")+"&cid3=undefined"
        data = scrapertools.cache_page( url )
        logger.info("data="+data)
        
        location = scrapertools.get_match(data,'url=([^\&]+)&')
        location = location + "?client=FLASH"

        video_urls.append( [ scrapertools.get_filename_from_url(location)[-4:] + " [premium][nowvideo]",location ] )
    else:

        data = scrapertools.cache_page( page_url )
        logger.debug("data:" + data)
        
        # URL a invocar: http://www.nowvideo.eu/api/player.api.php?file=3695bce6e6288&user=undefined&codes=1&pass=undefined&key=83%2E44%2E253%2E73%2D64a25e17853b4b19586841e04b0d9382
        # En la página:
        '''
        flashvars.domain="http://www.nowvideo.eu";
        flashvars.file="3695bce6e6288";
        flashvars.filekey="83.44.253.73-64a25e17853b4b19586841e04b0d9382";
        flashvars.advURL="0";
        flashvars.autoplay="false";
        flashvars.cid="1";
        '''
        file = scrapertools.get_match(data,'flashvars.file="([^"]+)"')
        key = scrapertools.get_match(data,'flashvars.filekey="([^"]+)"')
        #http://www.nowvideo.eu/api/player.api.php?key=88%2E19%2E203%2E156%2Dd140046f284485aedf05563b85f1e8e9&codes=undefined&user=undefined&pass=undefined&file=6f213c972dc5b
        url = "http://www.nowvideo.eu/api/player.api.php?file="+file+"&user=undefined&codes=undefined&pass=undefined&key="+key.replace(".","%2E").replace("-","%2D")
        data = scrapertools.cache_page( url )
        logger.info("data="+data)
        # url=http://f23.nowvideo.eu/dl/653d434d3cd95f1f7b9df894366652ba/4fc2af77/nnb7e7f45f276be5a75b10e8d6070f6f4c.flv&title=Title%26asdasdas&site_url=http://www.nowvideo.eu/video/3695bce6e6288&seekparm=&enablelimit=0
        
        location = scrapertools.get_match(data,'url=([^\&]+)&')
        location = location + "?client=FLASH"

        video_urls.append( [ scrapertools.get_filename_from_url(location)[-4:] + " [nowvideo]",location ] )

    for video_url in video_urls:
        logger.info("[nowvideo.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    #<a href="http://www.nowvideo.eu/video/3695bce6e6288" target="_blank">1° Tempo</a>
    patronvideos  = '<a href="(http://www.nowvideo.../video/[a-z0-9]+)"[^>]+>([^<]+)</a>'
    logger.info("[nowvideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = match[1]+" [nowvideo]"
        url = match[0]
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'nowvideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://www.nowvideo.eu/video/3695bce6e6288
    #http://www.nowvideo.eu/video/4fd0757fd4592
    patronvideos  = '(nowvideo.../video/[a-z0-9]+)'
    logger.info("[nowvideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[nowvideo]"
        url = "http://www."+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'nowvideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://www.player3k.info/nowvideo/?id=t1hkrf1bnf2ek
    patronvideos  = 'player3k.info/nowvideo/\?id\=([a-z0-9]+)'
    logger.info("[nowvideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[nowvideo]"
        url = "http://www.nowvideo.eu/video/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'nowvideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://embed.nowvideo.eu/embed.php?v=obkqt27q712s9&amp;width=600&amp;height=480
    #http://embed.nowvideo.eu/embed.php?v=4grxvdgzh9fdw&width=568&height=340
    patronvideos  = 'nowvideo.../embed.php\?v\=([a-z0-9]+)'
    logger.info("[nowvideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[nowvideo]"
        url = "http://www.nowvideo.eu/video/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'nowvideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://embed.nowvideo.eu/embed.php?width=600&amp;height=480&amp;v=9fb588463b2c8
    patronvideos  = 'nowvideo.../embed.php\?.+?v\=([a-z0-9]+)'
    logger.info("[nowvideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[nowvideo]"
        url = "http://www.nowvideo.eu/video/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'nowvideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

def test():

    video_urls = get_video_url("http://www.nowvideo.eu/video/xuntu4pfq0qye")

    return len(video_urls)>0