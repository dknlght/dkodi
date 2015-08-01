# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para AllDebrid
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[alldebrid.py] get_video_url( page_url='%s' , user='%s' , password='%s', video_password=%s)" % (page_url , user , "**************************"[0:len(password)] , video_password) )
    page_url = correct_url(page_url)

#Sin Logear

#    url = 'http://alldebrid.com/service.php?&link=%s' % page_url

    url = 'http://www.alldebrid.com/service.php?pseudo=%s&password=%s&link=%s' % (user,password,page_url)

    data = scrapertools.cache_page(url)
    #print data

    patron = "href='(.+?)'"
    matches = re.compile(patron).findall(data)
    if len(matches)>0:
        return matches[0]
    else:
        server_error = ""
        if "login" in data:
            server_error = " AllDebrid : Tu Cuenta puede haber expirado."
            
        elif "Hoster unsupported or under maintenance" in data:
            server_error = " AllDebrid : Host no soportado o en mantenimiento."

        elif '"error":"' in data:
            server_error = " Alldebrid ERROR<br/>"+scrapertools.get_match(data,'"error"\:"([^"]+)"')

        logger.info(data)
        return server_error
      
def correct_url(url):
    if "userporn.com" in url:
        url = url.replace("/e/","/video/")
    
    if "putlocker" in url:
        url = url.replace("/embed/","/file/")
    return url