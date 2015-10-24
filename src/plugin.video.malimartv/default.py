import httplib
import urlparse,urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
import json
import time,datetime
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
from BeautifulSoup import SoupStrainer

from t0mm0.common.addon import Addon


__settings__ = xbmcaddon.Addon(id='plugin.video.malimartv')
home = __settings__.getAddonInfo('path')

datapath = xbmc.translatePath(os.path.join(home, 'resources', ''))
showadult = __settings__.getSetting('use-adult') == 'true'

strdomain ="https://www.malimar.tv/"
AZ_DIRECTORIES = ['0','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y', 'Z']
net = Net()
authtoken=__settings__.getSetting('authcode') 
strCreds=__settings__.getSetting('login') 
strLoginurl = "https://www.malimar.tv/sessions.json"

def GetInput(strMessage, headtxt, ishidden):
    keyboard = xbmc.Keyboard("", strMessage, ishidden)
    keyboard.setHeading(headtxt)  # optional
    keyboard.doModal()
    inputText = ""
    if keyboard.isConfirmed():
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
	
def postContent(url,data,authvalue):
    opener = urllib2.build_opener()
    if authvalue != None:
		authval='Basic ' + authvalue
    else:
		authval='Bearer ' + __settings__.getSetting('authcode') 
    headerdic= [('Accept','application/json, text/plain, */*'),
                         ('Accept-Encoding','gzip, deflate'),
                         ('Referer', "https://www.malimar.tv/sign_in"),
                         ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0.1'),
                         ('Connection','keep-alive'),
                         ('Accept-Language','en-us,en;q=0.5'),
                         ('Host','malimar.tv'),
                         ('Content-Length','2'),
                         ('Content-Type','application/json;charset=UTF-8'),
						 ('API-VERSION','v1'),
						 ('Authorization',authval)]
    opener.addheaders=headerdic
    try:
		usock=opener.open(url,data)
		print usock.info().get('Content-Encoding')
		if usock.info().get('Content-Encoding') == 'gzip':
			buf = StringIO.StringIO(usock.read())
			f = gzip.GzipFile(fileobj=buf)
			response = f.read()
		else:
			response = usock.read()
		usock.close()
    except urllib2.HTTPError, error_code:
			print error_code
			print "get error"
			if error_code.code == 401: 
				d = xbmcgui.Dialog()
				d.ok("Expired Session","Your session has expired",'Please Login again')
				GetLoginToken()
    return response
	
def GetContentNoHandler(url, authvalue=None):
    opener = urllib2.build_opener()
    if authvalue != None:
		authval='Bearer ' + authvalue
    else:
		authval='Bearer ' + __settings__.getSetting('authcode') 
    print url
    print "inside secondcontent"
    headerdic= [('Accept','application/json, text/plain, */*'),
                         ('Accept-Encoding','gzip, deflate'),
                         ('Referer', url),
                         ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0.1'),
                         ('Connection','keep-alive'),
                         ('Accept-Language','en-us,en;q=0.5'),
                         ('Host','malimar.tv'),
						 ('API-VERSION','v1'),
						 ('Authorization',authval)]
    opener.addheaders=headerdic
    response=""
    if True:
		usock=opener.open(url)
		print usock.info().get('Content-Encoding')
		if usock.info().get('Content-Encoding') == 'gzip':
			buf = StringIO.StringIO(usock.read())
			f = gzip.GzipFile(fileobj=buf)
			response = f.read()
		else:
			response = usock.read()
		usock.close()
    return response
	
def GetContent(url, authvalue=None):
    opener = urllib2.build_opener()
    if authvalue != None:
		authval='Bearer ' + authvalue
    else:
		authval='Bearer ' + __settings__.getSetting('authcode') 
    print url
    headerdic= [('Accept','application/json, text/plain, */*'),
                         ('Accept-Encoding','gzip, deflate'),
                         ('Referer', url),
                         ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0.1'),
                         ('Connection','keep-alive'),
                         ('Accept-Language','en-us,en;q=0.5'),
                         ('Host','malimar.tv'),
						 ('API-VERSION','v1'),
						 ('Authorization',authval)]
    opener.addheaders=headerdic
    response=""
    try:
    #if True:
		usock=opener.open(url)
		print usock.info().get('Content-Encoding')
		if usock.info().get('Content-Encoding') == 'gzip':
			buf = StringIO.StringIO(usock.read())
			f = gzip.GzipFile(fileobj=buf)
			response = f.read()
		else:
			response = usock.read()
		usock.close()
    except:
				d = xbmcgui.Dialog()
				response=AutoLogin(url)
    return response

