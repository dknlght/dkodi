import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
import json
import re
from xml.dom.minidom import Document
import datetime
import HTMLParser
import itertools
from textwrap import wrap
addonid='plugin.video.hdonline'
ADDON=__settings__ = xbmcaddon.Addon(id=addonid)

if ADDON.getSetting('ga_visitor')=='':
    from random import randint
    ADDON.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))
    
PATH = "hdonline"  #<---- PLUGIN NAME MINUS THE "plugin.video"          
UATRACK="UA-40129315-1" #<---- GOOGLE ANALYTICS UA NUMBER   
VERSION = "1.0.0" #<---- PLUGIN VERSION

home = __settings__.getAddonInfo('path')
filename = xbmc.translatePath(os.path.join(home, 'resources', 'sub.srt'))
sublang = ADDON.getSetting('sublang')
strdomain ="http://hdonline.vn"
enableSubtitle=ADDON.getSetting('enableSub')
enableProxy= ADDON.getSetting('enableProxy')
enableTrans= (ADDON.getSetting('enableTrans')=="true")
translanguage=ADDON.getSetting('translang')

reg_list = ["http://webcache.googleusercontent.com/search?q=cache:*url*"]
proxyurl = ADDON.getSetting('proxyurl')

try:
    import urllib2 as request
    from urllib import quote
except:
    from urllib import request
    from urllib.parse import quote

class Translator:
    string_pattern = r"\"(([^\"\\]|\\.)*)\""
    match_string =re.compile(
                        r"\,?\["
                           + string_pattern + r"\,"
                           + string_pattern + r"\,"
                           + string_pattern + r"\,"
                           + string_pattern
                        +r"\]")

    def __init__(self, to_lang, from_lang='en'):
        self.from_lang = from_lang
        self.to_lang = to_lang

    def translate(self, source):
        self.source_list = wrap(source, 1000, replace_whitespace=False)
        return ' '.join(self._get_translation_from_google(s) for s in self.source_list)

    def _get_translation_from_google(self, source):
        json5 = self._get_json5_from_google(source)
        return self._unescape(self._get_translation_from_json5(json5))

    def _get_translation_from_json5(self, content):
        result = ""
        pos = 2
        while True:
            m = self.match_string.match(content, pos)
            if not m:
                break
            result += m.group(1)
            pos = m.end()
        return result

    def _get_json5_from_google(self, source):
        escaped_source = quote(source, '')
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'}
        data="client=t&ie=UTF-8&oe=UTF-8&sl=%s&tl=%s&text=%s" % (self.from_lang, self.to_lang, escaped_source)
        req = request.Request(url="http://translate.google.com/translate_a/t", headers = headers)
        r = request.urlopen(req,data)
        return r.read().decode('utf-8')

    def _unescape(self, text):
        return json.loads('"%s"' % text)


try: 
        from sqlite3 import dbapi2 as database
        print 'Loading sqlite3 as DB engine'
except: 
        from pysqlite2 import dbapi2 as database
        addon.log('pysqlite2 as DB engine')
DB = 'sqlite'
db_dir = os.path.join(xbmc.translatePath("special://database"), 'hdonline.db')
translator= Translator(from_lang="vi", to_lang=translanguage)
def initDatabase():
    if DB != 'mysql':
        if not os.path.isdir(os.path.dirname(db_dir)):
            os.makedirs(os.path.dirname(db_dir))
        db = database.connect(db_dir)
        db.execute('CREATE TABLE "medias" ("media_id" INTEGER NOT NULL  UNIQUE , "media_name" VARCHAR, "media_type" VARCHAR, "media_url" VARCHAR PRIMARY KEY  NOT NULL , "mscinfo" VARCHAR, "addonid" VARCHAR, "imgurl" VARCHAR, "update_dt" DATETIME DEFAULT CURRENT_TIMESTAMP)')
        db.execute('CREATE TABLE "episodes" ("epi_id" VARCHAR PRIMARY KEY  NOT NULL, "epi_name" VARCHAR, "sub_url", "epi_desc" VARCHAR, "epi_img" VARCHAR, "media_id" INTEGER, "update_dt" DATETIME DEFAULT CURRENT_TIMESTAMP)')
        db.execute('CREATE TABLE "videolinks" ("vid_id" INTEGER NOT NULL ,"vid_domain" VARCHAR,"vid_img" VARCHAR,"vid_url" VARCHAR PRIMARY KEY  NOT NULL ,"isbroken" BOOL DEFAULT (0) ,"update_dt" DATETIME DEFAULT (CURRENT_TIMESTAMP) ,"epi_id" INTEGER, "referer_url" VARCHAR)')
        db.execute('CREATE TABLE "groupings" ("grp_id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL , "grp_name" VARCHAR, "media_id" INTEGER, "update_dt" DATETIME DEFAULT CURRENT_TIMESTAMP)')
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
	
