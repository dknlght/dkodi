
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import re,sys

try:
    import urllib.parse as urllib
except ImportError:
    import urllib
try:
    import cookielib
except:
    import http.cookiejar
    cookielib = http.cookiejar

try:
    from StringIO import StringIO ## for Python 2
except ImportError:
    from io import StringIO ## for Python 3
import os,string,gzip
import os,time,base64,logging
#from t0mm0.common import Net
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
try: import simplejson as json
except ImportError: import json
import cgi
import datetime
from bs4 import BeautifulSoup
from bs4 import BeautifulStoneSoup
from bs4 import SoupStrainer
from requests import Session
import urlresolver
import resolveurl

import time
session = Session()
ADDON = xbmcaddon.Addon(id='plugin.video.DramaCool')
AZ_DIRECTORIES = ['0','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y', 'Z']
if ADDON.getSetting('ga_visitor')=='':
	from random import randint
	ADDON.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))
	
PATH = "PhumiKhmer"  #<---- PLUGIN NAME MINUS THE "plugin.video" 
UATRACK="UA-40129315-1" #<---- GOOGLE ANALYTICS UA NUMBER
VERSION = "1.0.4" #<---- PLUGIN VERSION

strdomain ='https://www2.dramacool.video'
strdomain2 ='https://www.dramacool9.co'
def HOME():
		addDir('Search',strdomain+'/search?type=movies&keyword=',4,'')
		addDir('List A-Z',strdomain+"/drama-list/char-start-#.html",3,'')
		addDir('Latest Drama',strdomain+'/recently-added',6,'')
		addDir('Latest Movie',strdomain+'/recently-added-movie',6,'')
		addDir('Latest KShow',strdomain+'/recently-added-kshow',6,'')
		GetMenu(strdomain2,strdomain2+"/category/drama/")
		GetMenu(strdomain2,strdomain2+"/category/movies/")

def GetMenu(url,menutype):
		link = GetContent(url)
		try:
			link =link.encode("UTF-8")
		except: pass
		newlink = link
		soup = BeautifulSoup(newlink,"html.parser")
		listcontent=soup.findAll('a', {"href":menutype})
		if(listcontent!= None):
			menuitem=listcontent[0].parent
			for item in menuitem.findAll('li'):
				if(item.a!=None and item.a.has_attr("href")):
					link = strdomain2+str(item.a['href'].encode('utf-8', 'ignore').decode('UTF-8'))
					vname=str(item.a.contents[0]).strip()
					addDir(vname,link,9,"")

def IndexLatest(url):
		link = GetContent(url)
		try:
			link =link.encode("UTF-8")
		except: pass
		newlink = link
		soup = BeautifulSoup(newlink,"html.parser")
		print('hello')
		menucontent=soup.findAll('ul', {"class" : "switch-block list-episode-item"})
		if(menucontent != None):
			for item in menucontent[0].findAll('li'):
				#print item
				vname=item.a.img["alt"]
				vurl=strdomain+item.a["href"]
				vimg=item.a.img["data-original"]
				addDir(vname.encode('utf-8', 'ignore'),vurl,5,vimg)
		pagingList=soup.findAll('ul', {"class" : "pagination"})
		if(pagingList!= None):
			for item in pagingList[0].findAll('li'):
				vname="Page "+ item.a["data-page"]
				vurl=url.split("?")[0]+item.a["href"]
				if(item.has_key("class")==False):
					addDir(vname.encode('utf-8', 'ignore'),vurl,6,"")
					
def Index_co(url):
		link = GetContent(url)
		try:
			link =link.encode("UTF-8")
		except: pass
		newlink = link
		soup = BeautifulSoup(newlink,"html.parser")
		print('hello')
		menucontent=soup.findAll('main', {"id" : "main"})
		if(menucontent!= None):
			for item in menucontent[0].findAll('li'):
				#print item
				vname=item.a["title"]
				vurl=item.a["href"]
				vimg=item.a.img["data-original"]
				addDir(vname.encode('utf-8', 'ignore'),vurl,10,vimg)
			pagingList=menucontent[0].findAll('div', {"class" : "nav-links"})
			if(pagingList!= None):
				for item in pagingList[0].findAll('a',{"class" : "page-numbers"}):
					vname="Page "+ item.contents[0]
					vurl=item["href"]
					if(vurl.find(strdomain2)==-1):
						vurl=strdomain2+item["href"]
					addDir(vname.encode('utf-8', 'ignore'),vurl,9,"")
					
				
