import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
import json
import re
import urlresolver
import HTMLParser
import urlparse
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
from BeautifulSoup import SoupStrainer
from xml.dom.minidom import Document
import datetime
import ssl
from functools import wraps
import math
import srt2ass
from textwrap import wrap
try:
    import urllib2 as request
    from urllib import quote
except:
    from urllib import request
    from urllib.parse import quote
	
ADDON=__settings__ = xbmcaddon.Addon(id='plugin.video.viki')

if ADDON.getSetting('ga_visitor')=='':
    from random import randint
    ADDON.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))
    
PATH = "Viki"  #<---- PLUGIN NAME MINUS THE "plugin.video"          
UATRACK="UA-40129315-1" #<---- GOOGLE ANALYTICS UA NUMBER   
VERSION = "1.1.8" #<---- PLUGIN VERSION

home = __settings__.getAddonInfo('path')
filename = xbmc.translatePath(os.path.join(home, 'resources', 'sub.srt'))
langfile = xbmc.translatePath(os.path.join(home, 'resources', 'lang.txt'))
strdomain ="https://www.viki.com"
enableProxy= ADDON.getSetting('enableProxy')
enableTrans= (ADDON.getSetting('enableTrans')=="true")
translanguage=ADDON.getSetting('translang')
showcomments=(ADDON.getSetting('showcomments')=="true")
reg_list = ["https://losangeles-s02-i01.cg-dialup.net/go/browse.php?u=*url*&b=7", 
            "https://bucharest-s05-i01.cg-dialup.net/go/browse.php?u=*url*&b=7",
            "https://frankfurt-s02-i01.cg-dialup.net/go/browse.php?u=*url*&b=7", 
            "https://frankfurt-s02-i01.cg-dialup.net/go/browse.php?u=*url*&b=7"]
proxyurl = reg_list[int(ADDON.getSetting('region'))]

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

translator= Translator(from_lang="en", to_lang=translanguage)

def RemoveHTML(inputstring):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', inputstring)
	
def GetContent2(url, useProxy=False):
    if useProxy==True:
        return GetContent2(url, useProxy)
    hostn= urlparse.urlparse(url).hostname
    conn = httplib.HTTPConnection(host=hostn,timeout=30)
    req = url.replace(url.split(hostn)[0]+hostn,'')
    headers = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"} 
    try:
        conn.request('GET',req,headers)
    except:
        print 'echec de connexion'
    content = conn.getresponse().read()
    conn.close()
    return content
	

def sslwrap(func):
    @wraps(func)
    def bar(*args, **kw):
        kw['ssl_version'] = ssl.PROTOCOL_TLSv1
        return func(*args, **kw)
    return bar

ssl.wrap_socket = sslwrap(ssl.wrap_socket)

def GetContent(url, useProxy=False):
    strresult=""
    response=None
    if useProxy==True:
        url = proxyurl.replace("*url*",urllib.quote_plus(url))
        #proxy_handler = urllib2.ProxyHandler({'http':us_proxy})
        #opener = urllib2.build_opener(proxy_handler)
        #urllib2.install_opener(opener)
        print "use proxy:" + str(useProxy) + url
    try:
        if(response!=None):
           connection.close()
        req = urllib2.Request(url)
        req.add_unredirected_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0')
        response = urllib2.urlopen(req)
        strresult=response.read()
        response.close()
    except Exception, e:
       print str(e)+" |" + url
       if(response!=None):
           connection.close()
    return strresult

def write2srt(url, fname):
    try:
          subcontent=GetContent(url).encode("utf-8")
    except:
          subcontent=GetContent(url)
    if(enableTrans):
          subcontent=Translate_lrge_str(subcontent)
    try:
          subcontent=subcontent.encode("utf-8")
    except: pass
    f = open(fname, 'w');f.write(subcontent);f.close()

