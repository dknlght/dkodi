import httplib
import urlparse,urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
import json
import urlresolver
import time,datetime
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
from BeautifulSoup import SoupStrainer
import core
from xml.dom.minidom import Document
from t0mm0.common.addon import Addon
import commands
import jsunpack
import math,random
import MyNet
__settings__ = xbmcaddon.Addon(id='plugin.video.onemovies')
addon_profile_path = xbmc.translatePath(os.path.join(xbmc.translatePath('special://profile'), 'addon_data', 'plugin.video.onemovies'))
home = __settings__.getAddonInfo('path')

datapath = xbmc.translatePath(os.path.join(home, 'resources', ''))

if not os.path.exists(addon_profile_path):
    try: xbmcvfs.mkdirs(addon_profile_path)
    except: os.mkdir(addon_profile_path)
	
_cookie_file = xbmc.translatePath(os.path.join(xbmc.translatePath(addon_profile_path), 'cookies.txt'))

def _is_cookie_file(the_file):
    exists = os.path.exists(the_file)
    if not exists:
        return False
    else:
        try:
            tmp = xbmcvfs.File(the_file).read()
            if tmp.startswith('#LWP-Cookies-2.0'):
                return True
            return False
        except:
            with open(the_file, 'r') as f:
                tmp = f.readline()
                if tmp == '#LWP-Cookies-2.0\n':
                    return True
                return False
				
def _create_cookie(the_file):
    try:
        if xbmcvfs.exists(the_file):
            xbmcvfs.delete(the_file)
        _file = xbmcvfs.File(the_file, 'w')
        _file.write('#LWP-Cookies-2.0\n')
        _file.close()
        return the_file
    except:
        try:
            _file = open(the_file, 'w')
            _file.write('#LWP-Cookies-2.0\n')
            _file.close()
            return the_file
        except:
            return ''

if not _is_cookie_file(_cookie_file):
    _cookie_file = _create_cookie(_cookie_file)

strdomain ="https://lookmovie.ag"
AZ_DIRECTORIES = ['0-9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y', 'Z']
GENRE_DIRECTORIES = ['action'
                                ,'adventure'
                                ,'animation'
                                ,'comedy'
                                ,'crime'
                                ,'drama'
                                ,'documentary'
                                ,'science-fiction'
                                ,'family'
                                ,'history'
                                ,'fantasy'
                                ,'horror'
                                ,'music'
                                ,'mystery'
                                ,'romance'
                                ,'thriller'
                                ,'war'
                                ,'western']
net2 = MyNet.MyNet(_cookie_file, cloudflare=True)

class InputWindow(xbmcgui.WindowDialog):# Cheers to Bastardsmkr code already done in Putlocker PRO resolver.
    def __init__(self, *args, **kwargs):
        self.cptloc = kwargs.get('captcha')
        self.img = xbmcgui.ControlImage(335,20,624,180,self.cptloc)
        self.addControl(self.img)
        self.kbd = xbmc.Keyboard()

    def get(self):
        self.show()
        self.kbd.doModal()
        if (self.kbd.isConfirmed()):
            text = self.kbd.getText()
            self.close()
            return text
        self.close()
        return False

def GetContent(url,referr=None):
    print url
    if(referr==None):
		referr=url
    headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                         'Accept-Encoding':'gzip, deflate',
                         'Referer': referr,
                         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
                         'Connection':'keep-alive',
                         'Accept-Language':'en-us,en;q=0.5',
                         'Pragma':'no-cache',
                         'Host':'lookmovie.ag'
	}
    resp = net2.http_GET(url,headers=headers,compression=True)
    net2.save_cookies(_cookie_file)
    return resp.content
    # opener = urllib2.build_opener()
    # opener.addheaders = 
    # usock=opener.open(url)
    # if usock.info().get('Content-Encoding') == 'gzip':
        # buf = StringIO.StringIO(usock.read())
        # f = gzip.GzipFile(fileobj=buf)
        # response = f.read()
    # else:
        # response = usock.read()
    # usock.close()
    # return response
	   
class MyHTTPRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        print "Cookie Manip Right Here"
        return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)

    http_error_301 = http_error_303 = http_error_307 = http_error_302
	