def ListSource(url):
		link = GetContent(url)
		try:
			link =link.encode("UTF-8")
		except: pass
		newlink = link
		soup = BeautifulSoup(newlink)
		listcontent=soup.findAll('div', {"class" : "anime_muti_link"})[0]
		srclist=listcontent.findAll('ul')
		if(srclist!= None):
			for item in srclist[0].findAll('li'):
				#print item
				vname=item.contents[0].encode('utf-8', 'ignore')
				vurl=item["data-video"]
				if(vname!="Standard Server" and vname!="Kvid"):
					addLink(vname,vurl,8,"")
				
def ListSource_co(url):
		link = GetContent(url)
		try:
			link =link.encode("UTF-8")
		except: pass
		newlink = link
		soup = BeautifulSoup(newlink)
		srclist=soup.findAll('div', {"id" : "w-server"})
		if(srclist != None):
			for item in srclist[0].findAll('div',{"class":re.compile("serverslist*")}):
				#print item
				vname=item.contents[0].encode('utf-8', 'ignore')
				vurl=item["data-server"]
				if(vname!="Standard Server" and vname!="Kvid"):
					addLink(vname,vurl,8,"")
				
def ListAZ(url,mode):
		for character in AZ_DIRECTORIES:
			chrUrl= url.replace('#',character)
			addDir(character,chrUrl,mode,"")
def log(description, level=0):
	print(description)

def fetchPage(params={}):
	get = params.get
	link = get("link")
	ret_obj = {}
	if get("post_data"):
		log("called for : " + repr(params['link']))
	else:
		log("called for : " + repr(params))

	if not link or int(get("error", "0")) > 2:
		log("giving up")
		ret_obj["status"] = 500
		return ret_obj

	if get("post_data"):
		if get("hide_post_data"):
			log("Posting data", 2)
		else:
			log("Posting data: " + urllib.urlencode(get("post_data")), 2)

		request = urllib2.Request(link, urllib.urlencode(get("post_data")))
		request.add_header('Content-Type', 'application/x-www-form-urlencoded')
	else:
		log("Got request", 2)
		request = urllib2.Request(link)

	if get("headers"):
		for head in get("headers"):
			request.add_header(head[0], head[1])

	request.add_header('User-Agent', "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1")

	if get("cookie"):
		request.add_header('Cookie', get("cookie"))

	if get("refering"):
		request.add_header('Referer', get("refering"))

	try:
		log("connecting to server...", 1)

		con = urllib2.urlopen(request)
		ret_obj["header"] = con.info()
		ret_obj["new_url"] = con.geturl()
		if get("no-content", "false") == u"false" or get("no-content", "false") == "false":
			inputdata = con.read()
			#data_type = chardet.detect(inputdata)
			#inputdata = inputdata.decode(data_type["encoding"])
			ret_obj["content"] = inputdata.decode("utf-8")

		con.close()

		log("Done")
		ret_obj["status"] = 200
		return ret_obj

	except urllib2.HTTPError as e:
		err = str(e)
		log("HTTPError : " + err)
		log("HTTPError - Headers: " + str(e.headers) + " - Content: " + e.fp.read())

		params["error"] = str(int(get("error", "0")) + 1)
		ret = fetchPage(params)

		if not "content" in ret and e.fp:
			ret["content"] = e.fp.read()
			return ret

		ret_obj["status"] = 500
		return ret_obj

	except urllib2.URLError as e:
		err = str(e)
		log("URLError : " + err)

		time.sleep(3)
		params["error"] = str(int(get("error", "0")) + 1)
		ret_obj = fetchPage(params)
		return ret_obj
		
