# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para filenium
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re,time
import os
import base64
#import json

from core import scrapertools
from core import logger
from core import config
from urllib import urlencode

TIMEOUT=50

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[filenium.py] get_video_url(page_url='%s')" % page_url)
    location=""
    page_url = correct_url(page_url)
    if premium:
        # Hace el login
        if "?.torrent" in page_url:
            location = page_url.replace("?.torrent","")        
        else:
            url = "http://filenium.com/welcome"
            post = "username=%s&password=%s" % (user,password)
            data = scrapertools.cache_page(url, post=post, timeout=TIMEOUT)
            link = urlencode({'filez':page_url})
            location = scrapertools.cache_page("http://filenium.com/?filenium&" + link, timeout=TIMEOUT)
            
        user = user.replace("@","%40")
        
        #logger.info("[filenium.py] torrent url (location='%s')" % location)
        
        if "xbmc" in config.get_platform():
            #location = location.replace("http://cdn.filenium.com","http://"+user+":"+password+"@cdn.filenium.com")
            location = location.replace("http://","http://"+user+":"+password+"@")
        else:
            location = location.replace("/?.zip","")
            user = user.replace(".","%2e")
            location = location + "?user="+user+"&passwd="+password

        logger.info("location="+location)

        '''
        if not location.startswith("http") and page_url.endswith(".torrent"):
            # Lee el id
            data=json.loads(location)
            logger.info("data="+str(data))
            name = data['name']

            datas = scrapertools.cachePage("http://filenium.com/xbmc_json", timeout=TIMEOUT)
            logger.info(datas)
            data = json.loads(datas)
            logger.info(str(data))
            
            for match in data:
                if match['status'] == "COMPLETED" and match['filename'].startswith(name):
                    location = match['download_url'] + "?.torrent"
                    logger.info("location="+location)
                    break
        '''

    return location

def get_file_extension(location):

    try:
        content_disposition_header = scrapertools.get_header_from_response(location,header_to_get="Content-Disposition")
        logger.info("content_disposition="+content_disposition_header)
        partes=content_disposition_header.split("=")
        if len(partes)<=1:
            extension=""
        else:
            fichero = partes[1]
            fichero = fichero.replace("\\","")
            fichero = fichero.replace("'","")
            fichero = fichero.replace('"',"")
            extension = fichero[-4:]
    except:
        extension=""
    return extension

def extract_authorization_header(url):
    # Obtiene login y password, y lo añade como cabecera Authorization
    partes = url[7:].split("@")
    partes = partes[0].split(":")
    username = partes[0].replace("%40","@")
    password = partes[1]
    logger.info("[filenium.py] username="+username)
    logger.info("[filenium.py] password="+password)
    
    import base64
    base64string = base64.encodestring('%s:%s' % (username, password))[:-1]
    logger.info("[filenium.py] Authorization="+base64string)
    authorization_header = "Basic %s" % base64string
    
    # Ahora saca el login y password de la URL
    partes = url.split("@")
    url = "http://"+partes[1]
    logger.info("[filenium.py] nueva url="+url)

    return url,authorization_header

def correct_url(url):
    if "userporn.com" in url:
        url = url.replace("/e/","/video/")
    
    if "putlocker" in url:
        url = url.replace("/embed/","/file/")
    return url