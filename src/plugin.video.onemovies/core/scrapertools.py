﻿#------------------------------------------------------------
# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Download Tools
# Based on the code from VideoMonkey XBMC Plugin
#------------------------------------------------------------
# pelisalacarta
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
# Creado por:
# Jesús (tvalacarta@gmail.com)
# jurrabi (jurrabi@gmail.com)
# bandavi (xbandavix@gmail.com)
# Licencia: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------
# Historial de cambios:
#------------------------------------------------------------

import urlparse,urllib2,urllib
import time
import os
import config
import logger
import re
import socket

logger.info("[scrapertools.py] init")

# True - Muestra las cabeceras HTTP en el log
# False - No las muestra
DEBUG_LEVEL = True

CACHE_ACTIVA = "0"  # Automatica
CACHE_SIEMPRE = "1" # Cachear todo
CACHE_NUNCA = "2"   # No cachear nada

CACHE_PATH = config.get_setting("cache.dir")
logger.info("[scrapertools.py] CACHE_PATH="+CACHE_PATH)

DEBUG = False

def cache_page(url,post=None,headers=[['User-Agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12']],modo_cache=CACHE_ACTIVA, timeout=socket.getdefaulttimeout()):
    return cachePage(url,post,headers,modo_cache,timeout=timeout)

# TODO: (3.1) Quitar el parámetro modoCache (ahora se hace por configuración)
# TODO: (3.2) Usar notación minusculas_con_underscores para funciones y variables como recomienda Python http://www.python.org/dev/peps/pep-0008/
def cachePage(url,post=None,headers=[['User-Agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12']],modoCache=CACHE_ACTIVA, timeout=socket.getdefaulttimeout()):
    logger.info("[scrapertools.py] cachePage url="+url)
    modoCache = config.get_setting("cache.mode")

    '''
    if config.get_platform()=="plex":
        from PMS import HTTP
        try:
            logger.info("url="+url)
            data = HTTP.Request(url)
            logger.info("descargada")
        except:
            data = ""
            logger.error("Error descargando "+url)
            import sys
            for line in sys.exc_info():
                logger.error( "%s" % line )
        
        return data
    '''
    # CACHE_NUNCA: Siempre va a la URL a descargar
    # obligatorio para peticiones POST
    if modoCache == CACHE_NUNCA or post is not None:
        logger.info("[scrapertools.py] MODO_CACHE=2 (no cachear)")
        
        try:
            data = downloadpage(url,post,headers, timeout=timeout)
        except:
            data=""
    
    # CACHE_SIEMPRE: Siempre descarga de cache, sin comprobar fechas, excepto cuando no está
    elif modoCache == CACHE_SIEMPRE:
        logger.info("[scrapertools.py] MODO_CACHE=1 (cachear todo)")
        
        # Obtiene los handlers del fichero en la cache
        cachedFile, newFile = getCacheFileNames(url)
    
        # Si no hay ninguno, descarga
        if cachedFile == "":
            logger.debug("[scrapertools.py] No está en cache")
    
            # Lo descarga
            data = downloadpage(url,post,headers)
    
            # Lo graba en cache
            outfile = open(newFile,"w")
            outfile.write(data)
            outfile.flush()
            outfile.close()
            logger.info("[scrapertools.py] Grabado a " + newFile)
        else:
            logger.info("[scrapertools.py] Leyendo de cache " + cachedFile)
            infile = open( cachedFile )
            data = infile.read()
            infile.close()
    
    # CACHE_ACTIVA: Descarga de la cache si no ha cambiado
    else:
        logger.info("[scrapertools.py] MODO_CACHE=0 (automática)")
        
        # Datos descargados
        data = ""
        
        # Obtiene los handlers del fichero en la cache
        cachedFile, newFile = getCacheFileNames(url)
    
            # Lo descarga
        data = downloadpage(url,post,headers)
            
            # Lo graba en cache
        outfile = open(newFile,"w")
        outfile.write(data)
        outfile.flush()
        outfile.close()
        logger.info("[scrapertools.py] Grabado a " + newFile)
    
      
    return data

def getCacheFileNames(url):

    # Obtiene el directorio de la cache para esta url
    siteCachePath = getSiteCachePath(url)
        
    # Obtiene el ID de la cache (md5 de la URL)
    cacheId = get_md5(url)
        
    logger.debug("[scrapertools.py] cacheId="+cacheId)

    # Timestamp actual
    nowtimestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
    logger.debug("[scrapertools.py] nowtimestamp="+nowtimestamp)

    # Nombre del fichero
    # La cache se almacena en una estructura CACHE + URL
    ruta = os.path.join( siteCachePath , cacheId[:2] , cacheId[2:] )
    newFile = os.path.join( ruta , nowtimestamp + ".cache" )
    logger.debug("[scrapertools.py] newFile="+newFile)
    if not os.path.exists(ruta):
        os.makedirs( ruta )

    # Busca ese fichero en la cache
    cachedFile = getCachedFile(siteCachePath,cacheId)

    return cachedFile, newFile 