def GetContent2(url,cookievalue=None,referer=None):
    # headers={'Accept':'application/json, text/javascript, */*; q=0.01',
                         # 'Accept-Encoding':'gzip, deflate',
                         # 'Referer': url,
                         # 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
                         # 'Connection':'keep-alive',
                         # #'Cookie':cookievalue,
                         # 'X-Requested-With':'XMLHttpRequest',
                         # 'Host':'123movies.is'
	# }
    xbmc.log(url)
    if(referer==None):
		referer=url

    cj = cookielib.LWPCookieJar()
    cj.load(_cookie_file, ignore_discard=True)
    if(cookievalue!=None):
		arcookie=cookievalue.split("=")
		new_cookie = cookielib.Cookie(
			version=0, name=arcookie[0], value=arcookie[1], port=None, port_specified=False,
			domain='lookmovie.ag', domain_specified=False, domain_initial_dot=False,
			path='/', path_specified=True, secure=False, expires=None, discard=True,
			comment=None, comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
		cj.set_cookie(new_cookie)
    redirhndler = MyHTTPRedirectHandler()
    opener = urllib2.build_opener(redirhndler, urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('Accept','application/json, text/javascript, */*; q=0.01'),
                         ('Accept-Encoding','gzip, deflate, br'),
                         #('Referer', referer),
                         ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1'),
                         ('Connection','keep-alive'),
                         #('Cookie',cookievalue),
                         #('X-Requested-With','XMLHttpRequest'),
                         ('Host','lookmovie.ag')]
    usock=opener.open(url)
    if usock.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(usock.read())
        f = gzip.GzipFile(fileobj=buf)
        response = f.read()
    else:
        response = usock.read()
    usock.close()
    return response


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
    db_dir = os.path.join(xbmc.translatePath("special://database"), 'onemoviesfav.db')

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

def HostResolver(url):
		print "in HostResolver"
		parsed_uri = urlparse.urlparse(url)
		server=str(parsed_uri.netloc)
		server=server.split(".")
		if(len(server)>2):
			server=server[1]
		else:
			server=server[0]
		server=server.replace("180upload","one80upload")
		exec "from servers import "+server+" as server_connector"
		rtnstatus,msg = server_connector.test_video_exists( page_url=url )
		if(rtnstatus):
			video_urls = server_connector.get_video_url( page_url=url , video_password="" )
			return video_urls[0][1]
		else:
			return ""
		
def SaveFav(fav_type, name, url, img):
        if fav_type == '': fav_type = getVideotype(url)
        statement  = 'INSERT INTO favorites (type, name, url, imgurl) VALUES (%s,%s,%s,%s)'
        if DB == 'mysql':
            db = database.connect(DB_NAME, DB_USER, DB_PASS, DB_ADDRESS, buffered=True)
        else:
            db = database.connect( db_dir )
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
        runstring = 'RunScript(plugin.video.onemovies,%s,?mode=22&vidtype=%s&name=%s&imageurl=%s&url=%s)' %(sys.argv[1],vidtype,vidname.decode('utf-8'),vidimg,vidurl)
        cm = add_contextsearchmenu(vidname,vidtype)
        cm.append(('Add to onemovies Favorites', runstring))
        return cm
def ListFavorites():
      addDir('TV','tv',25,'')
      #addDir('Movies','movie',25,'')
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
        remfavstring = 'RunScript(plugin.video.onemovies,%s,?mode=23&name=%s&url=%s)' %(sys.argv[1],urllib.quote_plus(title.encode("utf-8")),urllib.quote_plus(favurl))
        cm.append(('Remove from Favorites', remfavstring))
        nextmode=8
        addDirContext(title,favurl,nextmode,img,"",vtype,cm)
    db.close()

def DeleteFav(name,url): 
    builtin = 'XBMC.Notification(Remove Favorite,Removed '+name+' from Favorites,2000)'
    xbmc.executebuiltin(builtin)
    sql_del = 'DELETE FROM favorites WHERE name=%s AND url=%s'
    if DB == 'mysql':
            db = database.connect(DB_NAME, DB_USER, DB_PASS, DB_ADDRESS, buffered=True)
    else:
            db = database.connect( db_dir )
            sql_del = sql_del.replace('%s','?')
    cursor = db.cursor()
    cursor.execute(sql_del, (name, url))
    db.commit()
    db.close()
		
def jav(a):
	b = a + ''
	code = ord(b[0])
	if (0xD800 <= code and code <= 0xDBFF):
		c = code;
		if (len(b) == 1):
			return code
		d = ord(b[1])
		return ((c - 0xD800) * 0x400) + (d - 0xDC00) + 0x10000
	if (0xDC00 <= code and code <= 0xDFFF):
		return code
	return code

def encode64(a):
	b = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
	i = 0
	cur=0 
	prev=0 
	byteNum=0, 
	result = [];
	while (i < len(a)):
		cur = ord(a[i])
		byteNum = i % 3
		if byteNum==0:
			result.append(b[cur >> 2])
		if byteNum==1:
			result.append(b[(prev & 3) << 4 | (cur >> 4)])
		if byteNum==2:
			result.append(b[(prev & 0x0f) << 2 | (cur >> 6)])
			result.append(b[cur & 0x3f])
		prev = cur
		i=i+1

	if (byteNum == 0):
		result.append(b[(prev & 3) << 4]);
		result.append("==")
	elif (byteNum == 1):
		result.append(b[(prev & 0x0f) << 2])
		result.append("=")

	return "".join(result)


def decodestring(a,b):
	c = "";
	i = 0;
	for i in range(0, len(a)): 
		d = a[i:i+1]
		estart=i % len(b) - 1
		if(estart<0):
			e = b[estart:] 
		else:
			e = b[estart:estart+1] 
		d = int(math.floor(jav(d) + jav(e)))
		d = chr(d)
		c = c + d
	return encode64(c)
	
def GenerateHash(id,mid):

	respon=GetContent2(strdomain+"ajax/movie_token?eid="+id+"&mid="+mid)
	hasval=respon.replace(" ","").replace("_","").replace(",","&").replace("'","").replace('"','').replace(";","")
	return hasval

def GetValuePair(id,key):
	try:
		from hashlib import md5
	except:
		from md5 import md5
		
	a = RandomString();
	fstr=id + key[46: 58]
	b = md5(fstr).hexdigest()
	return (a,b)

def RandomString():
	a = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz"
	b = 16
	c = ''
	for ctr in range(0, b): 
		d = int(math.floor(random.randint(0, len(a))))
		c = c+ a[d:d + 1]
	return c
	
def SEARCH():
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        searchText = ''
        if (keyb.isConfirmed()):
                searchText = keyb.getText()
        ListShows(strdomain+"/movies/search/?q="+urllib.quote_plus(searchText),name)
		
def ListAZ():
        for character in AZ_DIRECTORIES:
                addDir(character,strdomain+"/az-list/"+character,18,"")
				
def YEAR(vidtype):
        now = datetime.datetime.now()
        for i in range(70):
           iyear=str(now.year-i)
           if vidtype =='movie':
                        url2 = strdomain + '/?y[]='+iyear
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %iyear,url2,18,'')
                        
           else:
                        url2 = strdomain + '/movie/filter/movie/latest/all/all/'+url2+'/all/all'
                        addDir('[B][COLOR white]%s[/COLOR][/B]' %iyear,url2,18,'')
                        

						
def TV():
        addDir('[B][COLOR white]Most Favorite[/COLOR][/B]',strdomain+'/movie/filter/series/favorite/all/all/all/all/all',18,'')
        addDir('[B][COLOR white]Most Ratings[/COLOR][/B]',strdomain+'/movie/filter/series/rating/all/all/all/all/all',18,'')
        addDir('[B][COLOR white]Most Viewed[/COLOR][/B]',strdomain+'/movie/filter/series/view/all/all/all/all/all',18,'')
        addDir('[B][COLOR white]Top IMDB[/COLOR][/B]',strdomain+'/movie/filter/series/imdb_mark/all/all/all/all/all',18,'')
        #addDir('[B][COLOR white]Country[/COLOR][/B]',strdomain+'/movie/filter/series',18,'')
        addDir('[B][COLOR white]Latest[/COLOR][/B]',strdomain+'/shows',18,'')
        addDir('[B][COLOR white]Year[/COLOR][/B]',strdomain+'/movie/filter/series',11,'')
        #addDir('[B][COLOR white]Genre[/COLOR][/B]',strdomain+'/movie/filter/series',18,'')
        #addDir('[B][COLOR white]Year[/COLOR][/B]',strdomain+'/movie/filter/series',18,'')
		
def HOME():
		addDir("Search",strdomain,9,"")
		#addDir("A-Z List",strdomain,16,"")
		#addDir("TV",strdomain,26,"")
		addDir('[B][COLOR white]Latest Movies[/COLOR][/B]',strdomain+'/movies',18,'')
		# addDir('[B][COLOR white]Top IMDB[/COLOR][/B]',strdomain+'/movie/filter/movie/imdb_mark/all/all/all/all/all',18,'')
		addDir('[B][COLOR white]Year[/COLOR][/B]','movie',11,'')
		addDir('[B][COLOR white]Genre[/COLOR][/B]','movie',6,'')
		#addDir("Favorites","type",25,"")

		#addDir("TV Shows",strdomain+"movie/filter/series",18,"")

				
def GetSubMenu(MenuTitle):
		link = GetContent(strdomain)
		try:
			link =link.encode("UTF-8")
		except: pass
		newlink = ''.join(link.splitlines()).replace('\t','')
		soup  = BeautifulSoup(newlink)
		subcontent=soup.findAll('a', {"title" : MenuTitle})
		if len(subcontent)> 0:
			sublist = subcontent[0].parent
			for item in sublist.findAll('li'):
				link = item.a['href'].encode('utf-8', 'ignore')
				vname=str(item.a.contents[0]).strip()
				addDir(vname,link,18,"")
					
def ListShows(url,name):
	link = GetContent(url)
	try:
		link =link.encode("UTF-8")
	except: pass
	newlink = ''.join(link.splitlines()).replace('\t','')
	soup  = BeautifulSoup(newlink)
	subcontent=soup.findAll('div', {"class" : "flex-wrap-movielist"})
	if len(subcontent)> 0:
		sublist = subcontent[0]
		for item in sublist.findAll('a'):
			vimg = item.img
			if(vimg!=None and vimg.has_key("alt")):
				vlink = strdomain+item['href'].encode('utf-8', 'ignore')
				vname=vimg["alt"]
				try:
					vname =vname.encode("UTF-8")
				except: pass
				imgurl = strdomain+vimg["data-src"]
				#addDirContext(vname,vlink,8,imgurl,"","type")
				addLink(vname,vlink,34,imgurl,"","") 
	pagecontent=soup.findAll('ul', {"class" : "pagination"})
	if len(pagecontent)> 0:
		for item in pagecontent[0].findAll('a'):
			if(item.has_key("class")==False and item.parent.has_key("class")==False):
				vlink="https:"+item["href"]
				vname=item.contents[0].encode('utf-8', 'ignore')
				addDir("Page "+vname.strip(),vlink,18,'')

				
