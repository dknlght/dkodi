# -*- coding: iso-8859-1 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Convierte una lista de vídeos en xml a una playlist PLS
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import re, os
import urlparse, urllib, urllib2

from core import scrapertools
from core import logger
from core import config
from core import downloadtools

DEBUG = True
CHANNELNAME = "xmltoplaylist"
PLAYLIST_XML_FILENAME_TEMP = "video_playlist.xml.temp.pls"
FULL_FILENAME_PATH_XML = os.path.join( config.get_setting("downloadpath"), PLAYLIST_XML_FILENAME_TEMP )
PLAYLIST_FILENAME_TEMP = "video_playlist.temp.pls"
FULL_FILENAME_PATH = os.path.join( config.get_setting("downloadpath"), PLAYLIST_FILENAME_TEMP )

# Returns an array of possible video url's from the page_url
def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[xmltoplaylist.py] get_video_url(page_url='%s')" % page_url)

    video_urls = [ ["[directo]" , MakePlaylistFromXML(page_url)] ]
    return video_urls
    
def MakePlaylistFromXML(xmlurl,title="default"):
    logger.info("[%s.py] MakePlaylistFromXML" %CHANNELNAME)
    
    if title== ("default" or ""):
        nombrefichero = FULL_FILENAME_PATH_XML
    else:
        nombrefichero = os.path.join( config.get_setting("downloadpath"),title + ".pls")
    xmldata = scrapertools.cachePage(xmlurl)
    patron = '<title>([^<]+)</title>.*?<location>([^<]+)</location>'
    matches = re.compile(patron,re.DOTALL).findall(xmldata)
    if len(matches)>0:
        playlistFile = open(nombrefichero,"w")
        playlistFile.write("[playlist]\n")
        playlistFile.write("\n")
        c = 0        
        for match in matches:
            c += 1
            playlistFile.write("File%d=%s\n"  %(c,match[1]))
            playlistFile.write("Title%d=%s\n" %(c,match[0]))
            playlistFile.write("\n")
            
        playlistFile.write("NumberOfEntries=%d\n" %c)
        playlistFile.write("Version=2\n")
        playlistFile.flush();
        playlistFile.close()    
        return nombrefichero
    else:
        return ""

def MakePlaylistFromList(Listdata,title="default"):
    logger.info("[%s.py] MakePlaylistFromList" %CHANNELNAME)
    
    if title== ("default" or ""):
        nombrefichero = FULL_FILENAME_PATH
    else:
        nombrefichero = os.path.join( config.get_setting("downloadpath"),title + ".pls")
    
    if len(Listdata)>0:
        playlistFile = open(nombrefichero,"w")
        playlistFile.write("[playlist]\n")
        playlistFile.write("\n")
        c = 0        
        for match in Listdata:
            c += 1
            playlistFile.write("File%d=%s\n"  %(c,match[1]))
            playlistFile.write("Title%d=%s\n" %(c,match[0]))
            playlistFile.write("\n")
            
        playlistFile.write("NumberOfEntries=%d\n" %c)
        playlistFile.write("Version=2\n")
        playlistFile.flush();
        playlistFile.close()    
        return nombrefichero
    else:
        return ""