# Busca ese fichero en la cache
def getCachedFile(siteCachePath,cacheId):
    mascara = os.path.join(siteCachePath,cacheId[:2],cacheId[2:],"*.cache")
    logger.debug("[scrapertools.py] mascara="+mascara)
    import glob
    ficheros = glob.glob( mascara )
    logger.debug("[scrapertools.py] Hay %d ficheros con ese id" % len(ficheros))

    cachedFile = ""

    # Si hay más de uno, los borra (serán pruebas de programación) y descarga de nuevo
    if len(ficheros)>1:
        logger.debug("[scrapertools.py] Cache inválida")
        for fichero in ficheros:
            logger.debug("[scrapertools.py] Borrando "+fichero)
            os.remove(fichero)
        
        cachedFile = ""

    # Hay uno: fichero cacheado
    elif len(ficheros)==1:
        cachedFile = ficheros[0]

    return cachedFile

def getSiteCachePath(url):
    # Obtiene el dominio principal de la URL    
    dominio = urlparse.urlparse(url)[1]
    logger.debug("[scrapertools.py] dominio="+dominio)
    nombres = dominio.split(".")
    if len(nombres)>1:
        dominio = nombres[len(nombres)-2]+"."+nombres[len(nombres)-1]
    else:
        dominio = nombres[0]
    logger.debug("[scrapertools.py] dominio="+dominio)
    
    # Crea un directorio en la cache para direcciones de ese dominio
    siteCachePath = os.path.join( CACHE_PATH , dominio )
    if not os.path.exists(CACHE_PATH):
        try:
            os.mkdir( CACHE_PATH )
        except:
            logger.error("[scrapertools.py] Error al crear directorio "+CACHE_PATH)

    if not os.path.exists(siteCachePath):
        try:
            os.mkdir( siteCachePath )
        except:
            logger.error("[scrapertools.py] Error al crear directorio "+siteCachePath)
    
    logger.debug("[scrapertools.py] siteCachePath="+siteCachePath)

    return siteCachePath

def cachePage2(url,headers):

    logger.info("Descargando " + url)
    inicio = time.clock()
    req = urllib2.Request(url)
    for header in headers:
        logger.info(header[0]+":"+header[1])
        req.add_header(header[0], header[1])

    try:
        response = urllib2.urlopen(req)
    except:
        req = urllib2.Request(url.replace(" ","%20"))
        for header in headers:
            logger.info(header[0]+":"+header[1])
            req.add_header(header[0], header[1])
        response = urllib2.urlopen(req)
    data=response.read()
    response.close()
    fin = time.clock()
    logger.info("Descargado en %d segundos " % (fin-inicio+1))

    '''
        outfile = open(localFileName,"w")
        outfile.write(data)
        outfile.flush()
        outfile.close()
        logger.info("Grabado a " + localFileName)
    '''
    return data

def cachePagePost(url,post):

    logger.info("Descargando " + url)
    inicio = time.clock()
    req = urllib2.Request(url,post)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')

    try:
        response = urllib2.urlopen(req)
    except:
        req = urllib2.Request(url.replace(" ","%20"),post)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
    data=response.read()
    response.close()
    fin = time.clock()
    logger.info("Descargado en %d segundos " % (fin-inicio+1))

    '''
        outfile = open(localFileName,"w")
        outfile.write(data)
        outfile.flush()
        outfile.close()
        logger.info("Grabado a " + localFileName)
    '''
    return data

class NoRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        infourl = urllib.addinfourl(fp, headers, req.get_full_url())
        infourl.status = code
        infourl.code = code
        return infourl
    http_error_300 = http_error_302
    http_error_301 = http_error_302
    http_error_303 = http_error_302
    http_error_307 = http_error_302

