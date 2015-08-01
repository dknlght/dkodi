# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para Megaupload
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import re
import urlparse, urllib, urllib2
import exceptions

from core import scrapertools
from core import logger
from core import config

DEBUG=False

PREMIUM=0
GRATIS=1
ANONIMO=2

def get_video_url( page_url , premium = False , user="" , password="" , video_password="", megavideo_mirror=True, verify=True ):
    logger.info("[megaupload.py] get_video_url( page_url='%s' , user='%s' , password='%s', video_password=%s)" % (page_url , user , "**************************"[0:len(password)] , video_password) )
    video_urls = []

    # Si sólo viene el código, se convierte a URL completa
    if len(page_url)==8:
        page_url = "http://www.megaupload.com/?d="+page_url

    # Obtiene el enlace para Megavideo
    if megavideo_mirror:
        try:
            megavideo_video_id = convertcode(page_url)
            if not megavideo_video_id=="":
                from servers import megavideo
                video_urls.extend( megavideo.get_video_url( megavideo_video_id, premium, user, password, megaupload_mirror=False ) )
        except:
            pass

    # page_url es del tipo "http://www.megaupload.com/?d="+code
    # Si el usuario es premium utiliza el método antiguo
    # Si el usuario es gratis o anónimo utiliza el método nuevo
    if premium:
        logger.info("[megaupload.py] Modo premium, averigua la cookie")
        #cookie = get_megaupload_cookie()
        cookie=""

        if cookie=="":
            #logger.info("[megaupload.py] No hay cookie, hace login")
            tipo_usuario , cookie = login(user,password)
            #logger.info("[megaupload.py] No hay cookie de Megaupload válida (error en login o password?)")
        else:
            tipo_usuario=PREMIUM
        
        # Obtiene el enlace para Megaupload
        if premium:
            video_url = get_premium_video_url(page_url,cookie,video_password,verify)
            if video_url!="":
                extension = video_url[-4:]
                video_urls.append( ['%s (Premium) [megaupload]' % extension , video_url] )
        else:
            tipo_usuario=GRATIS
            video_url = get_free_video_url(page_url,tipo_usuario,video_password)
            if video_url!="":
                extension = video_url[-4:]
                video_urls.append ( ['%s (Free) [megaupload]' % extension , video_url, 60] )
    else:
        logger.info("[megaupload.py] Modo free")
        video_url = get_free_video_url(page_url,ANONIMO,video_password)
        logger.info("[megaupload.py] video_url=%s" % video_url)
        if video_url!="":
            extension = video_url[-4:]
            video_urls.append( ['%s (Free) [megaupload]' % extension , video_url, 60] )

    #logger.info("[megaupload.py] get_video_urls returns %s" % video_url)
    
    return video_urls

# Extrae directamente la URL del vídeo de Megaupload
def login(user,password):
    logger.info("[megaupload.py] login( user='%s' , password='%s')" % (user , "**************************"[0:len(password)]) )

    # Parámetros
    url="http://www.megaupload.com/?c=login"
    post = "login=1&redir=1&username="+user+"&password="+urllib.quote(password)
    headers = [['User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'],['Referer','http://www.megaupload.com']]

    # Invocación
    data = scrapertools.cache_page(url=url,post=post,headers=headers,modo_cache=scrapertools.CACHE_NUNCA)

    # Extrae el tipo de usuario
    login = re.search('Welcome', data)
    premium = re.search('flashvars.status = "premium";', data)        

    # Si no está el welcome, no es una cuenta válida
    if login is None:
        tipo_usuario = ANONIMO
    else:
        # Si no es premium, es una cuenta gratis
        if premium is None:
            tipo_usuario = GRATIS
        else:
            tipo_usuario = PREMIUM
    
    # Saca la cookie del fichero
    cookie = get_megaupload_cookie()

    usuarios = ['PREMIUM','GRATIS','ANONIMO']
    logger.info("[megaupload.py] login returns tipo_usuario=%d (%s), cookie=%s" % (tipo_usuario , usuarios[tipo_usuario] , cookie) )

    return tipo_usuario , cookie