def json2srt(url, fname):
    print "jsonurl|"+url
    data = json.loads(GetContent(url))
    print data[1]

    def conv(t):
        return '%02d:%02d:%02d,%03d' % (
            math.floor(t/3600),
            t / 60 % 60,
            t % 60,
            0)

    with open(fname+"1", 'wb') as fhandle:
        for i, item in enumerate(data):
            fhandle.write('%d\n%s --> %s\n%s\n\n' %
                (i,
                 conv(int(item['time'])),
                 conv(int(item['time'])+1),
                 item["value"].encode('utf8')))

def HOME(translator):
        #addDir('Search channel','search',5,'')
        staticmenu="Choose Translation Language|Search Videos|Find Video By Viki ID|Country|Updated Tv shows|Updated Movies|Updated clips|Select Subtitle Language"
        
        if(enableTrans):
               transtext=translator.translate(staticmenu).replace(" | ","|")
               try:
                        transtext=transtext.encode("UTF-8")
               except: pass
               staticlist=transtext.split("|")
               addDir(staticlist[0],'search',17,'')
        else:
               staticlist=staticmenu.split("|")

        addDir(staticlist[1],'search',12,'')
        addDir(staticlist[2],'search',16,'')
        addDir(staticlist[3],'https://www.viki.com/explore?sort=latest&country=china',2,'')
        addDir(staticlist[4],'https://www.viki.com/explore?sort=latest&type=series',8,'')
        addDir(staticlist[5],'https://www.viki.com/explore?sort=latest&type=movie',8,'')
        addDir(staticlist[6],'https://www.viki.com/explore?sort=latest&type=clip',8,'')
        if(enableTrans==False):
               addDir(staticlist[7],'https://www.viki.com/explore?sort=latest&country=indonesia',10,'')
def LangOption():
        addDir('Show All Languages','All',10,'')

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
	
def ListGenres(url,name):
        print ("ListGenres url = " + url)
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\'','"')
        try:
            link =link.encode("UTF-8")
        except: pass
        soup = BeautifulSoup(link)
        vidlist=soup.findAll('select', {"data-explore-type" : "country"})
        transtext=""
        namelist=[]
        ctr=0
        if(len(vidlist)>0):
			if(enableTrans):
				for vlist in vidlist[0].findAll('option'):
					vname=vlist.contents[0]
					transtext=transtext+RemoveHTML(vname)+"|"
				transtext=translator.translate(transtext).replace(" | ","|")
				namelist=transtext.split("|")
			for vlist2 in vidlist[0].findAll('option'):
				vurl="https://www.viki.com/explore?sort=latest&country="+vlist2["value"]
				vname=vlist2.contents[0]
				if(len(namelist)>0):
					vname=namelist[ctr]
				addDir(RemoveHTML(vname.encode("UTF-8","ignore")).replace("&amp;","&"),vurl,8,"")
				ctr=ctr+1
			
def SaveLang(langcode, name):
    f = open(langfile, 'w');f.write(langcode);f.close()   
    d = xbmcgui.Dialog()
    d.ok(name,"Language Saved",'')
    HOME(translator)

def Genre(url,name):
        print("Genre url = " + url + " name = " + name)
        link = GetContent(url,False)
        link = ''.join(link.splitlines()).replace('\'','"')
        try:
            link =link.encode("UTF-8")
        except: pass
        soup = BeautifulSoup(link)
        vidlist=soup.findAll('select', {"id" : "genre"})
        transtext=""
        namelist=[]
        ctr=0
        if(len(vidlist)>0):
			if(enableTrans):
				for vlist in vidlist[0].findAll('option'):
					vname=vlist.contents[0]
					transtext=transtext+vname+"|"
				transtext=translator.translate(transtext).replace(" | ","|")
				namelist=transtext.split("|")
			for vlist2 in vidlist[0].findAll('option'):
				vurl="https://www.viki.com/explore?sort=latest&genre="+vlist2["value"]
				vname=vlist.contents[0]
				vid=re.compile('data-tooltip-src="/container_languages_tooltips/(.+?).json"').findall(vlist)
				if(len(vid)==0):
						vid=re.compile('data-tooltip-src="/video_languages_tooltips/(.+?).json"').findall(vlist)
				vid=vid[0]
				#vurl=re.compile('<a href="(.+?)" class="thumbnail pull-left">').findall(vlist)[0]
				#vname=re.compile('<li class="media">(.+?)</li>').findall(vlist)
				(vname,vtmp1,vimg,vtmp2)=re.compile('<img alt="(.+?)" height="(.+?)" src="(.+?)" width="(.+?)" />').findall(vlist)[0]
				if(len(namelist)>0):
					vname=namelist[ctr]
					try:
						vname=vname.encode("UTF-8")
					except:pass
				if(vurl.find("/tv/") > -1):
						vlink = strdomain+"/related_videos?container_id="+vid+"&page=1&type=episodes"
						mode=7
				else:
						vurlist=vurl.split("/")
						vid=vurlist[len(vurlist)-1].split("-")[0]
						vlink =vid
						mode=4
				addDir(vname.decode("UTF-8"),vlink,mode,vimg)
				ctr=ctr+1
        pagelist=re.compile('<div class="pagination">(.+?)</div>').findall(link)
        if(len(pagelist) > 0):
                navlist=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(pagelist[0])
                for purl,pname in navlist:
                    addDir("page " + pname.replace("&rarr;",">").decode("utf-8"),strdomain+purl,6,"")

