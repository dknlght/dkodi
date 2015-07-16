import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
from xml.dom.minidom import Document

__settings__ = xbmcaddon.Addon(id='plugin.video.DKEvents')
home = __settings__.getAddonInfo('path')
filename = xbmc.translatePath(os.path.join(home, 'resources', 'DKEvents.xml'))

def SearchXml(SearchText):
    if os.path.isfile(filename)==False:
        BuildXMl()
    f = open(filename, "r")
    text = f.read()
    if SearchText=='-1':
        match=re.compile('<movie name="[^A-Za-z](.+?)" url="(.+?)" year="(.+?)"/>', re.IGNORECASE).findall(text)	
        SearchText=""
    else:
        match=re.compile('<movie name="' + SearchText + '(.+?)" url="(.+?)" year="(.+?)"/>', re.IGNORECASE).findall(text)
    for i in range(len(match)):
        (mName,mNumber,vyear)=match[i]
        addDir(SearchText+mName,mNumber,6,"")
		
def ParseXml(tagname):
        f = open(filename, "r")
        text = f.read()
        xmlcontent=xml.dom.minidom.parseString(text)
        items=xmlcontent.getElementsByTagName('channel')
        print "calling " + tagname
        for channelitem in items:
                if(len(channelitem.getElementsByTagName('item'))>=1 and channelitem.getElementsByTagName('name')[0].childNodes[0].data==tagname):
                        chitems = channelitem.getElementsByTagName('item')
                        for itemXML in chitems:
                                vname=itemXML.getElementsByTagName('title')[0].childNodes[0].data.strip()
                                vurl=itemXML.getElementsByTagName('link')[0].childNodes[0].data.strip()
                                vimg=itemXML.getElementsByTagName('thumbnail')[0].childNodes[0].data.strip()
                                addLink(vname,vurl,3,vimg)
	
def GetXMLChannel():
        f = open(filename, "r")
        text = f.read()
        xmlcontent=xml.dom.minidom.parseString(text)
        items=xmlcontent.getElementsByTagName('channel')
        for channelitem in items:
                vname=channelitem.getElementsByTagName('name')[0].childNodes[0].data.strip()
                addDir(vname,"",2,"")



def playVideo(url):
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(url)
	

     	
def addLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        contextMenuItems = []
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok
		
def addNext(formvar,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&formvar="+str(formvar)+"&name="+urllib.quote_plus('Next >')
        ok=True
        liz=xbmcgui.ListItem('Next >', iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": 'Next >' } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param    



params=get_params()
url=None
name=None
mode=None
formvar=None
try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
        formvar=int(params["formvar"])
except:
        pass		
	
sysarg=str(sys.argv[1]) 

if mode==None:
        GetXMLChannel()
elif mode==2:
        ParseXml(name) 
elif mode==3:
        playVideo(url)
xbmcplugin.endOfDirectory(int(sysarg))