def AZIndex(url):
	link = GetContent(url)
	try:
		link =link.encode("UTF-8")
	except: pass
	newlink = ''.join(link.splitlines()).replace('\t','')
	soup  = BeautifulSoup(newlink)
	ServerList=soup.findAll('td', {"class" : "mlnh-thumb"})
	if len(ServerList) >0:
		for rowitem in ServerList:
			imgcell = rowitem
			vname=imgcell.a["title"]
			vlink=imgcell.a["href"]
			#showid=vlink.split("-")[-1].replace("/","")
			try:
				vname=vname.encode("utf-8")
			except:pass
			vimg = imgcell.a.img["src"]
			addDirContext(vname,vlink,8,vimg,"","type")
	pagecontent=soup.findAll('div', {"id" : "pagination"})
	if len(pagecontent)> 0:
		for item in pagecontent[0].findAll('a'):
			vlink=item["href"]
			vname=item.contents[0].encode('utf-8', 'ignore')
			if vlink!="#":
				addDir("Page "+vname.strip(),vlink,17,'')

			
	
				
def Episodes(mediaid,name):
	print "media_url|" + mediaid
	showid=mediaid.split("-")[-1].replace("/","")
	showname=mediaid.replace("-"+showid+"/","").split("/")[-1]
	#cookieurl ="https://hdonline.to/asset/images/"+showname
	#cookieval=GetContent(cookieurl,mediaid)
	link = GetContent2(strdomain+"ajax/movie_episodes/"+showid,None,mediaid)
	try:
		link =link.encode("UTF-8")
	except: pass
	data = json.loads(link)
	soup  = BeautifulSoup(data["html"])
	ServerList=soup.findAll('div', {"class" : re.compile("le-server server-item*")})
	for item in ServerList:
		
		srvname=item.findAll('strong')[0].contents[0].strip()
		addLink(srvname,"",0,"")
		if (srvname.lower().find("openload") > -1):
			mode=34
		else:
			mode=4
		mediatype="movie"
		episodenum=0
		season=1
		tvtitle=name
		ServerList=soup.findAll('div', {"class" : "les-content"})
		for epItem in ServerList[0].findAll('a'):
			if(epItem.has_key("data-id")):
				epID=epItem["data-id"]
				vLinkName=epItem.contents[0].strip()
				try:
					vLinkName=vLinkName.encode("UTF-8")
				except: pass
				#addDir("--"+vLinkName,epID,mode,'')
				epiname=vLinkName
				if (vLinkName.lower().find("episode") > -1):
					try:
						eparry= vLinkName.split(':')
						epiname= eparry[-1].strip()
						episodenum=int(eparry[0].lower().replace("episode","").strip())
						mediatype="episode"
						seasonarry=name.lower().split('- season')
						season=int(seasonarry[-1].strip())
						tvtitle=seasonarry[0].strip()
					except: pass
				else:
					epiname=tvtitle
				meta = {'tvshowtitle': tvtitle, 'title': epiname, 'mediatype': mediatype,'episode':episodenum,'season':season,'mirrorid':showid}
				addDirMeta("--"+vLinkName,epID,mode,'',meta)
				
def Mirrors(epid,name,strMeta):
	meta={}
	if(strMeta!=""):
		meta = json.loads(strMeta)
	hash=GenerateHash(epid,meta["mirrorid"])
	respon=GetContent2(strdomain+"ajax/movie_sources/"+epid+"?"+hash)
	data = json.loads(respon)
	suburl=""
	strLabel="default"

	if(len(data["playlist"][0]["tracks"])>0):
			suburl=data["playlist"][0]["tracks"][0]["file"]
	print suburl
	if(type(data["playlist"][0]["sources"]) is list ):
		for src in data["playlist"][0]["sources"]:
			if(src.has_key("label")):
				strLabel=src["label"]
			addLink(strLabel,src["file"],3,"",suburl,meta) 
	else:
		src=data["playlist"][0]["sources"]
		if(src.has_key("label")):
			strLabel=src["label"]
		addLink(strLabel,src["file"],3,"",suburl,meta) 





def GetJSON(url,data,referr):
    resp=GetContent2(url)
    data = json.loads(resp)
    return data
	
def GetJSON2(url,data,referr):
    resp=GetContent(url)
    data = json.loads(resp)
    return data
	
def CreateList(videoLink):
        liz = xbmcgui.ListItem('[B]PLAY VIDEO[/B]', thumbnailImage="")
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.add(url=videoLink, listitem=liz)
		