def UpdatedVideos(url,name):
        print("Updated Videos url = " + url + " name = " + name)
        useProxy=(enableProxy=="true")
        link = GetContent(url,useProxy)
        link = ''.join(link.splitlines()).replace('\'','"').replace("/go/browse.php?u=","").replace("http%3A%2F%2Fwww.viki.com","").replace("%2F","/").replace("&amp;b=1","")
        try:
            link =link.encode("UTF-8")
        except: pass
        soup = BeautifulSoup(link)
        mode=7
        transtext=""
        namelist=[]
        ctr=0
        listcontent=soup.findAll('div', {"class" : "thumbnail col-inline s6 m6 l3 js-follow-status js-express-player"})
        if(len(listcontent) >0):

			if(enableTrans):
				for divcotent in listcontent:
					if(divcotent.a.img!=None):
						vimg=divcotent.a.img["src"]
						vname=divcotent.a.img["alt"]
						transtext=transtext+vname+"|"
				transtext=translator.translate(transtext.encode("UTF-8","ignore")).replace(" | ","|")
				namelist=transtext.split("|")
			for divcotent in listcontent:
				vname=""
				vimg=""
				if(divcotent("img")!=None):
					img=divcotent("img")[0]
					vimg=img["src"]
					vname=img["alt"]
					if(len(namelist)>0):
						vname=namelist[ctr]
						vname=vname
				vlink=divcotent.a["href"]
				if(divcotent.a.has_key("data-watch-now-type")):
					vtype=divcotent.a["data-watch-now-type"]
					vid=divcotent.a["data-watch-now-episode"]
				else:
					spandata = divcotent.findAll('span', {"class" : "moonshine uppercase"})[0]
					vtype=spandata["data-watch-now-type"]          
					vid=spandata["data-watch-now-episode"]
          
				vidcon=divcotent["data-container-id"]
				if(vtype=="episode"):
					mode=7
					vlink= "http://api.viki.io/v4/containers/"+vidcon+"/episodes.json?per_page=1000&with_paging=true&page=1&blocked=true&sort=number&direction=desc&with_paywall=false&app=100000a"
				elif(vtype=="clip"):
					vlink=vid
					mode=4
				elif(vtype=="movie"):
					vlink=vid
					mode=4
				ctr=ctr+1
				addDir(vname.encode("UTF-8","ignore"),vlink,mode,urllib.unquote_plus(vimg.replace("&b=7","")))

        navcontent=soup.findAll('div', {"class" : "pagination"})
        if(len(navcontent) >0):
			for navitem in navcontent[0].findAll('a'):
				pname=navitem.contents[0]
				purl=urllib.unquote_plus(navitem["href"])
				addDir("page " + pname.replace("&rarr;",">").replace("&larr;","<"),strdomain+purl.replace(strdomain,""),8,"")
   