def downloadpage(url,post=None,headers=[['User-Agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12']],follow_redirects=True, timeout=socket.getdefaulttimeout()):
    logger.info("[scrapertools.py] downloadpage")
    logger.info("[scrapertools.py] url="+url)
    
    if post is not None:
        logger.info("[scrapertools.py] post="+post)
    else:
        logger.info("[scrapertools.py] post=None")
    
    # ---------------------------------
    # Instala las cookies
    # ---------------------------------

    #  Inicializa la librería de las cookies
    ficherocookies = os.path.join( config.get_setting("cookies.dir"), 'cookies.dat' )
    logger.info("[scrapertools.py] ficherocookies="+ficherocookies)

    cj = None
    ClientCookie = None
    cookielib = None

    # Let's see if cookielib is available
    try:
        logger.info("[scrapertools.py] Importando cookielib")
        import cookielib
    except ImportError:
        logger.info("[scrapertools.py] cookielib no disponible")
        # If importing cookielib fails
        # let's try ClientCookie
        try:
            logger.info("[scrapertools.py] Importando ClientCookie")
            import ClientCookie
        except ImportError:
            logger.info("[scrapertools.py] ClientCookie no disponible")
            # ClientCookie isn't available either
            urlopen = urllib2.urlopen
            Request = urllib2.Request
        else:
            logger.info("[scrapertools.py] ClientCookie disponible")
            # imported ClientCookie
            urlopen = ClientCookie.urlopen
            Request = ClientCookie.Request
            cj = ClientCookie.MozillaCookieJar()

    else:
        logger.info("[scrapertools.py] cookielib disponible")
        # importing cookielib worked
        urlopen = urllib2.urlopen
        Request = urllib2.Request
        cj = cookielib.MozillaCookieJar()
        # This is a subclass of FileCookieJar
        # that has useful load and save methods

    if cj is not None:
    # we successfully imported
    # one of the two cookie handling modules
        logger.info("[scrapertools.py] Hay cookies")

        if os.path.isfile(ficherocookies):
            logger.info("[scrapertools.py] Leyendo fichero cookies")
            # if we have a cookie file already saved
            # then load the cookies into the Cookie Jar
            try:
                cj.load(ficherocookies)
            except:
                logger.info("[scrapertools.py] El fichero de cookies existe pero es ilegible, se borra")
                os.remove(ficherocookies)

        # Now we need to get our Cookie Jar
        # installed in the opener;
        # for fetching URLs
        if cookielib is not None:
            logger.info("[scrapertools.py] opener usando urllib2 (cookielib)")
            # if we use cookielib
            # then we get the HTTPCookieProcessor
            # and install the opener in urllib2
            if not follow_redirects:
                opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=DEBUG_LEVEL),urllib2.HTTPCookieProcessor(cj),NoRedirectHandler())
            else:
                opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=DEBUG_LEVEL),urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)

        else:
            logger.info("[scrapertools.py] opener usando ClientCookie")
            # if we use ClientCookie
            # then we get the HTTPCookieProcessor
            # and install the opener in ClientCookie
            opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cj))
            ClientCookie.install_opener(opener)

    # -------------------------------------------------
    # Cookies instaladas, lanza la petición
    # -------------------------------------------------

    # Contador
    inicio = time.clock()

    # Diccionario para las cabeceras
    txheaders = {}

    # Construye el request
    if post is None:
        logger.info("[scrapertools.py] petición GET")
    else:
        logger.info("[scrapertools.py] petición POST")
    
    # Añade las cabeceras
    logger.info("[scrapertools.py] ---------------------------")
    for header in headers:
        logger.info("[scrapertools.py] header %s=%s" % (str(header[0]),str(header[1])) )
        txheaders[header[0]]=header[1]
    logger.info("[scrapertools.py] ---------------------------")

    req = Request(url, post, txheaders)

    try:

        if timeout is None:
            handle=urlopen(req)
        else:        
            #Para todas las versiones:
            deftimeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(timeout)
            handle=urlopen(req)            
            socket.setdefaulttimeout(deftimeout)
        
        # Actualiza el almacén de cookies
        cj.save(ficherocookies)

        # Lee los datos y cierra
        if handle.info().get('Content-Encoding') == 'gzip':
            logger.info("[scrapertools.py] gzipped")
            fin = inicio
            import StringIO
            data=handle.read()
            compressedstream = StringIO.StringIO(data)
            import gzip
            gzipper = gzip.GzipFile(fileobj=compressedstream)
            data = gzipper.read()
            gzipper.close()
            fin = time.clock()
        else:
            logger.info("[scrapertools.py] normal")
            data = handle.read()
    except urllib2.HTTPError,e:
        logger.info("error "+repr(e))
        import traceback
        traceback.print_exc()
        data = e.read()
        #logger.info("data="+repr(data))
        return data

    info = handle.info()
    logger.info("[scrapertools.py] Respuesta")
    logger.info("[scrapertools.py] ---------------------------")
    for header in info:
        logger.info("[scrapertools.py] "+header+"="+info[header])
    handle.close()
    logger.info("[scrapertools.py] ---------------------------")

    '''
    # Lanza la petición
    try:
        response = urllib2.urlopen(req)
    # Si falla la repite sustituyendo caracteres especiales
    except:
        req = urllib2.Request(url.replace(" ","%20"))
    
        # Añade las cabeceras
        for header in headers:
            req.add_header(header[0],header[1])

        response = urllib2.urlopen(req)
    '''
    
    # Tiempo transcurrido
    fin = time.clock()
    logger.info("[scrapertools.py] Descargado en %d segundos " % (fin-inicio+1))

    return data

def downloadpagewithcookies(url):
    # ---------------------------------
    # Instala las cookies
    # ---------------------------------

    #  Inicializa la librería de las cookies
    ficherocookies = os.path.join( config.get_data_path(), 'cookies.dat' )
    logger.info("[scrapertools.py] Cookiefile="+ficherocookies)

    cj = None
    ClientCookie = None
    cookielib = None

    # Let's see if cookielib is available
    try:
        import cookielib
    except ImportError:
        # If importing cookielib fails
        # let's try ClientCookie
        try:
            import ClientCookie
        except ImportError:
            # ClientCookie isn't available either
            urlopen = urllib2.urlopen
            Request = urllib2.Request
        else:
            # imported ClientCookie
            urlopen = ClientCookie.urlopen
            Request = ClientCookie.Request
            cj = ClientCookie.MozillaCookieJar()

    else:
        # importing cookielib worked
        urlopen = urllib2.urlopen
        Request = urllib2.Request
        cj = cookielib.MozillaCookieJar()
        # This is a subclass of FileCookieJar
        # that has useful load and save methods

    if cj is not None:
    # we successfully imported
    # one of the two cookie handling modules

        if os.path.isfile(ficherocookies):
            # if we have a cookie file already saved
            # then load the cookies into the Cookie Jar
            try:
                cj.load(ficherocookies)
            except:
                logger.info("[scrapertools.py] El fichero de cookies existe pero es ilegible, se borra")
                os.remove(ficherocookies)

        # Now we need to get our Cookie Jar
        # installed in the opener;
        # for fetching URLs
        if cookielib is not None:
            # if we use cookielib
            # then we get the HTTPCookieProcessor
            # and install the opener in urllib2
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)

        else:
            # if we use ClientCookie
            # then we get the HTTPCookieProcessor
            # and install the opener in ClientCookie
            opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cj))
            ClientCookie.install_opener(opener)

    #print "-------------------------------------------------------"
    theurl = url
    # an example url that sets a cookie,
    # try different urls here and see the cookie collection you can make !

    #txheaders =  {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3',
    #              'Referer':'http://www.megavideo.com/?s=signup'}
    txheaders =  {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Host':'www.meristation.com',
    'Accept-Language':'es-es,es;q=0.8,en-us;q=0.5,en;q=0.3',
    'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Keep-Alive':'300',
    'Connection':'keep-alive'}

    # fake a user agent, some websites (like google) don't like automated exploration

    req = Request(theurl, None, txheaders)
    handle = urlopen(req)
    cj.save(ficherocookies) # save the cookies again

    data=handle.read()
    handle.close()

    return data
    
def downloadpageWithoutCookies(url):
    logger.info("[scrapertools.py] Descargando " + url)
    inicio = time.clock()
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; es-ES; rv:1.9.0.14) Gecko/2009082707 Firefox/3.0.14')
    req.add_header('X-Requested-With','XMLHttpRequest')
    try:
        response = urllib2.urlopen(req)
    except:
        req = urllib2.Request(url.replace(" ","%20"))
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 6.0; es-ES; rv:1.9.0.14) Gecko/2009082707 Firefox/3.0.14')

        response = urllib2.urlopen(req)
    data=response.read()
    response.close()
    fin = time.clock()
    logger.info("[scrapertools.py] Descargado en %d segundos " % (fin-inicio+1))
    return data
    

