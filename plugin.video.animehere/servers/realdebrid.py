# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para Real_Debrid
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[realdebrid.py] get_video_url( page_url='%s' , user='%s' , password='%s', video_password=%s)" % (page_url , user , "**************************"[0:len(password)] , video_password) )
    page_url = correct_url(page_url)
    url = 'http://real-debrid.com/lib/api/account.php'
    data = scrapertools.cache_page(url)
    logger.info(data)
    if data is None or not re.search('expiration', data) or not re.search(user, data):
        
        # Hace el login y consigue la cookie
        post = urllib.urlencode({'user' : user, 'pass' : password})
        login_url = 'https://real-debrid.com/ajax/login.php?'+post
    
        data = scrapertools.cache_page(url=login_url)
        #print data
        if re.search('OK', data):
            logger.info("Se ha logueado correctamente en Real-Debrid ")
        else:
            logger.info(data)
            patron = 'message":"(.+?)"'
            matches = re.compile(patron).findall(data)
            if len(matches)>0:
                server_error = "REAL-DEBRID: "+urllib.unquote_plus(matches[0].replace("\\u00","%"))
            else:
                server_error = "REAL-DEBRID: Ha ocurrido un error con tu login"
            return server_error
    else:
        logger.info("Ya estas logueado en Real-Debrid")
    
    url = 'http://real-debrid.com/ajax/deb.php?lang=es&sl=1&link=%s' % page_url
    data = scrapertools.cache_page(url)
    #print data
    patron = 'ok"><a href="(.+?)"'
    matches = re.compile(patron).findall(data)
    if len(matches)>0:
        return matches[0]
    else:
        patron = '<span id="generation-error">(.+?)<'
        matches = re.compile(patron).findall(data)
        if len(matches)>0:
            server_error = "REAL-DEBRID: "+matches[0]
        else:
            server_error = "REAL-DEBRID: Ha ocurrido un error con el servidor "
        logger.info(data)
        return server_error

def correct_url(url):
    if "userporn.com" in url:
        url = url.replace("/e/","/video/")
    
    if "putlocker" in url:
        url = url.replace("/embed/","/file/")
    return url