def AutoLogin(url=""):
    strcredential=__settings__.getSetting('login')
    print "inside Autologin"
    strResult=""
    if strcredential is not None and strcredential != "":
        respon = postContent(strLoginurl,"",strcredential)
        data = json.loads(respon)
        __settings__.setSetting('authcode',data["sessions"]["id"])
        if(url!=""):
			strResult=GetContentNoHandler(url, authvalue=data["sessions"]["id"])
        return strResult
		
def GetLoginToken():
    strUsername = GetInput("Please enter your username", "Username", False)
    if strUsername is not None and strUsername != "":
        strpwd = urllib.quote_plus(GetInput("Please enter your password", "Password", True))
        strcredential=base64.b64encode(strUsername+":"+strpwd)
        __settings__.setSetting('login',strcredential)
        respon = postContent(strLoginurl,"",strcredential)
        data = json.loads(respon)
        __settings__.setSetting('authcode',data["sessions"]["id"])
        return data["sessions"]["id"]

if authtoken=="" and strCreds=="":
	authtoken=GetLoginToken()
	
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
    db_dir = os.path.join(xbmc.translatePath("special://database"), 'malimarfav.db')

def initDatabase():
    if DB == 'mysql':
        db = database.connect(DB_NAME, DB_USER, DB_PASS, DB_ADDRESS, buffered=True)
        cur = db.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS favorites (type VARCHAR(10), name TEXT, url VARCHAR(255) UNIQUE, imgurl VARCHAR(255))')
    else:
        if not os.path.isdir(os.path.dirname(db_dir)):
            os.makedirs(os.path.dirname(db_dir))
        db = database.connect(db_dir)
        db.execute('CREATE TABLE IF NOT EXISTS favorites (type, name, url, imgurl)')
    db.commit()
    db.close()
	
def SaveData(SQLStatement): #8888
    if DB == 'mysql':
        db = database.connect(DB_NAME, DB_USER, DB_PASS, DB_ADDRESS, buffered=True)
    else:
        db = database.connect( db_dir )
    cursor = db.cursor()
    cursor.execute(SQLStatement)
    db.commit()
    db.close()


		
def SaveFav(fav_type, name, url, img):
        print fav_type
        print url
        if fav_type == '': fav_type = getVideotype(url)
        statement  = 'INSERT INTO favorites (type, name, url, imgurl) VALUES (%s,%s,%s,%s)'
        if DB == 'mysql':
            db = database.connect(DB_NAME, DB_USER, DB_PASS, DB_ADDRESS, buffered=True)
        else:
            db = database.connect( db_dir )
            db.text_factory = str
            statement = statement.replace("%s","?")
        cursor = db.cursor()
        try: 
            cursor.execute(statement, (fav_type, urllib.unquote_plus(unicode(name,'latin1')), url, img))
            builtin = 'XBMC.Notification(Save Favorite,Added to Favorites,2000)'
            xbmc.executebuiltin(builtin)
        except database.IntegrityError: 
            builtin = 'XBMC.Notification(Save Favorite,Item already in Favorites,2000)'
            xbmc.executebuiltin(builtin)
        db.commit()
        db.close()
		
def AddFavContext(vidtype, vidurl, vidname, vidimg):
        runstring = 'RunScript(plugin.video.malimartv,%s,?mode=22&vidtype=%s&name=%s&imageurl=%s&url=%s)' %(sys.argv[1],vidtype,urllib.quote_plus(vidname.decode('utf-8', 'ignore')),vidimg,urllib.quote_plus(vidurl))
        cm =[] # add_contextsearchmenu(vidname.decode('utf-8', 'ignore'),vidtype)
        cm.append(('Add to malimartv Favorites', runstring))
        return cm
