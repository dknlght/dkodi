# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videopremium
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
#LvX Edited Patched

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[videopremium.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
   
    # Lee la URL
    data = scrapertools.cache_page( page_url )
    logger.info("data="+data)
    bloque = scrapertools.get_match(data,'<Form[^>]*method="POST"(.*)</.orm>')
    logger.info("bloque="+bloque)
    op = scrapertools.get_match(bloque,'<input type="hidden" name="op" value="([^"]+)"')
    usr_login = scrapertools.get_match(bloque,'<input type="hidden" name="usr_login" value="([^"]*)"')
    id = scrapertools.get_match(bloque,'<input type="hidden" name="id" value="([^"]+)"')
    fname = scrapertools.get_match(bloque,'<input type="hidden" name="fname" value="([^"]+)"')
    referer = scrapertools.get_match(bloque,'<input type="hidden" name="referer" value="([^"]*)"')
    method_free = scrapertools.get_match(bloque,'<input type="[^"]+" name="method_free" value="([^"]+)"')

    # Simula el botón
    #op=download1&usr_login=&id=buq4b8zunbm6&fname=Snow.Buddies-Avventura.In.Alaska.2008.iTALiAN.AC3.DVDRip.H264-PsYcOcReW.avi&referer=&method_free=Watch+Free%21
    post = "op="+op+"&usr_login="+usr_login+"&id="+id+"&fname="+fname+"&referer="+referer+"&method_free="+method_free
    data = scrapertools.cache_page( page_url , post=post )
    #logger.info("data="+data)
   
    try:
        packed = scrapertools.get_match(data,"(<script type='text/javascript'>eval\(function\(p,a,c,k,e,d\).*?</script>)")
    except:
        packed = scrapertools.get_match(data,"(function\(p, a, c, k, e, d\).*?</script>)")
        packed = "<script type='text/javascript'>eval("+packed

    logger.info("packed="+packed)

    from core import unpackerjs
    unpacked = unpackerjs.unpackjs(packed)
    logger.info("unpacked="+unpacked)
    '''
    23:47:40 T:2955980800  NOTICE: unpacked=('var vast=\'\';var flashvars={"comment":"VideoPremium.NET","st":"http://videopremium.net/uplayer/styles/video156-623.txt",
        "file":"rtmp://tengig0.lb.videopremium.net/play/mp4:8x0mq9hanl3a.f4v",
        p2pkey:"mp4:8x0mq9hanl3a.f4v",vast_preroll:vast};var params={bgcolor:"#ffffff",allowFullScreen:"true",allowScriptAccess:"always",id:"vplayer"};new swfobject.embedSWF("http://videopremium.net/uplayer/uppod.swf","vplayer","728","450","9.0.115.0",false,flashvars,params);',,paramsflashvars,
    '''
    '''
    Property 'app' String 'play'
    Property 'swfUrl' String 'http://videopremium.net/uplayer/uppod.swf'
    Property 'pageUrl' String 'http://videopremium.net/8x0mq9hanl3a'
    Property 'tcUrl' String 'rtmp://e5.videopremium.net/play'
    play: String 'mp4:8x0mq9hanl3a.f4v'
    '''
    '''
    00:55:30 T:2955980800   ERROR: Valid RTMP options are:
    00:55:30 T:2955980800   ERROR:      socks string   Use the specified SOCKS proxy
    00:55:30 T:2955980800   ERROR:        app string   Name of target app on server
    00:55:30 T:2955980800   ERROR:      tcUrl string   URL to played stream
    00:55:30 T:2955980800   ERROR:    pageUrl string   URL of played media's web page
    00:55:30 T:2955980800   ERROR:     swfUrl string   URL to player SWF file
    00:55:30 T:2955980800   ERROR:   flashver string   Flash version string (default MAC 10,0,32,18)
    00:55:30 T:2955980800   ERROR:       conn AMF      Append arbitrary AMF data to Connect message
    00:55:30 T:2955980800   ERROR:   playpath string   Path to target media on server
    00:55:30 T:2955980800   ERROR:   playlist boolean  Set playlist before play command
    00:55:30 T:2955980800   ERROR:       live boolean  Stream is live, no seeking possible
    00:55:30 T:2955980800   ERROR:  subscribe string   Stream to subscribe to
    00:55:30 T:2955980800   ERROR:        jtv string   Justin.tv authentication token
    00:55:30 T:2955980800   ERROR:       weeb string   Weeb.tv authentication token
    00:55:30 T:2955980800   ERROR:      token string   Key for SecureToken response
    00:55:30 T:2955980800   ERROR:     swfVfy boolean  Perform SWF Verification
    00:55:30 T:2955980800   ERROR:     swfAge integer  Number of days to use cached SWF hash
    00:55:30 T:2955980800   ERROR:    swfsize integer  Size of the decompressed SWF file
    00:55:30 T:2955980800   ERROR:    swfhash string   SHA256 hash of the decompressed SWF file
    00:55:30 T:2955980800   ERROR:      start integer  Stream start position in milliseconds
    00:55:30 T:2955980800   ERROR:       stop integer  Stream stop position in milliseconds
    00:55:30 T:2955980800   ERROR:     buffer integer  Buffer time in milliseconds
    00:55:30 T:2955980800   ERROR:    timeout integer  Session timeout in seconds
    '''
    rtmpurl=scrapertools.get_match(unpacked,'"file"\:"([^"]+)"').replace("tengig0.lb.videopremium.net","e4.videopremium.net")
    playpath=scrapertools.get_match(unpacked,'p2pkey\:"([^"]+)"')
    swfurl=scrapertools.get_match(unpacked,'embedSWF\("([^"]+)"')
    pageurl = page_url
    app="play"
    tcurl="rtmp://e4.videopremium.net/play"
    location = rtmpurl+" playpath="+playpath+" swfurl="+swfurl+" pageUrl="+page_url+" tcurl="+tcurl+" app="+app #swfvfy=true

    logger.info("location="+location)
    video_urls.append( [ "RTMP [videopremium]",location ] )

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    #<a href="http://videopremium.net/0yo7kkdsfdh6/21.Jump.Street.2012.Subbed.ITA.DVDRIP.XviD-ZDC.CD1.avi.flv.html" target="_blank">1° Tempo</a>
    patronvideos  = '<a href="(http://videopremium.net[^"]+)"[^>]+>([^<]+)</a>'
    logger.info("[videopremium.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = match[1]+" [videopremium]"
        url = match[0]
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'videopremium' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    #http://videopremium.net/buq4b8zunbm6
    #http://videopremium.net/0yo7kkdsfdh6/21.Jump.Street.2012.Subbed.ITA.DVDRIP.XviD-ZDC.CD1.avi.flv.html
    patronvideos  = '(videopremium.net/[a-z0-9]+)'
    logger.info("[videopremium.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[videopremium]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'videopremium' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

def test():
    video_urls = get_video_url("http://videopremium.net/8x0mq9hanl3a")
    return len(video_urls)>0