def downloadpageGzip(url):
    
    #  Inicializa la librería de las cookies
    ficherocookies = os.path.join( config.get_data_path(), 'cookies.dat' )
    logger.info("Cookiefile="+ficherocookies)
    inicio = time.clock()
    
    cj = None
    ClientCookie = None
    cookielib = None

    # Let's see if cookielib is available
    try:
        import cookielib
    except ImportError:
        # If importing cookielib fails
        # let's try ClientCookie
        try:
            import ClientCookie
        except ImportError:
            # ClientCookie isn't available either
            urlopen = urllib2.urlopen
            Request = urllib2.Request
        else:
            # imported ClientCookie
            urlopen = ClientCookie.urlopen
            Request = ClientCookie.Request
            cj = ClientCookie.MozillaCookieJar()

    else:
        # importing cookielib worked
        urlopen = urllib2.urlopen
        Request = urllib2.Request
        cj = cookielib.MozillaCookieJar()
        # This is a subclass of FileCookieJar
        # that has useful load and save methods

    # ---------------------------------
    # Instala las cookies
    # ---------------------------------

    if cj is not None:
    # we successfully imported
    # one of the two cookie handling modules

        if os.path.isfile(ficherocookies):
            # if we have a cookie file already saved
            # then load the cookies into the Cookie Jar
            try:
                cj.load(ficherocookies)
            except:
                logger.info("[scrapertools.py] El fichero de cookies existe pero es ilegible, se borra")
                os.remove(ficherocookies)

        # Now we need to get our Cookie Jar
        # installed in the opener;
        # for fetching URLs
        if cookielib is not None:
            # if we use cookielib
            # then we get the HTTPCookieProcessor
            # and install the opener in urllib2
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            urllib2.install_opener(opener)

        else:
            # if we use ClientCookie
            # then we get the HTTPCookieProcessor
            # and install the opener in ClientCookie
            opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cj))
            ClientCookie.install_opener(opener)

    #print "-------------------------------------------------------"
    theurl = url
    # an example url that sets a cookie,
    # try different urls here and see the cookie collection you can make !

    #txheaders =  {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3',
    #              'Referer':'http://www.megavideo.com/?s=signup'}
    
    import httplib
    parsedurl = urlparse.urlparse(url)
    logger.info("parsedurl="+str(parsedurl))
        
    txheaders =  {
    'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language':'es-es,es;q=0.8,en-us;q=0.5,en;q=0.3',
    'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Accept-Encoding':'gzip,deflate',
    'Keep-Alive':'300',
    'Connection':'keep-alive',
    'Referer':parsedurl[0]+"://"+parsedurl[1]}
    logger.info(str(txheaders))

    # fake a user agent, some websites (like google) don't like automated exploration

    req = Request(theurl, None, txheaders)
    handle = urlopen(req)
    cj.save(ficherocookies) # save the cookies again

    data=handle.read()
    handle.close()
    
    fin = time.clock()
    logger.info("[scrapertools.py] Descargado 'Gzipped data' en %d segundos " % (fin-inicio+1))
        
    # Descomprime el archivo de datos Gzip
    try:
        fin = inicio
        import StringIO
        compressedstream = StringIO.StringIO(data)
        import gzip
        gzipper = gzip.GzipFile(fileobj=compressedstream)
        data1 = gzipper.read()
        gzipper.close()
        fin = time.clock()
        logger.info("[scrapertools.py] 'Gzipped data' descomprimido en %d segundos " % (fin-inicio+1))
        return data1
    except:
        return data

def printMatches(matches):
    i = 0
    for match in matches:
        logger.info("[scrapertools.py] %d %s" % (i , match))
        i = i + 1
        
def get_match(data,patron,index=0):
    matches = re.findall( patron , data , flags=re.DOTALL )
    return matches[index]

def entityunescape(cadena):
    return unescape(cadena)

def unescape(text):
    """Removes HTML or XML character references 
       and entities from a text string.
       keep &amp;, &gt;, &lt; in the source code.
    from Fredrik Lundh
    http://effbot.org/zone/re-sub.htm#unescape-html
    """
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":   
                    return unichr(int(text[3:-1], 16)).encode("utf-8")
                else:
                    return unichr(int(text[2:-1])).encode("utf-8")
                  
            except ValueError:
                logger.info("error de valor")
                pass
        else:
            # named entity
            try:
                '''
                if text[1:-1] == "amp":
                    text = "&amp;amp;"
                elif text[1:-1] == "gt":
                    text = "&amp;gt;"
                elif text[1:-1] == "lt":
                    text = "&amp;lt;"
                else:
                    print text[1:-1]
                    text = unichr(htmlentitydefs.name2codepoint[text[1:-1]]).encode("utf-8")
                '''
                import htmlentitydefs
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]]).encode("utf-8")
            except KeyError:
                logger.info("keyerror")
                pass
            except:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

    # Convierte los codigos html "&ntilde;" y lo reemplaza por "ñ" caracter unicode utf-8
def decodeHtmlentities(string):
    string = entitiesfix(string)
    entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")

    def substitute_entity(match):
        from htmlentitydefs import name2codepoint as n2cp
        ent = match.group(2)
        if match.group(1) == "#":
            return unichr(int(ent)).encode('utf-8')
        else:
            cp = n2cp.get(ent)

            if cp:
                return unichr(cp).encode('utf-8')
            else:
                return match.group()
                
    return entity_re.subn(substitute_entity, string)[0]
    
def entitiesfix(string):
    # Las entidades comienzan siempre con el símbolo & , y terminan con un punto y coma ( ; ).
    string = string.replace("&aacute","&aacute;")
    string = string.replace("&eacute","&eacute;")
    string = string.replace("&iacute","&iacute;")
    string = string.replace("&oacute","&oacute;")
    string = string.replace("&uacute","&uacute;")
    string = string.replace("&Aacute","&Aacute;")
    string = string.replace("&Eacute","&Eacute;")
    string = string.replace("&Iacute","&Iacute;")
    string = string.replace("&Oacute","&Oacute;")
    string = string.replace("&Uacute","&Uacute;")
    string = string.replace("&uuml"  ,"&uuml;")
    string = string.replace("&Uuml"  ,"&Uuml;")
    string = string.replace("&ntilde","&ntilde;")
    string = string.replace("&#191"  ,"&#191;")
    string = string.replace("&#161"  ,"&#161;")
    string = string.replace(";;"     ,";")
    return string


def htmlclean(cadena):
    cadena = cadena.replace("<center>","")
    cadena = cadena.replace("</center>","")
    cadena = cadena.replace("<cite>","")
    cadena = cadena.replace("</cite>","")
    cadena = cadena.replace("<em>","")
    cadena = cadena.replace("</em>","")
    cadena = cadena.replace("<b>","")
    cadena = cadena.replace("</b>","")
    cadena = cadena.replace("<u>","")
    cadena = cadena.replace("</u>","")
    cadena = cadena.replace("<li>","")
    cadena = cadena.replace("</li>","")
    cadena = cadena.replace("<tbody>","")
    cadena = cadena.replace("</tbody>","")
    cadena = cadena.replace("<tr>","")
    cadena = cadena.replace("</tr>","")
    cadena = cadena.replace("<![CDATA[","")
    cadena = cadena.replace("<Br />","")
    cadena = cadena.replace("<BR />","")
    cadena = cadena.replace("<Br>","")

    cadena = re.compile("<script.*?</script>",re.DOTALL).sub("",cadena)

    cadena = re.compile("<option[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</option>","")

    cadena = re.compile("<i[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</iframe>","")
    cadena = cadena.replace("</i>","")
    
    cadena = re.compile("<table[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</table>","")
    
    cadena = re.compile("<td[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</td>","")
    
    cadena = re.compile("<div[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</div>","")
    
    cadena = re.compile("<dd[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</dd>","")

    cadena = re.compile("<font[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</font>","")
    
    cadena = re.compile("<strong[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</strong>","")

    cadena = re.compile("<small[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</small>","")

    cadena = re.compile("<span[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</span>","")

    cadena = re.compile("<a[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</a>","")
    
    cadena = re.compile("<p[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</p>","")

    cadena = re.compile("<ul[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</ul>","")
    
    cadena = re.compile("<h1[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</h1>","")
    
    cadena = re.compile("<h2[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</h2>","")

    cadena = re.compile("<h3[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</h3>","")

    cadena = re.compile("<h4[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</h4>","")

    cadena = re.compile("<!--[^-]+-->",re.DOTALL).sub("",cadena)
    
    cadena = re.compile("<img[^>]*>",re.DOTALL).sub("",cadena)
    
    cadena = re.compile("<br[^>]*>",re.DOTALL).sub("",cadena)

    cadena = re.compile("<object[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</object>","")
    cadena = re.compile("<param[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</param>","")
    cadena = re.compile("<embed[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</embed>","")

    cadena = re.compile("<title[^>]*>",re.DOTALL).sub("",cadena)
    cadena = cadena.replace("</title>","")

    cadena = re.compile("<link[^>]*>",re.DOTALL).sub("",cadena)

    cadena = cadena.replace("\t","")
    cadena = entityunescape(cadena)
    return cadena


def slugify(title):
    
    #print title
    
    # Sustituye acentos y eñes
    title = title.replace("Á","a")
    title = title.replace("É","e")
    title = title.replace("Í","i")
    title = title.replace("Ó","o")
    title = title.replace("Ú","u")
    title = title.replace("á","a")
    title = title.replace("é","e")
    title = title.replace("í","i")
    title = title.replace("ó","o")
    title = title.replace("ú","u")
    title = title.replace("À","a")
    title = title.replace("È","e")
    title = title.replace("Ì","i")
    title = title.replace("Ò","o")
    title = title.replace("Ù","u")
    title = title.replace("à","a")
    title = title.replace("è","e")
    title = title.replace("ì","i")
    title = title.replace("ò","o")
    title = title.replace("ù","u")
    title = title.replace("ç","c")
    title = title.replace("Ç","C")
    title = title.replace("Ñ","n")
    title = title.replace("ñ","n")
    title = title.replace("/","-")
    title = title.replace("&amp;","&")

    # Pasa a minúsculas
    title = title.lower().strip()

    # Elimina caracteres no válidos 
    validchars = "abcdefghijklmnopqrstuvwxyz1234567890- "
    title = ''.join(c for c in title if c in validchars)

    # Sustituye espacios en blanco duplicados y saltos de línea
    title = re.compile("\s+",re.DOTALL).sub(" ",title)
    
    # Sustituye espacios en blanco por guiones
    title = re.compile("\s",re.DOTALL).sub("-",title.strip())

    # Sustituye espacios en blanco duplicados y saltos de línea
    title = re.compile("\-+",re.DOTALL).sub("-",title)
    
    # Arregla casos especiales
    if title.startswith("-"):
        title = title [1:]
    
    if title=="":
        title = "-"+str(time.time())

    return title


def remove_show_from_title(title,show):
    #print slugify(title)+" == "+slugify(show)
    # Quita el nombre del programa del título
    if slugify(title).startswith(slugify(show)):

        # Convierte a unicode primero, o el encoding se pierde
        title = unicode(title,"utf-8","replace")
        show = unicode(show,"utf-8","replace")
        title = title[ len(show) : ].strip()

        if title.startswith("-"):
            title = title[ 1: ].strip()
    
        if title=="":
            title = str( time.time() )
        
        # Vuelve a utf-8
        title = title.encode("utf-8","ignore")
        show = show.encode("utf-8","ignore")
    
    return title

def getRandom(str):
    return get_md5(str)

def getLocationHeaderFromResponse(url):
    return get_header_from_response(url,header_to_get="location")

def get_header_from_response(url,header_to_get="",post=None,headers=[['User-Agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12']]):
    header_to_get = header_to_get.lower()
    logger.info("[scrapertools.py] get_header_from_response url="+url+", header_to_get="+header_to_get)

    if post is not None:
        logger.info("[scrapertools.py] post="+post)
    else:
        logger.info("[scrapertools.py] post=None")
    
    #  Inicializa la librería de las cookies
    ficherocookies = os.path.join( config.get_setting("cookies.dir"), 'cookies.dat' )
    logger.info("[scrapertools.py] ficherocookies="+ficherocookies)

    cj = None
    ClientCookie = None
    cookielib = None

    import cookielib
    # importing cookielib worked
    urlopen = urllib2.urlopen
    Request = urllib2.Request
    cj = cookielib.MozillaCookieJar()
    # This is a subclass of FileCookieJar
    # that has useful load and save methods

    if os.path.isfile(ficherocookies):
        logger.info("[scrapertools.py] Leyendo fichero cookies")
        # if we have a cookie file already saved
        # then load the cookies into the Cookie Jar
        try:
            cj.load(ficherocookies)
        except:
            logger.info("[scrapertools.py] El fichero de cookies existe pero es ilegible, se borra")
            os.remove(ficherocookies)

    if header_to_get=="location":
        opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=DEBUG_LEVEL),urllib2.HTTPCookieProcessor(cj),NoRedirectHandler())
    else:
        opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=DEBUG_LEVEL),urllib2.HTTPCookieProcessor(cj))

    urllib2.install_opener(opener)

    # Contador
    inicio = time.clock()

    # Diccionario para las cabeceras
    txheaders = {}

    # Traza la peticion
    if post is None:
        logger.info("[scrapertools.py] petición GET")
    else:
        logger.info("[scrapertools.py] petición POST")
    
    # Login y password Filenium
    # http://abcd%40gmail.com:mipass@filenium.com/get/Oi8vd3d3/LmZpbGVz/ZXJ2ZS5j/b20vZmls/ZS9kTnBL/dm11/b0/?.zip
    if "filenium" in url:
        from servers import filenium
        url , authorization_header = filenium.extract_authorization_header(url)
        headers.append( [ "Authorization",authorization_header ] )
    
    # Array de cabeceras
    logger.info("[scrapertools.py] ---------------------------")
    for header in headers:
        logger.info("[scrapertools.py] header=%s" % str(header[0]))
        txheaders[header[0]]=header[1]
    logger.info("[scrapertools.py] ---------------------------")

    # Construye el request
    req = Request(url, post, txheaders)
    handle = urlopen(req)
    
    # Actualiza el almacén de cookies
    cj.save(ficherocookies)

    # Lee los datos y cierra
    #data=handle.read()
    info = handle.info()
    logger.info("[scrapertools.py] Respuesta")
    logger.info("[scrapertools.py] ---------------------------")
    location_header=""
    for header in info:
        logger.info("[scrapertools.py] "+header+"="+info[header])
        if header==header_to_get:
            location_header=info[header]
    handle.close()
    logger.info("[scrapertools.py] ---------------------------")

    # Tiempo transcurrido
    fin = time.clock()
    logger.info("[scrapertools.py] Descargado en %d segundos " % (fin-inicio+1))

    return location_header

