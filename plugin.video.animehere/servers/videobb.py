# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para videobb
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import os,re
import base64

from core import scrapertools
from core import logger
from core import config

HOSTER_KEY="MjI2NTkz"
HOSTER_TOKEN="token1"

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[videobb.py] get_video_url(page_url='%s')" % page_url)

    # Espera un poco como hace el player flash
    logger.info("[videobb.py] waiting 3 secs")
    import time
    time.sleep(3)

    video_urls = []
    
    # Obtiene el id
    code = Extract_id(page_url)
    if code == "":
        return []

    video_urls=getFinalLink("http://videobb.com/watch_video.php?v="+code,HOSTER_TOKEN)

    for video_url in video_urls:
        logger.info("[videobb.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

def Extract_id(url):
    # Extract video id from URL
    patron = "http\://www.videobb.com/watch_video.php\?v=([a-zA-Z0-9]{12})"
    matches = re.compile(patron,re.DOTALL).findall(url)
    if len(matches)>0:
        return matches[0]
    else:
        _VALID_URL = r'^((?:http://)?(?:\w+\.)?videobb\.com/(?:(?:(?:e/)|(?:video/))|(?:f/))?)?([0-9A-Za-z_-]+)(?(1).+)?$'
        mobj = re.match(_VALID_URL, url)
        if mobj is None:
            logger.info('[videobb.py] ERROR: URL invalida: %s' % url)
            return ""
        else:        
            return mobj.group(2)
            
# Crypt routines ported from Java VideoBbCom.java from jDownloader
# Thank you .bismarck ;)
def getFinalLink(downloadLink, token):
    
    # Lee la página
    logger.info(downloadLink)
    data = scrapertools.cache_page(downloadLink)
    #print "data="+data
    
    # Extrae el referer
    try:
        referer = re.findall('<param value="([^"]+)" name="movie">',data,re.DOTALL)[0]
        logger.info("referer="+referer)
    except:
        referer = ""

    if referer == "":
        referer = "http://videobb.com/player/p.swf?v=1_2_8_0"
    
    if not referer.startswith("http"):
        referer = "http://videobb.com" + referer
    logger.info("referer="+referer)

    # Extrae la url de la configuración del player
    setting = re.findall('<param value="setting=([^"]+)"',data,re.DOTALL)[0]
    logger.info("setting="+setting)
    setting = base64.decodestring(setting)
    logger.info("setting="+setting)

    # Descarga la configuración del player (json)
    data = scrapertools.cache_page(setting)
    #filedata = open("/Users/jesus/Downloads/texto.json")
    #data = filedata.read()
    #filedata.close()
    #print "data="+data

    headers=[]
    headers.append(["Referer",referer])
    headers.append(["x-flash-version","10,3,183,7"])

    # Parámetros del cifrado
    token1=re.findall(token + '":"([^"]+)",',data,re.DOTALL)[0]
    logger.info("token1="+token1)
    dllink = base64.decodestring( token1 )

    # Convierte el json en un diccionario
    datajson = data.replace("false","False").replace("true","True")
    datajson = datajson.replace("null","None")
    datadict = eval("("+datajson+")")

    # Formatos
    formatos = datadict["settings"]["res"]
    video_urls = []
    for formato in formatos:
        # Si la URL viene vacía, es porque esa calidad no es visible
        if formato["u"]!="":
            dllink = base64.decodestring(formato["u"])
            video_url = build_url(dllink,HOSTER_KEY,data)
            resolucion = formato["l"]
            video_urls.append( ["%s [videobb]" % resolucion , video_url , 5 ])

    return video_urls

def build_url(dllink,hoster_key,data):
    if not dllink.endswith("&"):
        dllink = dllink + "&"
    
    logger.info("dllink="+dllink)

    keyTwo = int( base64.decodestring(hoster_key) )
    logger.info("keyTwo="+str(keyTwo))

    keyOne = int( re.findall('rkts":(\d+),',data,re.DOTALL)[0] )
    logger.info("keyOne="+str(keyOne))

    algoCtrl = base64.decodestring( re.findall('spn":"([^"]+)",',data,re.DOTALL)[0] )
    logger.info("algoCtrl="+algoCtrl)
    
    for eachValue in algoCtrl.split("&"):
        parameterTyp = eachValue.split("=")

        if parameterTyp[1]=="1":
            keyString = re.findall('sece2":"([0-9a-f]+)",',data,re.DOTALL)[0]
            decryptedString = decryptByte(keyString, keyOne, keyTwo)
        elif parameterTyp[1]=="2":
            keyString = re.findall('\{"url":"([0-9a-f]+)",',data,re.DOTALL)[0]
            decryptedString = decryptBit(keyString, keyOne, keyTwo)
        elif parameterTyp[1]=="3":
            keyString = re.findall('type":"([0-9a-f]+)",',data,re.DOTALL)[0]
            decryptedString = decryptBit9300(keyString, keyOne, keyTwo)
        elif parameterTyp[1]=="4":
            keyString = re.findall('time":"(.*?)"',data,re.DOTALL)[0]
            decryptedString = decryptBitLion(keyString, keyOne, keyTwo)

        dllink = dllink + parameterTyp[0] + "=" + decryptedString + "&"
    
    return dllink + "start=0";

def decryptByte(arg1,arg2,arg3):
    logger.info("[decryptByte] keyString=%s, keyOne=%d, keyTwo=%d" % (arg1,arg2,arg3))
    devuelve = zDecrypt(True, arg1, arg2, arg3, 11, 77213, 81371, 17, 92717, 192811)
    return devuelve

def decryptBit(arg1,arg2,arg3):
    logger.info( "[decryptBit] keyString=%s, keyOne=%d, keyTwo=%d" % (arg1,arg2,arg3) )
    devuelve = zDecrypt(False, arg1, arg2, arg3, 11, 77213, 81371, 17, 92717, 192811)
    return devuelve

def decryptBit9300(arg1,arg2,arg3):
    logger.info( "[decryptBit9300] keyString=%s, keyOne=%d, keyTwo=%d" % (arg1,arg2,arg3) )
    devuelve = zDecrypt(False, arg1, arg2, arg3, 26, 25431, 56989, 93, 32589, 784152)
    return devuelve

def decryptBitLion(arg1,arg2,arg3):
    logger.info( "[decryptBitLion] keyString=%s, keyOne=%d, keyTwo=%d" % (arg1,arg2,arg3) )
    devuelve = zDecrypt(False, arg1, arg2, arg3, 82, 84669, 48779, 32, 65598, 115498)
    return devuelve

def zDecrypt(algo, cipher, keyOne, keyTwo, arg0, arg1, arg2, arg3, arg4, arg5):
    #int x = 0, y = 0, z = 0;
    x = 0; y = 0; z = 0

    #final char[] C = convertStr2Bin(cipher).toCharArray();
    C = list(convertStr2Bin(cipher))
    
    #int len = C.length * 2;
    longitud = len(C) * 2
    
    '''
    if (algo) {
        len = 256;
    }
    '''
    if algo:
        longitud = 256

    #final int[] B = new int[(int) (len * 1.5)];
    B = []
    
    #final int[] A = new int[C.length];
    A = []
    
    '''
    int i = 0;
    for (final char c : C) {
        A[i++] = Character.digit(c, 10);
    }
    '''
    i = 0
    for i in range(0,len(C)):
        A.append( int(C[i],10) )
    
    '''
    i = 0;
    while (i < len * 1.5) {
        keyOne = (keyOne * arg0 + arg1) % arg2;
        keyTwo = (keyTwo * arg3 + arg4) % arg5;
        B[i] = (keyOne + keyTwo) % (len / 2);
        i++;
    }
    '''
    i=0
    while i<longitud*1.5:
        keyOne = (keyOne * arg0 + arg1) % arg2
        keyTwo = (keyTwo * arg3 + arg4) % arg5
        B.append( (keyOne + keyTwo) % (longitud / 2) )
        i=i+1
  

    '''
    i = len;
    while (i >= 0) {
        x = B[i];
        y = i % (len / 2);
        z = A[x];
        A[x] = A[y];
        A[y] = z;
        i--;
    }
    '''
    i=longitud
    while i >= 0:
        x = B[i]
        y = i % (longitud / 2)
        z = A[x]
        A[x] = A[y]
        A[y] = z
        i=i-1
    
    '''
    i = 0;
    while (i < len / 2) {
        A[i] = A[i] ^ B[i + len] & 1;
        i++;
    }
    '''
    i=0
    while i < longitud/2:
        A[i] = A[i] ^ B[i + longitud] & 1
        i=i+1

    '''
    i = 0;
    final StringBuilder sb = new StringBuilder();
    while (i < A.length) {
        sb.append(A[i]);
        i++;
    }
    return convertBin2Str(sb.toString());
    '''
    i = 0
    result = ""
    while i < len(A):
        result = result + str(A[i])
        i = i + 1

    return convertBin2Str(result)

def convertBin2Str(s):
    # 11111111 -> FF
    BI = int(s, 2)
    dev = "%x" % BI
    return dev

def convertStr2Bin(s):
    # FF -> 11111111
    BI = int(s, 16)

    # Convierte a binario    
    result = ''
    if BI == 0: return '0'
    while BI > 0:
        result = str(BI % 2) + result
        BI = BI >> 1
    
    while len(result) < 256:
        result = "0" + result

    return result

def decrypt32byte(cipher, keyOne, keyTwo):
    '''
    int x = 0, y = 0, z = 0;
    '''
    x = 0; y = 0; z = 0
    
    '''
    final char[] C = convertStr2Bin(cipher).toCharArray();
    '''
    C = list(convertStr2Bin(cipher))
    
    '''
    final int[] B = new int[384];
    '''
    B = []
    
    '''
    final int[] A = new int[C.length];
    '''
    A = []

    '''
    int i = 0;
    for (final char c : C) {
        A[i++] = Character.digit(c, 10);
    }
    '''
    i = 0
    for i in range(0,len(C)):
        A.append( int(C[i],10) )
    
    '''
    i = 0;
    while (i < 384) {
        keyOne = (keyOne * 11 + 77213) % 81371;
        keyTwo = (keyTwo * 17 + 92717) % 192811;
        B[i] = (keyOne + keyTwo) % 128;
        i++;
    }
    '''
    i = 0
    while i<384:
        keyOne = (keyOne * 11 + 77213) % 81371
        keyTwo = (keyTwo * 17 + 92717) % 192811
        B.append( (keyOne + keyTwo) % 128 )
        i=i+1

    '''
    i = 256;
    while (i >= 0) {
        x = B[i];
        y = i % 128;
        z = A[x];
        A[x] = A[y];
        A[y] = z;
        i--;
    }
    '''
    i = 256
    while i >= 0:
        x = B[i]
        y = i % 128
        z = A[x]
        A[x] = A[y]
        A[y] = z
        i=i-1
    '''
    i = 0;
    while (i < 128) {
        A[i] = A[i] ^ B[i + 256] & 1;
        i++;
    }
    '''
    i = 0
    while i < 128:
        A[i] = A[i] ^ B[i + 256] & 1
        i=i+1

    '''
    i = 0;
    final StringBuilder sb = new StringBuilder();
    while (i < A.length) {
        sb.append(A[i]);
        i++;
    }
    '''
    i = 0
    result = ""
    while i < len(A):
        result = result + str(A[i])
        i = i + 1

    return convertBin2Str(result)

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    # TODO: de jdownloader "http://(www\\.)?videobb\\.com/(video/|watch_video\\.php\\?v=|e/)\\w+"
    patronvideos  = "(http\:\/\/(?:www\.)?videobb.com\/(?:(?:e/)|(?:(?:video/|f/)))?[a-zA-Z0-9]{12})"
    logger.info("[videobb.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[videobb]"
        url = match
    
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'videobb' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    patronvideos  = "(http\://www.videobb.com/watch_video.php\?v=[a-zA-Z0-9]{12})"
    logger.info("[videobb.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[videobb]"
        url = match

        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'videobb' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve