# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para rutube
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    return False,"Rutube no es compatible con ningun media center"

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[rutube.py] url="+page_url)
    video_urls = []

    # http://video.rutube.ru/c787127815fb977fee41c9c745495e63
    patron = 'http://video.rutube.ru/([a-z0-9]+)'
    matches = re.compile(patron,re.DOTALL).findall(page_url)
    if len(matches)==0:return []
    code = matches[0]
    logger.info("code="+code)

    #http://bl.rutube.ru/c787127815fb977fee41c9c745495e63.f4m
    url = "http://bl.rutube.ru/"+code+".f4m"
    data = scrapertools.cache_page( url )
    logger.info("data="+data)

    '''
    <?xml version="1.0" encoding="UTF-8"?><manifest xmlns="http://ns.adobe.com/f4m/1.0"><responseCode>200</responseCode><responseDsc>Success</responseDsc><baseURL>rtmp://video-1-13.rutube.ru</baseURL><media url="/rutube_vod_2/mp4:n6vol1/movies/c7/87/c787127815fb977fee41c9c745495e63.mp4?e=1338076898&amp;s=f4622e19943508f93e5781d1d6646835" bitrate="0" width="0" height="0"/></manifest>
    '''
    #rtmp://video-1-13.rutube.ru
    baseURL = scrapertools.get_match(data,"<baseURL>([^<]+)</baseURL")
    #/rutube_vod_2/mp4:n6vol1/movies/c7/87/c787127815fb977fee41c9c745495e63.mp4?e=1338076898&amp;s=f4622e19943508f93e5781d1d6646835
    mediaURL = scrapertools.get_match(data,'<media url="([^"]+)"')
    
    app = scrapertools.get_match(mediaURL,"\/(rutube_vod[^\/]+\/)")
    playpath = scrapertools.get_match(mediaURL,"(mp4\:.*?)$")
    swfurl = 'http://rutube.ru/player.swf'
    
    # ANTES rtmp://video-1-1.rutube.ru:1935/ app=rutube_vod_2/_definst_/ swfurl=http://rutube.ru/player.swf playpath=mp4:vol32/movies/14/bd/14bd98f3733ef080507ff5f517f28830.mp4?e=1295385656&s=adb28dba086b7394013c37550cb48dd8&blid=957c0d2befa18c8d286b2076cecf01bd
    # AHORA rtmp://video-1-13.rutube.ru:1935 app=rutube_vod_2/           swfurl=http://rutube.ru/player.swf playpath=mp4:n6vol1/movies/c7/87/c787127815fb977fee41c9c745495e63.mp4?e=1338077658&amp;s=cc16803c683a4216875eb3bb9216ad45


    streamURL = baseURL + ":1935 app="+app+" swfurl="+swfurl+" playpath="+playpath.replace("&amp;","&")

    video_urls.append(["[rutube]",streamURL])
    ''' 
    patron = "<finalAddress>[^<]+<\!\[CDATA\[([^\]]+)\]\]>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    if len(matches)>0:
        
        # Code adapted from http://code.google.com/p/xbmc-xstream-plugin/
        sRtmpFile = matches[0]
        
        if "rutube_vod_1" in sRtmpFile:
            aSplitt = sRtmpFile.split('rutube_vod_1/')
        else:
            aSplitt = sRtmpFile.split('rutube_vod_2/')
        sPlaypath = aSplitt[1]
            
        aSplitt = sRtmpFile.split('.ru/')
        sRtmp = aSplitt[0] + '.ru:1935/'
        
        aSplitt = aSplitt[1].split('mp4')
        sApp = aSplitt[0]

        sSwfUrl = 'http://rutube.ru/player.swf'

        sStreamUrl = sRtmp + ' app=' + sApp + ' swfurl=' + sSwfUrl + ' playpath=' + sPlaypath
        #rtmp://video-1-1.rutube.ru:1935/ app=rutube_vod_2/_definst_/ swfurl=http://rutube.ru/player.swf playpath=mp4:vol32/movies/14/bd/14bd98f3733ef080507ff5f517f28830.mp4?e=1295385656&s=adb28dba086b7394013c37550cb48dd8&blid=957c0d2befa18c8d286b2076cecf01bd
        
        logger.info("stream="+sStreamUrl)

        video_urls.append( ["[rutube]",sStreamUrl])
    '''

    for video_url in video_urls:
        logger.info("[rutube.py] %s - %s" % (video_url[0],video_url[1]))
    
    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://video.rutube.ru/91203fc46405f06c2cadb98c9052dd68
    patronvideos  = '(http://video.rutube.ru/[a-z0-9]+)'
    logger.info("[rutube.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[rutube]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'rutube' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://rutube.ru/video/embed/6302367?p=ATQKgmK0YweoP2JPwj07Ww
    patronvideos  = '(rutube.ru/video/embed/[a-z0-9]+)'
    logger.info("[rutube.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[rutube]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'rutube' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)


    return devuelve