def buildMovieInsertSQl(vidurl,vidname,vidtype,vidimg,vplot,parenturl,tablename,referer_url,isbroken=0):
    strSQL=""
    try:
         vidname= vidname.encode("utf-8")
    except: pass
    try:
         vidurl= vidurl.encode("utf-8")
    except: pass
    if(tablename=="media"):
         strSQL='INSERT OR REPLACE INTO medias(media_id, media_url,media_name,media_type,imgurl,addonid,update_dt)VALUES ("%s","%s","%s","%s","%s","%s",CURRENT_TIMESTAMP );' %(vidurl,vidurl,vidname,vidtype,vidimg,addonid)
    elif(tablename=="episodes"):
         strSQL='INSERT OR REPLACE INTO episodes(epi_id, sub_url,epi_name,epi_desc,media_id,update_dt)VALUES ("%s","%s","%s","%s","%s",CURRENT_TIMESTAMP );' %(vidurl,vidimg,vidname,vplot,parenturl)
    elif(tablename=="groupings"):
         strSQL='INSERT OR REPLACE INTO groupings(grp_name, media_id,update_dt)VALUES ("%s",(SELECT media_id FROM medias WHERE media_url = "%s"),CURRENT_TIMESTAMP );' %(vidname,vidurl)
    elif(tablename=="groupings2"):
         strSQL='INSERT OR REPLACE INTO groupings(grp_name, media_id,update_dt)VALUES ("%s",(select media_id from episodes where epi_id="%s"),CURRENT_TIMESTAMP );' %(vidname,vidurl)
    #think of how to group video parts.
    elif(tablename=="videolinks"):
         strSQL='INSERT OR REPLACE INTO videolinks(vid_id, vid_url,vid_domain,vid_img,epi_id,referer_url,update_dt,isbroken)VALUES (COALESCE((SELECT vid_id FROM videolinks WHERE vid_url = "%s"), (SELECT COALESCE((select MAX(vid_id) from videolinks), 0) + 1)),"%s","%s","%s","%s","%s",CURRENT_TIMESTAMP,%s );' %(vidurl,vidurl,vidname,vidimg,parenturl,referer_url,isbroken)
    try:
         strSQL= strSQL.encode("utf-8")
    except: pass
    #print strSQL
    return strSQL
	
def SaveMovieTVshow(vname,vurl,vimg,vtype):
        SaveData(buildMovieInsertSQl(vurl,vname,vtype,vimg,"","","media",vurl))
		
def SaveEpisodes(vname,vurl,vimg,parenturl):
        SaveData(buildMovieInsertSQl(vurl,vname,"",vimg,"",parenturl,"episodes",parenturl))
		
def SaveVideoLink(vname,vurl,vimg,parenturl):
        SaveData(buildMovieInsertSQl(vurl,vname,"",vimg,"",parenturl,"videolinks",parenturl))
def SaveGroupings(vname,vurl,type):
        SaveData(buildMovieInsertSQl(vurl,vname,"","","","",type,""))
		
def RemoveHTML(inputstring):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', inputstring)
	
