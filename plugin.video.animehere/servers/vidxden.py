# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para vidxden
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import unpackerjs

def test_video_exists( page_url ):
    logger.info("[vidxden.py] test_video_exists(page_url='%s')" % page_url)
    
    data = scrapertools.cache_page( page_url )
    if "This server is in maintenance mode, please try again later." in data:
        return False,"El servidor de vidxden no está disponible<br/>por tareas de mantenimiento"
    elif "No such file or the file has been removed due to copyright infringement issues." in data:
        return False,"Ese video ha sido borrado de vidxden"
    else:
        return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):

    logger.info("[vidxden.py] url="+page_url)

    # Lo pide una vez
    headers = []
    headers.append(['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'])
    data = scrapertools.cache_page( page_url , headers=headers )
    fname = scrapertools.get_match(data,'<input name="fname" type="hidden" value="([^"]+)">')
    codigo = scrapertools.get_match(page_url,'vidxden.com/(\w+)')

    # Lo pide una segunda vez, como si hubieras hecho click en el banner
    #op=download1&usr_login=&id=qtrv0ufkz3e4&fname=El_cazador_de_sue_os-dvd.avi&referer=&method_free=Continue+to+Video
    headers.append(['Referer',page_url])
    post = "op=download1&usr_login=&id="+codigo+"&fname="+fname+"&referer=&method_free=Continue+to+Video"
    data = scrapertools.cache_page( page_url , post=post, headers=headers )
    logger.info("data="+data)

    # Extrae el trozo cifrado
    #<div id="embedcontmvshre" style="position: absolute; top: 0; left: 0; visibility: hidden;"><script type='text/javascript'>eval(function(p,a,c,k,e,d){while(c--)if(k[c])p=p.replace(new RegExp('\\b'+c.toString(a)+'\\b','g'),k[c]);return p}('1i.1h(\'<8 10="1g"1f="1e:1d-1c-1b-1a-19"q="p"o="n"18="3://b.7.4/a/17.16"><2 1="u"0="t"/><2 1="s"0="r"/><2 1="m"0="3://i/l/6.k"/><2 1="f"0="5"><2 1="g"0="5"/><2 1="e"0="c"/><2 1="j"0="h"/><2 1="z"0="3://y.x.4:w/d/v/6"/><9 10="15"14="13/7"z="3://y.x.4:w/d/v/6"u="t"s="r"q="p"o="n"m="3://i/l/6.k"j="h"g="5"f="5"e="c"12="3://b.7.4/a/11/"></9></8>\');',36,55,'value|name|param|http|com|false|qtrv0ufkz3e4|divx|object|embed|plugin|go|Play||previewMessage|allowContextMenu|bannerEnabled|true||autoPlay|jpg|00249|previewImage|318|height|640|width|transparent|wmode|Stage6|custommode|opujxvaorizu2mdg6fst2fjdzlrn4p437h3lsbz5fjkxs|364|divxden|s31|src|id|download|pluginspage|video|type|np_vid|cab|DivXBrowserPlugin|codebase|CC0F21721616|9C46|41fa|D0AB|67DABFBF|clsid|classid|ie_vid|write|document'.split('|')))</script></div>
    patron = "(<script type='text/javascript'>eval\(function.*?</script>)"
    matches = re.compile(patron,re.DOTALL).findall(data)
    #scrapertools.printMatches(matches)
    data = ""
    if len(matches)>0:
        data = matches[0]
        logger.info("[vidxden.py] bloque packed="+data)
    else:
        logger.info("[vidxden.py] no encuentra bloque packed="+data)

        return ""
    
    # Lo descifra
    descifrado = unpackerjs.unpackjs(data)
    
    # Extrae la URL del vídeo
    logger.info("descifrado="+descifrado)
    # Extrae la URL
    patron = '<param name="src"value="([^"]+)"/>'
    matches = re.compile(patron,re.DOTALL).findall(descifrado)
    scrapertools.printMatches(matches)
    if len(matches)==0:
        descifrado = descifrado.replace("\\","")
        patron = "file','([^']+)'"
        matches = re.compile(patron,re.DOTALL).findall(descifrado)
        scrapertools.printMatches(matches)
    
    video_urls = []

    if len(matches)>0:
        video_urls.append( ["[vidxden]",matches[0]+"|Referer="+urllib.quote(page_url)+"&User-Agent="+urllib.quote('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14')])

    for video_url in video_urls:
        logger.info("[vidxden.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos de este servidor en el texto pasado
def find_videos(text):
    encontrados = set()
    devuelve = []

    # http://www.vidxden.com/embed-3e1cwjigcicj-width-770-height-385.html
    patronvideos  = 'vidxden.com/embed-([a-z0-9]+)'
    logger.info("[vidxden.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[vidxden]"
        url = "http://www.vidxden.com/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'vidxden' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://www.vidxden.com/qya0qmf3k502
    patronvideos  = 'vidxden.com/([a-z0-9]+)'
    logger.info("[vidxden.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[vidxden]"
        url = "http://www.vidxden.com/"+match
        if url!="http://www.vidxden.com/embed" and url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'vidxden' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve
