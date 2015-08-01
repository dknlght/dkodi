# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Megavideo server connector
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
# Python Video Decryption and resolving routines.
# Courtesy of Voinage, Coolblaze.
#------------------------------------------------------------
# Note:
# How to set a cookie or Header in XBMC player
# http://some/url|Cookie=<urlencodedcookie>&User-Agent=<urlencode dvalue>
import os
import re
import urlparse, urllib, urllib2

from core import scrapertools
from core import logger
from core import config

DEBUG = False

# Returns an array of possible video url's from the page_url, supporting premium user account and password protected video
def get_video_url( page_url , premium = False , user="" , password="", video_password="", megaupload_mirror=True ):
    logger.info("[megavideo.py] get_video_url( page_url='%s' , user='%s' , password='%s', video_password=%s)" % (page_url , user , "**************************"[0:len(password)] , video_password) )

    video_urls = []

    # If user has premium account, retrieve the cookie_id from the cookie store and passes to the request as parameter "u"
    if premium:
        logger.info("[megavideo.py] Modo premium, averigua la cookie")
        # Extrae la cookie del almacen
        #megavideo_cookie_id = get_megavideo_cookie_id()

        # Si no está, hace el login
        #if megavideo_cookie_id == "":
        #    logger.info("[megavideo.py] No hay cookie, hace login")
        megavideo_cookie_id = login(user, password)

        # Si aún así no está, la cuenta no es válida
        if megavideo_cookie_id == "":
            logger.info("[megavideo.py] No hay cookie de Megavideo válida (error en login o password?), pasa a modo Free")
            premium = False

    if premium:
        account_type = "(Premium) [megavideo]"
    else:
        account_type = "(Free) [megavideo]"

    '''
        video_urls.append( [ "SD (Free)"          , get_sd_video_url(page_url,premium,user,password,video_password) ] )
    else:
        do_login(premium,user,password)
        video_urls.append( [ "SD (Premium)"       , get_sd_video_url(page_url,premium,user,password,video_password) ] )
        video_urls.append( [ "Original (Premium)" , get_original_video_url(page_url,premium,user,password,video_password) ] )
    '''

    # Extract vídeo code from page URL
    # http://www.megavideo.com/?v=ABCDEFGH -> ABCDEFGH
    # Si es de megaupload como en http://www.megavideo.com/?d=ABCDEFGH -> convierte primero a formato v=
    megavideo_video_id = extract_video_id(page_url)

    if megavideo_video_id!="":
        # Base URL for obtaining Megavideo URL
        url = "http://www.megavideo.com/xml/videolink.php?v="+megavideo_video_id
    
        if premium:
            url = url + "&u="+megavideo_cookie_id
    
        # If video is password protected, it is sent with the request as parameter "password"
        if video_password!="":
            url = url + "&password="+video_password
    
        # Perform the request to Megavideo
        logger.info("[megavideo.py] calling Megavideo")
        data = scrapertools.cache_page( url , headers=[['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'],['Referer', 'http://www.megavideo.com/']] , )
    
        # Search for an SD link
        logger.info("[megavideo.py] SD Link")
        try:
            s = re.compile(' s="(.+?)"').findall(data)
            k1 = re.compile(' k1="(.+?)"').findall(data)
            k2 = re.compile(' k2="(.+?)"').findall(data)
            un = re.compile(' un="(.+?)"').findall(data)
            video_url = "http://www" + s[0] + ".megavideo.com/files/" + decrypt(un[0], k1[0], k2[0]) + "/?.flv"
            video_urls.append( ["SD "+account_type , video_url ])
        # Video is not available
        except:
            import sys
            for line in sys.exc_info():
                logger.error( "%s" % line )
            logger.info("[megavideo.py] Megavideo URL not valid, or video not available")
            return []
    
        # Search for an HD link if it exists
        logger.info("[megavideo.py] HD Link")
        hd = re.compile(' hd="(.+?)"').findall(data)
        if len(hd)>0 and hd[0]=="1":
            s = re.compile(' hd_s="(.+?)"').findall(data)
            k1 = re.compile(' hd_k1="(.+?)"').findall(data)
            k2 = re.compile(' hd_k2="(.+?)"').findall(data)
            un = re.compile(' hd_un="(.+?)"').findall(data)
            video_url = "http://www" + s[0] + ".megavideo.com/files/" + decrypt(un[0], k1[0], k2[0]) + "/?.flv"
            video_urls.append( ["HD "+account_type , video_url ])
    
        # If premium account, search for the original video link
        if premium:
            logger.info("[megavideo.py] ORIGINAL Link")
            url = "http://www.megavideo.com/xml/player_login.php?u="+megavideo_cookie_id+"&v="+megavideo_video_id+"&password="+video_password
            data2 = scrapertools.cache_page( url , headers=[['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.14) Gecko/20080404 Firefox/2.0.0.14'],['Referer', 'http://www.megavideo.com/']] , )
            logger.info(data2)
        
            patronvideos  = 'downloadurl="([^"]+)"'
            matches = re.compile(patronvideos,re.DOTALL).findall(data2)
            video_url = matches[0].replace("%3A",":").replace("%2F","/").replace("%20"," ")
            video_urls.append( ["ORIGINAL "+video_url[-4:]+" [megavideo]" , video_url ])
    
        # Truco http://www.protegerurl.com.es/v9v/00Z8VNVZ.flv
        #if not premium:
        #    logger.info("[megavideo.py] SIN LIMITE Link")
        #    video_urls.append( ["SIN LIMITE [megavideo]" , "http://www.protegerurl.com.es/v9v/"+megavideo_video_id+".flv" ])

        # Search for error conditions
        errortext = re.compile(' errortext="(.+?)"').findall(data)	
        if len(errortext)>0:
            password_required = re.compile('password_required="(.*?)"').findall(data)
            if len(password_required) > 0:
                # Launches an exception to force the user to input the password
                raise PasswordRequiredException()

    if page_url.startswith("http://www.megavideo.com/?d=") and megaupload_mirror:
        logger.info("[megavideo.py] Es una URL tipo Megaupload")
        from servers import megaupload
        video_urls.extend( megaupload.get_video_url( page_url.replace("megavideo.com","megaupload.com"), premium, user, password, megavideo_mirror=False ) )

    logger.info("[megavideo.py] Ended with %d links" % len(video_urls))

    return video_urls

