import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
try: import simplejson as json
except ImportError: import json
import cgi
import datetime


import time
ADDON = xbmcaddon.Addon(id='plugin.video.MovieKhmer')
if ADDON.getSetting('ga_visitor')=='':
    from random import randint
    ADDON.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))
    
PATH = "moviekhmer"  #<---- PLUGIN NAME MINUS THE "plugin.video"          
UATRACK="UA-40129315-1" #<---- GOOGLE ANALYTICS UA NUMBER   
VERSION = "1.0.8" #<---- PLUGIN VERSION

strdomain ='http://lakhoan.com/'
def HOME():
        #addDir('Khmer Comedy',strdomain+'category/khmer/khmer-comedy/',2,strdomain+'wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        #addDir('Khmer Movies',strdomain+'category/khmer/',2,strdomain+'wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        #addDir('Khmer Song',strdomain+'category/khmer/khmer-songs/',2,strdomain+'wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Khmer TV drama',strdomain+'category/khmer/',2,strdomain+'wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Thai Movies',strdomain+'category/thai/',2,strdomain+'wp-content/uploads/2012/03/lbach-sneah-prea-kai-180x135.jpg')
        addDir('Thai Lakorns',strdomain+'category/thai/thai-lakorn/',2,strdomain+'wp-content/uploads/2012/03/lbach-sneah-prea-kai-180x135.jpg')
        #addDir('Korean Drama',strdomain+'category/korean/korean-dramas/',2,'http://d3v6rrmlq7x1jk.cloudfront.net/hwdvideos/thumbs/category21.jpg')
        #addDir('Korean Movies',strdomain+'category/korean/korean-movies/',2,'http://d3v6rrmlq7x1jk.cloudfront.net/hwdvideos/thumbs/category21.jpg')
        addDir('Chinese Movies',strdomain+'category/chinese/chinese-movie/',2,'http://d3v6rrmlq7x1jk.cloudfront.net/hwdvideos/thumbs/category29.jpg')
        addDir('Chinese Series',strdomain+'category/chinese/chinese-drama/',2,'http://d3v6rrmlq7x1jk.cloudfront.net/hwdvideos/thumbs/category29.jpg')
        addDir('Documentaries',strdomain+'category/uncategorized/',2,strdomain+'wp-content/uploads/2011/04/vlcsnap-2011-04-04-21h01m29s71-180x135.jpg')
		
def log(description, level=0):
    print description

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

    except urllib2.HTTPError, e:
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

    except urllib2.URLError, e:
        err = str(e)
        log("URLError : " + err)

        time.sleep(3)
        params["error"] = str(int(get("error", "0")) + 1)
        ret_obj = fetchPage(params)
        return ret_obj
		
