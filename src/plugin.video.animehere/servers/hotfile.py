# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para hotfile
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    logger.info("[hotfile.py] test_video_exists(page_url='%s')" % page_url)

    # Existe: http://hotfile.com/dl/57556961/6606499/01_Cagayake_GIRLS.mp4.html
    # No existe: http://hotfile.com/dl/57978410/73e1090/08_Coolly_Hotty_Tension.mp4.html
    data = scrapertools.cache_page(page_url)
    patron  = '<table border="0" cellpadding="0" cellspacing="0" id="download_file" style="margin-bottom. 0.">[^<]+'
    patron += '<tr>[^<]+'
    patron += '<td colspan="3" class="first_row"><div class="arrow_down">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    
    if len(matches)>0:
        return True,""
    else:
        patron  = '<table id="download_file">[^<]+'
        patron  = '<tr>[^<]+'
        patron  = '<td>([^<]+)</td>[^<]+'
        patron  = '</tr>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if len(matches)>0:
            return False,matches[0][0]
    
    return True,""
    

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[hotfile.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # http://hotfile.com/dl/146349096/8d52053/Matalobos._3_Temada._Captulo_67___Eu_son_Mateo_Veloso_____carta___CRTVG.mp4.flv.html
    patronvideos  = '(http://hotfile.com/dl/.*?\.html)'
    logger.info("[hotfile.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[hotfile]"
        url = match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'hotfile' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