def GetContentMob(url):
    proxy = urllib2.ProxyHandler({'http': proxyurl})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    opener.addheaders = [(
        'Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
        ('Accept-Encoding', 'gzip, deflate'),
        ('Referer',"http://hdonline.vn/player/vplayer.swf"),
        #('Content-Type', 'application/x-www-form-urlencoded'),
        ('User-Agent', 'Mozilla/5.0 (Windows NT 5.2; rv:28.0) Gecko/20100101 Firefox/28.0'),
        ('Connection', 'keep-alive'),
        ('Accept-Language', 'en-us,en;q=0.5'),
        ('Pragma', 'no-cache'),
        ('Host','hdonline.vn')]
    usock = opener.open(url)
    if usock.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(usock.read())
        f = gzip.GzipFile(fileobj=buf)
        response = f.read()
    else:
        response = usock.read()
    usock.close()
    return response

def ShowLangDiag(translator):
	dialog = xbmcgui.Dialog()
	langlist ="Afrikaans|Albanian|Arabic|Azerbaijani|Basque|Bengali|Belarusian|Bulgarian|Catalan|Chinese Simplified|Chinese Traditional|Croatian|Czech|Danish|Dutch|English|Esperanto|Estonian|Filipino|Finnish|French|Galician|Georgian|German|Greek|Gujarati|Haitian Creole|Hebrew|Hindi|Hungarian|Icelandic|Indonesian|Irish|Italian|Japanese|Kannada|Khmer|Korean|Latin|Latvian|Lithuanian|Macedonian|Malay|Maltese|Norwegian|Persian|Polish|Portuguese|Romanian|Russian|Serbian|Slovak|Slovenian|Spanish|Swahili|Swedish|Tamil|Telugu|Thai|Turkish|Ukrainian|Urdu|Vietnamese|Welsh|Yiddish".split("|")
	langcode="af|sq|ar|az|eu|bn|be|bg|ca|zh-CN|zh-TW|hr|cs|da|nl|en|eo|et|tl|fi|fr|gl|ka|de|el|gu|ht|iw|hi|hu|is|id|ga|it|ja|kn|km|ko|la|lv|lt|mk|ms|mt|no|fa|pl|pt|ro|ru|sr|sk|sl|es|sw|sv|ta|te|th|tr|uk|ur|vi|cy|yi".split("|")
	index = dialog.select('Choose the language to translate to', langlist)
	win = xbmcgui.Window(10000)
	ADDON.setSetting('translang', langcode[index])
	translanguage=langcode[index]
	translator= Translator(from_lang="vi", to_lang=translanguage)
	HOME(translator)
	
def GetContent(url, useProxy=False):
    strresult=""
    if useProxy==True:
        url = "http://webcache.googleusercontent.com/search?q=cache:*url*".replace("*url*",urllib.quote_plus(url))
    try:
		opener = urllib2.build_opener()
		opener.addheaders = [('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
							 ('Accept-Encoding','gzip, deflate'),
							 ('Referer', "http://hdonline.vn/player/vplayer.swf"),
							 ('Content-Type', 'application/x-www-form-urlencoded'),
							 ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0'),
							 ('Connection','keep-alive'),
							 ('Accept-Language','en-us,en;q=0.5'),
							 ('Pragma','no-cache'),
							 ('Host','hdonline.vn')]
		usock=opener.open(url)
		if usock.info().get('Content-Encoding') == 'gzip':
			buf = StringIO.StringIO(usock.read())
			f = gzip.GzipFile(fileobj=buf)
			strresult = f.read()
		else:
			strresult = usock.read()
		usock.close()
    except Exception, e:
       print str(e)+" |" + url
    return strresult

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))
	