def getVimeoUrl(videoid,currentdomain=""):
		result = fetchPage({"link": "http://player.vimeo.com/video/%s?title=0&byline=0&portrait=0" % videoid,"refering": currentdomain})
		collection = {}
		if result["status"] == 200:
			html = result["content"]
			html = html[html.find('={')+1:]
			html = html[:html.find('}};')]+"}}"
			try:
				  collection = json.loads(html)
				  return collection["request"]["files"]["h264"]["sd"]["url"]
			except:
				  return getVimeoVideourl(videoid,currentdomain)

def scrapeVideoInfo(videoid,currentdomain):
		result = fetchPage({"link": "http://player.vimeo.com/video/%s?title=0&byline=0&portrait=0" % videoid,"refering": currentdomain})
		collection = {}
		if result["status"] == 200:
			html = result["content"]
			html = html[html.find('{config:{'):]
			html = html[:html.find('}}},') + 3]
			html = html.replace("{config:{", '{"config":{') + "}"
			collection = json.loads(html)
		return collection

def getVideoInfo(videoid,currentdomain):

		collection = scrapeVideoInfo(videoid)

		video = {}
		if collection.has_key("config"):
			video['videoid'] = videoid
			title = collection["config"]["video"]["title"]
			if len(title) == 0:
				title = "No Title"
			#title = common.replaceHTMLCodes(title)
			video['Title'] = title
			video['Duration'] = collection["config"]["video"]["duration"]
			video['thumbnail'] = collection["config"]["video"]["thumbnail"]
			video['Studio'] = collection["config"]["video"]["owner"]["name"]
			video['request_signature'] = collection["config"]["request"]["signature"]
			video['request_signature_expires'] = collection["config"]["request"]["timestamp"]

			isHD = collection["config"]["video"]["hd"]
			if str(isHD) == "1":
				video['isHD'] = "1"


		if len(video) == 0:
			log("- Couldn't parse API output, Vimeo doesn't seem to know this video id?")
			video = {}
			video["apierror"] = ""
			return (video, 303)

		log("Done")
		return (video, 200)

def getVimeoVideourl(videoid,currentdomain):

		(video, status) = getVideoInfo(videoid,currentdomain)


		urlstream="http://player.vimeo.com/play_redirect?clip_id=%s&sig=%s&time=%s&quality=%s&codecs=H264,VP8,VP6&type=moogaloop_local&embed_location="
		get = video.get
		if not video:
			# we need a scrape the homepage fallback when the api doesn't want to give us the URL
			log("getVideoObject failed because of missing video from getVideoInfo")
			return ""

		quality = "sd"

		if ('apierror' not in video):
			video_url =  urlstream % (get("videoid"), video['request_signature'], video['request_signature_expires'], quality)
			result = fetchPage({"link": video_url, "no-content": "true"})
			video['video_url'] = result["new_url"]

			log("Done")
			return video['video_url']
		else:
			log("Got apierror: " + video['apierror'])
			return ""
			
def SEARCH():
	try:
		keyb = xbmc.Keyboard('', 'Enter search text')
		keyb.doModal()
		#searchText = '01'
		if (keyb.isConfirmed()):
				searchText = urllib.quote_plus(keyb.getText())
		url = strdomain+'/search?type=movies&keyword='+searchText
		IndexLatest(url)
	except: pass
	
def INDEX(url):
		link = GetContent(url)
		try:
			link =link.encode("UTF-8")
		except: pass
		newlink = link
		soup = BeautifulSoup(newlink)
		listcontent=soup.findAll('ul', {"class" : "switch-block list-episode-item"})
		for item in listcontent[0].findAll('li'):
			#print item
			vname=item.a["title"]
			vurl=strdomain+item.a["href"]
			vimg=item.a.img["data-original"]
			addDir(vname.encode('utf-8', 'ignore'),vurl,5,vimg)
		#pagecontent=soup.findAll('div', {"class" : re.compile("page-nav*")})
		# label=""#re.compile("/label/(.+?)\?").findall(url)[0]
		# pagenum=re.compile("PageNo=(.+?)").findall(url)
		# prev="0"
		# if(len(pagenum)>0):
			  # prev=str(int(pagenum[0])-1)
			  # pagenum=str(int(pagenum[0])+1)

		# else:
			  # pagenum="2"
		# nexurl=buildNextPage(pagenum,label)

		# if(int(pagenum)>2 and prev=="1"):
			  # urlhome=url.split("?")[0]+"?"
			  # addDir("<< Previous",urlhome,2,"")
		# elif(int(pagenum)>2):
			  # addDir("<< Previous",buildNextPage(prev,label),2,"")
		# if(nexurl!=""):
			  # addDir("Next >>",nexurl,2,"")
	#except: pass


	
def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False
		
def SearchResults(url):
		link = GetContent(url)
		newlink = link
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
		try:
			link =link.encode("UTF-8")
		except: pass
		newlink = link
		soup = BeautifulSoup(newlink)
		menucontent=soup.findAll('ul', {"class" : "list-episode-item-2 all-episode"})
		if(len(menucontent) >0):
			for item in menucontent[0].findAll('li'):
				#print item
				vname=item.h3.contents[0]
				vurl=strdomain+item.a["href"]
				addDir(vname.encode('utf-8', 'ignore'),vurl,7,"")
				
	
def Episodes_co(url,name):
		link = GetContent(url)
		try:
			link =link.encode("UTF-8")
		except: pass
		newlink = link
		soup = BeautifulSoup(newlink)
		menucontent=soup.findAll('div', {"id" : "all-episodes"})
		if(len(menucontent) >0):
			for item in menucontent[0].findAll('li'):
				#print item
				vname=item.h3.a["title"]
				vurl=item.h3.a["href"]
				addDir(vname.encode('utf-8', 'ignore'),vurl,11,"")
	#except: pass		


		

def ParseSeparate(vcontent,namesearch,urlsearch):
		newlink = ''.join(str(vcontent).splitlines()).replace('\t','')
		match2=re.compile(urlsearch).findall(newlink)
		match3=re.compile(namesearch).findall(newlink)
		imglen = len(match3)
		if(len(match2) >= 1):
				for i in range(len(match2)):
					if(i < imglen ):
						namelink = match3[i]
					else:
						namelink ='part ' + str(i+1)
					addLink(namelink.encode("utf-8"),match2[i],3,"")
				return True
		return False
					
def GetContent2(url,referr, cj):
	response = session.get(url).text

	return (cj, response)
	
def GetContent(url):
	try:
		response = session.get(url).text
		return response
	except:	
		print(url)
		d = xbmcgui.Dialog()
		d.ok(url,"Can't Connect to site",'Try again in a moment')

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
						 ('Host','www.phim.li')]
	usock=opener.open(url,data)
	if usock.info().get('Content-Encoding') == 'gzip':
		resultat = StringIO()
		buf = resultat.write(usock.read())
		f = gzip.GzipFile(fileobj=buf)
		response = f.read()
	else:
		response = usock.read()
	usock.close()
	return response

	
def playVideo(videoType,videoId):
	url = ""
	print(str(videoType) + '=' + str(videoId))
	win = xbmcgui.Window(10000)
	#win.setProperty('1ch.playing.title', videoId)
	#win.setProperty('1ch.playing.season', str(3))
	#win.setProperty('1ch.playing.episode', str(4))
	if (videoType == "youtube"):
		try:
				url = getYoutube(videoId)
				xbmcPlayer = xbmc.Player()
				xbmcPlayer.play(url)
		except:
				url = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + videoId.replace('?','')
				xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
	elif (videoType == "vimeo"):
		url = getVimeoUrl(videoId,strdomain)
		xbmcPlayer = xbmc.Player()
		xbmcPlayer.play(url)
	elif (videoType == "tudou"):
		url = 'plugin://plugin.video.tudou/?mode=3&url=' + videoId	
	else:
		xbmcPlayer = xbmc.Player()
		liz = xbmcgui.ListItem(name)
		liz.setArt({'poster': 'DefaultVideo.png'})
		liz.setInfo(type='Video', infoLabels={ "Title": videoType })
		liz.setProperty("IsPlayable","true")
		liz.setPath(videoId)
		xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, liz) 
		
def GetDirVideoUrl(url, cj):
	if cj is None:
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
	
def loadVideos(url,name):
		#try:
		newlink=url
		xbmc.executebuiltin("XBMC.Notification(Please Wait!,Loading selected video)")
		print(newlink)
		playtype="direct"
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
				vidlink=urllib2.unquote(dm_low[0]).decode("utf8")
		elif (newlink.find("4shared") > -1):
				d = xbmcgui.Dialog()
				d.ok('Not Implemented','Sorry 4Shared links',' not implemented yet')		
		elif (newlink.find("docs.google.com") > -1 or newlink.find("drive.google.com") > -1):  
				docid=re.compile('/d/(.+?)/preview').findall(newlink)[0]
				cj = cookielib.LWPCookieJar()
				(cj,vidcontent) = GetContent2("https://docs.google.com/get_video_info?docid="+docid,"", cj) 
				html = urllib2.unquote(vidcontent)
				cookiestr=""
				try:
					html=html.encode("utf-8","ignore")
				except: pass
				stream_map = re.compile('fmt_stream_map=(.+?)&fmt_list').findall(html)
				if(len(stream_map) > 0):
					formatArray = stream_map[0].replace("\/", "/").split(',')
					for formatContent in formatArray:
						 formatContentInfo = formatContent.split('|')
						 qual = formatContentInfo[0]
						 url = (formatContentInfo[1]).decode('unicode-escape')

				else:
						cj = cookielib.LWPCookieJar()
						newlink1="https://docs.google.com/uc?export=download&id="+docid  
						(cj,vidcontent) = GetContent2(newlink1,newlink, cj)
						soup = BeautifulSoup(vidcontent)
						downloadlink=soup.findAll('a', {"id" : "uc-download-link"})[0]
						newlink2 ="https://docs.google.com" + downloadlink["href"]
						url=GetDirVideoUrl(newlink2,cj) 
				for cookie in cj:
					cookiestr += '%s=%s;' % (cookie.name, cookie.value)
				vidlink=url+ ('|Cookie=%s' % cookiestr)
		elif (newlink.find("vimeo") > -1):
				idmatch =re.compile("http://player.vimeo.com/video/([^\?&\"\'>]+)").findall(newlink)
				if(len(idmatch) > 0):
						playVideo('vimeo',idmatch[0])
		elif (newlink.find("youtube") > -1) and (newlink.find("playlists") > -1):
				playlistid=re.compile('playlists/(.+?)\?v').findall(newlink)
				vidlink="plugin://plugin.video.youtube?path=/root/video&action=play_all&playlist="+playlistid[0]
		elif (newlink.find("youtube") > -1) and (newlink.find("list=") > -1):
				playlistid=re.compile('videoseries\?list=(.+?)&').findall(newlink+"&")
				vidlink="plugin://plugin.video.youtube?path=/root/video&action=play_all&playlist="+playlistid[0]
		elif (newlink.find("youtube") > -1) and (newlink.find("/p/") > -1):
				playlistid=re.compile('/p/(.+?)\?').findall(newlink)
				vidlink="plugin://plugin.video.youtube?path=/root/video&action=play_all&playlist="+playlistid[0]
		elif (newlink.find("youtube") > -1) and (newlink.find("/embed/") > -1):
				playlistid=re.compile('/embed/(.+?)\?').findall(newlink+"?")
				vidlink=getYoutube(playlistid[0])
		elif (newlink.find("youtube") > -1):
				match=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(newlink)
				if(len(match) == 0):
					match=re.compile('http://www.youtube.com/watch\?v=(.+?)&dk;').findall(newlink1)
				if(len(match) > 0):
					lastmatch = match[0][len(match[0])-1].replace('v/','')
				print("in youtube" + lastmatch[0])
				vidlink=lastmatch
				playtype="youtube"
		
		else:
				sources = []
				label=name
				hosted_media = resolveurl.HostedMediaFile(url=newlink, title=label)
				sources.append(hosted_media)
				source = resolveurl.choose_source(sources)
				print("inresolver=" + newlink)
				print(source)
				if source:
						vidlink = source.resolve()
				else:
						hosted_media = urlresolver.HostedMediaFile(url=newlink, title=label)
						sources.append(hosted_media)
						source = urlresolver.choose_source(sources)
						vidlink = source.resolve()
				print("done getting link")
				print (vidlink)
		playVideo(playtype,vidlink )
		
def OtherContent():
	net = Net()
	response = net.http_GET('http://khmerportal.com/videos')
	print(response)
def extractFlashVars(data):
	for line in data.split("\n"):
			index = line.find("ytplayer.config =")
			if index != -1:
				found = True
				p1 = line.find("=", (index-3))
				p2 = line.rfind(";")
				if p1 <= 0 or p2 <= 0:
						continue
				data = line[p1 + 1:p2]
				break
	if found:
			data=data.split(";(function()",1)[0]
			data=data.split(";ytplayer.load",1)[0]
			data = json.loads(data)
			flashvars = data["args"]
	return flashvars 
		
def selectVideoQuality(links):
		link = links.get
		video_url = ""
		fmt_value = {
				5: "240p h263 flv container",
				18: "360p h264 mp4 container | 270 for rtmpe?",
				22: "720p h264 mp4 container",
				26: "???",
				33: "???",
				34: "360p h264 flv container",
				35: "480p h264 flv container",
				37: "1080p h264 mp4 container",
				38: "720p vp8 webm container",
				43: "360p h264 flv container",
				44: "480p vp8 webm container",
				45: "720p vp8 webm container",
				46: "520p vp8 webm stereo",
				59: "480 for rtmpe",
				78: "seems to be around 400 for rtmpe",
				82: "360p h264 stereo",
				83: "240p h264 stereo",
				84: "720p h264 stereo",
				85: "520p h264 stereo",
				100: "360p vp8 webm stereo",
				101: "480p vp8 webm stereo",
				102: "720p vp8 webm stereo",
				120: "hd720",
				121: "hd1080"
		}
		hd_quality = 1

		# SD videos are default, but we go for the highest res
		#print video_url
		if (link(35)):
			video_url = link(35)
		elif (link(59)):
			video_url = link(59)
		elif link(44):
			video_url = link(44)
		elif (link(78)):
			video_url = link(78)
		elif (link(34)):
			video_url = link(34)
		elif (link(43)):
			video_url = link(43)
		elif (link(26)):
			video_url = link(26)
		elif (link(18)):
			video_url = link(18)
		elif (link(33)):
			video_url = link(33)
		elif (link(5)):
			video_url = link(5)

		if hd_quality > 1:  # <-- 720p
			if (link(22)):
				video_url = link(22)
			elif (link(45)):
				video_url = link(45)
			elif link(120):
				video_url = link(120)
		if hd_quality > 2:
			if (link(37)):
				video_url = link(37)
			elif link(121):
				video_url = link(121)

		if link(38) and False:
			video_url = link(38)
		for fmt_key in links.iterkeys():

			if link(int(fmt_key)):
					text = repr(fmt_key) + " - "
					if fmt_key in fmt_value:
						text += fmt_value[fmt_key]
					else:
						text += "Unknown"

					if (link(int(fmt_key)) == video_url):
						text += "*"
			else:
					print("- Missing fmt_value: " + repr(fmt_key))

		video_url += " | " + 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'


		return video_url

def getYoutube(videoid):

				code = videoid
				linkImage = 'http://i.ytimg.com/vi/'+code+'/default.jpg'
				req = urllib2.Request('http://www.youtube.com/watch?v='+code+'&fmt=18')
				req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
				response = urllib2.urlopen(req)
				link=response.read()
				response.close()
				
				if len(re.compile('shortlink" href="http://youtu.be/(.+?)"').findall(link)) == 0:
						if len(re.compile('\'VIDEO_ID\': "(.+?)"').findall(link)) == 0:
								req = urllib2.Request('http://www.youtube.com/get_video_info?video_id='+code+'&asv=3&el=detailpage&hl=en_US')
								req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
								response = urllib2.urlopen(req)
								link=response.read()
								response.close()
				
				flashvars = extractFlashVars(link)

				links = {}

				for url_desc in flashvars[u"url_encoded_fmt_stream_map"].split(u","):
						url_desc_map = cgi.parse_qs(url_desc)
						if not (url_desc_map.has_key(u"url") or url_desc_map.has_key(u"stream")):
								continue

						key = int(url_desc_map[u"itag"][0])
						url = u""
						if url_desc_map.has_key(u"url"):
								url = urllib.unquote(url_desc_map[u"url"][0])
						elif url_desc_map.has_key(u"stream"):
								url = urllib.unquote(url_desc_map[u"stream"][0])

						if url_desc_map.has_key(u"sig"):
								url = url + u"&signature=" + url_desc_map[u"sig"][0]
						links[key] = url
				highResoVid=selectVideoQuality(links)
				return highResoVid 