def get_megaupload_cookie():
    logger.info("[megaupload.py] get_megaupload_cookie")
    cookie_data = config.get_cookie_data()
    patron  = 'user="([^"]+)".*?domain=".megaupload.com"'
    matches = re.compile(patron,re.DOTALL).findall(cookie_data)
    
    if len(matches)==0:
        patron  = 'user=([^\;]+);.*?domain=".megaupload.com"'
        matches = re.compile(patron,re.DOTALL).findall(cookie_data)
        
    if len(matches)==0:
        cookie = ""
    else:
        cookie = matches[0]
    
    return cookie

class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        raise ImportError(302,headers.getheader("Location"))

def get_premium_video_url(page_url,cookie,video_password,verify):
    logger.info("[megaupload.py] get_premium_video_url( page_url='%s' , cookie=%s )" % (page_url , "********************************************************************************************************************************************************************************************************************************************************************"[0:len(cookie)]))

    req = urllib2.Request(page_url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    req.add_header('Cookie', 'l=es; user='+cookie)
    try:
        opener = urllib2.build_opener(SmartRedirectHandler())
        response = opener.open(req)
    except ImportError, inst:
        status,mediaurl=inst
        logger.info("[megaupload.py] detectado redirect 302, mediaurl=%s" % mediaurl)
    else:
        logger.info("[megaupload.py] descarga la página y busca la url")
        data=response.read()
        response.close()
        patronvideos  = '<a href="([^"]+)" class="download_premium_but">'
        matches = re.compile(patronvideos,re.DOTALL).findall(data)
        #scrapertools.printMatches(matches)
        mediaurl = ""
        if len(matches)>0:
            mediaurl = matches[0]
            if verify:
                logger.info("[megaupload.py] verifica la URL %s" % mediaurl)
                # Timeout del socket a 60 segundos
                import socket
                socket.setdefaulttimeout(10)
    
                h=urllib2.HTTPHandler(debuglevel=0)
                request = urllib2.Request(mediaurl)
    
                opener = urllib2.build_opener(h)
                urllib2.install_opener(opener)
                try:
                    connexion = opener.open(request)
                    mediaurl= connexion.geturl()
                    logger.info("[megaupload.py] ->mediaurl="+mediaurl)
    
                except urllib2.HTTPError,e:
                    logger.error( "[megaupload.py]  error %d (%s) al abrir la url %s" % (e.code,e.msg,mediaurl) )
                    logger.error(e.read())
            else:
                logger.info("[megaupload.py] -> mediaurl=%s" % mediaurl)

    return mediaurl

def get_free_video_url(page_url , tipo_usuario , video_password=None):
    logger.info("[megaupload.py] get_free_video_url( page_url='%s', tipo_usuario=%d, video_password='%s' )" % (page_url,tipo_usuario,str(video_password)))

    # Descarga la página de MU
    data = scrapertools.cache_page(page_url,modo_cache=scrapertools.CACHE_NUNCA)
    logger.info("data="+data)
    
    # Si tiene password lo pide
    password_data = re.search('filepassword',data)
    if password_data is not None:
        logger.info("[megaupload.py] Es un video con PASSWORD")
        teclado = password_mega(video_password)
        
        # Vuelve a descargar la página con password
        if teclado is not None:
            data = scrapertools.cache_page(page_url, post="filepassword="+teclado,modo_cache=scrapertools.CACHE_NUNCA)
        else:
            #print data
            return ""

    # Comprueba si es un enlace premium
    match1=re.compile('<a href="([^"]+)" class="download_regular_usual"').findall(data)
    if str(match1)=='[]':
        match2=re.compile('id="downloadlink"><a href="(.+?)" class=').findall(data)
        try:
            url=match2[0]
        except:
            logger.info("[megaupload.py] Es un enlace PREMIUM, no puedes acceder a él sin cuenta")
            #print data
            return ""
    else:
        url=match1[0]

    # TODO ¿?
    #Si es un archivo .divx lo sustituye por .avi
    if url.endswith('divx'):
        url = url[:-4]+'avi'

    #if url=="":
    #    print data
    return url

def password_mega(password):
    logger.info ("[megaupload.py] password_mega")

    try:
        if password is not None:
            keyboard = xbmc.Keyboard(password,"Contraseña:")
        else:
            keyboard = xbmc.Keyboard("","Contraseña:")
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            tecleado = keyboard.getText()
            if len(tecleado)<=0:
                return
            else:
                return tecleado
    except:
        return None

# Convierte el código de megaupload a megavideo
def convertcode(megaupload_page_url):
    logger.info("[megaupload.py] convertcode "+megaupload_page_url)

    # Si sólo viene el código, convierte a URL completa
    if len(megaupload_page_url)==8:
        megaupload_page_url = "http://www.megaupload.com/?d="+megaupload_page_url

    # Descarga la página de megavideo pasándole el código de megaupload
    url = megaupload_page_url.replace("megaupload","megavideo")
    data = scrapertools.cache_page(url,modo_cache=scrapertools.CACHE_NUNCA)
    #logger.info(data)

    # Extrae las entradas (carpetas)
    patronvideos  = 'flashvars.v = "([^"]+)"'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    #scrapertools.logger.infoMatches(matches)
    
    megavideocode = ""
    if len(matches)>0:
        megavideocode = matches[0]

    logger.info("[megaupload.py] convertcode returns #%s#" % megavideocode)

    return megavideocode

def getlowurl(code , password=None):
    import megavideo
    return megavideo.getlowurl(convertcode(code),password)

# Encuentra vídeos de megaupload en el texto pasado
# Los devuelve con URL "http://www.megaupload.com/?d=AQW9ED93"
def find_videos(text):
    encontrados = set()
    devuelve = []

    patronvideos  = '<a.*?href="http://www.megaupload.com/\?d=([A-Z0-9a-z]{8})".*?>(.*?)</a>'
    logger.info("[megaupload.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos).findall(text)
    for match in matches:
        titulo = scrapertools.htmlclean(match[1].strip())+" [Megaupload]"
        url = "http://www.megaupload.com/?d="+match[0]
        if url not in encontrados:
            logger.info("  titulo="+titulo)
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'megaupload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
    
    patronvideos  = 'www.megaupload.com/(?:es/)?\?.*?d\=([A-Z0-9a-z]{8})(?:[^>]*>([^<]+)</a>)?'
    logger.info("[megaupload.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos).findall(text)
    for match in matches:
        if match[1]<>"":
            titulo = match[1].strip()+" - [Megaupload]"
        else:
            titulo = "[Megaupload]"
        url = "http://www.megaupload.com/?d="+match[0]
        if url not in encontrados:
            logger.info("  titulo="+titulo)
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'megaupload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # Código especial cinetube
    #xrxa("BLYT2ZC9=d?/moc.daolpuagem.www//:ptth")
    patronvideos  = 'xrxa\("([A-Z0-9a-z]{8})=d\?/moc.daolpuagem.www//\:ptth"\)'
    logger.info("[megaupload.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos).findall(text)
    for match in matches:
        titulo = "[Megaupload]"
        url = "http://www.megaupload.com/?d="+match[::-1]
        if url not in encontrados:
            logger.info("  titulo="+titulo)
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'megaupload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos  = 'http://www.megavideo.com/\?d\=([A-Z0-9a-z]{8})'
    logger.info("[megaupload.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(text)

    for match in matches:
        titulo = "[Megaupload]"
        url = "http://www.megaupload.com/?d="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'megaupload' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve