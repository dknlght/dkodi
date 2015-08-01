import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
from BeautifulSoup import SoupStrainer
try: import simplejson as json
except ImportError: import json
import cgi
import CommonFunctions
import datetime
common = CommonFunctions
common.plugin = "plugin.video.bharatmovies"

import time
ADDON = xbmcaddon.Addon(id='plugin.video.bharatmovies')

    
AZ_DIRECTORIES = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y', 'Z']
strdomain ='http://www.bharatmovies.com/'

class youkuDecoder:
    def __init__( self ):
        return

    def getFileIDMixString(self,seed):  
        mixed = []  
        source = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/\:._-1234567890")  
        seed = float(seed)  
        for i in range(len(source)):  
            seed = (seed * 211 + 30031 ) % 65536  
            index = math.floor(seed /65536 *len(source))  
            mixed.append(source[int(index)])  
            source.remove(source[int(index)])  
        return mixed  

    def getFileId(self,fileId,seed):  
        mixed = self.getFileIDMixString(seed)  
        ids = fileId.split('*')  
        realId = []  
        for i in range(0,len(ids)-1):
            realId.append(mixed[int(ids[i])])  
        return ''.join(realId)

    def trans_e(self, a, c):
        b = range(256)
        f = 0
        result = ''
        h = 0
        while h < 256:
            f = (f + b[h] + ord(a[h % len(a)])) % 256
            b[h], b[f] = b[f], b[h]
            h += 1
        q = f = h = 0
        while q < len(c):
            h = (h + 1) % 256
            f = (f + b[h]) % 256
            b[h], b[f] = b[f], b[h]
            result += chr(ord(c[q]) ^ b[(b[h] + b[f]) % 256])
            q += 1
        return result

    def trans_f(self, a, c):
        """
        :argument a: list
        :param c:
        :return:
        """
        b = []
        for f in range(len(a)):
            i = ord(a[f][0]) - 97 if "a" <= a[f] <= "z" else int(a[f]) + 26
            e = 0
            while e < 36:
                if c[e] == i:
                    i = e
                    break
                e += 1
            v = i - 26 if i > 25 else chr(i + 97)
            b.append(str(v))
        return ''.join(b)

    f_code_1 = 'becaf9be'
    f_code_2 = 'bf7e5f01'

    def _calc_ep2(self, vid, ep):
        e_code = self.trans_e(self.f_code_1, base64.b64decode(ep))
        sid, token = e_code.split('_')
        new_ep = self.trans_e(self.f_code_2, '%s_%s_%s' % (sid, vid, token))
        return base64.b64encode(new_ep), token, sid
		
def HOME():
        addDir('Hindi Movies','http://www.bharatmovies.com/hindi/movies/list.htm',5,'')
        addDir('Hindi Movies By Year','http://www.bharatmovies.com/hindi/movies/hindi-newrelease-movies.htm',7,'')
        addDir('telugu Movies','http://www.bharatmovies.com/telugu/movies/list.htm',5,'')
        addDir('telugu Movies By Year','http://www.bharatmovies.com/telugu/movies/telugu-newrelease-movies.htm',7,'')
        addDir('tamil Movies','http://www.bharatmovies.com/tamil/movies/list.htm',5,'')
        addDir('tamil Movies By Year','http://www.bharatmovies.com/tamil/movies/tamil-newrelease-movies.htm',7,'')
        addDir('malayalam Movies','http://www.bharatmovies.com/malayalam/movies/list.htm',5,'')
        addDir('malayalam Movies By Year','http://www.bharatmovies.com/malayalam/movies/malayalam-newrelease-movies.htm',7,'')
        addDir('kannada Movies','http://www.bharatmovies.com/kannada/movies/list.htm',5,'')
        addDir('kannada Movies By Year','http://www.bharatmovies.com/kannada/movies/kannada-newrelease-movies.htm',7,'')
        addDir('bengali Movies','http://www.bharatmovies.com/bengali/info/moviepages.htm',5,'')
        addDir('bengali Movies By Year','http://www.bharatmovies.com/bengali/movies/bengali-newrelease-movies.htm',7,'')
        addDir('marathi Movies','http://www.bharatmovies.com/marathi/movies/list.htm',6,'')
		
def ListAZ(url):
        for character in AZ_DIRECTORIES:
			addDir(character,url.replace(".htm","-"+character+".htm").replace("-A.htm",".htm"),6,"")
			