def parseDate(dateString):
	try:
		return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
	except:
		return datetime.datetime.today() - datetime.timedelta(days = 1) #force update


def checkGA():

	secsInHour = 60 * 60
	threshold  = 2 * secsInHour

	now= datetime.datetime.today()
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
		print("GA fail: %s" % utm_url)
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
						print("============================ POSTING TRACK EVENT ============================")
						send_request_to_google_analytics(utm_track)
					except:
						print("============================  CANNOT POST TRACK EVENT ============================")
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
								
			print("============================ POSTING ANALYTICS ============================")
			send_request_to_google_analytics(utm_url)
			
		except:
			print("================  CANNOT POST TO ANALYTICS  ================")
			
			
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
			print('======================= more than ====================')
			log_path = xbmc.translatePath('special://logpath')
			log = os.path.join(log_path, logname)
			logfile = open(log, 'r').read()
			match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
		else:
			logfile='Starting XBMC (Unknown Git:.+?Platform: Unknown. Built.+?'
			match=re.compile('Starting XBMC \((.+?) Git:.+?Platform: (.+?)\. Built.+?').findall(logfile)
		print('=========================='+PATH+' '+VERSION+'  ==========================')
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
				print("============================ POSTING APP LAUNCH TRACK EVENT ============================")
				send_request_to_google_analytics(utm_track)
			except:
				print("============================  CANNOT POST APP LAUNCH TRACK EVENT ============================")
				
#checkGA()

def addLink(name,url,mode,iconimage):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
		ok=True
		liz=xbmcgui.ListItem(name)
		liz.setArt({'poster': iconimage})
		liz.setArt({'icon': iconimage})
		liz.setInfo( type="Video", infoLabels={ "Title": name } )
		liz.setProperty("IsPlayable","true")
		contextMenuItems = []
		liz.addContextMenuItems(contextMenuItems, replaceItems=True)
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
		return ok
		
def addNext(formvar,url,mode,iconimage):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&formvar="+str(formvar)+"&name="+urllib.quote_plus('Next >')
		ok=True
		liz=xbmcgui.ListItem('Next >')
		liz.setArt({'poster': iconimage})
		liz.setArt({'icon': iconimage})
		liz.setInfo( type="Video", infoLabels={ "Title": 'Next >' } )
		ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
		return ok
		
def addDir(name,url,mode,iconimage):
		u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
		ok=True
		liz=xbmcgui.ListItem(name)
		liz.setArt({'poster': iconimage})
		liz.setArt({'icon': iconimage})
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

print("mode below")
print(url)
sysarg=str(sys.argv[1]) 
if mode==None or url==None or len(url)<1:
		#OtherContent()
		HOME()
	
elif mode==2:
		#d = xbmcgui.Dialog()
		#d.ok('mode 2',str(url),' ingore errors lol')
		GA("INDEX",name)
		INDEX(url)
elif mode==3:
		#sysarg="-1"
		ListAZ(strdomain+"/drama-list/char-start-#.html",2)
elif mode==4:
		SEARCH()
elif mode==5:
	GA("episode",name)
	Episodes(url,name)
elif mode==6:
	IndexLatest(url)
elif mode==7:
	ListSource(url)
elif mode==8:
	loadVideos(url,name)
elif mode==9:
	Index_co(url)
elif mode==10:
	Episodes_co(url,name)
elif mode==11:
	ListSource_co(url)
xbmcplugin.endOfDirectory(int(sysarg))