def PLAYLIST_VIDEOLINKS(vidlist,name):
        ok=True
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
        #time.sleep(2)
        links = vidlist.split('|')
        pDialog = xbmcgui.DialogProgress()
        ret = pDialog.create('Loading playlist...')
        totalLinks = len(links)-1
        loadedLinks = 0
        remaining_display = 'Videos loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B] into XBMC player playlist.'
        pDialog.update(0,'Please wait for the process to retrieve video link.',remaining_display)
        
        for videoLink in links:
                #CreateList(ParseVideoLink(videoLink,name,name+str(loadedLinks + 1)))
                CreateList(videoLink)
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
    title=urllib.quote(title)
    contextmenuitems = []
    if os.path.exists(xbmc.translatePath("special://home/addons/") + 'plugin.video.1channel'):
        contextmenuitems.append(('Search 1channel',
                                 'XBMC.Container.Update(%s?mode=%s&section=%s&query=%s)' % (
                                     'plugin://plugin.video.1channel/', '7000',video_type, title)))
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
	


			
def ParseVideoLink(url,name,movieinfo):
    dialog = xbmcgui.DialogProgress()
    dialog.create('Resolving', 'Resolving video Link...')       
    dialog.update(0)
    if movieinfo=="direct":
		return url
    link =GetContent(url)
    link = ''.join(link.splitlines()).replace('\'','"')
    # borrow from 1channel requires you to have 1channel
   
    # end 1channel code
    media_url = re.compile('id_movie:\s*(.+?),').findall(link)
    #print str(link)
    if(len(media_url)>0):
		infolink="https://false-promise.lookmovie.ag/api/v1/storage/movies?id_movie="+media_url[0]
		print infolink
		srclink=""
		srclink =GetJSON(infolink,srclink,strdomain)
		vidsrc="https://lookmovie.ag/manifests/movies/json/"+str(media_url[0])+"/"+str(srclink["data"]["expires"])+"/"+str(srclink["data"]["accessToken"])+"/master.m3u8"
		srclink =GetJSON2(vidsrc,srclink,strdomain)
		if(srclink.has_key("1080p" ==True) and srclink["1080p"].find("index.m3u8") > -1):
			return srclink["1080p"]
		elif (srclink.has_key("720p")==True and srclink["720p"].find("index.m3u8") > -1):
			return srclink["720p"]
		elif (srclink.has_key("480p")==True and srclink["480p"].find("index.m3u8") > -1):
			return srclink["480p"]
		print srclink
		
    try:
    #if True:
        if (redirlink.find("youtube") > -1):
                vidmatch=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(redirlink)
                vidlink=vidmatch[0][len(vidmatch[0])-1].replace('v/','')
                vidlink='plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid='+vidlink
        elif (redirlink.find("dailymotion") > -1):
                match=re.compile('http://www.dailymotion.com/embed/video/(.+?)\?').findall(redirlink)
                if(len(match) == 0):
                        match=re.compile('http://www.dailymotion.com/video/(.+?)&dk;').findall(redirlink+"&dk;")
                if(len(match) == 0):
                        match=re.compile('http://www.dailymotion.com/swf/(.+?)\?').findall(redirlink)
                if(len(match) == 0):
                	match=re.compile('www.dailymotion.com/embed/video/(.+?)\?').findall(redirlink.replace("$","?"))
                print match
                vidlink=getDailyMotionUrl(match[0])
        elif (redirlink.find(".me/embed") > -1 or redirlink.find(".net/embed") > -1 or redirlink.find(".me/gogo") > -1 or redirlink.find("embed.php?") > -1):
                media_url= ""
                media_url = re.compile('_url\s*=\s*"(.+?)";').findall(link)[0]
                vidlink = urllib.unquote_plus(media_url) #GetDirVideoUrl(media_url)
        elif (redirlink.find("yourupload") > -1 or redirlink.find("oose.io") > -1 or redirlink.find("yucache.net") > -1):
                media_url= ""
                media_url = re.compile('<meta property="og:video" [^>]*content=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                vidlink = media_url+"|referer=http://www.yourupload.com/jwplayer/jwplayer.flash.swf"
        elif (redirlink.find("video44") > -1):
                media_url= ""
                media_url = re.compile('file:\s*"(.+?)"').findall(link)
                if(len(media_url)==0):
                     media_url = re.compile('url:\s*"(.+?)"').findall(link)
                vidlink = media_url[0]
        elif (redirlink.find("videobug") > -1):
                media_url= ""
                media_url = re.compile('playlist:\s*\[\s*\{\s*url:\s*"(.+?)",').findall(link)[0]
                vidlink = urllib.unquote(media_url)
        elif (redirlink.find("play44") > -1):
                media_url= ""
                media_url = re.compile('playlist:\s*\[\s*\{\s*url:\s*"(.+?)",').findall(link)[0]
                vidlink = urllib.unquote(media_url)
        elif (redirlink.find("byzoo") > -1):
                media_url= ""
                media_url = re.compile('playlist:\s*\[\s*\{\s*url:\s*"(.+?)",').findall(link)[0]
                vidlink = urllib.unquote(media_url)
        elif (redirlink.find("vidzur") > -1 or redirlink.find("videofun") > -1 or redirlink.find("auengine") > -1):
                media_url= ""
                op = re.compile('playlist:\s*\[(.+?)\]').findall(link)[0]
                urls=op.split("{")
                for rows in urls:
                     if(rows.find("url") > -1):
                          murl= re.compile('url:\s*"(.+?)"').findall(rows)[0]
                          media_url=urllib.unquote_plus(murl)
                vidlink = media_url
        elif (redirlink.find("cheesestream") > -1 or redirlink.find("yucache") > -1):
                vidlink = re.compile('<meta property="og:video" content="(.+?)"/>').findall(link)[0]
        elif (redirlink.find("embed.novamov") > -1):
                vidid=re.compile('flashvars.file="(.+?)";').findall(link)[0] 
                vidkey =re.compile('flashvars.filekey="(.+?)";').findall(link)[0]
                vurl ="http://www.novamov.com/api/player.api.php?file="+urllib.quote_plus(vidid)+"&key="+urllib.quote_plus(vidkey)
                linkcontent=GetContent(vurl)
                vidlink =re.compile('url=(.+?)&').findall(linkcontent)[0]
        elif (redirlink.find("video.google.com") > -1):
                match=redirlink.split("docid=")
                glink=""
                newlink=redirlink+"&dk"
                if(len(match) > 0):
                        glink = GetContent("http://www.flashvideodownloader.org/download.php?u=http://video.google.com/videoplay?docid="+match[1].split("&")[0])
                else:
                        match=re.compile('http://video.google.com/googleplayer.swf.+?docId=(.+?)&dk').findall(newlink)
                        if(len(match) > 0):
                                glink = GetContent("http://www.flashvideodownloader.org/download.php?u=http://video.google.com/videoplay?docid="+match[0])
                gcontent=re.compile('<div class="mod_download"><a href="(.+?)" title="Click to Download">').findall(glink)
                if(len(gcontent) > 0):
                        vidlink=gcontent[0]
                else:
                        vidlink=""
        elif (redirlink.find("movshare") > -1):
                fileid=re.compile('flashvars.file="(.+?)";').findall(link)[0]
                codeid=re.compile('flashvars.cid="(.+?)";').findall(link)[0]
                keycode=re.compile('flashvars.filekey="(.+?)";').findall(link)[0]
                vidcontent=GetContent("http://www.movshare.net/api/player.api.php?codes="+urllib.quote_plus(codeid) + "&key="+urllib.quote_plus(keycode) + "&file=" + urllib.quote_plus(fileid))
                vidlink = re.compile('url=(.+?)\&').findall(vidcontent)[0]
        elif (redirlink.find("nowvideo") > -1):
                fileid=re.compile('flashvars.file="(.+?)";').findall(link)[0]
                codeid=re.compile('flashvars.cid="(.+?)";').findall(link)[0]
                keycode=re.compile('flashvars.filekey=(.+?);').findall(link)[0]
                keycode=re.compile('var\s*'+keycode+'="(.+?)";').findall(link)[0]
                vidcontent=GetContent("http://www.nowvideo.sx/api/player.api.php?codes="+urllib.quote_plus(codeid) + "&key="+urllib.quote_plus(keycode) + "&file=" + urllib.quote_plus(fileid))
                vidlink = re.compile('url=(.+?)\&').findall(vidcontent)[0]
        elif (redirlink.find("bestreams") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":"","hash":hash})
                dialog.close()
                do_wait('Waiting on link to activate', '', 2)
                dialog.create('Resolving', 'Resolving bestreams Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata+"&imhuman=Proceed+to+video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('setup\(\{\s*file:\s*"(.+?)",\s*').findall(pcontent)
                if(len(vidlink) == 0):
                        vidlink = re.compile('"file","(.+?)"').findall(pcontent)
                vidlink=vidlink[0]
        elif (redirlink.find("vidx") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":"","hash":hash})
                dialog.close()
                do_wait('Waiting on link to activate', '', 10)
                dialog.create('Resolving', 'Resolving vidx Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata+"&imhuman=Weiter+%2F+continue",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('setup\(\{\s*file:\s*"(.+?)",\s*').findall(pcontent)
                if(len(vidlink) == 0):
                        vidlink = re.compile('"file","(.+?)"').findall(pcontent)
                vidlink=vidlink[0]
        elif (redirlink.find("streamin") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":"","hash":hash})
                dialog.close()
                do_wait('Waiting on link to activate', '', 5)
                dialog.create('Resolving', 'Resolving streamin Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata+"&imhuman=Proceed+to+video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                tmplink = re.compile('setup\(\{\s*file:\s*"(.+?)",\s*streamer:\s*"(.+?)"').findall(pcontent)
                vidlink = tmplink[0][1]+"/"+tmplink[0][0] + " playPath="+tmplink[0][0]
                if(tmplink[0][0].find("http:") > -1):
                        #vidlink = re.compile('setup\(\{\s*file:\s*"(.+?)",\s*').findall(pcontent)
                        vidlink = tmplink[0][0]
        elif (redirlink.find("slickvid") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":"","hash":hash})
                dialog.close()
                do_wait('Waiting on link to activate', '', 5)
                dialog.create('Resolving', 'Resolving slickvid Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata+"&imhuman=Watch",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('file:\s*"(.+?)",').findall(pcontent)
                if(len(vidlink) == 0):
                        vidlink = re.compile('"file","(.+?)"').findall(pcontent)
                vidlink=vidlink[0]
        elif (redirlink.find("vidpaid") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":"","hash":hash})
                dialog.close()
                do_wait('Waiting on link to activate', '', 1)
                dialog.create('Resolving', 'Resolving vidpaid Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata+"&imhuman=Continue+to+Video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('setup\(\{\s*file:\s*"(.+?)",\s*').findall(pcontent)
                if(len(vidlink) == 0):
                        vidlink = re.compile('"file","(.+?)"').findall(pcontent)
                vidlink=vidlink[0]
        elif (redirlink.find("uploadnetwork") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                rand = re.compile('<input type="hidden" name="rand" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download2","rand":rand,"id":idkey,"referer":url,"method_free":"","method_premium":"","down_direct":"1"})
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('"file":\s*"(.+?)"').findall(pcontent)
                if(len(vidlink) == 0):
                        vidlink = re.compile('"file","(.+?)"').findall(pcontent)
                vidlink=vidlink[0]
        elif (redirlink.find("divxpress") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                rand = re.compile('<input type="hidden" name="rand" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download2","rand":rand,"id":idkey,"referer":url,"method_free":"","method_premium":"","down_direct":"1"})
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('swfobject.js"></script><script type="text/javascript">(.+?)</script>').findall(pcontent)
                if(len(packed) == 0):
                      packed = re.compile('<div id="player_code"><script type="text/javascript">(.+?)</script>').findall(pcontent)[0]
                      sUnpacked = unpackjs4(packed).replace("\\","")
                      vidlink = re.compile('src="(.+?)"').findall(sUnpacked)[0]
                else:
                      packed=packed[0]
                      sUnpacked = unpackjs4(packed).replace("\\","")
                      vidlink = re.compile('addVariable\("file",\s*"(.+?)"\)').findall(sUnpacked)

        elif (redirlink.find("videopremium") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                mfree = re.compile('<input type="submit" name="method_free" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download1","usr_login":"","id":idkey,"referer":"","method_free":mfree})
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('src="/swfobject.js"></script>\s*<script type="text/javascript">(.+?)</script>').findall(pcontent)[0]
                sUnpacked = unpackjs4(packed)  
                vidpart = re.compile('"file":"(.+?)",p2pkey:"(.+?)"').findall(sUnpacked)[0]
                vidswf = re.compile('embedSWF\("(.+?)",').findall(sUnpacked)[0]
                vidlink=""
                if(len(vidpart) > 0):
                        vidlink = "rtmp://e9.md.iplay.md/play/"+vidpart[1]+" swfUrl="+vidswf+" playPath="+vidpart[1] +" pageUrl=" + redirlink + " tcUrl=rtmp://e9.md.iplay.md/play"
                #vidlink="rtmp://e9.md.iplay.md/play/mp4:rx90tddtnfmc.f4v swfUrl=http://videopremium.tv/uplayer/uppod.swf pageUrl=http://videopremium.tv/rx90tddtnfmc playPath=mp4:rx90tddtnfmc.f4v tcUrl=rtmp://e9.md.iplay.md/play"
        elif (redirlink.find("faststream") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download1","usr_login":"","id":idkey,"fname":fname,"referer":url,"hash":hash})
                dialog.close()
                do_wait('Waiting on link to activate', '', 3)
                dialog.create('Resolving', 'Resolving faststream Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata+"&imhuman=Continue+to+video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('file:\s*"(.+?)",').findall(pcontent)[0]
        elif (redirlink.find("videomega") > -1):
                refkey= re.compile('\?ref=(.+?)&dk').findall(redirlink+"&dk")[0]
                vidcontent="http://videomega.tv/iframe.php?ref="+refkey
                pcontent=GetContent(vidcontent)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                urlcode = re.compile('if\s*\(!validstr\){\s*document.write\(unescape\("(.+?)"\)\);\s*}').findall(pcontent)[0]
                vidcontent=urllib.unquote_plus(urlcode)
                vidlink = re.compile('file:\s*"(.+?)",').findall(vidcontent)[0]
        elif (redirlink.find("v-vids") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                rand = re.compile('<input type="hidden" name="rand" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download2","rand":rand,"id":idkey,"referer":url,"method_free":"","method_premium":"","down_direct":"1"})
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('file:\s*"(.+?)",').findall(pcontent)[0]
        elif (redirlink.find("thefile") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                rand = re.compile('<input type="hidden" name="rand" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download2","rand":rand,"id":idkey,"referer":url,"method_free":"","method_premium":"","down_direct":"1"})
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = re.compile('<span>\s*<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>\s*</span>').findall(pcontent)[0][0]
        elif (redirlink.find("topvideo") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download1","usr_login":"","id":idkey,"fname":fname,"referer":url,"hash":hash})
                pcontent=postContent(redirlink,posdata+"&imhuman=Proceed+to+video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('jwplayer.key="(.+?)";</script>\s*<script type="text/javascript">(.+?)</script>').findall(pcontent)[0][1]
                sUnpacked = unpackjs4(packed)
                unpacked = sUnpacked.replace("\\","")
                vidlink = re.compile('file:"(.+?)",').findall(unpacked)[0]
        elif (redirlink.find("gamovideo") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download1","usr_login":"","id":idkey,"fname":fname,"referer":url,"hash":hash})
                dialog.close()
                do_wait('Waiting on link to activate', '', 5)
                dialog.create('Resolving', 'Resolving gamovideo Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata+"&imhuman=Proceed+to+video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('/jwplayer.js"></script>\s*<script type="text/javascript">(.+?)</script>').findall(pcontent)[0]
                sUnpacked = unpackjs4(packed)
                unpacked = sUnpacked.replace("\\","")
                vidlink = re.compile('file:"(.+?)",').findall(unpacked)[0]
        elif (redirlink.find("vodlocker") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                hash = re.compile('<input type="hidden" name="hash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download1","usr_login":"","id":idkey,"fname":fname,"referer":url,"hash":hash})
                dialog.close()
                do_wait('Waiting on link to activate', '', 3)
                dialog.create('Resolving', 'Resolving bestreams Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata+"&imhuman=Proceed+to+video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = ""
                vidlink2 = re.compile('setup\(\{\s*file: "(.+?)",\s*streamer: "(.+?)",\s*').findall(pcontent)
                if(len(vidlink2) > 0):
                        vidlink = vidlink2[0][1]+"/mp4:"+vidlink2[0][0]+" swfUrl=http://vodlocker.com/player/player.swf playPath=mp4:"+vidlink2[0][0]
        elif (redirlink.find("exashare") > -1):
                packed = re.compile('/jwplayer.js"></script>\s*<script type="text/javascript">(.+?)</script>').findall(link)[0]
                sUnpacked = unpackjs4(packed)
                unpacked = sUnpacked.replace("\\","")
                vidlink = re.compile('file:"(.+?)",').findall(unpacked)[0]
        elif (redirlink.find("sharesix") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download1","usr_login":"","id":idkey,"fname":fname,"referer":url})
                pcontent=postContent(redirlink,posdata+"&method_free=Free",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('swfobject.js"></script>\s*<script type="text/javascript">(.+?)</script>').findall(pcontent)[0]
                unpacked = unpackjs4(packed)
                if unpacked=="":
                        unpacked = unpackjs3(packed,tipoclaves=2)
                        
                unpacked = unpacked.replace("\\","")
                vidlink = re.compile('.addVariable\("file",\s*"(.+?)"').findall(unpacked)[0]
        elif (redirlink.find("bonanzashare") > -1):
                capchacon =re.compile('<b>Enter code below:</b>(.+?)</table>').findall(link)
                capchar=re.compile('<span style="position:absolute;padding-left:(.+?);[^>]*>(.+?)</span>').findall(capchacon[0])
                capchar=sorted(capchar, key=lambda x: int(x[0].replace("px","")))
                capstring =""
                for tmp,aph in capchar:
                        capstring=capstring+chr(int(aph.replace("&#","").replace(";","")))
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                rand = re.compile('<input type="hidden" name="rand" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                ddirect = re.compile('<input type="hidden" name="down_direct" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"id":idkey,"referer":url,"method_free":"","rand":rand,"method_premium":"","code":capstring,"down_direct":ddirect})
                newpcontent=postContent(redirlink,posdata,url)
                newpcontent=''.join(newpcontent.splitlines()).replace('\'','"')
                vidlink=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>Download the file</a>').findall(newpcontent)[0] 
        elif (redirlink.find("videozed") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                mfree = re.compile('<input type="submit" name="method_free"  value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":url,"method_free":mfree})
                pcontent=postContent(redirlink,posdata,"http://onemovies.com/")
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                capchacon =re.compile('<b>Enter code below:</b>(.+?)</table>').findall(pcontent)
                capchar=re.compile('<span style="position:absolute;padding-left:(.+?);[^>]*>(.+?)</span>').findall(capchacon[0])
                capchar=sorted(capchar, key=lambda x: int(x[0].replace("px","")))
                capstring =""
                for tmp,aph in capchar:
                        capstring=capstring+chr(int(aph.replace("&#","").replace(";","")))

                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(pcontent)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(pcontent)[0]
                mfree = re.compile('<input type="hidden" name="method_free" value="(.+?)">').findall(pcontent)[0]
                rand = re.compile('<input type="hidden" name="rand" value="(.+?)">').findall(pcontent)[0]
                ddirect = re.compile('<input type="hidden" name="down_direct" value="(.+?)">').findall(pcontent)[0]
                posdata=urllib.urlencode({"op":op,"id":idkey,"referer":url,"method_free":mfree,"rand":rand,"method_premium":"","code":capstring,"down_direct":ddirect})
                newpcontent=postContent(redirlink,posdata,url)
                newpcontent=''.join(newpcontent.splitlines()).replace('\'','"')
                packed = re.compile('<div id="player_code">(.+?)</div>').findall(newpcontent)[0]
                packed = packed.replace("</script>","")
                unpacked = unpackjs4(packed)  
                unpacked = unpacked.replace("\\","")
                vidsrc = re.compile('src="(.+?)"').findall(unpacked)
                if(len(vidsrc) == 0):
                         vidsrc=re.compile('"file","(.+?)"').findall(unpacked)
                vidlink=vidsrc[0]
        elif (redirlink.find("donevideo") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('action=""><input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                mfree = re.compile('<input type="submit" name="method_free"  value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":url,"method_free":mfree})
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('<div id="player_code">(.+?)</div>').findall(pcontent)[0]
                packed = packed.replace("</script>","")
                unpacked = unpackjs4(packed)  
                unpacked = unpacked.replace("\\","")
                vidlink = re.compile('src="(.+?)"').findall(unpacked)
                if(len(vidlink) == 0):
                        vidlink = re.compile('"file","(.+?)"').findall(unpacked)
                vidlink=vidlink[0]
        elif (redirlink.find("clicktovie") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                mfree = re.compile('<input type="submit" name="method_free" value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":url,"method_free":mfree})
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                capchacon =re.compile('another captcha</a>(.+?)</script>').findall(pcontent)[0]
                capchalink=re.compile('<script type="text/javascript" src="(.+?)">').findall(capchacon)
                strCodeInput="recaptcha_response_field"
                respfield=""
                if(len(capchalink)==0):
                         capchacon =re.compile('<b>Enter code below:</b>(.+?)</table>').findall(pcontent)
                         capchar=re.compile('<span style="position:absolute;padding-left:(.+?);[^>]*>(.+?)</span>').findall(capchacon[0])
                         capchar=sorted(capchar, key=lambda x: int(x[0].replace("px","")))
                         capstring =""
                         for tmp,aph in capchar:
                                  capstring=capstring+chr(int(aph.replace("&#","").replace(";","")))
                         puzzle=capstring
                         strCodeInput="code"
                else:
                         imgcontent=GetContent(capchalink[0])
                         respfield=re.compile("challenge : '(.+?)'").findall(imgcontent)[0]
                         imgurl="http://www.google.com/recaptcha/api/image?c="+respfield
                         solver = InputWindow(captcha=imgurl)
                         puzzle = solver.get()
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(pcontent)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(pcontent)[0]
                mfree = re.compile('<input type="hidden" name="method_free" value="(.+?)">').findall(pcontent)[0]
                rand = re.compile('<input type="hidden" name="rand" value="(.+?)">').findall(pcontent)[0]
                ddirect = re.compile('<input type="hidden" name="down_direct" value="(.+?)">').findall(pcontent)[0]
                #replace codevalue with capture screen
                posdata=urllib.urlencode({"op":op,"id":idkey,"referer":url,"method_free":mfree,"rand":rand,"method_premium":"","recaptcha_challenge_field":respfield,strCodeInput:puzzle,"down_direct":ddirect})
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('<div id="player_code">(.+?)</div>').findall(pcontent)[0]
                packed = packed.split("</script>")[1]
                unpacked = unpackjs4(packed)  
                unpacked = unpacked.replace("\\","")
                vidlink = re.compile('"file","(.+?)"').findall(unpacked)[0]
        elif (redirlink.find("vidbull") > -1):
                idkey = re.compile('<input type="hidden" name="id" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                rand = re.compile('<input type="hidden" name="rand" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":"download2","rand":rand,"id":idkey,"referer":url,"method_free":"","method_premium":"","down_direct":"1"})
                #They need to wait for the link to activate in order to get the proper 2nd page
                dialog.close()
                do_wait('Waiting on link to activate', '', 3)
                dialog.create('Resolving', 'Resolving vidbull Link...') 
                dialog.update(50)
                pcontent=postContent2(redirlink,posdata,url)
                #pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink= re.compile('<!--RAM disable direct link<a href="(.+?)" target="_top">').findall(pcontent)
                if(len(vidlink) > 0):
                         filename = vidlink[0].split("/")[-1:][0]
                         vidlink=vidlink[0].replace(filename,"video.mp4")
                else:
                         sPattern =  '<script type=(?:"|\')text/javascript(?:"|\')>eval\(function\(p,a,c,k,e,[dr]\)(?!.+player_ads.+).+?</script>'
                         r = re.search(sPattern, pcontent, re.DOTALL + re.IGNORECASE)
                         if r:
                              sJavascript = r.group()
                              sUnpacked = jsunpack.unpack(sJavascript)
                              stream_url = re.search('[^\w\.]file[\"\']?\s*[:,]\s*[\"\']([^\"\']+)', sUnpacked)
                              if stream_url:
                                    vidlink= stream_url.group(1)

        elif (redirlink.find("nosvideo") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","fname":fname,"rand":"","id":idkey,"referer":url,"method_free":"Continue+to+Video","method_premium":"","down_script":"1"})
                pcontent=postContent2(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                scriptcontent=re.compile('<div name="placeholder" id="placeholder">(.+?)</div></div>').findall(pcontent)[0]
                packed = scriptcontent.split("</script>")[1]
                unpacked = unpackjs4(packed)
                if unpacked=="":
                        unpacked = unpackjs3(packed,tipoclaves=2)
                        
                unpacked = unpacked.replace("\\","")

                xmlUrl=re.compile('"playlist=(.+?)&').findall(unpacked)[0]
                vidcontent = postContent2(xmlUrl,None,url)
                vidlink=re.compile('<file>(.+?)</file>').findall(vidcontent)[0]

        elif (redirlink.find("flashx.tv") > -1):
                idkey = re.compile('<input name="objectid" id="objectid" type="hidden" value="(.+?)" />').findall(link)[0]
                ebmurl="http://play.flashx.tv/player/embed.php?vid="+idkey
                plycontent=GetContent(ebmurl)
                plycontent= ''.join(plycontent.splitlines()).replace('\'','"')
                yes = re.compile('<input name="yes" type="hidden" value="(.+?)">').findall(plycontent)[0]
                sec = re.compile('<input name="sec" type="hidden" value="(.+?)">').findall(plycontent)[0]
                posdata=urllib.urlencode({"yes":yes,"sec":sec})
                plycontent=postContent2("http://play.flashx.tv/player/playfx.php",posdata,ebmurl)
                plycontent= ''.join(plycontent.splitlines()).replace('\'','"')
                playercode=re.compile('<object [^>]*data=["\']?([^>^"^\']+)["\']?[^>]*>').findall(plycontent)[0]
                playercode=playercode.split("config=")[1]
                finalcontent=GetContent(playercode)
                vidlink=re.compile('<file>(.+?)</file>').findall(finalcontent)
                if(len(vidlink)==0):
                      finalcontent=GetContent(playercode)
                      vidlink=re.compile('<file>(.+?)</file>').findall(finalcontent)[0]
                else:
                      vidlink=vidlink[0]
        elif (redirlink.find("speedvid") > -1):
                keycode=re.compile('\|image\|(.+?)\|(.+?)\|file\|').findall(link)
                domainurl=re.compile('\[IMG\](.+?)\[/IMG\]').findall(link)[0]
                domainurl=domainurl.split("/i/")[0]
                vidlink=domainurl+"/"+keycode[0][1]+"/v."+keycode[0][0]
        elif (redirlink.find("vreer") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)" />').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)" />').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)" />').findall(link)[0]
                rand = re.compile('<input type="hidden" name="hash" value="(.+?)" />').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","fname":fname,"hash":rand,"id":idkey,"referer":"","method_free":"Free Download"})
                #They need to wait for the link to activate in order to get the proper 2nd page
                dialog.close()
                do_wait('Waiting on link to activate', '', 20)
                dialog.create('Resolving', 'Resolving vreer Link...') 
                dialog.update(50)
                pcontent=postContent(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink=re.compile('file: "(.+?)",').findall(pcontent)[0]
        elif (redirlink.find("allmyvideos") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                mfree = re.compile('<input type="hidden" name="method_free" value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":url,"method_free":mfree})
                pcontent=postContent2(redirlink,posdata,url)
                packed = get_match( pcontent , "(<script type='text/javascript'>eval\(.*?function\(p,\s*a,\s*c,\s*k,\s*e,\s*d.*?)</script>",1)
                unpacked = unpackjs(packed)
                if unpacked=="":
                        unpacked = unpackjs3(packed,tipoclaves=2)
                        
                unpacked = unpacked.replace("\\","")
                try:
                    vidlink = get_match(unpacked,"'file'\s*\:\s*'([^']+)'")+"?start=0"+"|"+urllib.urlencode( {'Referer':'http://allmyvideos.net/player/player.swf','User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12'} )
                except:
                    vidlink = get_match(unpacked,'"file"\s*\:\s*"([^"]+)"')+"?start=0"+"|"+urllib.urlencode( {'Referer':'http://allmyvideos.net/player/player.swf','User-Agent':'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12'} )

        elif (redirlink.find("cyberlocker") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('action=""><input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":url,"method_free":"Free Download"})
                pcontent=postContent2(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('<div id="player_code">(.+?)</div>').findall(pcontent)[0]
                packed = packed.replace("</script>","")
                unpacked = unpackjs4(packed)  
                unpacked = unpacked.replace("\\","")
                vidlink = re.compile('name="src"value="(.+?)"').findall(unpacked)[0]
        elif (redirlink.find("promptfile") > -1):
                chash = re.compile('<input type="hidden" name="chash" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"chash":chash})
                pcontent=postContent2(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>Download File</a>').findall(pcontent)[0]
        elif (redirlink.find("veervid") > -1):
                posturl=re.compile('<form action="(.+?)" method="post">').findall(link)[0]
                pcontent=postContent(posturl,"continue+to+video=Continue+to+Video",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink=re.compile('so.addVariable\("file","(.+?)"').findall(pcontent)[0]
        elif (redirlink.find("sharerepo") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                ddirect = re.compile('<input type="hidden" name="down_direct" value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","fname":fname.encode('utf-8'),"id":idkey,"referer":url,"method_free":"Free Download","down_direct":ddirect})
                pcontent=postContent2(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('<div id="player_code">(.+?)</div>').findall(pcontent)[0]
                packed=packed.split("</script>")[1]
                unpacked = unpackjs4(packed)  
                unpacked = unpacked.replace("\\","")
                vidlink = re.compile('"file","(.+?)"').findall(unpacked)[0]
        elif (redirlink.find("nowdownloa") > -1):
                ddlpage = re.compile('<a class="btn btn-danger" href="(.+?)">Download your file !</a>').findall(link)[0]
                mainurl = redirlink.split("/dl/")[0]
                ddlpage= mainurl+ddlpage
                #They need to wait for the link to activate in order to get the proper 2nd page
                dialog.close()
                do_wait('Waiting on link to activate', '', 30)
                dialog.create('Resolving', 'Resolving nowdownloads Link...') 
                dialog.update(50)
                pcontent=GetContent(ddlpage)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                linkcontent =re.compile('Slow download</span>(.+?)</div>').findall(pcontent)[0]
                vidlink = re.compile('<a href="(.+?)" class="btn btn-success">').findall(linkcontent)[0]
        elif (redirlink.find("youwatch") > -1):
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                rand = re.compile('<input type="hidden" name="hash" value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","fname":fname,"hash":rand,"id":idkey,"referer":"","imhuman":"Slow Download","method_premium":""})
                #They need to wait for the link to activate in order to get the proper 2nd page
                dialog.close()
                do_wait('Waiting on link to activate', '', 10)
                dialog.create('Resolving', 'Resolving youwatch Link...') 
                dialog.update(50)
                pcontent=postContent2(redirlink,posdata,url)
                pcontent=''.join(pcontent.splitlines())
                packed = re.compile("<span id='flvplayer'></span>(.+?)</script>").findall(pcontent)[0]
                unpacked = unpackjs5(packed)  
                unpacked = unpacked.replace("\\","")
                vidlink = re.compile('file:"(.+?)"').findall(unpacked)[0]
        elif (redirlink.find("videoslasher") > -1):
                user=re.compile('user: ([^"]+),').findall(link)[0]
                code=re.compile('code: "([^"]+)",').findall(link)[0]
                hash1=re.compile('hash: "([^"]+)"').findall(link)[0]
                formdata = { "user" : user, "code": code, "hash" : hash1}
                data_encoded = urllib.urlencode(formdata)
                request = urllib2.Request('http://www.videoslasher.com/service/player/on-start', data_encoded) 
                response = urllib2.urlopen(request)
                ccontent = response.read()
                ckStr = cj['.videoslasher.com']['/']['authsid'].name+'='+cj['.videoslasher.com']['/']['authsid'].value
                playlisturl = re.compile('playlist: "(.+?)",').findall(link)[0]
                playlisturl = redirlink.split("/video/")[0]+playlisturl
                pcontent=postContent2(playlisturl,"",url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink= re.compile(':content url="([^"]+)" type="video/x-flv" [^>]*>').findall(pcontent)[0]
                vidlink= ( '%s|Cookie="%s"' % (vidlink,ckStr) )
        #elif (redirlink.find("billionuploads") > -1):
        #        vidlink=resolve_billionuploads(redirlink,tmpcontent)
        #elif (redirlink.find("movreel") > -1):
        #        vidlink=resolve_movreel(redirlink,tmpcontent)
        elif (redirlink.find("jumbofiles") > -1):
                vidlink=resolve_jumbofiles(redirlink,tmpcontent)
        elif (redirlink.find("glumbouploads") > -1):
                vidlink=resolve_glumbouploads(redirlink,tmpcontent)
        elif (redirlink.find("sharebees") > -1):
                vidlink=resolve_sharebees(redirlink,tmpcontent)
        elif (redirlink.find("uploadorb") > -1):
                vidlink=resolve_uploadorb(redirlink,tmpcontent)
        elif (redirlink.find("vidhog") > -1):
                vidlink=resolve_vidhog(redirlink,tmpcontent)
        elif (redirlink.find("speedyshare") > -1):
                vidlink=resolve_speedyshare(redirlink,tmpcontent)
        elif (redirlink.find("180upload") > -1):
                vidcode = re.compile('180upload.com/(.+?)dk').findall(redirlink+"dk")[0] 
                urlnew= 'http://180upload.com/embed-'+vidcode+'.html'
                link=GetContent(urlnew)
                file_code = re.compile('<input type="hidden" name="file_code" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                embed_width = re.compile('<input type="hidden" name="embed_width" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                embed_height = re.compile('<input type="hidden" name="embed_height" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                test34 = re.compile('<input type="hidden" name="test34" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"file_code":file_code,"referer":url,"embed_width":embed_width,"embed_height":embed_height,"test34":test34})
                pcontent=postContent2(urlnew,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('/swfobject.js"></script><script type="text/javascript">(.+?)</script>').findall(pcontent)[0]
                unpacked = unpackjs4(packed)
                if unpacked=="":
                        unpacked = unpackjs3(packed,tipoclaves=2)
                unpacked=unpacked.replace("\\","")
                vidlink = re.compile('addVariable\("file",\s*"(.+?)"\)').findall(unpacked)[0]
				
        else:
                if(redirlink.find("putlocker.com") > -1 or redirlink.find("sockshare.com") > -1):
                        redir = redirlink.split("/file/")
                        redirlink = redir[0] +"/file/" + redir[1].upper()
                sources = []
                label=name
                hosted_media = urlresolver.HostedMediaFile(url=redirlink, title=label)
                sources.append(hosted_media)
                source = urlresolver.choose_source(sources)
                print "inresolver=" + redirlink
                if source:
                        vidlink = source.resolve()
                else:
                        vidlink =HostResolver(redirlink)
    except:
                if(redirlink.find("putlocker.com") > -1 or redirlink.find("sockshare.com") > -1):
                        redir = redirlink.split("/file/")
                        redirlink = redir[0] +"/file/" + redir[1].upper()
                sources = []
                label=name
                hosted_media = urlresolver.HostedMediaFile(url=redirlink, title=label)
                sources.append(hosted_media)
                source = urlresolver.choose_source(sources)
                print "inresolver=" + redirlink
                if source:
                        vidlink = source.resolve()
                else:
                        vidlink =HostResolver(redirlink)
    dialog.close()
    return vidlink






		

def postContent(url,data,referr):
    opener = urllib2.build_opener()
    opener.addheaders = [('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                         ('Accept-Encoding','gzip, deflate'),
                         ('Referer', referr),
                         ('Content-Type', 'application/x-www-form-urlencoded'),
                         ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0'),
                         ('Connection','keep-alive'),
                         ('Accept-Language','en-us,en;q=0.5'),
                         ('Pragma','no-cache'),
                         ('Host','player.phim47.com')]
    usock=opener.open(url,data)
    if usock.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(usock.read())
        f = gzip.GzipFile(fileobj=buf)
        response = f.read()
    else:
        response = usock.read()
    usock.close()
    return response
	
def GenreList(mode):
        for genre in GENRE_DIRECTORIES:
			addDir(genre,strdomain+"/movies/genre/"+genre,mode,"")
					





#borrowed from pelisalacarta
def get_match(data,patron,index=0):
    matches = re.findall( patron , data , flags=re.DOTALL )
    return matches[index]


		
if os.path.isfile(db_dir)==False:
     initDatabase()
	 
def playVideo(url,name,playtype,movieinfo,strMeta):
		meta={}
		if(strMeta!=""):
			meta = json.loads(strMeta)
			print meta
		if(playtype!="direct"):
			vidurl=ParseVideoLink(url,name,playtype);
		else:
			vidurl=url;
		
		xbmcPlayer = xbmc.Player()
		liz = xbmcgui.ListItem(name, iconImage='DefaultVideo.png', thumbnailImage="")
		liz.setInfo(type='Video', infoLabels=meta)
		liz.setProperty("IsPlayable","true")
		liz.setPath(vidurl)
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz) 
		if(movieinfo!=None and movieinfo!=""):
			for i in range(500):
				if(xbmcPlayer.isPlaying()):
					print "Subtitle is delaying:"+ str(i*50)+" ms"
					break
				xbmc.sleep(50)
			else:
					print "subtitle timeout error"
			print "loading sub|" +movieinfo
			xbmcPlayer.setSubtitles(movieinfo) 
		
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
    	
def addLink(name,url,mode,iconimage,movieinfo="",meta={}):
        strMeta = json.dumps(meta)
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&movieinfo="+urllib.quote_plus(movieinfo)+"&meta="+urllib.quote_plus(strMeta)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels = meta)
        liz.setProperty("IsPlayable","true")
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
		
def addDirMeta(name,url,mode,iconimage,meta={}):
        strMeta = json.dumps(meta)
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name) +"&meta="+urllib.quote_plus(strMeta)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo(type='Video', infoLabels = meta)
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
imageurl=None
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
		
try:
        metainfo=urllib.unquote_plus(params["meta"])
except:
        pass

sysarg=str(sys.argv[1]) 

print "currentmode" + str(mode)
if mode==None or url==None or len(url)<1:
        HOME()
elif mode==3:
        playVideo(url,name,"direct",movieinfo,metainfo)
elif mode==34:
        playVideo(url,name,"",movieinfo,"")
elif mode==4:
        Mirrors(url,name,metainfo) 
elif mode==5:
        GetSubMenu(name)
elif mode==6:
        GenreList(18)
elif mode==8:
        Episodes(url,name)
elif mode==9:
        SEARCH()
elif mode==10:
        News()
elif mode==11:
		YEAR(url)
elif mode==16:
        ListAZ()
elif mode==17:
        AZIndex(url)
elif mode==18:
        ListShows(url,name)
elif mode==22:
        SaveFav(vidtype, name, url, imageurl)
elif mode==23:
        DeleteFav(name,url)
elif mode==24:
        ListFavorites()
elif mode==25:
        BrowseFavorites(url)
elif mode==26:
        TV()
        #testcontent()
elif mode==27:
        ListShows("name","tv",url,name,8)
elif mode==28:
        PLAYLIST_VIDEOLINKS(url,name)

xbmcplugin.endOfDirectory(int(sysarg))