def Translate_lrge_str(string):
    totaltext =""
    chunksize=90000
    ctr=0
    pDialog = xbmcgui.DialogProgress()
    ret = pDialog.create('Please wait while text is being translated')
    percent = (ctr * 100)/chunksize
    remaining_display  = '[B]'+str(percent)+'%[/B] is done'
    pDialog.update(0,'Please wait while text is being translated',remaining_display)
    checklist=list(chunkstring(string, chunksize))
    for idx in checklist:
        transcontent = translator.translate(idx)
        totaltext=totaltext+transcontent.replace("- >","->").replace(" ->"," -->").replace("< / ","</").replace(" >",">")
        ctr = ctr + 1
        percent = (ctr * 100)/chunksize
        remaining_display = '[B]'+str(percent)+'%[/B] is done'
        pDialog.update(percent,'Please wait while text is being translated',remaining_display)

    return totaltext

def write2srt(url, fname):
    try:
          subcontent=GetContent(url).encode("utf-8")
    except:
          subcontent=GetContent(url)
    subcon=re.compile('vplugin\*\*\*(.+?)&').findall(subcontent+"&")
    if(len(subcon)>0):
          subcontent=decodevplug(subcon[0]).decode('base-64')
    if(enableTrans):
          subcontent=Translate_lrge_str(subcontent)
    try:
          subcontent=subcontent.encode("utf-8")
    except: pass

    f = open(fname, 'w');f.write(subcontent);f.close()

def json2srt(url, fname):

    data = json.load(urllib2.urlopen(url))['subtitles']

    def conv(t):
        return '%02d:%02d:%02d,%03d' % (
            t / 1000 / 60 / 60,
            t / 1000 / 60 % 60,
            t / 1000 % 60,
            t % 1000)

    with open(fname, 'wb') as fhandle:
        for i, item in enumerate(data):
            fhandle.write('%d\n%s --> %s\n%s\n\n' %
                (i,
                 conv(item['start_time']),
                 conv(item['end_time']),
                 item['content'].encode('utf8')))
def HOME(translator):
        #addDir('Search channel','search',5,'')

        useProxy=(enableProxy=="true")
        link = GetContent("http://hdonline.vn/",useProxy)
        link = ''.join(link.splitlines()).replace('\'','"')
        try:
            link =link.encode("UTF-8")
        except: pass
        staticmenu="Choose Translation Language|Search|View Cached Videos|New Movies"
        staticlist=staticmenu.split("|")
        if(enableTrans):
               transtext=translator.translate(staticmenu).replace(" | ","|")
               try:
                        transtext=transtext.encode("UTF-8")
               except: pass
               staticlist=transtext.split("|")
               addDir(staticlist[0],"http://hdonline.vn/",9,"")
        addDir(staticlist[1],"http://hdonline.vn/tim-kiem/superman.html",5,"")
        addDir(staticlist[2],"http://hdonline.vn/",7,"")
        addDir(staticlist[3],"http://hdonline.vn/danh-sach/phim-moi.html",2,"")
        vidcontent=re.compile('<nav class="tn-gnav">(.+?)</nav> ').findall(link)
        vidcontentlist=[]
        if(len(vidcontent)>0):
			vidcontentlist=re.compile('<li>(.+?)</div>\s*</div>\s*</li>').findall(vidcontent[0])
        for vidcontent in vidcontentlist:
            mainpart=re.compile('<a href="(.+?)"> <span class="tnico-(.+?)"></span>(.+?)</a>').findall(vidcontent)
            mainname=mainpart[0][2]
            splitcat=""
            vidlist=re.compile('<li><a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a></li>').findall(vidcontent)
            if(enableTrans):
                  transtext=mainname+"|"
                  for vurl,vname in vidlist:
                       transtext=transtext+"|"+vname
                  transtext=translator.translate(transtext).replace("| |","||")
                  try:
                        transtext=transtext.encode("UTF-8")
                  except: pass
                  splitcat=transtext.split("||")
                  mainname=splitcat[0]
            addLink(mainname,"",0,'')
            if(len(splitcat)>1):
				tranlist=splitcat[1].split("|")
            ctr=0
            for vurl,vname in vidlist:
				if(enableTrans):
					vname=tranlist[ctr]
					try:
						vname=vname.encode("UTF-8")
					except:pass
				ctr=ctr+1
				if(vurl.find("javascript:") ==-1 and len(vurl) > 3):
					addDir("--"+vname,strdomain+vurl,2,"")