# Extract vídeo code from page URL
# http://www.megavideo.com/?v=ABCDEFGH -> ABCDEFGH
def extract_video_id( page_url ):
    logger.info("[megavideo.py] extract_video_id(page_url="+page_url+")")
    
    if page_url.startswith('http://www.megavideo.com/?v='):
        patron = 'http://www.megavideo.com.*\?v\=([A-Z0-9a-z]{8})'
        matches = re.compile(patron,re.DOTALL).findall(page_url)
        video_id = matches[0]
    elif page_url.startswith('http://www.megavideo.com/?d='):
        patron = 'http://www.megavideo.com.*\?d\=([A-Z0-9a-z]{8})'
        matches = re.compile(patron,re.DOTALL).findall(page_url)
        video_id = matches[0]
        import megaupload
        video_id = megaupload.convertcode(video_id)
    else:
        video_id = page_url

    logger.info("[megavideo.py] video_id="+video_id)
    return video_id

# Get the Megavideo user ID (cookie) from the user and password credentials
def login(user, password):
    logger.info("[megavideo.py] login(user="+user+", password="+"**************************"[0:len(password)]+")")

    url = "http://www.megavideo.com/?c=login"
    post = "login=1&redir=1&username="+user+"&password="+urllib.quote(password)
    headers = [ ['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'],['Referer','http://www.megavideo.com/?s=signup'] ]
    data = scrapertools.cache_page(url=url, post=post)
    
    return get_megavideo_cookie_id()

def get_megavideo_cookie_id():
    logger.info("[megavideo.py] get_megavideo_cookie_id")

    cookie=""

    cookie_data = config.get_cookie_data()
    logger.info("cookie_data="+cookie_data)
    
    lines = cookie_data.split("\n")
    for line in lines:
        logger.info("line="+line)
    
        if "megavideo.com" in line:
            logger.info("[megavideo.py] patron1")
            patron = 'user="([^"]+)"'
            matches = re.compile(patron,re.DOTALL).findall(line)
        
            if len(matches)>0:
                cookie = matches[0]
                break
            else:
                logger.info("[megavideo.py] patron2")
                patron = 'user=([^\;]+);'
                matches = re.compile(patron,re.DOTALL).findall(line)
                if len(matches)>0:
                    cookie = matches[0]
                    break
                else:
                    logger.info("[megavideo.py] No se ha encontrado la cookie de Megavideo")
                    cookie=""
    
    logger.info("cookie="+cookie)
        
    return cookie

