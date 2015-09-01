import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
from xml.dom.minidom import Document
import datetime
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import SoupStrainer
try: import simplejson as json
except ImportError: import json

ADDON = __settings__ = xbmcaddon.Addon(id='plugin.video.KhmerTv')
home = __settings__.getAddonInfo('path')
filename = xbmc.translatePath(os.path.join(home, 'resources', 'KhmerTv.xml'))

if ADDON.getSetting('ga_visitor')=='':
    from random import randint
    ADDON.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))
    
PATH = "KhmerTv"  #<---- PLUGIN NAME MINUS THE "plugin.video"          
UATRACK="UA-40129315-1" #<---- GOOGLE ANALYTICS UA NUMBER   
VERSION = "1.0.3" #<---- PLUGIN VERSION
kodiversionNumber = int(xbmc.getInfoLabel("System.BuildVersion" )[0:2])
TAG_RE = re.compile(r'<[^>]+>')

try:

    DB_NAME = 	 ADDON.getSetting('db_name')
    DB_USER = 	 ADDON.getSetting('db_user')
    DB_PASS = 	 ADDON.getSetting('db_pass')
    DB_ADDRESS = ADDON.getSetting('db_address')

    if  ADDON.getSetting('use_remote_db')=='true' and DB_ADDRESS is not None and DB_USER is not None and DB_PASS is not None and DB_NAME is not None:
        import mysql.connector as database
        print 'Loading MySQL as DB engine'
        DB = 'mysql'
    else:
        print'MySQL not enabled or not setup correctly'
        raise ValueError('MySQL not enabled or not setup correctly')

except:

    try: 
        from sqlite3 import dbapi2 as database
        print 'Loading sqlite3 as DB engine'
    except: 
        from pysqlite2 import dbapi2 as database
        addon.log('pysqlite2 as DB engine')
    DB = 'sqlite'
    db_dir = os.path.join(xbmc.translatePath("special://database"), 'khmermusic.db')

def ListArtistType():
    addDir("FEMALE SINGERS","http://www.muzik-online.net/search/label/Khmer%20New?&max-results=1",5,"")
    addDir("MALE SINGERS","http://www.muzik-online.net/search/label/Khmer%20New?&max-results=1",5,"")

def ListArtist(url,arttype):
    sql = 'SELECT * FROM artist where art_type =? ORDER BY name'

    if DB == 'mysql':
        db = database.connect(DB_NAME, DB_USER, DB_PASS, DB_ADDRESS, buffered=True)
        sql = sql.replace('?','%s')
    else: db = database.connect( db_dir )
    cur = db.cursor()

    cur.execute(sql, (arttype,))
    favs = cur.fetchall()
    artist=""
    totalartist = 0
    addLink("Refresh Artist Database",url+"|"+arttype,8,"")
    for row in favs:
        totalartist=totalartist+1
        artistname = row[0]

        artisturl   = row[1].replace(" ","%20")

        artistimg   = row[2]

        addDir(artistname,artisturl,6,artistimg)


    db.close()
    if(totalartist==0):
        artistlist=GetArtist(url,arttype)
        for vurl,vimg,aname in artistlist:
                        cursql=""
                        addDir(TAG_RE.sub('', aname),vurl,6,vimg)
def ListAlbum(url):
    sql = 'SELECT distinct artist_url,album,img FROM songs where artist_url=? order by album'

    if DB == 'mysql':
        db = database.connect(DB_NAME, DB_USER, DB_PASS, DB_ADDRESS, buffered=True)
        sql = sql.replace('?','%s')
    else: db = database.connect( db_dir )
    cur = db.cursor()

    cur.execute(sql, (url,))
    favs = cur.fetchall()
    artist=""
    totalalbum = 0
    addLink("Refresh Album Database",url,9,"")
    for row in favs:
        totalalbum=totalalbum+1
        arturl = row[0]
        album   = row[1]
        albumimg   = row[2]
        addDir(album,arturl,7,albumimg)
    db.close()
    if(totalalbum==0):
        (SongList,xmlpath)=GetSongs(url)
        for albid,auth,alimg,alname,tracks in SongList:
                addDir(TAG_RE.sub('', alname),url,7,xmlpath+alimg)

def ListSongs(artist_url,album):

    sql = 'SELECT artist_url,album, img, name,url FROM songs where artist_url=? and album =? ORDER BY name'

    if DB == 'mysql':
        db = database.connect(DB_NAME, DB_USER, DB_PASS, DB_ADDRESS, buffered=True)
        sql = sql.replace('?','%s')
    else: db = database.connect( db_dir )
    cur = db.cursor()

    cur.execute(sql, (artist_url,album))
    favs = cur.fetchall()
    artist=""
    totalsong = 0
    xbmc.PlayList(0).clear()
    addLink("Play All",artist_url,10,"")
    for row in favs:
        totalsong=totalsong+1
        arturl = row[0]
        album=row[1]
        songImg=row[2]
        songname   = row[3]
        songurl   = row[4].replace(" ","%20")
        addPlaylist(songname,songurl,songImg,"")
        songitem(songname,songurl,songImg,album,artist, totalsong)


    db.close()
	