if os.path.exists(db_dir)==False:
	initDatabase()

def HOMEMob():
        #addDir('Search channel','search',5,'')
        addDir('Search Videos','search',12,'')
        link = GetContent("http://m.hdonline.vn//?noscript=true")
        link = ''.join(link.splitlines()).replace('\'','"')
        try:
            link =link.encode("UTF-8")
        except: pass
        vidcontentlist=re.compile('<div id="fnNav" class="sidebar none">(.+?)<div class="s-footer">').findall(link)
        if(len(vidcontentlist)>0):
             mainnavcontent=re.compile('<ul class="navigator">(.+?)</ul>').findall(vidcontentlist[0])
             if(len(mainnavcontent)>0):
                     mainnavitem=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(mainnavcontent[0])
                     for vurl,vname in mainnavitem:
                           addDir(vname,vurl,2,'')
        mainnavcontent=re.compile('<div class="glist">(.+?)</div>').findall(vidcontentlist[0])
        for glistcontent in mainnavcontent:
                     mainnavitem=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(glistcontent)
                     mainnavnames=re.compile('<h3 class="stitle">(.+?)</h3>').findall(glistcontent)
                     addLink(mainnavnames[0],"",0,"")
                     for vurl,vname in mainnavitem:
                           addDir("-----"+vname,vurl,2,'')


def decodevplug(_arg_1):
            import math
            _local_2 = "";
            _local_3 = list("1234567890qwertyuiopasdfghjklzxcvbnm")
            _local_4= len(_local_3)
            strlen=len(_arg_1)
            _local_5= list("f909e34e4b4a76f4a8b1eac696bd63c4")
            _local_6 = list(_arg_1[((_local_4 * 2) + 32):strlen])
            _local_7= list(_arg_1[0:(_local_4 * 2)])
            _local_8= []
            _local_9= _arg_1[((_local_4 * 2) + 32):strlen]
            _local_10 = 0
            while (_local_10 < (_local_4 * 2)):
                _local_11 = (_local_3.index(_local_7[_local_10]) * _local_4)
                _local_11 = (_local_11 + _local_3.index(_local_7[(_local_10 + 1)]))
                idx= int(math.floor((_local_10 / 2)) % len(_local_5))
                str(_local_5[idx])[0]
                _local_11 = (_local_11 - ord(str(_local_5[idx])[0]))
                _local_8.append(chr(_local_11))
                _local_10 = (_local_10 + 2)
				
            _local_10 = 0
            while (_local_10 < len(_local_6)):
                _local_11 = (_local_3.index(_local_6[_local_10]) * _local_4)
                _local_11 = (_local_11 + _local_3.index(_local_6[(_local_10 + 1)]))
                idx= int((math.floor((_local_10 / 2)) % _local_4))
                _local_11 = (_local_11 - ord(str(_local_8[idx])[0]))
                _local_2 = (_local_2 + chr(_local_11))
                _local_10 = (_local_10 + 2)

            return _local_2
			
def INDEXCache():
    sql = 'SELECT distinct media_name,imgurl,medias.media_id FROM medias inner join episodes on episodes.media_id = medias.media_id where addonid=? order by medias.update_dt desc' 

    db = database.connect(db_dir)
    cur = db.cursor()

    cur.execute(sql, (addonid,))
    favs = cur.fetchall()
    totalvideos = 0
    for row in favs:
        totalvideos=totalvideos+1
        try:
            media_name = row[0].encode("UTF-8")
        except:
            media_name = row[0]
        imgurl   = row[1].replace(" ","%20")
        media_id   = row[2]
        #print media_name+"+" +str(media_id)+"+"+imgurl
        addDir(media_name,str(media_id),8,imgurl)
    db.close()