def getVimeoUrl(videoid,currentdomain=""):
        result = fetchPage({"link": "http://player.vimeo.com/video/%s?title=0&byline=0&portrait=0" % videoid,"refering": currentdomain})
        collection = {}
        print result
        if result["status"] == 200:
            html = result["content"]
            html = html[html.find('={"cdn_url"')+1:]
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
			
			
def INDEX(url):
    #try:
        link = GetContent(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        #start=newlink.index('<div id="main">')
        #end=newlink.index('<!-- main -->')
        match=re.compile('<div class="arc-main">((.|\s)*?)<div id="page-sidebar">').findall(newlink)
        if(len(match) >= 1 and len(match[0]) >= 1):
                match=re.compile('<div class="img-th">((.|\s)*?)</h4>').findall(match[0][0])
                if(len(match) >= 1):
                        for vcontent in match:
                            #match1=re.compile('<a href="(.+?)" rel="bookmark"><img [^>]*src="(.+?)" class="attachment-thumbnail wp-post-image" alt="(.+?)"').findall(vcontent[0])
                            vlink=re.compile('<h4 class="post-tit"><a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(vcontent[0])
                            vurl=vlink[0][0]
                            vimage=re.compile('<img [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(vcontent[0])
                            if(len(vimage)>0):
                                vimage=vimage[0]
                            else:
                                vimage=""
                            vname=vlink[0][1]
                            #(vurl, vimage, vname)=match1[0]
                            try:
								vname=vname.encode("utf-8")
                            except:pass
                            addDir(vname.replace("Thai Lakorn &#8211;",""),vurl,5,vimage)
        match5=re.compile("<div class='wp-pagenavi'>((.|\s)*?)</div>").findall(newlink)
        if(len(match5) >= 1 and len(match5[0]) >= 1 ):
                pagelist =re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(match5[0][0])
                for pageurl,pagenum in pagelist:
					addDir("page " + pagenum.replace('Last \xc2\xbb','Last >>').replace('\xc2\xab',"Prev <<").replace("Prev << First","<< First").replace('\xc2\xbb',"Next >>"),pageurl,2,"")

    #except: pass
			
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
    #try:
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        framesrc=re.compile('<iframe id="gdVideoIframe" [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(newlink)
        if(len(framesrc)==0):
			framesrc=re.compile('<video id="html5Video" [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(newlink)
        match1=re.compile('<ul class="v-list" id="vList">(.+?)</ul>').findall(newlink)
        if(len(match1) > 0):

				match1=re.compile('data-vid="(.+?)" data-source="(.+?)">\s*<img [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>\s*<span class="v-title">(.+?)</span>').findall(match1[0])
				if(len(framesrc)>0 and framesrc[0].find("vimeo") > -1):
					vidurl="http://player.vimeo.com/video/%s"
				elif(len(framesrc)>0 and framesrc[0].find("totptnt") > -1):
					vidurl=framesrc[0].replace(framesrc[0].split("/")[-1],"")+"%s"
				elif(len(framesrc)>0 and framesrc[0].find("docs.google") > -1):
					vidurl="https://docs.google.com/file/d/%s/preview"
				else:
					vidurl=framesrc[0].replace(framesrc[0].split("/")[-1],"%s")
				for mcontent in match1:
					vLink,vtype,vimage,vLinkName=mcontent
					addLink(vLinkName.encode("utf-8"),vidurl%vLink,3,vimage)
        match=re.compile('\{\s*"file":\s*"(.+?)",\s*"title":\s*"(.+?)",\s*"description":').findall(link)
        if(len(match) >= 1):
                for mcontent in match:
                    vLink, vLinkName=mcontent
                    addLink(vLinkName.encode("utf-8"),vLink,3,'')
        else:
                match=re.compile('"file": "(.+?)",').findall(link)
                if(len(match) >= 1):
                        if(".xml" in match[0]):
                                newcontent=GetContent(strdomain+match[0].replace(" ","%20"))
                                ParseXml(newcontent)
                        elif (len(match) > 1):
                                counter = 0
                                for mcontent in match:
                                        counter += 1
                                        addLink(name.encode("utf-8") + " part " + str(counter),mcontent,3,"")
                        else:
                                addLink(name.encode("utf-8"),match[0],3,"")
                else:
                        match=re.compile('<embed [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
                        if(len(match) >= 1):
                                if(match[0].find(".swf") > -1):
                                        match=re.compile('<iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
                                        if(len(match) >= 1):
                                              addLink(name.encode("utf-8"),match[0],3,"")
                                else:
                                        addLink(name.encode("utf-8"),match[0],3,"")
                        else:
                                match=re.compile("'flashvars','&#038;file=(.+?)'").findall(link)
                                if(len(match) >= 1):
                                        ParseXml(GetContent(match[0]).encode("utf-8"))
                                elif(len(re.compile('file: "(.+?)",').findall(link)) >=1):
                                        hasitem=ParseSeparate(newlink,'title: "(.+?)",','file: "(.+?)",')
                                else:
                                        hasitem=ParseSeparate(newlink,'{"title":"(.+?)","creator":','"levels":\[{"file":"(.+?)"}')
        if(len(match1) ==0):
			match=re.compile('<iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
			if(len(match) >= 1):
				addLink(name.encode("utf-8"),match[0],3,"")
        match=re.compile('\).setup\((.+?)\)').findall(newlink)
        if(len(match) > 0):
            epimatch =re.compile('urls:\s*\[(.+?)\]').findall(newlink)
            if(len(epimatch) > 0):
                epilist = epimatch[0].split(",")
                counter = 0
                for mcontent in epilist:
                     counter += 1
                     addLink(name.encode("utf-8") + " part " + str(counter),mcontent,3,"")
 
 
              
    #except: pass		


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
       print "xmlurl="+url
       net = Net()
       second_response = net.http_GET(url)
       return second_response.content
    except:	
       d = xbmcgui.Dialog()
       d.ok(url,"Can't Connect to site",'Try again in a moment')

def PostContent(url):
                req = urllib2.Request(url)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                data=response.read()
                response.close()
                return data
	
def playVideo(videoType,videoId):
    url = ""
    print videoType + '=' + videoId
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
        #url =getVimeoUrlDirect(videoId)
        print "url back" + str(url)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(url)
    elif (videoType == "tudou"):
        url = 'plugin://plugin.video.tudou/?mode=3&url=' + videoId	
    else:
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoId)
	
def loadVideos(url,name):
        #try:
           newlink=url
           print newlink
           xbmc.executebuiltin("XBMC.Notification(Please Wait!,Loading selected video)")
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
           elif (newlink.find("docs.google.com") > -1):  
                vidcontent = GetContent(newlink)
                html = vidcontent.decode('utf8')
                stream_map = re.compile('fmt_stream_map","(.+?)"').findall(html)[0].replace("\/", "/")
                formatArray = stream_map.split(',')
                for formatContent in formatArray:
                     formatContentInfo = formatContent.split('|')
                     qual = formatContentInfo[0]
                     url = (formatContentInfo[1]).decode('unicode-escape')
                     playVideo("direct",url)
           elif (newlink.find("4shared") > -1):
                d = xbmcgui.Dialog()
                d.ok('Not Implemented','Sorry 4Shared links',' not implemented yet')		
           elif (newlink.find("vimeo") > -1):
                idmatch =re.compile("http://player.vimeo.com/video/([^\?&\"\'>]+)").findall(newlink)
                if(len(idmatch) > 0):
                        idmatch=idmatch[0].replace("'","")
                else:
                        idmatch =re.compile("//vimeo.com/(.+?)dk").findall(newlink+"dk")
                        idmatch=idmatch[0].replace("'","")
                playVideo('vimeo',idmatch)
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
		
def addNext(formvar,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&formvar="+str(formvar)+"&name="+urllib.quote_plus('Next >')
        ok=True
        liz=xbmcgui.ListItem('Next >', iconImage="http://i42.tinypic.com/4uz9lc.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": 'Next >' } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="http://i42.tinypic.com/4uz9lc.png", thumbnailImage=iconimage)
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
        GA("INDEX",name)
        INDEX(url)
elif mode==3:
        #sysarg="-1"
        loadVideos(url,name)
elif mode==5:
       GA("episode",name)
       Episodes(url,name)

	   
xbmcplugin.endOfDirectory(int(sysarg))