def songitem(songname,songurl,songImg,album,artist, totalsong):
        remfavstring = 'RunScript(plugin.video.1channel,%s,?mode=DeleteFav&section=%s&title=%s&year=%s&url=%s)' %(sys.argv[1],songImg,songname,"",songurl)
        cm = []
        cm.append(('Remove from Favorites', remfavstring))
		
        trackLabel = artist + " - " + album + " - " + songname
        item = xbmcgui.ListItem(label = trackLabel, thumbnailImage=songImg, iconImage=songImg)
        item.setPath(songurl)
        item.setInfo( type="Video", infoLabels={ "title": name, "album": album, "artist": artist} )
        item.setProperty('mimetype', 'audio/mpeg')
        item.setProperty("IsPlayable", "true")
        item.setProperty('title', songname)
        item.setProperty('album', album)
        item.setProperty('artist', artist)
        item.addContextMenuItems(cm, replaceItems=False)
        u=sys.argv[0]+"?url="+urllib.quote_plus(songurl)+"&mode=3&name="+urllib.quote_plus(songname)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=songurl,listitem=item,isFolder=False, totalItems=totalsong)

def initDatabase():

    print 'Building Khmermusic Database'

    if DB == 'mysql':

        db = database.connect(DB_NAME, DB_USER, DB_PASS, DB_ADDRESS, buffered=True)

        cur = db.cursor()

        cur.execute('CREATE TABLE IF NOT EXISTS artist ( name TEXT,artist_url VARCHAR(255) UNIQUE,img VARCHAR(255) ,art_type VARCHAR(255),PRIMARY KEY (url))')

        cur.execute('CREATE TABLE IF NOT EXISTS songs (artist_url VARCHAR(255), album TEXT,img VARCHAR(255) ,name TEXT, url VARCHAR(255) UNIQUE,PRIMARY KEY (url))')

        cur.execute('CREATE TABLE IF NOT EXISTS playlist (playlist_id,url VARCHAR(255), name UNIQUE)')



    else:

        if not os.path.isdir(os.path.dirname(db_dir)):

            os.makedirs(os.path.dirname(db_dir))

        db = database.connect(db_dir)

        db.execute('CREATE TABLE IF NOT EXISTS artist (name,artist_url PRIMARY KEY,img, art_type)')

        db.execute('CREATE TABLE IF NOT EXISTS songs ( artist_url, album TEXT,img,name, url PRIMARY KEY)')

        db.execute('CREATE TABLE IF NOT EXISTS playlist (playlist_id INTEGER PRIMARY KEY AUTOINCREMENT,song_id,url, name)')

    db.commit()

    db.close()

def GetContent2(url):
    try:
       net = Net()
       second_response = net.http_GET(url)
       return second_response.content
    except:	
       d = xbmcgui.Dialog()
       d.ok(url,"Can't Connect to site",'Try again in a moment')
	   
def GetContent(url):

    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('Accept-Encoding', 'gzip, deflate'),
        ('User-Agent', 'SupreNet_iPad/2.3.7.6 (iPad; iOS 8.3; Scale/2.00)'),
        ('Connection', 'keep-alive'),
        ('Accept-Language', 'en;q=1'),
        ('Host', 'mobile.interface.stmg.net.kh')]
    usock = opener.open(url)
    if usock.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(usock.read())
        f = gzip.GzipFile(fileobj=buf)
        response = f.read()
    else:
        response = usock.read()
    usock.close()
    return (response)
	
