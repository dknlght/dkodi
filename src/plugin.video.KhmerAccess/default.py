import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import xbmcaddon,xbmcplugin,xbmcgui


strdomain ='www.khmeraccess.com'
def HOME():
        addLink('Khmeraccess no longer exist Use KhmerPortal addon','',3,'http://d3v6rrmlq7x1jk.cloudfront.net/hwdvideos/thumbs/category29.jpg')
        
def SEARCH(url):
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        searchText = ''
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        url = 'http://www.khmeraccess.com/video/videolist/videonew.html?tags=' + searchText 
        INDEX_Old(GetContent(url),url) 
def INDEX(url):
        addDir('Series',url,7,'')
        addDir('Individual Episodes',url,8,'')

def INDEX_New(link,url):
    try:
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<img src="http://www.khmeraccess.com/files/video_category/(.+?)" /></a>                                                </span></div>                                                <a href="(.+?)">(.+?)</a>').findall(newlink)
        if(len(match) >= 1):
                for vLinkPic,vLink,vLinkName in match:
                    addDir(vLinkName.strip(),vLink,8,'http://www.khmeraccess.com/files/video_category/' + vLinkPic)
    except: pass

def INDEX_Old(link,url):
    try:
        newlink = ''.join(link.splitlines()).replace('\t','')
        match2=re.compile('<table summary="My Videos Table" class="clsContentsDisplayTbl clsVideoListTable" id="selDisplayTable">((.|\s)*?)</table>').findall(newlink)
        strfind,strempty = match2[0]
        match=re.compile('<img src="http://khmeraccess.com/files/videos/thumbnails/(.+?)"   />').findall(strfind)
        match3=re.compile('<a href="http://www.khmeraccess.com/video/viewvideo/(.+?)">(.+?)</a>').findall(strfind)
        imglen = len(match)
        if(len(match3) >= 1):
                for i in range(len(match3)):
                    (vLink,vLinkName)=match3[i]
                    if(i < imglen ):
                        imglink = 'http://khmeraccess.com/files/videos/thumbnails/' + match[i]
                    else:
                        imglink =''
                    addLink(vLinkName.strip(),'http://www.khmeraccess.com/video/viewvideo/'+vLink,3,imglink)
        if (link.find('<li class="clsLastPageLink clsInActivePageLink">Next</li>') == -1):
            match=re.compile("'seachAdvancedFilter','(.+?)'").findall(link)
            intlength = len(match)
            #print match
            if(intlength >= 1):  
                nexpage= match[intlength-2]
                addNext(nexpage,url,10,'')
    except: pass
			
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
                        addLink(vLinkName,vLink,3,'') 
                    addLink(name,url,3,'')   						
						
def GetCookie():
     response = ClientCookie.urlopen("http://www.khmerportal.com/")
     print response

def GetContent(url):
    try:
       net = Net()
       second_response = net.http_GET(url)
       return second_response.content
    except:	
       d = xbmcgui.Dialog()
       d.ok('Time out',"Can't Connect to site",'Try again in a moment')

def PostContent(formvar,url):
        try:
                net = Net()
                headers = {}
                headers['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
                headers['Accept-Encoding'] = 'gzip, deflate'
                headers['Accept-Charset']='ISO-8859-1,utf-8;q=0.7,*;q=0.7'
                headers['Referer'] = 'http://www.khmeraccess.com/video/videolist/videonew.html?cid=1'
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:5.0.1) Gecko/20100101 Firefox/5.0.1'
                headers['Connection'] = 'keep-alive'
                headers['Host']='www.khmeraccess.com'
                headers['Accept-Language']='en-us,en;q=0.5'
                headers['Pragma']='no-cache'
                formdata={}                      
                formdata['start']=formvar


                #first_response = net.http_Get('http://khmerfever.com/wp-login.php',headers=header_dict)
                #net.save_cookies('c:\cookies.txt')
                #net.set_cookies('c:\cookies.txt')
                second_response = net.http_POST(url,formdata,headers=headers,compression=False)
                return second_response.content
        except: 
                d = xbmcgui.Dialog()
                d.ok('Time out',"Can't Connect to site",'Try again in a moment')
	
def playVideo(videoType,videoId):
    url = ""
    print videoType + '=' + videoId
    if (videoType == "youtube"):
        url = 'plugin://plugin.video.youtube?path=/root&action=play_video&videoid=' + videoId.replace('?','')
        xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
    elif (videoType == "vimeo"):
        url = 'plugin://plugin.video.vimeo/?action=play_video&videoID=' + videoId
    elif (videoType == "tudou"):
        url = 'plugin://plugin.video.tudou/?mode=3&url=' + videoId	
    else:
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoId)
	