def ListFavorites():
      addDir('TV','tvshow',25,'')
      addDir('Movies','movie',25,'')
def BrowseFavorites(section):
    sql = 'SELECT type, name, url, imgurl FROM favorites WHERE type = ? ORDER BY name'
    if DB == 'mysql':
        db = database.connect(DB_NAME, DB_USER, DB_PASS, DB_ADDRESS, buffered=True)
        sql = sql.replace('?','%s')
    else: db = database.connect( db_dir )
    cur = db.cursor()
    cur.execute(sql, (section,))
    favs = cur.fetchall()
    for row in favs:
        title      = row[1]
        favurl      = row[2]
        img      = row[3]
        vtype= row[0]
        fanart = ''
        cm = add_contextsearchmenu(title,vtype)
        remfavstring = 'RunScript(plugin.video.malimartv,%s,?mode=23&name=%s&url=%s)' %(sys.argv[1],urllib.quote_plus(title.encode('utf-8', 'ignore')),urllib.quote_plus(favurl.encode('utf-8', 'ignore')))
        cm.append(('Remove from Favorites', remfavstring))
        if(vtype=="movie"):
			nextmode=31
        else:
			nextmode=8
        addDirContext(title.encode('utf-8', 'ignore'),favurl.encode('utf-8', 'ignore'),nextmode,img,"",vtype,cm)
    db.close()

def DeleteFav(name,url): 
    builtin = 'XBMC.Notification(Remove Favorite,Removed '+name+' from Favorites,2000)'
    xbmc.executebuiltin(builtin)
    sql_del = 'DELETE FROM favorites WHERE name=%s AND url=%s'
    if DB == 'mysql':
            db = database.connect(DB_NAME, DB_USER, DB_PASS, DB_ADDRESS, buffered=True)
    else:
            db = database.connect( db_dir )
            db.text_factory = str
            sql_del = sql_del.replace('%s','?')
    cursor = db.cursor()
    cursor.execute(sql_del, (name, url))
    db.commit()
    db.close()
		
def HOME(authtoken):
        #addDir('Search Dramas','http://malimartv.se/',10,'')
        #addDir('Search Movies','http://malimartv.se/',9,'')
        addLink('Login','tvshow',31,'')
        addDir('Your Favorites','tvshow',25,'')
        try:
			ListShows(strdomain+"thumbnails.json?container=Premium_View_CF")
			GetGrid(strdomain+"grids.json?dashboard=Home")
			if(showadult==True):
				addDir('Adult +18',strdomain+'grids.json?dashboard=Adult18',4,'')
        except:
			try:
				ListShows(strdomain+"thumbnails.json?container=Premium_View_CF")
				GetGrid(strdomain+"grids.json?dashboard=Home")
				if(showadult==True):
					addDir('Adult +18',strdomain+'grids.json?dashboard=Adult18',4,'')
			except:
				__settings__.setSetting('authcode',"")

def GetGrid(url):
		resp=GetContent(url)
		data = json.loads(resp)
		for item in data["grids"]:
			link = strdomain+"thumbnails.json?container="+item["id"]
			vname=item["title"]
			if(item["id"]!="Premium_View_CF"):
				addDir(vname.encode("utf-8","ignore"),link,18,"")
				


def CreateList(videoLink):
        liz = xbmcgui.ListItem('[B]PLAY VIDEO[/B]', thumbnailImage="")
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.add(url=videoLink, listitem=liz)
		
def PLAYLIST_VIDEOLINKS(vidlist,name):
        ok=True
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
        #time.sleep(2)
        links = vidlist.split(',')
        pDialog = xbmcgui.DialogProgress()
        ret = pDialog.create('Loading playlist...')
        totalLinks = len(links)-1
        loadedLinks = 0
        remaining_display = 'Videos loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B] into XBMC player playlist.'
        pDialog.update(0,'Please wait for the process to retrieve video link.',remaining_display)
        
        for videoLink in links:
                CreateList(ParseVideoLink(videoLink,name,name+str(loadedLinks + 1)))
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                #print percent
                remaining_display = 'Videos loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B] into XBMC player playlist.'
                pDialog.update(percent,'Please wait for the process to retrieve video link.',remaining_display)
                if (pDialog.iscanceled()):
                        return False   
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playList)
        if not xbmcPlayer.isPlayingVideo():
                d = xbmcgui.Dialog()
                d.ok('videourl: ' + str(playList), 'One or more of the playlist items','Check links individually.')
        return ok
		



