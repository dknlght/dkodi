import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
import xbmcaddon,xbmcplugin,xbmcgui
#from t0mm0.common.net import Net
import hashlib,random
import json
from t0mm0.common.addon import Addon
import datetime
from resources.lib.ooyala.utils.Common import Common as CommonUtils
from resources.lib.ooyala.MagicNaming import MagicNaming
from resources.lib.ooyala.ooyalaCrypto import ooyalaCrypto

addon = Addon("plugin.video.MyPinoyTv")
ADDON = xbmcaddon.Addon(id='plugin.video.MyPinoyTv')
if ADDON.getSetting('ga_visitor')=='':
    from random import randint
    ADDON.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))
    
PATH = "MyPinoyTv"  #<---- PLUGIN NAME MINUS THE "plugin.video"          
UATRACK="UA-40129315-1" #<---- GOOGLE ANALYTICS UA NUMBER   
VERSION = "1.1.6" #<---- PLUGIN VERSION

datapath = addon.get_profile()
cookie_path = os.path.join(datapath, 'cookies')
strdomain ='mypinoy.tv'
strServerUrl=""
settingfilename= os.path.join(cookie_path, "setting.txt")
cookiefile= os.path.join(cookie_path, "cookiejar.lwp")
cj=None
def HOME(cj):

    addDir('Search','/videos/categories',4,'')
    addLink('Login','/videos/categories',8,'','')
    (cj,menuContent)=postContent("http://"+strdomain,"","http://"+strdomain,cj)
    menuContent=''.join(menuContent.splitlines()).replace('\'','"')
    tvlist = re.compile('<ul class="one-column">(.+?)</ul>').findall(menuContent)
    if(len(tvlist)>0):
		addLink('TV','',0,'','')
		addDir("---PBA Games","http://mypinoy.tv/pba-games/",2,'')
		listitem= re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(tvlist[0])
		for vurl,vname in listitem:
			addDir("---"+vname,vurl,2,'')
    movielist = re.compile('<ul class="two-column">(.+?)</ul>').findall(menuContent)
    if(len(movielist)>0):
		addLink('Movies','',0,'','')
		listitem= re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(movielist[0])
		for vurl,vname in listitem:
			addDir("---"+vname,vurl,2,'')

if os.path.exists(cookiefile):
    cj = cookielib.LWPCookieJar()
    cj.load(cookiefile, ignore_discard=True)
	
