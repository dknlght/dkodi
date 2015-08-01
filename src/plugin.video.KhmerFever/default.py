import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
import xbmcaddon,xbmcplugin,xbmcgui
from t0mm0.common.net import Net

strdomain ='khmerfever.com'
def HOME():
        addLink('Khmerfever no longer exist Use KhmerPortal addon','',3,'http://d3v6rrmlq7x1jk.cloudfront.net/hwdvideos/thumbs/category29.jpg')
        
def SEARCH(url):
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        searchText = ''
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        url = 'http://khmerfever.com/?s=' + searchText + '&submit.x=16&submit.y=11'
        SearchResults(url)
        
def INDEX(url):
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<div class="post ">                <a href="(.+?)" rel="bookmark" title="(.+?)"><img src="(.+?)" alt="').findall(newlink)
        if(len(match) >= 1):
                for vLink, vLinkName,vLinkPic in match:
                    addDir(urllib2.unquote(vLinkName).decode("utf8"),vLink,5,vLinkPic)
        match=re.compile('<a class="next page-numbers" href="(.+?)">').findall(link)
        if(len(match) >= 1):
            nexurl= match[0]
            addDir('Next>',nexurl,2,'')

def SearchResults(url):
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<h2 class="title"><a href="(.+?)" rel="bookmark" title="">(.+?)</a></h2>').findall(newlink)
        if(len(match) >= 1):
                for vLink, vLinkName in match:
                    addDir(vLinkName,vLink,5,'')
        match=re.compile('<a class="next page-numbers" href="(.+?)">').findall(link)
        if(len(match) >= 1):
            nexurl= match[0]
            addDir('Next>',nexurl,6,'')			
			
def Episodes(url,name):
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile("<ol class='related_post'>(.+?)</ol>").findall(link)
        #print newlink
        if(len(match) >= 1):
                for mcontent in match:
                    quickLinks=re.compile("<a href='(.+?)' title='(.+?)'>").findall(mcontent)
                    for vLink, vLinkName in quickLinks:
                        #vLinkName=''.join(vLinkName.splitlines()).replace('\u','')
                        #addDir(vLinkName.encode("utf-8"),vLink,3,'')
                        addLink(vLinkName.encode("utf-8"),vLink,3,'')						
                    #addDir(name,url,3,'')
                    addLink(name,url,3,'')					
						
def GetCookie():
     response = ClientCookie.urlopen("http://www.khmerportal.com/")
     print response

def GetContent(url):
    net = Net()
    second_response = net.http_GET(url)
    return second_response.content

def playVideo(videoType,videoId):
    url = ""
    if (videoType == "youtube"):
        url = 'plugin://plugin.video.youtube?path=/root&action=play_video&videoid=' + videoId.replace('?','')
        xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
    elif (videoType == "vimeo"):
        url = 'plugin://plugin.video.vimeo/?action=play_video&videoID=' + videoId
    elif (videoType == "tudou"):
        url = 'plugin://plugin.video.tudou/?mode=3&url=' + videoId	
    elif (videoType == "khmerportal"):
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoId)
	
def loadVideos(url,name):
        xbmc.executebuiltin("XBMC.Notification(Please Wait!,Loading selected video)")
        link=GetContent(url)
        link = ''.join(link.splitlines()).replace('\t','').replace('\'','"')
        #print link
        #YouTube
        try:
                newlink = re.compile('"file": "(.+?)",').findall(link)
                newlink1 = urllib2.unquote(newlink[0]).decode("utf8")+'&dk;'
                print 'NEW url = '+ newlink1
                match=re.compile('http://youtu.be/(.+?)&dk;').findall(newlink1)
                if(len(match) == 0):
                    match=re.compile('http://www.youtube.com/watch\?v=(.+?)&dk;').findall(newlink1)
                    print match
                if(len(match) > 0):
                    playVideo('youtube',match[0])
                else:
                    playVideo('khmerportal',urllib2.unquote(newlink[0]).decode("utf8"))
        except: pass
        
def OtherContent():
    net = Net()
    response = net.http_GET('http://khmerportal.com/videos')
    print response
	
def addLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        contextMenuItems = []
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="http://khmerfever.com/wp-content/uploads/2011/09/kflogo.png", thumbnailImage=iconimage)
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
		
sysarg=str(sys.argv[1]) 		
if mode==None or url==None or len(url)<1:
        #OtherContent()
        HOME()
       
elif mode==2:
        #d = xbmcgui.Dialog()
        #d.ok('mode 2',str(url),' ingore errors lol')
        INDEX(url)
        
elif mode==3:
        loadVideos(url,name)
elif mode==4:
        SEARCH(url) 
elif mode==5:
       Episodes(url,name)
elif mode==6:
       SearchResults(url)

xbmcplugin.endOfDirectory(int(sysarg))