def add_contextsearchmenu(title, video_type):
    title=urllib.quote(title.encode('utf-8', 'ignore'))
    contextmenuitems = []
    #if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.1channel'):
    #    contextmenuitems.append(('Search 1channel',
    #                             'XBMC.Container.Update(%s?mode=%s&section=%s&query=%s)' % (
    #                                 'plugin://plugin.video.1channel/', '7000',video_type, title)))
    if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.icefilms'):
        contextmenuitems.append(('Search Icefilms',
                                 'XBMC.Container.Update(%s?mode=555&url=%s&search=%s&nextPage=%s)' % (
                                     'plugin://plugin.video.icefilms/', 'http://www.icefilms.info/', title, '1')))
    if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.movie25'):
        contextmenuitems.append(('Search Mash Up',
                                 'XBMC.Container.Update(%s?mode=%s&url=%s)' % (
                                     'plugin://plugin.video.movie25/', '4', title)))
    if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.tubeplus'):
        if video_type == 'tv':
            section = 'None'
            serurl='http://www.tubeplus.me/search/tv-shows/%s/'%(title)
        else:
            serurl='http://www.tubeplus.me/search/movies/"%s"/'%(title)
            section = 'movie'
       
        contextmenuitems.append(('Search tubeplus', 'XBMC.Container.Update(%s?mode=150&types=%s&url=%s&linkback=latesttv)' % (
            'plugin://plugin.video.tubeplus/', section, serurl)))
    if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.tvlinks'):
        if video_type == 'tv':
            contextmenuitems.append(('Search tvlinks', 'XBMC.Container.Update(%s?mode=Search&query=%s)' % (
                'plugin://plugin.video.tvlinks/', title)))
    if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.solarmovie'):
        if video_type == 'tv':
            section = 'tv-shows'
        else:
            section = 'movies'
        contextmenuitems.append(('Search solarmovie', 'XBMC.Container.Update(%s?mode=Search&section=%s&query=%s)' % (
            'plugin://plugin.video.solarmovie/', section, title)))

    return contextmenuitems
	