def EpisodesCache(media_id,name):
    sql = 'SELECT epi_name,vid_url,sub_url,epi_desc, ifnull(vid_img,"") as epi_img FROM videolinks inner join episodes on episodes.epi_id = videolinks.epi_id where episodes.media_id = ? order by episodes.epi_id' 
    db = database.connect(db_dir)
    cur = db.cursor()

    cur.execute(sql, (media_id,))
    favs = cur.fetchall()
    totalcnt = 0
    
    for row in favs:
        totalcnt=totalcnt+1
        try:
            media_name = row[0].encode("UTF-8")
        except:
            media_name = row[0]
        media_url   = row[1].replace(" ","%20")
        suburl= row[2]
        imgurl   = row[4]
        addLinkSub(media_name,media_url,3,imgurl,suburl)
    db.close()
	
def Index(url,name):
        useProxy=(enableProxy=="true")
        link = GetContent(url,False)
        link = ''.join(link.splitlines()).replace('\'','"')
        try:
            link =link.encode("UTF-8")
        except: pass
        vidcontentlist=re.compile('<ul id="cat_tatca"(.+?)</section>').findall(link)
        #trancontent=translator.translate(vidcontentlist[0]).replace(" = ","=").replace("< img","<img")
        if(len(vidcontentlist)>0):
			movielist=re.compile('<li>\s*<div class="tn-bxitem">(.+?)</li>').findall(vidcontentlist[0])
			#tranlist=re.compile('[^>]*alt=["\']?([^>^"^\']+)["\']?[^>]*>').findall(trancontent)
			transtext=""
			namelist=[]
			if(enableTrans):
				for vcontent in movielist:
					vname=re.compile('<h1 class="bxitem-txt">(.+?)</h1>').findall(vcontent)
					if(len(vname)>0):
						vname=vname[0]
					else:
						vname=re.compile('<p class="bxitem-txt">(.+?)</p>').findall(vcontent)[0]
					transtext=transtext+vname+"|"
				transtext=translator.translate(transtext).replace("| |","||")
				namelist=transtext.split("|")
			for idx in range(len(movielist)):
				vcontent = movielist[idx]
				vurl=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>').findall(vcontent)[0]
				vimgl=re.compile('<img [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(vcontent)
				vimg=""
				if(len(vimgl)>0):
					vimg=vimgl[0]
				if(len(namelist)>0):
					vname=namelist[idx]
				try:
					vname=vname.encode("UTF-8")
				except:pass
				vidid=vurl.split("-")[-1].replace('.html','')
				SaveMovieTVshow(vname.replace('"',"'"),vidid,vimg,"")
				addDir(vname,vidid,4,vimg)
        pagecontent=re.compile('<ul class="pagination">(.+?)</ul>').findall(link)
        if(len(pagecontent)>0):
			pagelist=re.compile('<li><a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a></li>').findall(pagecontent[0])
			for vurl,vname in pagelist:
				addDir("page "+vname,vurl,2,"")

def Episodes(vidid,name):
        url="http://hdonline.vn/episode/vxml?film="+vidid
        print url
        if (enableProxy=="true"):
            link = GetContentMob(url)
        else:
            link = GetContent(url,False)
        link = ''.join(link.splitlines()).replace('\'','"')
        try:
            link =link.encode("UTF-8")
        except: pass
        episodelist=re.compile('<item>(.+?)</item>').findall(link)
        epid="0"
        transtext=""
        namelist=[]
        ctr=0
        h = HTMLParser.HTMLParser()
        if(enableTrans):
			for episodecontent in episodelist:
				vname=re.compile('<title>(.+?)</title>').findall(episodecontent)[0]
				transtext=transtext+h.unescape(vname)+"|"
			try:
				transtext=transtext.encode("UTF-8")
			except: pass
			transtext=translator.translate(transtext).replace("| |","||")
			namelist=transtext.split("|")
        #innerlink=GetContentMob("http://hdonline.vn/vxml.php?episode=31501")
        #print decodevplug(str(innerlink).strip())
        for episodecontent in episodelist:
             vurl=re.compile('<jwplayer:file>(.+?)</jwplayer:file>').findall(episodecontent)[0]
             if(vurl.find("http") == -1):
                   vurl=decodevplug(vurl)
             if(vurl.find("xmlconfig") > -1):
				vurl=re.compile('<jwplayer:backuplink>(.+?)</jwplayer:backuplink>').findall(episodecontent)[0]
				if(vurl.find("http") == -1):
					vurl=decodevplug(vurl)
             if(len(namelist)>0):
                    vname=namelist[ctr]
             else:
                    vname=re.compile('<title>(.+?)</title>').findall(episodecontent)[0]
             try:
                    vname=h.unescape(vname).encode("UTF-8")
             except:
                    vname=h.unescape(vname)
             vimg=re.compile('<jwplayer:vplugin.image>(.+?)</jwplayer:vplugin.image>').findall(episodecontent.replace(":image",":vplugin.image"))[0]
             if(vimg.find("http") == -1):
                   vimg=decodevplug(re.compile('<jwplayer:vplugin.image>(.+?)</jwplayer:vplugin.image>').findall(episodecontent)[0])
             vsubtitle=re.compile('<jwplayer:vplugin.subfile>(.+?)</jwplayer:vplugin.subfile>').findall(episodecontent)
             epid=re.compile("<jwplayer:vplugin.episodeid>(.+?)</jwplayer:vplugin.episodeid>").findall(episodecontent)
             suburl=""
             if(len(vsubtitle)>0 and vsubtitle[0].find("http")>-1):
                 suburl=vsubtitle[0]
                 vname=vname+"(soft sub)"
             elif(len(vsubtitle)>0):
                 suburl=decodevplug(vsubtitle[0])
                 vname=vname+"(soft sub)"
             if(len(epid)>0):
                 epid=epid[0]
             SaveEpisodes(vname,epid,suburl,vidid)
             SaveVideoLink(vname,vurl,vimg,epid)
             addLinkSub(vname,vurl,3,vimg,suburl)
             ctr=ctr+1



def SEARCHVideos():
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        searchText = ''
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        searchurl="http://hdonline.vn/tim-kiem/"+searchText+".html"
        Index(searchurl,searchText.lower())



def playVideo(suburl,videoId):
        print videoId
        vidinfo = videoId.split("_")[0]
        win = xbmcgui.Window(10000)
        win.setProperty('1ch.playing.title', vidinfo)
        win.setProperty('1ch.playing.season', str(3))
        win.setProperty('1ch.playing.episode', str(4))
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoId)
        xbmcPlayer.setSubtitles(suburl) 



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
	