def get_headers_from_response(url,post=None,headers=[['User-Agent', 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12']]):
    return_headers = []
    logger.info("[scrapertools.py] get_headers_from_response url="+url)

    if post is not None:
        logger.info("[scrapertools.py] post="+post)
    else:
        logger.info("[scrapertools.py] post=None")
    
    #  Inicializa la librería de las cookies
    ficherocookies = os.path.join( config.get_setting("cookies.dir"), 'cookies.dat' )
    logger.info("[scrapertools.py] ficherocookies="+ficherocookies)

    cj = None
    ClientCookie = None
    cookielib = None

    import cookielib
    # importing cookielib worked
    urlopen = urllib2.urlopen
    Request = urllib2.Request
    cj = cookielib.MozillaCookieJar()
    # This is a subclass of FileCookieJar
    # that has useful load and save methods

    if os.path.isfile(ficherocookies):
        logger.info("[scrapertools.py] Leyendo fichero cookies")
        # if we have a cookie file already saved
        # then load the cookies into the Cookie Jar
        try:
            cj.load(ficherocookies)
        except:
            logger.info("[scrapertools.py] El fichero de cookies existe pero es ilegible, se borra")
            os.remove(ficherocookies)

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj),NoRedirectHandler())
    urllib2.install_opener(opener)

    # Contador
    inicio = time.clock()

    # Diccionario para las cabeceras
    txheaders = {}

    # Traza la peticion
    if post is None:
        logger.info("[scrapertools.py] petición GET")
    else:
        logger.info("[scrapertools.py] petición POST")
    
    # Array de cabeceras
    logger.info("[scrapertools.py] ---------------------------")
    for header in headers:
        logger.info("[scrapertools.py] header=%s" % str(header[0]))
        txheaders[header[0]]=header[1]
    logger.info("[scrapertools.py] ---------------------------")

    # Construye el request
    req = Request(url, post, txheaders)
    handle = urlopen(req)
    
    # Actualiza el almacén de cookies
    cj.save(ficherocookies)

    # Lee los datos y cierra
    #data=handle.read()
    info = handle.info()
    logger.info("[scrapertools.py] Respuesta")
    logger.info("[scrapertools.py] ---------------------------")
    location_header=""
    for header in info:
        logger.info("[scrapertools.py] "+header+"="+info[header])
        return_headers.append( [header,info[header]] )
    handle.close()
    logger.info("[scrapertools.py] ---------------------------")

    # Tiempo transcurrido
    fin = time.clock()
    logger.info("[scrapertools.py] Descargado en %d segundos " % (fin-inicio+1))

    return return_headers

def unseo(cadena):
    if cadena.upper().startswith("VER GRATIS LA PELICULA "):
        cadena = cadena[23:]
    elif cadena.upper().startswith("VER GRATIS PELICULA "):
        cadena = cadena[20:]
    elif cadena.upper().startswith("VER ONLINE LA PELICULA "):
        cadena = cadena[23:]
    elif cadena.upper().startswith("VER GRATIS "):
        cadena = cadena[11:]
    elif cadena.upper().startswith("VER ONLINE "):
        cadena = cadena[11:]
    elif cadena.upper().startswith("DESCARGA DIRECTA "):
        cadena = cadena[17:]
    return cadena

def get_filename_from_url(url):
    
    import urlparse
    parsed_url = urlparse.urlparse(url)
    try:
        filename = parsed_url.path
    except:
        # Si falla es porque la implementación de parsed_url no reconoce los atributos como "path"
        if len(parsed_url)>=4:
            filename = parsed_url[2]
        else:
            filename = ""

    return filename

def get_domain_from_url(url):
    
    import urlparse
    parsed_url = urlparse.urlparse(url)
    try:
        filename = parsed_url.netloc
    except:
        # Si falla es porque la implementación de parsed_url no reconoce los atributos como "path"
        if len(parsed_url)>=4:
            filename = parsed_url[1]
        else:
            filename = ""

    return filename

# Parses the title of a tv show episode and returns the season id + episode id in format "1x01"
def get_season_and_episode(title):
    logger.info("get_season_and_episode('"+title+"')")

    patron ="(\d+)[x|X](\d+)"
    matches = re.compile(patron).findall(title)
    logger.info(str(matches))
    filename=matches[0][0]+"x"+matches[0][1]

    logger.info("get_season_and_episode('"+title+"') -> "+filename)
    
    return filename

def get_sha1(cadena):
    try:
        import hashlib
        devuelve = hashlib.sha1(cadena).hexdigest()
    except:
        import sha
        import binascii
        devuelve = binascii.hexlify(sha.new(url).digest())
    
    return devuelve

def get_md5(cadena):
    try:
        import hashlib
        devuelve = hashlib.md5(cadena).hexdigest()
    except:
        import md5
        import binascii
        devuelve = binascii.hexlify(md5.new(url).digest())
    
    return devuelve