# Megavideo decryption routines
def ajoin(arr):
    strtest = ''
    for num in range(len(arr)):
        strtest = strtest + str(arr[num])
    return strtest

def asplit(mystring):
    arr = []
    for num in range(len(mystring)):
        arr.append(mystring[num])
    return arr
        
def decrypt(str1, key1, key2):

    __reg1 = []
    __reg3 = 0
    while (__reg3 < len(str1)):
        __reg0 = str1[__reg3]
        holder = __reg0
        
        # Optimización de aabilio@gmail.com :)
        for i in range(16):

            if i == 0:
                tmp = holder
            else:
                tmp = __reg0

            if tmp == hex(i).split("x")[1]:
                __reg1.append("".join([str((i >> y) & 1) for y in range(3, -1, -1)]))
                break

        __reg3 = __reg3 + 1

    mtstr = ajoin(__reg1)
    __reg1 = asplit(mtstr)
    __reg6 = []
    __reg3 = 0
    while (__reg3 < 384):
    
        key1 = (int(key1) * 11 + 77213) % 81371
        key2 = (int(key2) * 17 + 92717) % 192811
        __reg6.append((int(key1) + int(key2)) % 128)
        __reg3 = __reg3 + 1
    
    __reg3 = 256
    while (__reg3 >= 0):

        __reg5 = __reg6[__reg3]
        __reg4 = __reg3 % 128
        __reg8 = __reg1[__reg5]
        __reg1[__reg5] = __reg1[__reg4]
        __reg1[__reg4] = __reg8
        __reg3 = __reg3 - 1
    
    __reg3 = 0
    while (__reg3 < 128):
    
        __reg1[__reg3] = int(__reg1[__reg3]) ^ int(__reg6[__reg3 + 256]) & 1
        __reg3 = __reg3 + 1

    __reg12 = ajoin(__reg1)
    __reg7 = []
    __reg3 = 0
    while (__reg3 < len(__reg12)):

        __reg9 = __reg12[__reg3:__reg3 + 4]
        __reg7.append(__reg9)
        __reg3 = __reg3 + 4
        
    
    __reg2 = []
    __reg3 = 0
    while (__reg3 < len(__reg7)):
        __reg0 = __reg7[__reg3]
        holder2 = __reg0

        # Optimización de aabilio@gmail.com :)
        for i in range(16):
            if i == 0:
                tmp = holder2
            else:
                tmp = __reg0

            if tmp == "".join([str((i >> y) & 1) for y in range(3, -1, -1)]):
                __reg2.append(hex(i).split("x")[1])
                break

        __reg3 = __reg3 + 1

    endstr = ajoin(__reg2)
    return endstr

