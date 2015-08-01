#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para cineraculo (genera vinculos desde videos de megaupload)
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import sys,os,traceback

from core import scrapertools
from core import logger
from core import config

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    try :
        logger.info("[cineraculo.py] get_video_url(page_url='%s')" % page_url)
    
        ua=['User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.52.7 (KHTML, like Gecko) Version/5.1.2 Safari/534.52.7']
        referer1=['Referer', 'http://www.cineraculo.com']
        referer2=['Referer', 'http://www.cineraculo.com/vermegavideolink.aspx']
        data = scrapertools.cache_page("http://www.cineraculo.com/vermegavideolink.aspx", headers=[ua, referer1], timeout=10000)
        patron = '<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="([^"]+)" />.*?'
        patron += '<input type="hidden" name="__EVENTVALIDATION" id="__EVENTVALIDATION" value="([^"]+)"'
        matches = re.compile(patron,re.DOTALL).findall(data)
        code1 = urllib.quote(matches[0][0]).replace("/","%2F")
        code2 = urllib.quote(matches[0][1]).replace("/","%2F")
        url=urllib.quote(page_url).replace("/","%2F")
        post = "__VIEWSTATE=%s&__EVENTVALIDATION=%s&txt_megavideo_url=%s&txt_movie_title=&btn_watch=Ver" % (code1,code2,url)
        data = scrapertools.cache_page("http://www.cineraculo.com/vermegavideolink.aspx", post = post , headers=[ua, referer2], timeout=20000)

        patron = "unescape\('([^']+)'"
        matches = re.compile(patron,re.DOTALL).findall(data)
        text = ''
        for match in matches:
            text += urllib.unquote(match)
        #logger.info("text = " + text)
        
        m = re.compile('fromCharCode\(([^\)]+)\)').findall(text)
        url = ""
        if m != None and len(m) > 1 :
            def compute_expr(ex) :
                op_pos = ex.find('+')
                if op_pos != -1 : return chr(int(ex[0:op_pos]) + int(ex[op_pos+1:]))
                op_pos = ex.find('-')
                if op_pos != -1 : return chr(int(ex[0:op_pos]) - int(ex[op_pos+1:]))
                return '?'
            
            deobfuscated_js = "".join(map(lambda expr : compute_expr(expr), m[1].split(',')))
            m = re.compile('(http://[^"]+\.flv)"').search(deobfuscated_js)
            if m != None and m.group(1) != None : url = m.group(1)
            else: logger.info("URL no encontrada:\n" + deobfuscated_js)
        
        if len(url) > 0 :
            #hash = get_match(url, 's.aspx/([^/]+)/')
            #mirror = get_match(url, 's.aspx/[^/]+/([^/]+)/')
            return [["(Free)", url + '|User-Agent=' + ua[1] ]]
    except Exception as ex :
        logger.error("[cineracylo.py] Error al obtener la url del flujo: " + str(ex) )
        traceback.print_exc(file=sys.stdout)
    
    # FIXME: ugly
    return []
    
def get_match(data, regex) :
    match = "";
    m = re.search(regex, data)
    if m != None :
        match = m.group(1)
    return match

def find_videos(data):
    import megavideo
    logger.info("[cineraculo.py] find_videos")
    return add_videos(megavideo.find_videos(data))

def add_videos(found_videos):
    logger.info("[cineraculo.py] add_videos")
    # Filter the found videos with megavideo url
    filtered_videos = filter( lambda video : video[1].find('www.megavideo.com') > 0 , found_videos)
    # Map the filtered videos to set a cineraculo server entry on them and return a copy
    return map( lambda video : ['[Cineraculo]', video[1], 'cineraculo'], filtered_videos)