def loadVideos(url,name):
        link=GetContent(url)
        link = ''.join(link.splitlines()).replace('\t','').replace('\'','"')
        #print link
        #4shared
        newlink = re.compile('"file","(.+?)"\);').findall(link)
        #general
        if(len(newlink)==0):
                match2=re.compile('<div id="flashcontent2" class="clsVideoPlayerBorder">((.|\s)*?)</div>').findall(link)
                link,strempty = match2[0]
                newlink = re.compile('<embed wmode="transparent" src="(.+?)" width="470" height="320" allowfullscreen="true" allowscriptaccess="always">').findall(link)
        if(len(newlink)==0):
                newlink = re.compile('<iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
        if(len(newlink)==0):
                newlink = re.compile('<param name="flashvars" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
                newlink[0] = newlink[0].replace("file=", "")
        if(len(newlink)==0):
                newlink = re.compile('<param name="movie" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)

         #dailymotion       
        #if(len(newlink)==0):
        #        newlink = re.compile('<div id="flashcontent2" class="clsVideoPlayerBorder">                                                <iframe frameborder="0" width="(.+?)" height="(.+?)" src="(.+?)">').findall(link)
        #        if(len(newlink)!=0):
        #           strempty,strempty,newlink[0]=newlink[0]
        #zshare
        #if(len(newlink)==0):
        #        newlink = re.compile('<div id="flashcontent2" class="clsVideoPlayerBorder">                                                <iframe src="(.+?)" height="415" width="648"  border=0 frameborder=0 scrolling=no>').findall(link)               
        #if(len(newlink)==0):
        #        newlink = re.compile('"file","(.+?)"\);').findall(link)
        #print newlink
        #Khmeraccess
        if(True):
           newlink=newlink[0] 
           if (newlink.find("dailymotion") > -1):
                match=re.compile('(dailymotion\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(newlink)
                lastmatch = match[0][len(match[0])-1]
                link = 'http://www.dailymotion.com/'+str(lastmatch)
                req = urllib2.Request(link)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                sequence=re.compile('"sequence",  "(.+?)"').findall(link)
                newseqeunce = urllib.unquote(sequence[0]).decode('utf8').replace('\\/','/')
                #print 'in dailymontion:' + str(newseqeunce)
                imgSrc=re.compile('"videoPreviewURL":"(.+?)"').findall(newseqeunce)
                if(len(imgSrc[0]) == 0):
                	imgSrc=re.compile('/jpeg" href="(.+?)"').findall(link)
                dm_low=re.compile('"sdURL":"(.+?)"').findall(newseqeunce)
                dm_high=re.compile('"hqURL":"(.+?)"').findall(newseqeunce)
                playVideo('dailymontion',urllib2.unquote(dm_low[0]).decode("utf8"))
           elif (newlink.find("4shared") > -1):
                d = xbmcgui.Dialog()
                d.ok('Not Implemented','Sorry 4Shared links',' not implemented yet')		
           else:
                if (newlink.find("linksend.net") > -1):
                     d = xbmcgui.Dialog()
                     d.ok('Not Implemented','Sorry videos on linksend.net does not work','Site seem to not exist')		
                newlink1 = urllib2.unquote(newlink).decode("utf8")+'&dk;'
                print 'NEW url = '+ newlink1
                match=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(newlink1)
                if(len(match) == 0):
                    match=re.compile('http://www.youtube.com/watch\?v=(.+?)&dk;').findall(newlink1)
                if(len(match) > 0):
                    lastmatch = match[0][len(match[0])-1].replace('v/','')
                    playVideo('youtube',lastmatch)
                else:
                    playVideo('khmerportal',urllib2.unquote(newlink).decode("utf8"))
        #except: pass
        
def OtherContent():
    net = Net()
    response = net.http_GET('http://khmerportal.com/videos')
    print response       

def addNext(formvar,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&formvar="+str(formvar)+"&name="+urllib.quote_plus('Next >')
        ok=True
        liz=xbmcgui.ListItem('Next >', iconImage="http://www.khmeraccess.com/design/templates/orient/root/images/screen_blue/header/logo.jpg", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": 'Next >' } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

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
        liz=xbmcgui.ListItem(name, iconImage="http://www.khmeraccess.com/design/templates/orient/root/images/screen_blue/header/logo.jpg", thumbnailImage=iconimage)
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

#url='http://www.khmeraccess.com/video/viewvideo/6604/31end.html'		
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
elif mode==7:
       INDEX_New(GetContent(url),url)
elif mode==8:
       INDEX_Old(GetContent(url),url)
elif mode==9:
       INDEX_New(PostContent(formvar,url),url)
elif mode==10:
       INDEX_Old(PostContent(formvar,url),url)
elif mode==11:
       xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
xbmcplugin.endOfDirectory(int(sysarg))