def parseDate(dateString):
    try:
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except:
        return datetime.datetime.today() - datetime.timedelta(days = 1) #force update

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

def playVideoPart(suburl,videoId,subfilepath):
        try:
                  json2srt(suburl, subfilepath)
        except:  
                  f = open(filename, 'w');f.write("");f.close()
        vidurl=getVideoUrl(videoId,"")
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(vidurl)
        xbmcPlayer.setSubtitles(subfilepath)

def addLinkSub(name,url,mode,iconimage,suburl):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&suburl="+urllib.quote_plus(suburl)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        contextMenuItems = []
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
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
subtitleurl=None
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

print "mode is:"+ str(mode)
sysarg=str(sys.argv[1]) 
if mode==None or url==None or len(url)<1:
        GA("Home","Home")
        HOME(translator)
elif mode==2:
        Index(url,name) 
elif mode==3:
        if(enableSubtitle=="true"):
           sublist=subtitleurl.split(",")
           if(len(sublist)>1):
               subtitleurl=sublist[int(sublang)]
           else:
               subtitleurl=sublist[0]
        else:
           subtitleurl=""
        write2srt(subtitleurl,filename)
        playVideo(filename,url)
elif mode==4:
        Episodes(url,name)
elif mode==5:
        SEARCHVideos()
elif mode==6:
        GA("Genre",name)
        Genre(url,name)
elif mode==7:
        INDEXCache()
elif mode==8:
        EpisodesCache(url,name)
elif mode==9:
        ShowLangDiag(translator)


xbmcplugin.endOfDirectory(int(sysarg))