def getContainerID(url):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\t','')
        vidid,vtype=re.compile('"container":\{"id":"(.+?)","type":"(.+?)",').findall(link)[0]
        if(vtype=="series"):
			newurl="http://api.viki.io/v4/containers/"+vidid+"/episodes.json?per_page=1000&with_paging=true&page=1&blocked=true&sort=number&direction=desc&with_paywall=false&app=100000a"
        else:
		
			#vidid=re.compile('video_json\s*=\s*\{"id":"(.+?)",').findall(link)[0]
			print vidid
			newurl="http://api.viki.io/v4/series/"+vidid+"/clips.json?app=65535a"
        return newurl

def getRelatedVID(url):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\t','')
        vidcontent=re.compile('<li data-replace-with="(.+?)"').findall(link)
        return urllib.unquote_plus(vidcontent[0])
		
		
def getVidPage(url,page):
		url=urllib.unquote_plus(url)
		print ("getVidPage = " + url)

		if(url.find("/video_esi/") > -1):
			url=getContainerID(url)
		link = GetContent(url)
		data = json.loads(link)
		transtext=""
		namelist=[]
		ctr=0
		vimg=""
		if(enableTrans):
			for episode in data["response"]:
				vname = "Episode " + str(episode["number"]) +": "+ episode["container"]["titles"]["en"]
				transtext=transtext+vname+"|"
			transtext=translator.translate(transtext.encode("UTF-8","ignore")).replace(" | ","|")
			namelist=transtext.split("|")
		totalpage=round((int(data["count"])/50)+ .5)

		for episode in data["response"]:
			HD=False
			try:
				HD=episode['flags']['hd']
			except:pass
			vname = "Episode " + str(episode["number"]) +": "+ episode["container"]["titles"]["en"]
			vimg= episode["container"]["images"]["poster"]["url"]
			vid= episode["id"]
			if(len(namelist)>0):
				vname=namelist[ctr]
			if(HD):
				vname=vname+"(HD)"
			addDir(vname.encode("UTF-8","ignore"),vid,4,vimg)
			ctr=ctr+1
		if(url.find("page=") > -1):
			nextpagenum=re.compile('&page=(.+?)&').findall(url)
			nextnum=int(nextpagenum[0])+1
			prevnum=int(nextpagenum[0])-1
			if(nextnum <= totalpage):
				addDir("Next page>>",url.replace("page="+nextpagenum[0],"page="+str(nextnum)),7,vimg)
			if(prevnum >= 1):
				addDir("<<Previous page",url.replace("page="+nextpagenum[0],"page="+str(prevnum)),7,vimg)
				