# Encuentra vídeos de megavideo en el texto pasado
# Los devuelve con URL "http://www.megavideo.com/?v=AQW9ED93"
def find_videos(data):
    encontrados = set()
    devuelve = []

    #Megavideo con partes para cinetube
    #id="http://www.megavideo.com/?v=CN7DWZ8S"><a href="#parte1">Parte 1 de 2</a></li>
    patronvideos = 'id.+?http://www.megavideo.com..v.(.+?)".+?(parte\d+)'
    logger.info("[megavideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos).findall(data)
    for match in matches:
        titulo = "[Megavideo " + match[1] + "]"
        url = "http://www.megavideo.com/?v="+match[0]
        if url not in encontrados:
            logger.info(" url="+url)
            devuelve.append( [ titulo , url , 'megavideo' ] )
            encontrados.add(url)
        else:
            logger.info(" url duplicada="+url)

    # Megavideo - Vídeos con título
    patronvideos  = '<div[^>]+>([^<]+)<.*?<param name="movie" value="http://www.megavideo.com/v/([A-Z0-9a-z]{8})[^"]+"'
    logger.info("[megavideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = match[0].strip()
        if titulo == "":
            titulo = "[Megavideo]"
        url = "http://www.megavideo.com/?v="+match[1]
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'megavideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # Megavideo - Vídeos con título
    patronvideos  = '<a href\="http\:\/\/www.megavideo.com/\?v\=([A-Z0-9a-z]{8})".*?>([^<]+)</a>'
    logger.info("[megavideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = match[1].strip()
        if titulo == "":
            titulo = "[Megavideo]"
        url = "http://www.megavideo.com/?v="+match[0]
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'megavideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # Megavideo - Vídeos sin título
    patronvideos  = 'http\:\/\/www.megavideo.com/.*?\?v\=([A-Z0-9a-z]{8})'
    logger.info("[megavideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for match in matches:
        titulo = ""
        if titulo == "":
            titulo = "[Megavideo]"
        url = "http://www.megavideo.com/?v="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'megavideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # Megavideo - Vídeos sin título
    #http://wwwstatic.megavideo.com/mv_player.swf?v=HFZMTQ9N
    patronvideos  = 'megavideo.com/mv_player.swf\?v\=([A-Z0-9a-z]{8})'
    logger.info("[megavideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Megavideo]"
        url = "http://www.megavideo.com/?v="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'megavideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # Megavideo - Vídeos sin título
    patronvideos  = "www.megavideo.com.*?mv_player.swf.*?v(?:=|%3D)(\w{8})"
    logger.info("[megavideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Megavideo]"
        url = "http://www.megavideo.com/?v="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'megavideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # Megavideo - Vídeos sin título
    patronvideos  = 'http://www.megavideo.com/v/([A-Z0-9a-z]{8})'
    logger.info("[megavideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[Megavideo]"
        url = "http://www.megavideo.com/?v="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'megavideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # Megavideo - Vídeos con título
    patronvideos  = '<a href="http://www.megavideo.com/\?v\=([^"]+)".*?>(.*?)</a>'
    logger.info("[megavideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    for match in matches:
        titulo = match[1].strip()
        if titulo == "":
            titulo = "[Megavideo]"
        url = "http://www.megavideo.com/?v="+match[0]
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'megavideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # Megavideo - Vídeos con título
    patronvideos  = '<param name="movie" value=".*?v\=([A-Z0-9a-z]{8})" />'
    logger.info("[megavideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    for match in matches:
        titulo = "[Megavideo]"
        url = "http://www.megavideo.com/?v="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'megavideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # Megavideo... formato watchanimeon")
    patronvideos  = 'src="http://wwwstatic.megavideo.com/mv_player.swf.*?\&v\=([^"]+)"'
    logger.info("[megavideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    for match in matches:
        titulo = "[Megavideo]"
        url = "http://www.megavideo.com/?v="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'megavideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # Megavideo... parámetro megaupload ?d
    # http://www.megavideo.com/?d=0I8GDC55
    patronvideos  = 'http://www.megavideo.com/\?d\=([A-Z0-9a-z]{8})'
    logger.info("[megavideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        #import megaupload
        #megavideo_code = megaupload.convertcode(match)
        #if megavideo_code<>"":
        titulo = "[Megavideo]"
        url = "http://www.megavideo.com/?d="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'megavideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # Megavideo... formato cine-adicto")
    patronvideos = '<div style="visibility:hidden;" id="megaid">(.*?)&langid.*?</div>'
    logger.info("[megavideo.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    for match in matches:
        titulo = "[Megavideo]"
        url = "http://www.megavideo.com/?d="+match.strip()
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'megavideo' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

if __name__ == "__main__":
    import getopt
    import sys
    options, arguments = getopt.getopt(sys.argv[1:], "", ["video_url=","login=","password="])
    
    video_url = ""
    login = ""
    password = ""
    
    logger.info("%s %s" % (str(options),str(arguments)))
    
    for option, argument in options:
        print option,argument
        if option == "--video_url":
            video_url = argument
        elif option == "--login":
            login = argument
        elif option == "--password":
            password = argument
        else:
            assert False, "Opcion desconocida"

    if video_url=="":
        print "ejemplo de invocacion"
        print "megavideo --video_url http://www.megavideo.com/?v=ABCDEFGH --login usuario --password secreto"
    else:
        
        if login!="":
            premium=True
        else:
            premium=False
        
        print get_video_url(video_url,premium,login,password)