def SEARCH(url,cj):
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        searchText = ''
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        url = 'http://'+strdomain+'/search?s='+urllib.quote_plus(searchText)
        (cj,mediacontent)=postContent(url,"","http://"+strdomain,cj)
        mediacontent=''.join(mediacontent.splitlines()).replace('\'','"')
        tvlist = re.compile('<div class="search-result">(.+?)<div style="clear: both;">').findall(mediacontent)
        if(len(tvlist)>0):
			listitem= re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(tvlist[0])
			imageitem= re.compile('<img [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(tvlist[0])
			ctr=0
			for vurl,vname in listitem:
				if(vname.find("<") == -1):
					vimg=imageitem[ctr]
					addDir(vname,vurl,3,vimg)
					ctr=ctr+1
        
def INDEX(url,name,cj):
        (cj,mediacontent)=postContent(url,"","http://"+strdomain,cj)
        mediacontent=''.join(mediacontent.splitlines()).replace('\'','"')
        tvlist = re.compile('<div id="category_list" class="is_pagination">(.+?)<div style="clear: both;">').findall(mediacontent)
        if(len(tvlist)>0):
			listitem= re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>\s*<img class="image" src="(.+?)" alt="(.+?)" />\s*</a>').findall(tvlist[0])
			for vurl,vimg,vname in listitem:
				addDir(vname,vurl,3,vimg)
				

def streamGetter(embedCode):
	## Decrypts the embed code and returns a stream path
	retlist = []
	smil = CommonUtils().grabEncrypted(embedCode)
	decrypted_smil = ooyalaCrypto().ooyalaDecrypt(smil)
	videoList = MagicNaming().getVideoUrl(decrypted_smil)
	retlist.extend(videoList)
	videoArray = ''.join(videoList)
	## Pulls the playpath from the stream path
	Segments = videoArray.rsplit('/',2)
	playpath = 'mp4:s/' + Segments[1]+ '/' +Segments[2]

	## Returns the title, description, thumbnail url and playpath
	return playpath
	
def Episodes(url,name,cj):
        (cj,mediacontent)=postContent(url,"","http://"+strdomain,cj)
        mediacontent=''.join(mediacontent.splitlines()).replace('\'','"')
        islogin= re.compile('<p>Free Sign Up</p>').findall(mediacontent)
        if(len(islogin)>0):
            cj=AutoLogin(cj,url)
            (cj,mediacontent)=postContent(url,"","http://"+strdomain,cj)
            mediacontent=''.join(mediacontent.splitlines()).replace('\'','"')
        tvlist = re.compile('<div class="thumbnails is_pagination" id="videos" >(.+?)<div style="clear: both;">').findall(mediacontent)
        if(len(tvlist)>0):
			listitem= re.compile('<a href="(.+?)" class="images" title="(.+?)" >\s*<img [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>\s*</a>').findall(tvlist[0])
			for vurl,vname,vimg in listitem:
				addLink(vname,vurl,14,vimg,'')
        else:
				embedcode=GetEmbedcode(mediacontent)
				addLink(name,embedcode,5,"",'')

def GetVideoStream(name,url,cj):
        (cj,mediacontent)=postContent(url,"","http://"+strdomain,cj)
        mediacontent=''.join(mediacontent.splitlines()).replace('\'','"')
        islogin= re.compile('<p>Free Sign Up</p>').findall(mediacontent)
        if(len(islogin)>0):
            cj=AutoLogin(cj,url)
            (cj,mediacontent)=postContent(url,"","http://"+strdomain,cj)
            mediacontent=''.join(mediacontent.splitlines()).replace('\'','"')
        embedcode=GetEmbedcode(mediacontent)
        playVideo(name,embedcode)

def GetEmbedcode(htmlcontent):
    emcode= re.compile('OO.Player.create\("videoplayer",\s*"(.+?)",').findall(htmlcontent)[0]
    return emcode

def GetJSON(url,data,referr,cj):
    if cj==None:
        cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    #opener = urllib2.build_opener()
    opener.addheaders = [('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                         ('Accept-Encoding','gzip, deflate'),
                         ('Referer', "http://www.mydootv.com/video.php"),
                         ('Content-Type', 'application/x-www-form-urlencoded'),
                         ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0'),
                         ('Connection','keep-alive'),
                         ('Accept-Language','en-us,en;q=0.5'),
                         ('Pragma','no-cache')]
    usock=opener.open(url,data)
    data = json.load(usock)
    usock.close()
    return data

def postContent(url,data,referr,cj):
    if cj==None:
        cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                         ('Accept-Encoding','gzip, deflate'),
                         ('Referer', referr),
                         ('Content-Type', 'application/x-www-form-urlencoded'),
                         ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0'),
                         ('Connection','keep-alive'),
                         ('Accept-Language','en-us,en;q=0.5'),
                         ('Pragma','no-cache')]
    usock=opener.open(url,data)
    if usock.info().get('Content-Encoding') == 'gzip':
           buf = StringIO.StringIO(usock.read())
           f = gzip.GzipFile(fileobj=buf)
           response= f.read()
    else:
           response= usock.read()
    usock.close()
    return (cj,response)


def playVideo(name,embedcode):
	rtmpurl = 'rtmp://cp76677.edgefcs.net/ondemand/'
	playpath = streamGetter(embedcode)
	rtmpurl = rtmpurl + playpath
	li = xbmcgui.ListItem(name, thumbnailImage="")
	li.setProperty('tagline', name)
	xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(rtmpurl, li)
def GetInput(strMessage,headtxt,ishidden):
    keyboard = xbmc.Keyboard("",strMessage,ishidden)
    keyboard.setHeading(headtxt) # optional
    keyboard.doModal()
    inputText=""
    if (keyboard.isConfirmed()):
        inputText = keyboard.getText()
    del keyboard
    return inputText

def getSettings(name,isencrypted):
    rtnvalue=None
    if os.path.isfile(settingfilename)!=False:
         f = open(settingfilename, "r")
         text = f.read()
         rtnvalue=re.compile('<'+name+'>(.+?)</'+name+'>', re.IGNORECASE).findall(text)
         if(len(rtnvalue) >0):
              rtnvalue=rtnvalue[0]
         else:
              rtnvalue=""
         if(isencrypted==True):
              rtnvalue=rtnvalue.decode('base-64')
    return rtnvalue
	
def setSettings(username,password,isencrypted):
    if(isencrypted==True):
         username=username.encode('base-64')
         password=password.encode('base-64')
    vfilecontent="<username>"+username.strip()+"</username><password>"+password.strip()+"</password>"
    f = open(settingfilename, 'w');f.write(vfilecontent);f.close()
	
def AutoLogin(cj,url):
      if not os.path.exists(datapath): os.makedirs(datapath)
      if not os.path.exists(cookie_path): os.makedirs(cookie_path)
      if cj==None:
           cj = cookielib.LWPCookieJar()
      strUsername=getSettings('username',True)
      strpwd=getSettings('password',True)
      if strUsername != None and strUsername !="" and strpwd != None and strpwd !="":
           (cj,respon)=postContent("http://mypinoy.tv/customers/login","username="+strUsername+"&redirect_to="+urllib.quote_plus(url)+"&password="+strpwd,"http://mypinoy.tv",cj)
           cj.save(cookiefile, ignore_discard=True)
      cj.load(cookiefile,ignore_discard=True)
      return cj

def GetLoginCookie(cj,cookiefile):
      if not os.path.exists(datapath): os.makedirs(datapath)
      if not os.path.exists(cookie_path): os.makedirs(cookie_path)
      if cj==None:
           cj = cookielib.LWPCookieJar()
      strUsername=urllib.quote_plus(GetInput("Please enter your username","Username",False))
      if strUsername != None and strUsername !="":
           strpwd=urllib.quote_plus(GetInput("Please enter your password","Password",True))
           (cj,respon)=postContent("http://mypinoy.tv/customers/login","username="+strUsername+"&redirect_to=http%3A%2F%2Fmypinoy.tv%2F&password="+strpwd,"http://mypinoy.tv",cj)
           setSettings(strUsername,strpwd,True)
      cj.save(cookiefile, ignore_discard=True)
      cj=None
      cj = cookielib.LWPCookieJar()
      cj.load(cookiefile,ignore_discard=True)
      #(cj,respon)=postContent("http://www.mydootv.com/video.php","","http://www.mydootv.com/",cj)
      #if (respon.find("player_content") == -1):
      #          d = xbmcgui.Dialog()
      #          d.ok("Incorrect Login","Login failed",'Try logging in again')
tmpUser=getSettings('username',False)
tmpPwd=getSettings('password',False)
if cj==None:
      cj = cookielib.LWPCookieJar()
if (tmpUser == None or tmpUser =="") and (tmpPwd == None or tmpPwd ==""):
      if os.path.isfile(cookiefile)==False:
                   GetLoginCookie(cj,cookiefile)
elif (tmpUser != None and tmpUser !="") and (tmpPwd != None and tmpPwd !="") and os.path.isfile(cookiefile)==False:
      AutoLogin(cj)

cj.load(cookiefile,ignore_discard=True)
                 #GetLoginCookie(cj,cookiefile)

def parseDate(dateString):
    try:
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except:
        return datetime.datetime.today() - datetime.timedelta(days = 1) #force update


def checkGA():

    secsInHour = 60 * 60
    threshold  = 2 * secsInHour

    now   = datetime.datetime.today()
    prev  = parseDate(ADDON.getSetting('ga_time'))
    delta = now - prev
    nDays = delta.days
    nSecs = delta.seconds

    doUpdate = (nDays > 0) or (nSecs > threshold)
    if not doUpdate:
        return

    ADDON.setSetting('ga_time', str(now).split('.')[0])
    APP_LAUNCH()    
    
                    
def send_request_to_google_analytics(utm_url):
    ua='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
    import urllib2
    try:
        req = urllib2.Request(utm_url, None,
                                    {'User-Agent':ua}
                                     )
        response = urllib2.urlopen(req).read()
    except:
        print ("GA fail: %s" % utm_url)         
    return response
       
def GA(group,name):
        try:
            try:
                from hashlib import md5
            except:
                from md5 import md5
            from random import randint
            import time
            from urllib import unquote, quote
            from os import environ
            from hashlib import sha1
            VISITOR = ADDON.getSetting('ga_visitor')
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            if not group=="None":
                    utm_track = utm_gif_location + "?" + \
                            "utmwv=" + VERSION + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmt=" + "event" + \
                            "&utme="+ quote("5("+PATH+"*"+group+"*"+name+")")+\
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
                    try:
                        print "============================ POSTING TRACK EVENT ============================"
                        send_request_to_google_analytics(utm_track)
                    except:
                        print "============================  CANNOT POST TRACK EVENT ============================" 
            if name=="None":
                    utm_url = utm_gif_location + "?" + \
                            "utmwv=" + VERSION + \
                            "&utmn=" + str(randint(0, 0x7fffffff)) + \
                            "&utmp=" + quote(PATH) + \
                            "&utmac=" + UATRACK + \
                            "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
            else:
                if group=="None":
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + VERSION + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                else:
                       utm_url = utm_gif_location + "?" + \
                                "utmwv=" + VERSION + \
                                "&utmn=" + str(randint(0, 0x7fffffff)) + \
                                "&utmp=" + quote(PATH+"/"+group+"/"+name) + \
                                "&utmac=" + UATRACK + \
                                "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR, VISITOR,"2"])
                                
            print "============================ POSTING ANALYTICS ============================"
            send_request_to_google_analytics(utm_url)
            
        except:
            print "================  CANNOT POST TO ANALYTICS  ================" 
            
            
def APP_LAUNCH():
        versionNumber = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
        if versionNumber < 12:
            if xbmc.getCondVisibility('system.platform.osx'):
                if xbmc.getCondVisibility('system.platform.atv2'):
                    log_path = '/var/mobile/Library/Preferences'
                else:
                    log_path = os.path.join(os.path.expanduser('~'), 'Library/Logs')
            elif xbmc.getCondVisibility('system.platform.ios'):
                log_path = '/var/mobile/Library/Preferences'
            elif xbmc.getCondVisibility('system.platform.windows'):
                log_path = xbmc.translatePath('special://home')
                log = os.path.join(log_path, 'xbmc.log')
                logfile = open(log, 'r').read()
            elif xbmc.getCondVisibility('system.platform.linux'):
                log_path = xbmc.translatePath('special://home/temp')
            else:
                log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, 'xbmc.log')
            logfile = open(log, 'r').read()
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        elif versionNumber > 11:
            print '======================= more than ===================='
            log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, 'xbmc.log')
            logfile = open(log, 'r').read()
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        else:
            logfile='Starting XBMC (Unknown Git:.+?Platform: Unknown. Built.+?'
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        print '==========================   '+PATH+' '+VERSION+'  =========================='
        try:
            from hashlib import md5
        except:
            from md5 import md5
        from random import randint
        import time
        from urllib import unquote, quote
        from os import environ
        from hashlib import sha1
        import platform
        VISITOR = ADDON.getSetting('ga_visitor')
        for build, PLATFORM in match:
            if re.search('12',build[0:2],re.IGNORECASE): 
                build="Frodo" 
            if re.search('11',build[0:2],re.IGNORECASE): 
                build="Eden" 
            if re.search('13',build[0:2],re.IGNORECASE): 
                build="Gotham" 
            print build
            print PLATFORM
            utm_gif_location = "http://www.google-analytics.com/__utm.gif"
            utm_track = utm_gif_location + "?" + \
                    "utmwv=" + VERSION + \
                    "&utmn=" + str(randint(0, 0x7fffffff)) + \
                    "&utmt=" + "event" + \
                    "&utme="+ quote("5(APP LAUNCH*"+build+"*"+PLATFORM+")")+\
                    "&utmp=" + quote(PATH) + \
                    "&utmac=" + UATRACK + \
                    "&utmcc=__utma=%s" % ".".join(["1", VISITOR, VISITOR, VISITOR,VISITOR,"2"])
            try:
                print "============================ POSTING APP LAUNCH TRACK EVENT ============================"
                send_request_to_google_analytics(utm_track)
            except:
                print "============================  CANNOT POST APP LAUNCH TRACK EVENT ============================" 
checkGA()
def addLink(name,url,mode,iconimage,serverurl):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('tis-620'))+"&serverurl="+urllib.quote_plus(serverurl)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        contextMenuItems = []
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('tis-620'))
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
serverurl=None
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
        serverurl=urllib.unquote_plus(params["serverurl"])
except:
        pass
		
sysarg=str(sys.argv[1]) 		
if mode==None or url==None or len(url)<1:
        #OtherContent()
        HOME(cj)
elif mode==2:
        GA("INDEX",name)
        INDEX(url,name,cj)
elif mode==3:
        GA("Episodes",name)
        Episodes(url,name,cj)
elif mode==4:
        SEARCH(url,cj)     
elif mode==5:
        playVideo(name,url)
elif mode==8:
        GetLoginCookie(cj,cookiefile)
elif mode==14:
        GA("PlayVideo",name)
        GetVideoStream(name,url,cj)


	   
xbmcplugin.endOfDirectory(int(sysarg))