def getVidPage2(url,page):
  url1=url
  if(url.find("related_videos") == -1):
        vcontainerid=getContainerID(url)
        url1=strdomain+"/related_videos?container_id="+vcontainerid+"&page=1&type=episodes"
  link = GetContent(url1)
  link = ''.join(link.splitlines()).replace('\'','"')
  if(len(link) ==0 or link.find("Oh no! Something went wrong.")!= -1):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\'','"')
        match=re.compile('<ul class="medias medias-block[^>]*data-slider-items="1">(.+?)</ul>').findall(link)
        link=match[0]
  
  try:
        link =link.encode("UTF-8")
  except: pass
  vidcontainer=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>\s*<div class="thumbnail-small pull-left">\s*<img alt="(.+?)" [^s][^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
  vidnum=re.compile('\/([0-9]*)([a-z]|\s*).json"').findall(link)
  transtext=""
  namelist=[]
  ctr=0
  if(enableTrans):
		for y in range(0, len(vidnum)):
			(vurl,vname,vimg) = vidcontainer[y]
			transtext=transtext+vname+"|"
		transtext=translator.translate(transtext).replace(" | ","|")
		namelist=transtext.split("|")
  for x in range(0, len(vidnum)):
       vid="".join(vidnum[x])
       if(vidnum[x][1]==""):
           vid=vidnum[x][0]+"v"
       (vurl,vname,vimg) = vidcontainer[x]
       if(len(namelist)>0):
			vname=namelist[ctr]
       try:
			vname=vname.encode("UTF-8")
       except:pass
       vurl = vurl.split("/videos/")[0]
       addDir(vname,vid,4,vimg)
       ctr=ctr+1
  #for vid,vtmp,vurl,vname,vimg in vidcontainer:
  #      vurl = vurl.split("/videos/")[0]
  #      addDir(vname,vid,4,vimg)
  pagelist=re.compile('<a class="btn btn-small btn-wide" href="#">Show more</a>').findall(link)
  if(len(pagelist) > 0):
          pagenum=re.compile('&page=(.+?)&type=episodes').findall(url1)
          pagectr=int(pagenum[0])+1
          addDir("page " + str(pagectr),url1.replace("&page="+pagenum[0]+"&","&page="+str(pagectr)+"&"),7,"")


def getLanguages(url, ltype):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\'','"')
        try:
            link =link.encode("UTF-8")
        except: pass
        soup = BeautifulSoup(link)
        vidlist=soup.findAll('select', {"id" : "language"})
        transtext=""
        namelist=[]
        ctr=0
        if(len(vidlist)>0):
			if(enableTrans):
				for vlist in vidlist[0].findAll('option'):
					vname=vlist.contents[0].encode("UTF-8","ignore")
					transtext=transtext+RemoveHTML(vname)+"|"
				transtext=translator.translate(transtext).replace(" | ","|")
				namelist=transtext.split("|")
			for vlist2 in vidlist[0].findAll('option'):
				vurl=vlist2["value"]
				vname=vlist2.contents[0].encode("UTF-8","ignore")
				if(len(namelist)>0):
					vname=namelist[ctr]
				if(vurl!="all"):
					addDir(vname,vurl,11,"")
				ctr=ctr+1
                             
					   
def checkLanguage(mediaid):
        data = GetVideoInfo(mediaid)
        f = open(langfile, "r")
        langs = f.read()
        langcnew=""
        try:
               transpercent=data["subtitle_completions"][langs]
               if(transpercent < 50):
                      langs="en"
                      xbmc.executebuiltin("Language is less then 50% finish,defaulting to english,5000)")
        except:
               langs="en"
               xbmc.executebuiltin("Language you selected isn't available,defaulting to english for this video,5000)")
        return langs
		
def SearchChannelresults(url,searchtext):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\'','"')
        vidlist=re.compile('<div class="thumb-container big-thumb">        <a href="(.+?)">          <img alt="(.+?)" class="thumb-design" src="(.+?)" />').findall(link)
        for vurl,vname,vimg in vidlist:
            vurl = vurl.split("/videos/")[0]
            addDir(vname.lower().replace("<em>"+searchtext+"</em>",searchtext),strdomain+vurl+"/videos",7,vimg)
        pagelist=re.compile('<div class="pagination">(.+?)</li>').findall(link)
        if(len(pagelist) > 0):
                navlist=re.compile('<a[^>]* href="(.+?)">(.+?)</a>').findall(pagelist[0])
                for purl,pname in navlist:
                    addDir("page " + pname.decode("utf-8"),strdomain+purl,13,"")
					
def SEARCHChannel():
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        searchText = ''
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        searchurl="https://www.viki.com/search_channel?q=" + searchText
        SearchChannelresults(searchurl,searchText.lower())
		