def GetArtist(url,name):
        dialog = xbmcgui.DialogProgress()
        dialog.create('Refreshing Data', 'Refreshing Database...')       
        dialog.update(0)
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\'','"')
        vidcontent=re.compile('<h2 class="title">'+name+'</h2>(.+?)</table>').findall(link)
        artlist1=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>\s*<img [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*><!-- End(.+?)-->').findall(vidcontent[0])
        artlist2=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>\s*<img [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*></a><!-- End(.+?)-->').findall(vidcontent[0])
        artlist = list(set(artlist1 + artlist2))
        for vurl,vimg,aname in artlist:
                        cursql=""
                        cursql = "REPLACE INTO artist( name,artist_url,img,art_type) VALUES('%s','%s','%s','%s'); " %(TAG_RE.sub('', aname),vurl.replace("'",""),vimg,name)
                        if DB == 'sqlite':
                                cursql = 'INSERT OR ' + cursql.replace('%s','?')
                        SaveData(cursql)
        dialog.close()
        return artlist
						
def GetSongs(url):
        dialog = xbmcgui.DialogProgress()
        dialog.create('Refreshing Data', 'Refreshing Database...')       
        dialog.update(0)
        link = GetContent(url)
        link = link.encode("UTF-8")
        link = ''.join(link.splitlines()).replace('\t','')
        embsrc=re.compile('<embed [^>]*flashvars=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
        xmlsrc = embsrc[0].split("&amp;")
        srchttp=""
        srcfile=""
        for parts in xmlsrc:
                keypair = parts.split("=")
                if keypair[0] =="pathToFiles":
                        srchttp=keypair[1]
                if keypair[0] =="contentXMLPath":
                        srcfile=keypair[1]
        full=srchttp+srcfile
        xmllink = GetContent(full)
        xmllink  = xmllink.decode("UTF-8").encode("UTF-8")
        xmllink  = ''.join(xmllink.splitlines()).replace('\t','')
        match=re.compile('<album id="(.+?)"><author>(.+?)</author><image>(.+?)</image><name [^>]*>(.+?)</name><tracks>(.+?)</tracks></album>', re.IGNORECASE).findall(xmllink)
        for albid,auth,alimg,alname,tracks in match:
                songs=re.compile('<item><song>(.+?)</song><title>(.+?)</title></item>', re.IGNORECASE).findall(tracks)
                for songurl,songname in songs:
                        cursql=""
                        cursql = "REPLACE INTO songs(artist_url,album,img, name, url) VALUES('%s','%s','%s','%s','%s'); " %(url,TAG_RE.sub('', alname),srchttp+alimg,songname.replace("'",""),songurl.replace("'",""))
                        if DB == 'sqlite':
                                cursql = 'INSERT OR ' + cursql.replace('%s','?')
                        SaveData(cursql)
        dialog.close()
        return (match,srchttp)
				
def SaveData(SQLStatement): #8888
    if DB == 'mysql':
        db = database.connect(DB_NAME, DB_USER, DB_PASS, DB_ADDRESS, buffered=True)
    else:
        db = database.connect( db_dir )
    cursor = db.cursor()
    #try: 
        
    #    builtin = 'XBMC.Notification(Save Favorite,Added to Favorites,2000)'
    #    xbmc.executebuiltin(builtin)
    #except database.IntegrityError: 
    #    builtin = 'XBMC.Notification(Save Favorite,Item already in Favorites,2000)'
    #    xbmc.executebuiltin(builtin)
    cursor.execute(SQLStatement)
    db.commit()
    db.close()
	
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
		
def Resolver(url):
		vidlink=url

		line1 = "Please Wait!  Loading selected video."
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%("",line1,3000,""))
		if(url.find("stmg.net.kh") > -1):
			mydata=GetContent(url)
			data = json.loads(mydata)
			if(kodiversionNumber < 15):
				vidlink=data["url"] + " live=true"
			else:
				vidlink=data["url"] 
		return vidlink
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
                                #if(len(itemXML.getElementsByTagName('resolve')) > 0):
								#	vurl=Resolver(itemXML.getElementsByTagName('link')[0].childNodes[0].data.strip())
                                addLink(vname,vurl,3,vimg)
	
def GetXMLChannel():
        f = open(filename, "r")
        text = f.read()
        xmlcontent=xml.dom.minidom.parseString(text)
        items=xmlcontent.getElementsByTagName('channel')
        addDir("Khmer Songs","",4,"")
        for channelitem in items:
                vname=channelitem.getElementsByTagName('name')[0].childNodes[0].data.strip()
                addDir(vname,"",2,"")


def PlayAll():
    pl=xbmc.PlayList(0)
    xbmc.Player(xbmc.PLAYER_CORE_MPLAYER).play(pl)
def playVideo(url):
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(url)
	
if os.path.isfile(db_dir)==False:
     initDatabase()
#GetArtist("http://www.muzik-online.net/2012/10/mp3-playlist-preab-sovath.html",'MALE SINGERS')
#GetSongs("http://www.muzik-online.net/2012/10/mp3-playlist-preab-sovath.html")
	 
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
        if versionNumber > 13:
			logname="kodi.log"
        else:
			logname="xbmc.log"
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
                log = os.path.join(log_path, logname)
                logfile = open(log, 'r').read()
            elif xbmc.getCondVisibility('system.platform.linux'):
                log_path = xbmc.translatePath('special://home/temp')
            else:
                log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, logname)
            logfile = open(log, 'r').read()
            match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
        elif versionNumber > 11:
            print '======================= more than ===================='
            log_path = xbmc.translatePath('special://logpath')
            log = os.path.join(log_path, logname)
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

def addLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        contextMenuItems = []
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok

def addPlaylist(name,url,iconimage,fanart):
        ok=True
        pl=xbmc.PlayList(0)
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo("Video", infoLabels={ "Title": name})
        liz.setProperty('mimetype', 'audio/mpeg')
        liz.setProperty( "Fanart_Image", fanart )
        pl.add(url, liz)
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
        GA("GetChannels",name)
        GetXMLChannel()
elif mode==2:
        ParseXml(name) 
elif mode==3:
        GA("PlayVideo",name)
        playVideo(Resolver(url))
elif mode==4:
        ListArtistType()
elif mode==5:
        ListArtist(url,name)
elif mode==6:
        ListAlbum(url)
elif mode==7:
        ListSongs(url,name)
elif mode==8:
        (url,artype)=url.split("|")
        GetArtist(url,artype)
        ListArtist(url,artype)
elif mode==9:
        GetSongs(url)
        ListAlbum(url)
elif mode==10:
        PlayAll()
		
xbmcplugin.endOfDirectory(int(sysarg))