def ListYear(url):
        link = GetContent(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        menucontent=re.compile('<div id="cmain">(.+?)<div id="cside">').findall(newlink)[0]
        menuhead = SoupStrainer('div', {"align" : "center"})
        soup = BeautifulStoneSoup(menucontent, parseOnlyThese=menuhead,convertEntities=BeautifulSoup.XML_ENTITIES)
        for item in soup.findAll('a'):
			addDir(str(item.contents[0]),url.replace(url.split("/")[-1],item['href']),6,"")
			
def ListMovies(url):
        link = GetContent(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        menucontent=re.compile('<div id="cmain">(.+?)<div id="cside">').findall(newlink)[0]
        menuhead = SoupStrainer('div', {"id" : re.compile('L.*')})
        soup = BeautifulStoneSoup(menucontent, parseOnlyThese=menuhead,convertEntities=BeautifulSoup.XML_ENTITIES)
        for item in soup.findAll('a'):
			addLink(str(item.contents[0]),url.replace(url.split("/")[-1],item['href']),3,"")
			
def GetMenu(url):
        link = GetContent(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        menucontent=re.compile('<div class="main_navigation">(.+?)</div>').findall(newlink)[0]
        menuhead = SoupStrainer('li')
        soup = BeautifulStoneSoup(menucontent, parseOnlyThese=menuhead,convertEntities=BeautifulSoup.XML_ENTITIES)
        for item in soup.findAll('li'):
			link = item.a['href'].encode('utf-8', 'ignore')
			addDir(str(item.a.contents[0]).strip(),link,5,"")


def getVimeoUrl(videoid):
        result = common.fetchPage({"link": "http://player.vimeo.com/video/%s?title=0&byline=0&portrait=0" % videoid,"refering": strdomain})
        collection = {}
        if result["status"] == 200:
            html = result["content"]
            html = html[html.find(',a={'):]
            html = html[:html.find('}};') + 2]
            html = html.replace(",a={", '{') 
            try:
                  collection = json.loads(html)
                  codec=collection["request"]["files"]["codecs"][0]
                  filecol = collection["request"]["files"][codec]
                  return filecol["sd"]["url"]
            except:
                  return getVimeoVideourl(videoid)
				  
def scrapeVideoInfo(videoid):
        result = common.fetchPage({"link": "http://player.vimeo.com/video/%s" % videoid,"refering": strdomain})
        collection = {}
        if result["status"] == 200:
            html = result["content"]
            html = html[html.find('{config:{'):]
            html = html[:html.find('}}},') + 3]
            html = html.replace("{config:{", '{"config":{') + "}"
            collection = json.loads(html)
        return collection

def getVideoInfo(videoid):
        common.log("")
        collection = scrapeVideoInfo(videoid)

        video = {}
        if collection.has_key("config"):
            video['videoid'] = videoid
            title = collection["config"]["video"]["title"]
            if len(title) == 0:
                title = "No Title"
            title = common.replaceHTMLCodes(title)
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
            common.log("- Couldn't parse API output, Vimeo doesn't seem to know this video id?")
            video = {}
            video["apierror"] = ""
            return (video, 303)

        common.log("Done")
        return (video, 200)

def getVimeoVideourl(videoid):
        common.log("")
        
        (video, status) = getVideoInfo(videoid)


        urlstream="http://player.vimeo.com/play_redirect?clip_id=%s&sig=%s&time=%s&quality=%s&codecs=H264,VP8,VP6&type=moogaloop_local&embed_location="
        get = video.get
        if not video:
            # we need a scrape the homepage fallback when the api doesn't want to give us the URL
            common.log("getVideoObject failed because of missing video from getVideoInfo")
            return ""

        quality = "sd"
        
        if ('apierror' not in video):
            video_url =  urlstream % (get("videoid"), video['request_signature'], video['request_signature_expires'], quality)
            result = common.fetchPage({"link": video_url, "no-content": "true"})
            video['video_url'] = result["new_url"]
            common.log("Done")
            return video['video_url'] 
        else:
            common.log("Got apierror: " + video['apierror'])
            return ""
			
def SEARCH():
    try:
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        #searchText = '01'
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        url = 'http://www.dramakhmer.com/search?q='+searchText
        INDEX(url)
    except: pass



def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
		
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


def ParseXml(newcontent):
        try:
                xmlcontent=xml.dom.minidom.parseString(newcontent)
        except:
                ParsePlayList(newcontent)
                return ""
        if('<tracklist>' in newcontent):
                ParsePlayList(newcontent)
                channels = xmlcontent.getElementsByTagName('tracklist')
                items=xmlcontent.getElementsByTagName('track')
                for itemXML in items:
                        vname=itemXML.getElementsByTagName('title')[0].childNodes[0].data
                        vurl=itemXML.getElementsByTagName('location')[0].childNodes[0].data
                        addLink(vname.encode("utf-8"),vurl.encode("utf-8"),3,"")
        else:
                channels = xmlcontent.getElementsByTagName('channel')
                if len(channels) == 0:
                    channels = xmlcontent.getElementsByTagName('feed')
                items=xmlcontent.getElementsByTagName('item')
                for itemXML in items:
                        vname=itemXML.getElementsByTagName('title')[0].childNodes[0].data
                        vurl=itemXML.getElementsByTagName('media:content')[0].getAttribute('url')
                        addLink(vname.encode("utf-8"),vurl.encode("utf-8"),3,"")

def ParsePlayList(newcontent):
        newcontent=''.join(newcontent.splitlines()).replace('\t','')
        match=re.compile('<title>(.+?)</title>[^>]*<location>(.+?)</location>').findall(newcontent)
        for vcontent in match:
                (vname,vurl)=vcontent
                addLink(vname.encode("utf-8"),vurl.encode("utf-8"),3,"")				

def ParseSeparate(vcontent,namesearch,urlsearch):
        newlink = ''.join(vcontent.splitlines()).replace('\t','')
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
					
def GetContent2(url):
    conn = httplib.HTTPConnection(host="moviekhmer.com",timeout=30)
    req = url
    try:
        conn.request('GET',req)
        content = conn.getresponse().read()
    except:
        print 'echec de connexion'
    conn.close()
    return content
	
def GetContent(url):
    try:
       net = Net()
       second_response = net.http_GET(url)
       return second_response.content
    except:	
       print url
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
        buf = StringIO.StringIO(usock.read())
        f = gzip.GzipFile(fileobj=buf)
        response = f.read()
    else:
        response = usock.read()
    usock.close()
    return response

	
def playVideo(videoType,videoId):
    url = ""
    print videoType + '=' + videoId
    win = xbmcgui.Window(10000)
    win.setProperty('1ch.playing.title', videoId)
    win.setProperty('1ch.playing.season', str(3))
    win.setProperty('1ch.playing.episode', str(4))
    if (videoType == "youtube"):
        try:
                url = getYoutube(videoId)
                xbmcPlayer = xbmc.Player()
                xbmcPlayer.play(url)
        except:
                url = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + videoId.replace('?','')
                xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
    elif (videoType == "vimeo"):
        url = getVimeoUrl(videoId)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(url)
    elif (videoType == "tudou"):
        url = 'plugin://plugin.video.tudou/?mode=3&url=' + videoId	
    else:
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoId)

def selResolution(streamtypes):
    ratelist = []
    for i in range(0,len(streamtypes)):
        if streamtypes[i] == 'flv': ratelist.append([4, '??', i]) # [??????, ???, streamtypes??]
        if streamtypes[i] == 'mp4': ratelist.append([3, '??', i])
        if streamtypes[i] == 'hd2': ratelist.append([2, '??', i])
        if streamtypes[i] == 'hd3': ratelist.append([1, '1080P', i])
    ratelist.sort()
    if len(ratelist) > 1:
        resolution = 4
        if resolution == 0:    # ?????????
            list = [x[1] for x in ratelist]
            sel = xbmcgui.Dialog().select('select resolution', list)
            if sel == -1:
                return None, None
        else:
            sel = 0
            while sel < len(ratelist)-1 and resolution > ratelist[sel][0]: sel += 1
    else:
        sel = 0
    return streamtypes[ratelist[sel][2]], ratelist[sel][1]
	
def loadVideos(url,name):
        #try:
           xbmc.executebuiltin("XBMC.Notification(Please Wait!,Loading selected video)")
           link = GetContent(url)
           try:
               link =link.encode("UTF-8")
           except: pass
           link = ''.join(link.splitlines()).replace('\t','')
           vidcontent=re.compile('<div id="vidcontainer">(.+?)</div>').findall(link)[0]
           match=re.compile('<iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(vidcontent)
           if(len(match)==0):
				match=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>').findall(vidcontent)
           newlink=urllib.unquote_plus(match[0])
           print newlink
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
           elif (newlink.find("youku") > -1):
				idmatch =re.compile("id_([^\?&\"\'>]+)").findall(newlink)
				url = 'http://v.youku.com/player/getPlayList/VideoIDS/%s/ctype/12/ev/1' % (idmatch[0])
				link = GetContent(url)
				json_response = json.loads(link)

				vid = id
				lang_select = 0
				if lang_select != 0 and json_response['data'][0].has_key('dvd') and 'audiolang' in json_response['data'][0]['dvd']:
					langlist = json_response['data'][0]['dvd']['audiolang']
					if lang_select == 1:
						list = [x['lang'] for x in langlist]
						sel = xbmcgui.Dialog().select('????', list)
						if sel ==-1:
							return
						vid = langlist[sel]['vid'].encode('utf-8')
						name = '%s %s' % (name, langlist[sel]['lang'].encode('utf-8'))
					else:
						lang_prefer = __addon__.getSetting('lang_prefer') # ??|??
						for i in range(0,len(langlist)):
							if langlist[i]['lang'].encode('utf-8') == lang_prefer:
								vid = langlist[i]['vid'].encode('utf-8')
								name = '%s %s' % (name, langlist[i]['lang'].encode('utf-8'))
								break
				if vid != id:
					url = 'http://v.youku.com/player/getPlayList/VideoIDS/%s/ctype/12/ev/1' % (vid)
					link = GetContent(url)
					json_response = simplejson.loads(link)

				typeid, typename = selResolution(json_response['data'][0]['streamtypes'])
				if typeid:
					video_id = json_response['data'][0]['videoid']
					oip = json_response['data'][0]['ip']
					ep = json_response['data'][0]['ep']
					ep, token, sid = youkuDecoder()._calc_ep2(video_id, ep)
					query = urllib.urlencode(dict(
						vid=video_id, ts=int(time.time()), keyframe=1, type=typeid,
						ep=ep, oip=oip, ctype=12, ev=1, token=token, sid=sid,
					))
					movurl = 'http://pl.youku.com/playlist/m3u8?%s' % (query)
					playVideo("direct",movurl)
           elif (newlink.find("docs.google.com") > -1):
                vidcontent = postContent("http://javaplugin.org/WL/grp2/plugins/plugins_player.php","iagent=Mozilla%2F5%2E0%20%28Windows%3B%20U%3B%20Windows%20NT%206%2E1%3B%20en%2DUS%3B%20rv%3A1%2E9%2E2%2E8%29%20Gecko%2F20100722%20Firefox%2F3%2E6%2E8&ihttpheader=true&url="+urllib.quote_plus(newlink)+"&isslverify=true",strDomain)
                if(len(vidcontent.strip())==0):
                     vidcontent = GetContent(newlink)
                vidmatch=re.compile('"url_encoded_fmt_stream_map":"(.+?)",').findall(vidcontent)
                if(len(vidmatch) > 0):
                        vidparam=urllib.unquote_plus(vidmatch[0]).replace("\u003d","=")
                        vidlink=re.compile('url=(.+?)\u00').findall(vidparam)
                        playVideo("direct",vidlink[0])
           elif (newlink.find("vimeo") > -1):
                idmatch =re.compile("http://player.vimeo.com/video/([^\?&\"\'>]+)").findall(newlink)
                if(len(idmatch) > 0):
                        playVideo('vimeo',idmatch[0])
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
                    #d = xbmcgui.Dialog()
                    #d.ok('mode 2',str(lastmatch),'launching yout')
                    playVideo('youtube',lastmatch)
                else:
                    playVideo('moviekhmer',urllib2.unquote(newlink).decode("utf8"))
        #except: pass
        
def OtherContent():
    net = Net()
    response = net.http_GET('http://khmerportal.com/videos')
    print response       
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
                    print "- Missing fmt_value: " + repr(fmt_key)

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
if mode==None or url==None or len(url)<1:
        #OtherContent()
        HOME()
       
elif mode==2:
        #d = xbmcgui.Dialog()
        #d.ok('mode 2',str(url),' ingore errors lol')
        GetMenu(url)
elif mode==3:
        #sysarg="-1"
        loadVideos(url,name)
elif mode==4:
        SEARCH()
elif mode==5:
       ListAZ(url)
elif mode==6:
       ListMovies(url)
elif mode==7:
       ListYear(url)
	   
xbmcplugin.endOfDirectory(int(sysarg))