def GetDirVideoUrl(url):

    cj = cookielib.LWPCookieJar()

    class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):

        def http_error_302(self, req, fp, code, msg, headers):
            self.video_url = headers['Location']
            return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)

        http_error_301 = http_error_303 = http_error_307 = http_error_302

    redirhndler = MyHTTPRedirectHandler()

    opener = urllib2.build_opener(redirhndler, urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [(
        'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        ('Accept-Encoding', 'gzip, deflate'),
        ('Referer', url),
        ('Content-Type', 'application/x-www-form-urlencoded'),
        ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0'),
        ('Connection', 'keep-alive'),
        ('Accept-Language', 'en-us,en;q=0.5'),
        ('Pragma', 'no-cache')]
    # urllib2.install_opener(opener)
    usock = opener.open(url)
    return redirhndler.video_url

def ParseVideoLink(url,name,movieinfo):
    dialog = xbmcgui.DialogProgress()
    dialog.create('Resolving', 'Resolving video Link...')       
    dialog.update(0)
    if movieinfo=="direct":
		return url
    resp=GetContent(url)
    data = json.loads(resp)

    # borrow from 1channel requires you to have 1channel
    win = xbmcgui.Window(10000)
    win.setProperty('1ch.playing.title', movieinfo)
    win.setProperty('1ch.playing.season', str(3))
    win.setProperty('1ch.playing.episode', str(4))
    # end 1channel code
    redirlink=url
    if(data.has_key("episodes")):
		vidlink=data["episodes"]["stream_url"]
    if(data.has_key("channels")):
		vidlink=data["channels"]["stream_url"]
    dialog.close()
    return vidlink

def ListShows(url):
		resp=GetContent(url)
		data = json.loads(resp)
		for item in data["thumbnails"]:
			
			if(item["href"].find("/shows/") > -1):
				vlink = strdomain+"episodes.json?show="+item["id"]
				mode=8
			elif(item["href"].find("/dashboards/") > -1):
				vlink = strdomain+"grids.json?dashboard="+item["id"]
				mode=4
			elif(item["href"].find("/channels/") > -1):
				vlink =item["href"].replace(item["id"]+"?grid=",item["id"]+".json?grid=")
				mode=3
			else:
				vlink = strdomain+"thumbnails.json?container="+item["id"]
				mode=18
			vimg=item["cover_image"]["hd"]
			vname=item["title"].encode("utf-8","ignore")
			try:
				vplot=item["synopsis"].encode("utf-8","ignore")
			except: pass
			if(item["id"]!="Adult18"):
				if(mode==8):
					addDirContext(vname,vlink,mode,vimg,vplot,"tvshow")
				elif(mode==3):
					addLink(vname,vlink,mode,vimg)
				else:
					addDir(vname,vlink,mode,vimg,vplot)

			
			



def SEARCH(url,type):
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        searchText = ''
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        if(type=="movie"):
			url = 'http://movies.malimartv.se/?s='+searchText
			MovieIndex(url)
        else:
			url = 'http://malimartv.se/?s='+searchText
			ListShows(url)
		





def Episodes(url):
		resp=GetContent(url)
		data = json.loads(resp)
		for item in data["episodes"]:
			vimg=item["cover_image"]["hd"]
			vname=item["title"]
			vplot=item["synopsis"]
			vlink =item["href"].replace(item["id"]+"?show=",item["id"]+".json?show=")
			addLink(vname,vlink,3,vimg)



		
if os.path.isfile(db_dir)==False:
     initDatabase()
	 
def playVideo(url,name,movieinfo):
        vidurl=ParseVideoLink(url,name,movieinfo);
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(vidurl)
		
def RemoveHTML(strhtml):
            html_re = re.compile(r'<[^>]+>')
            strhtml=html_re.sub('', strhtml)
            return strhtml

def addDirContext(name,url,mode,iconimage,plot="",vidtype="", cm=[]):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&vidtype="+vidtype
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot": plot} )
        if(len(cm)==0):
                contextMenuItems = AddFavContext(vidtype, url, name, iconimage)
        else:
                contextMenuItems=cm
        liz.addContextMenuItems(contextMenuItems, replaceItems=False)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
    	
def addLink(name,url,mode,iconimage,movieinfo=""):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&movieinfo="+urllib.quote_plus(movieinfo)
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
		
def addDir(name,url,mode,iconimage,plot=""):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name,"Plot": plot} )
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
subtitleurl=None
alturl=None
try: 
        alturl=urllib.unquote_plus(params["alturl"])
except:
        pass
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
try:
        subtitleurl=urllib.unquote_plus(params["suburl"])
except:
        pass
try:
        vidtype=urllib.unquote_plus(params["vidtype"])
except:
        pass
try:
        imageurl=urllib.unquote_plus(params["imageurl"])
except:
        pass
try:
        movieinfo=urllib.unquote_plus(params["movieinfo"])
except:
        pass
		
sysarg=str(sys.argv[1]) 

print "currentmode" + str(mode)

if mode==None or url==None or len(url)<1:
        HOME(authtoken)
elif mode==3:
        playVideo(url,name,movieinfo)
elif mode==4:
        GetGrid(url)
elif mode==5:
        GenreList(url,18)
elif mode==6:
        GenreList(url,19)
elif mode==8:
        Episodes(url)
elif mode==9:
        SEARCH(url,"movie")
elif mode==10:
        SEARCH(url,"tv")
elif mode==18:
        ListShows(url)
elif mode==22:
        SaveFav(vidtype, name, url, imageurl)
elif mode==23:
        DeleteFav(name,url)
elif mode==24:
        ListFavorites()
elif mode==25:
        BrowseFavorites(url)
elif mode==28:
        PLAYLIST_VIDEOLINKS(url,name)
elif mode==30:
		MovieIndex(url)
elif mode==31:
		GetLoginToken()
elif mode==32:
		GetVideo(url)
elif mode==33:
		SensenLatestIndex(url)
xbmcplugin.endOfDirectory(int(sysarg))