def getVideoUrl(url,name):
   #data = json.load(urllib2.urlopen(url))['streams']
   #for i, item in enumerate(data):
        if(url.find("dailymotion") > -1):
                dailylink = url+"&dk;"
                match=re.compile('www.dailymotion.pl/video/(.+?)-').findall(dailylink)
                if(len(match) == 0):
                        match=re.compile('/video/(.+?)&dk;').findall(dailylink)
                link = 'http://www.dailymotion.com/video/'+str(match[0])
                vidlink=getDailyMotionUrl(str(match[0]))
        elif (url.find("docs.google.com") > -1 or url.find("drive.google.com") > -1):  
                vidcontent = GetContent(url)
                html = vidcontent.encode("utf-8","ignore")
                stream_map = re.compile('fmt_stream_map","(.+?)"').findall(html)
                vidlink=""
                if(len(stream_map) > 0):
					formatArray = stream_map[0].replace("\/", "/").split(',')
					for formatContent in formatArray:
						 formatContentInfo = formatContent.split('|')
						 qual = formatContentInfo[0]
						 vidlink = (formatContentInfo[1]).decode('unicode-escape')
        elif(url.find("google") > -1):
            vidcontent=GetContent(url)
            vidmatch=re.compile('"application/x-shockwave-flash"\},\{"url":"(.+?)",(.+?),(.+?),"type":"video/mpeg4"\}').findall(vidcontent)
            vidlink=vidmatch[0][0]
        elif(url.find("youtube") > -1):
            vidmatch=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(url)
            vidlink=vidmatch[0][len(vidmatch[0])-1].replace('v/','')
            vidlink='plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid='+vidlink
        else:
            sources = []
            label=name
            hosted_media = urlresolver.HostedMediaFile(url=url, title=label)
            sources.append(hosted_media)
            source = urlresolver.choose_source(sources)
            print "urlrsolving" + url
            if source:
                vidlink = source.resolve()
            else:
                vidlink =""
        return vidlink
		
def getDailyMotionUrl(id):
    content = GetContent("http://www.dailymotion.com/embed/video/"+id)
    if content.find('"statusCode":410') > 0 or content.find('"statusCode":403') > 0:
        xbmc.executebuiltin('XBMC.Notification(Info:,'+translation(30022)+' (DailyMotion)!,5000)')
        return ""
    
    else:
        get_json_code = re.compile(r'dmp\.create\(document\.getElementById\(\'player\'\),\s*(.+?)}}\)').findall(content)[0]
        #print len(get_json_code)
        print get_json_code
        cc= json.loads(get_json_code+"}}")['metadata']['qualities']  #['380'][0]['url']
        #print cc
        if '1080' in cc.keys():
            #print 'found hd'
            return cc['1080'][0]['url']
        elif '720' in cc.keys():
            return cc['720'][0]['url']
        elif '480' in cc.keys():
            return cc['480'][0]['url']
        elif '380' in cc.keys():
            return cc['380'][0]['url']
        elif '240' in cc.keys():
            return cc['240'][0]['url']
        elif 'auto' in cc.keys():
            return cc['auto'][0]['url']
        else:
            xbmc.executebuiltin('XBMC.Notification(Info:, No playable Link found (DailyMotion)!,5000)')
		
def SearchVideoresults(url,searchtext=""):
        link = GetContent(url)
        link = ''.join(link.splitlines()).replace('\'','"')
        soup = BeautifulSoup(link)
        listcontent=soup.findAll('li', {"class" : "media row"})
        mode=7
        if(len(listcontent)>0):
          for item in listcontent:
            vname=""
            vimg=""
            
            try:
              divcotent = item.findAll('div', {"class" : "media-left col s6 m5 l4"})[0]
              if(divcotent.a.img!=None):
                vimg=divcotent.a.img["src"]
                vname=divcotent.a.img["alt"].encode("UTF-8","ignore")
              
              typeitem =item.findAll('p')[0]
              if (typeitem.a["href"].find("/tv/") > -1):
                mode=7
                vid=typeitem.a["href"].split("/tv/")[-1]
                vid=vid.split("-")[0]
                vlink= "http://api.viki.io/v4/containers/"+vid+"/episodes.json?per_page=1000&with_paging=true&page=1&blocked=true&sort=number&direction=desc&with_paywall=false&app=100000a"          
               
                #print(vname + " -- " + vlink)          
                addDir(vname.lower().replace("<em>"+searchtext+"</em>",searchtext),vlink,mode,vimg)
              elif (typeitem.a["href"].find("/movies/") > -1):
                mode=4
                vid=typeitem.a["href"].split("/movies/")[-1]
                vid=vid.split("-")[0]
                vlink= "http://api.viki.io/v4/videos/"+vid+".json?per_page=1000&with_paging=true&page=1&blocked=true&sort=number&direction=desc&with_paywall=false&app=100000a"
                link = GetContent(vlink)  
                data = json.loads(link)
                vlink = data["watch_now"]["id"]     
               
                #print(vname + " -- " + vlink)          
                addDir(vname.lower().replace("<em>"+searchtext+"</em>",searchtext),vlink,mode,vimg)
            except: pass
          
          pagelist=soup.findAll('div', {"class" : "pagination"})
          if(len(pagelist) > 0):
            for navitem in pagelist[0].findAll('a'):
              pname=navitem.contents[0]
              purl=navitem["href"]
              addDir("page " + pname.decode("utf-8"),strdomain+purl,14,"")


def SEARCHVideos():
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        searchText = ''
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        searchurl="https://www.viki.com/search?q=" + searchText 
        SearchVideoresults(searchurl,searchText.lower())

def SEARCHByID():
        keyb = xbmc.Keyboard('', 'Enter Viki Video ID')
        keyb.doModal()
        searchText = ''
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText()) 
        getVidQuality(searchText,"",filename,True) 

def GetVideoInfo(vidid):
    infourl=sign_request(vidid,".json")
    print infourl 
    data = json.loads(GetContent(infourl))
    return data
    
def expires():
    '''return a UNIX style timestamp representing 5 minutes from now'''
    return int(time.time())

def sign_request(vidid,vtype):
		from hashlib import sha1
		import hmac
		import binascii

		timestamp = str(int(time.time()))
		key = 'MM_d*yP@`&1@]@!AVrXf_o-HVEnoTnm$O-ti4[G~$JDI/Dc-&piU&z&5.;:}95=Iad'
		rawtxt = '/v4/videos/'+vidid+vtype+'?app=100005a&t='+timestamp+'&site=www.viki.com'
		hashed = hmac.new(key, rawtxt, sha1)
		fullurl = 'https://api.viki.io' + rawtxt+'&sig='+binascii.hexlify(hashed.digest())
		return fullurl

	
def getVidQuality(vidid,name,filename,checkvideo):
  GA("Playing",name)
  print ("getVidQuality name = " + name)  
  useProxy=(enableProxy=="true")
  commenturl="http://api.viki.io/v4/videos/"+vidid+"/timed_comments/en.json?app=65535a&t=1470614411&site=www.viki.com"
  pardata=None
  data=None
  try:
	os.remove(filename)
	os.remove(filename.replace(".srt",".ass"))
  except OSError:
      pass
  if(checkvideo):
          pardata=GetVideoInfo(vidid)

          if "parts" in pardata:
             partnum=len(pardata["parts"])
             if(partnum>1):
                for i in range(partnum):
                     addDir(name +" part " + str(pardata["parts"][i]["part"]),pardata["parts"][i]["id"],15,"")
                return ""
  if(useProxy):
          vidurl=proxyurl.replace("*url*",urllib.quote_plus(sign_request(vidid,"/streams.json")))
  else:
          vidurl = sign_request(vidid,"/streams.json")
  
  print vidurl
  try:
	data = json.loads(GetContent(vidurl))
  except: pass
  if(data!=None and len(data) == 0):
          if(useProxy):
                vidurl=proxyurl.replace("*url*",urllib.quote_plus(sign_request(vidid+"v","/streams")))
          else:
                #vidurl = sign_request(vidid+"v","/streams")
                vidurl = sign_request(vidid,".json")
          data = json.loads(GetContent(vidurl))
  langcode=checkLanguage(vidid)
  strQual=""
  strprot=""
  print ("vidid = " + vidurl)
  try:
          if(enableTrans):
                suburl=sign_request(vidid,"/subtitles/en.srt")
          else:
                suburl=sign_request(vidid,"/subtitles/" + langcode + ".srt")
          print ("suburl = " + suburl)
          write2srt(suburl, filename) 

  except:
          suburl=sign_request(vidid,"/subtitles/en.srt")
          write2srt(suburl, filename) 

  if(pardata!=None and len(pardata["subtitle_completions"]) > 0):
	srt2ass.main(filename,json.loads(GetContent(commenturl)))
  #movies = data["movies"]["url"]["api"]
  show720p=(name.find("(HD)") > -1)
  if data!=None and data.has_key("vcode")!=True:
	  for i, item in enumerate(data):
			  strQual=str(item)
			  #print data
			  mydata = data[item]
			  if(mydata==401):
				print("401 error detected")
				break 
			  if(item!="external"):
				  for seas in mydata:
					  strprot=str(seas)
					  vlink=mydata[seas]["url"]
					  print("Video Link = " + vlink)
					  if(strprot=="rtmp" or strprot=="http"):
							#addLink(strQual +"("+strprot+")",vlink,3,"")
						newvlink=vlink.split(vidid+"/")[-1]
						newvlink="http://content.viki.com/"+vidid+"/"+newvlink
						addLinkSub(strQual +"("+strprot+")",newvlink,3,"",suburl)
					  if(show720p and strQual=="360p" and strprot=="rtmp"):
						newvlink=vlink.split(vidid+"/")[-1].replace('360p','720p')
						newvlink="http://content.viki.com/"+vidid+"/"+newvlink
						#addLink("720p("+strprot+")",newvlink,3,"")
						addLinkSub("720p(http)",newvlink,3,"",suburl)
			  else:
				  vlink=getVideoUrl(mydata["url"],name)
				  addLink("external Video",vlink,3,"")
  else:
		vidata = json.loads(GetContent(sign_request(vidid,".json")))
		posterurl= vidata["images"]["poster"]["url"]
		print posterurl
		idpart=re.compile(vidid+'_(.+?)_').findall(posterurl)
		if(len(idpart)>0):
			newvlink="http://content.viki.com/%s/%s_high_720p_%s.mp4" % (vidid,vidid,idpart[0])
			addLinkSub("720p(?)",newvlink,3,"",suburl)
			newvlink="http://content.viki.com/%s/%s_high_480p_%s.mp4" % (vidid,vidid,idpart[0])
			addLinkSub("480p(?)",newvlink,3,"",suburl)
			newvlink="http://content.viki.com/%s/%s_high_360p_%s.mp4" % (vidid,vidid,idpart[0])
			addLinkSub("360p(?)",newvlink,3,"",suburl)
		
                 

