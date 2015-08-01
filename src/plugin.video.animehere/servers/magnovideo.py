# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para magnovideo
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    logger.info("[modovideo.py] test_video_exists(page_url='%s')" % page_url)
    
    if "?d=" in page_url:
        return False,"Formato de URL de Magnovideo no soportado"
    else:
        return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[magnovideo.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []

    headers = []
    headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:17.0) Gecko/20100101 Firefox/17.0"])
    
    id_video = scrapertools.get_match(page_url,"\?v\=([A-Z0-9]+)")
    data = scrapertools.cache_page("http://www.magnovideo.com/player_config.php?mdid="+id_video)
    logger.info("data="+data)
    
    #http://e1.magnovideo.com:8080/storage/files/0/0/16/161/1.mp4?burst=3890k&u=600k&st=ybNoWopdpGeeDy6dXVh4kw&e=1360030261
    #<first_frame>http://s2.magnovideo.com/storage/files/0/0/99/197/large/1.jpg</first_frame>
    #<video_name>1.mp4</video_name>
    #<storage_path>http://e1.magnovideo.com:8080/</storage_path>
    #<movie_burst>3890</movie_burst>
    #<burst_speed>600</burst_speed>
    #<ste>st=ybNoWopdpGeeDy6dXVh4kw&e=1360030261</ste>

    first_frame = scrapertools.get_match(data,"<first_frame>([^<]+)</first_frame>")
    logger.info("first_frame="+first_frame)

    video_name = scrapertools.get_match(data,"<video_name>([^<]+)</video_name>")
    logger.info("video_name="+video_name)
    
    storage_path = scrapertools.get_match(data,"<storage_path>([^<]+)</storage_path>")
    logger.info("storage_path="+storage_path)
    
    movie_burst = scrapertools.get_match(data,"<movie_burst>([^<]+)</movie_burst>")
    logger.info("movie_burst="+movie_burst)
    
    burst_speed = scrapertools.get_match(data,"<burst_speed>([^<]+)</burst_speed>")
    logger.info("burst_speed="+burst_speed)
    
    ste = scrapertools.get_match(data,"<ste>([^<]+)</ste>")
    logger.info("ste="+ste)

    #http://e1.magnovideo.com:8080/storage/files/0/0/16/161/1.mp4?burst=3890k&u=600k&st=ybNoWopdpGeeDy6dXVh4kw&e=1360030261

    base_path = re.compile("http\://.*?/",re.DOTALL).sub(storage_path,first_frame)
    logger.info("base_path="+base_path)

    location = base_path.replace("large/1.jpg",video_name)
    location = location+"?burst="+movie_burst+"k&u="+burst_speed+"k&"+ste
    
    '''
    # Pide la primera
    logger.info("----------------------------------------------------------------------------------------------------")
    data = scrapertools.cache_page(page_url,headers=headers)
    logger.info("cookies="+config.get_cookie_data())
    logger.info("data="+data)
    
    # Pide la segunda con el v.php
    #http://www.magnovideo.com/?v=QRATZ9UN
    #http://www.magnovideo.com/v.php?dl=QRATZ9UN
    headers.append(["Referer",page_url])
    logger.info("----------------------------------------------------------------------------------------------------")
    data = scrapertools.cache_page(page_url.replace("?v=","v.php?dl="),headers=headers)
    logger.info("cookies="+config.get_cookie_data())
    logger.info("data="+data)

    # Vuelve a pedir la primera, esta vez con las cookies bien
    headers[1][1]=page_url.replace("?v=","v.php?dl=")
    logger.info("----------------------------------------------------------------------------------------------------")
    data = scrapertools.cache_page(page_url,headers=headers)
    logger.info("cookies="+config.get_cookie_data())
    logger.info("data="+data)

    # Busca el enlace
    location = scrapertools.get_match(data,"http\://www.magnovideo.com/templates_mu/player/crilance_player.swf\?flv\=([^\&]+)\&")
    location = location+"?burst=5568k"
    '''
    
    video_urls.append( [scrapertools.get_filename_from_url(location)[-4:]+" [magnovideo]" , location] )

    for video_url in video_urls:
        logger.info("[magnovideo.py] %s - %s" % (video_url[0],video_url[1]))


    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://www.magnovideo.com/?v=QRATZ9UN
    patronvideos  = '(magnovideo.com/\?v\=[A-Z0-9]+)'
    logger.info("[magnovideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[magnovideo]"
        url = "http://www."+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'magnovideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://www.magnovideo.com/?d=DKTLC6BS
    patronvideos  = '(magnovideo.com/\?d\=[A-Z0-9]+)'
    logger.info("[magnovideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[magnovideo]"
        url = "http://www."+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'magnovideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://www.magnovideo.com/v.php?dl=ZTL2VDPV
    patronvideos  = 'magnovideo.com/v.php\?dl\=([A-Z0-9]+)'
    logger.info("[magnovideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[magnovideo]"
        url = "http://www.magnovideo.com/?v="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'magnovideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    
    return devuelve