def playVideo(suburl,videoId):
        print filename
        if os.path.exists(filename):
			suburl=filename
			print "filename srt exists"
        if showcomments and os.path.exists(suburl.replace(".srt",".ass")):
			suburl=suburl.replace(".srt",".ass")
			print "filename ass exists"
        vidinfo = videoId.split("_")[0]
        win = xbmcgui.Window(10000)
        win.setProperty('1ch.playing.title', vidinfo)
        win.setProperty('1ch.playing.season', str(3))
        win.setProperty('1ch.playing.episode', str(4))
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoId)
        for i in range(400):
			if(xbmcPlayer.isPlaying()):
				print "Subtitle is delaying:"+ str(i*50)+" ms"
				break
			xbmc.sleep(50)
        else:
				print "subtitle timeout error"
        xbmcPlayer.setSubtitles(suburl) 

		
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
        liz.setProperty('mimetype', 'video/x-msvideo') 
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        contextMenuItems = []
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok
    	
def addLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setProperty('mimetype', 'video/x-msvideo') 
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
        ListGenres(url,name) 
elif mode==3:
        playVideo(subtitleurl,url)
elif mode==4:
        getVidQuality(url,name,filename,True) 
elif mode==5:
        SEARCHChannel()
elif mode==6:
        GA("Genre",name)
        Genre(url,name)
elif mode==7:
        getVidPage(url,name)
elif mode==8:
        GA("Recent_Videos",name)
        UpdatedVideos(url,name)
elif mode==9:
        LangOption()
elif mode==10:
        getLanguages(url,name)
elif mode==11:
        SaveLang(url,name)
elif mode==12:
        SEARCHVideos()
elif mode==13:
        SearchChannelresults(url)
elif mode==14:
        SearchVideoresults(url)
elif mode==15:
        getVidQuality(url,name,filename,False) 
elif mode==16:
        SEARCHByID() 
elif mode==17:
        ShowLangDiag(translator)

xbmcplugin.endOfDirectory(int(sysarg))
