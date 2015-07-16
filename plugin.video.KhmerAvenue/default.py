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

ADDON = xbmcaddon.Addon(id='plugin.video.KhmerAvenue')
if ADDON.getSetting('ga_visitor')=='':
    from random import randint
    ADDON.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))

PATH = "KhmerAvenue"  #<---- PLUGIN NAME MINUS THE "plugin.video"
UATRACK="UA-40129315-1" #<---- GOOGLE ANALYTICS UA NUMBER
VERSION = "1.0.16" #<---- PLUGIN VERSION


strDomain ='http://www.merlkon.com/'
def HOME():
        addDir('Search','http://www.merlkon.net/',4,'http://www.merlkon.com/wp-contents/uploads/logo.jpg')
        addDir('Khmer Video','http://www.merlkon.net/albumcategory/khmer-media/',2,'http://www.merlkon.com/wp-content/uploads/2013/03/snep-150x150.jpg')
        addDir('Thai Lakorns','http://www.merlkon.net/albumcategory/thai-videos/',2,'http://www.merlkon.com/wp-content/uploads/2014/10/kew-150x150.jpg')
        addDir('Korean Videos','http://www.khmerstream.com/albumcategory/korean-videos/',2,'http://www.merlkon.com/wp-content/uploads/2012/04/lietome.jpg')
        addDir('Chinese KhmerAve','http://www.khmeravenue.com/albumcategory/chinese-videos/',2,'http://www.khmeravenue.com/wp-content/uploads/2014/09/a-150x150.png')
        addDir('Chinese KhmerStream','http://www.khmerstream.com/albumcategory/chinese-videos/',2,'http://www.khmerstream.com/wp-content/uploads/2014/10/d-150x150.png')
        addDir('Bollywood Videos','http://www.merlkon.net/albumcategory/bollywood-videos/',2,'http://www.merlkon.com/wp-content/uploads/2012/10/bol-150x150.jpg')
        addDir('Philippines Videos','http://www.merlkon.net/albumcategory/philippines-videos/',2,'http://www.merlkon.com/wp-content/uploads/2012/09/dyesebel.jpg')
def INDEX(url):
    #try:
        link = GetContent(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<div class="widget-background-wrapper" id="enhancedtextwidget-17-background-wrapper">(.+?)<div class=\'loop\'>').findall(newlink)
        match=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(match[0])
        for vurl,vcontent in match:
            imgmatch=re.compile('<img src="(.+?)" alt="(.+?)"').findall(vcontent)[0]
            (vimage,vname)=imgmatch
            addDir(vname,vurl,5,vimage)
        match5=re.compile("<div class='wp-pagenavi'>(.+?)</div>").findall(newlink)
        if(len(match5)):
			pagelist=re.compile('<a class="page larger" [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(match5[0])
			for vurl,vcontent in pagelist:
				addDir("page "+vcontent,vurl,2,"")
    #except: pass

def SEARCH():
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        #searchText = '01'
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        url = 'http://www.merlkon.com/page/1/?s='+ searchText +'&x=4&y=6'
        SearchResults(url)

def SearchResults(url):
        link = GetContent(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<div class="loop-content">(.+?)<div class="loop-footer">').findall(newlink)
        match=re.compile('<h3 class="entry-title"><a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a></h3>').findall(match[0])
        if(len(match) > 0):
                for vLink,vLinkName in match:
                    addDir(vLinkName,vLink,5,"")
        match=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>Next Page').findall(link)
        if(len(match) > 0):
            url=match[0]
            addDir("Next >>",url,6,"")
			
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
        #currentdomain="http://www.khmeravenue.com"
        result = fetchPage({"link": "http://player.vimeo.com/video/%s?title=0&byline=0&portrait=0" % videoid,"refering": currentdomain})
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

def Episodes(url,name):
    #try:
        link = GetContent(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        addLink(name.encode("utf-8"),url,3,'')
        match=re.compile('>Related Videos</h4>(.+?)</div>').findall(newlink)
        match=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(match[0])
        counter = 1
        videolist =url+";#"
        vidPerGroup = 5
        if(len(match) >= 1):
                for vLink,mcontent in match:
                    vLinkName=re.compile('<span [^>]*style=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</span>').findall(mcontent)[0][1]
                    counter += 1
                    addLink(vLinkName.encode("utf-8"),vLink,3,'')
                    videolist=videolist+vLink+";#"
                    if(counter%vidPerGroup==0 or counter==len(match)+1):
                            addLink("-------Play the "+ str(len(videolist.split(';#'))-1)+" videos above--------",videolist,8,"")
                            videolist =""

    #except: pass

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
    print usock
    if usock.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(usock.read())
        f = gzip.GzipFile(fileobj=buf)
        response = f.read()
    else:
        response = usock.read()
    usock.close()
    return response

def GetContent(url):
    try:
       net = Net()
       second_response = net.http_GET(url)
       return second_response.content
    except:
       d = xbmcgui.Dialog()
       d.ok(url,"Can't Connect to site",'Try again in a moment')

def playVideo(videoType,videoId):
    url = videoId
    if (videoType == "youtube"):
        try:
                url = getYoutube(videoId)
        except:
                url = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + videoId.replace('?','')
    elif (videoType == "vimeo"):
        url = 'plugin://plugin.video.vimeo/?action=play_video&videoID=' + videoId
    elif (videoType == "tudou"):
        url = 'plugin://plugin.video.tudou/?mode=3&url=' + videoId

    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(url)

def PLAYLIST_VIDEOLINKS(url,name):
        ok=True
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
        #time.sleep(2)
        links = url.split(';#')
        print "linksurl" + str(url)
        pDialog = xbmcgui.DialogProgress()
        ret = pDialog.create('Loading playlist...')
        totalLinks = len(links)-1
        loadedLinks = 0
        remaining_display = 'Videos loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B] into XBMC player playlist.'
        pDialog.update(0,'Please wait for the process to retrieve video link.',remaining_display)
        for videoLink in links:
             if(len(videoLink)>2):
                loadPlaylist(videoLink,name)
                loadedLinks = loadedLinks
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

def CreateList(videoType,videoId):
    url1 = ""
    if (videoType == "youtube"):
        try:
                url1 = getYoutube(videoId)
        except:
                url1 = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + videoId.replace('?','')
    elif (videoType == "vimeo"):
        url1 = 'plugin://plugin.video.vimeo/?action=play_video&videoID=' + videoId
    elif (videoType == "tudou"):
        url1 = 'plugin://plugin.video.tudou/?mode=3&url=' + videoId
    else:
        url1=videoId
    print "addingplay" + url1
    if(len(videoId) >0):
        liz = xbmcgui.ListItem('[B]PLAY VIDEO[/B]', thumbnailImage="")
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.add(url=url1, listitem=liz)

def loadPlaylist(url,name):
        #try:
           link=GetContent(url)
           newlink = ''.join(link.encode("utf-8").splitlines()).replace('\t','')
           vidurl=""
           match=re.compile("'file': '(.+?)',").findall(newlink)
           if(len(match) == 0):
                   match=re.compile('<div class="video_main">\s*<iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(newlink)
                   if(len(match)==0):
                           match=re.compile('<iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(newlink)
                           if(len(match)==0):
                                   match=re.compile("<param name='flashvars' value='file=(.+?)&").findall(newlink)
           newlink=match[0]
           if (newlink.find("dailymotion") > -1):
                match=re.compile('www.dailymotion.com/embed/video/(.+?)\?').findall(newlink+"?")
                if(len(match) == 0):
                        match=re.compile('www.dailymotion.com/video/(.+?)&dk;').findall(newlink+"&dk;")
                if(len(match) == 0):
                        match=re.compile('www.dailymotion.com/swf/(.+?)\?').findall(newlink)
                if(len(match) == 0):
                	match=re.compile('www.dailymotion.com/embed/video/(.+?)\?').findall(newlink.replace("$","?"))
                print match
                vidlink=getDailyMotionUrl(match[0])
                CreateList('dailymontion',vidlink)
           elif (newlink.find("docs.google.com") > -1):
                vidcontent =postContent("http://javaplugin.org/WL/grp2/plugins/plugins_player.php","iagent=Mozilla%2F5%2E0%20%28Windows%3B%20U%3B%20Windows%20NT%206%2E1%3B%20en%2DUS%3B%20rv%3A1%2E9%2E2%2E8%29%20Gecko%2F20100722%20Firefox%2F3%2E6%2E8&ihttpheader=true&url="+urllib.quote_plus(newlink)+"&isslverify=true",strDomain)
                vidmatch=re.compile('"url_encoded_fmt_stream_map":"(.+?)",').findall(vidcontent)

                if(len(vidmatch) > 0):
                        vidparam=urllib.unquote_plus(vidmatch[0]).replace("\u003d","=")
                        vidlink=re.compile('url=(.+?)\u00').findall(vidparam)
                        CreateList('googledocs',vidlink[0])
           elif (newlink.find("video.google.com") > -1):
                match=re.compile('http://video.google.com/videoplay.+?docid=(.+?)&.+?').findall(newlink)
                glink=""
                if(len(match) > 0):
                        glink = GetContent("http://www.flashvideodownloader.org/download.php?u=http://video.google.com/videoplay?docid="+match[0])
                else:
                        match=re.compile('http://video.google.com/googleplayer.swf.+?docId=(.+?)&dk').findall(newlink)
                        if(len(match) > 0):
                                glink = GetContent("http://www.flashvideodownloader.org/download.php?u=http://video.google.com/videoplay?docid="+match[0])
                gcontent=re.compile('<div class="mod_download"><a href="(.+?)" title="Click to Download">').findall(glink)
                if(len(gcontent) > 0):
                        CreateList('google',gcontent[0])
           elif (newlink.find("vimeo") > -1):
                print "newlink|" + newlink
                idmatch =re.compile("//player.vimeo.com/video/(.+?)\?").findall(newlink+"?")
                print idmatch
                vidurl=getVimeoUrl(idmatch[0],"http://"+url.split('/')[2])
                CreateList("other",vidurl)
           elif (newlink.find("vid.me") > -1):
                link=GetContent(newlink)
                link = ''.join(link.splitlines()).replace('\'','"')
                match=re.compile('<meta property="og:video:url" [^>]*content=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
                for vbam in match:
                     if(vbam.find(newlink) == -1):
                          vidurl=urllib2.unquote(vbam).replace("&amp;","&") 
                CreateList('khmeravenue',vidurl)
           elif (newlink.find("videobam") > -1):
                link=GetContent(newlink)
                link = ''.join(link.splitlines()).replace('\'','"')
                match=re.compile('"url"\s*:\s*"(.+?)","').findall(link)
                for vbam in match:
                     if(vbam.find("mp4") > -1):
                          vidurl=vbam.replace("\\","")
                CreateList("other",vidurl)
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
                    CreateList("youtube",lastmatch)
                else:
                    CreateList("other",urllib2.unquote(newlink).decode("utf8"))
        #except: pass

def loadVideos(url,name):
        #try:
           GA("LoadVideos",name)
           link=GetContent(url)
           newlink = ''.join(link.encode("utf-8").splitlines()).replace('\t','')
           vidurl=""
           match=re.compile("'file': '(.+?)',").findall(newlink)
           if(len(match) == 0):
                   match=re.compile('<div class="video_main">\s*<iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(newlink)
                   if(len(match)==0):
                           match=re.compile('<iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(newlink)
                           if(len(match)==0):
                                   match=re.compile("<param name='flashvars' value='file=(.+?)&").findall(newlink)
           newlink=match[0]
           print newlink
           #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Loading selected video)")
           if (newlink.find("dailymotion") > -1):
                match=re.compile('www.dailymotion.com/embed/video/(.+?)\?').findall(newlink+"?")
                if(len(match) == 0):
                        match=re.compile('www.dailymotion.com/video/(.+?)&dk;').findall(newlink+"&dk;")
                if(len(match) == 0):
                        match=re.compile('www.dailymotion.com/swf/(.+?)\?').findall(newlink)
                if(len(match) == 0):
                	match=re.compile('www.dailymotion.com/embed/video/(.+?)\?').findall(newlink.replace("$","?"))
                vidlink=getDailyMotionUrl(match[0])
                playVideo('dailymontion',vidlink)
           elif (newlink.find("docs.google.com") > -1):
                vidcontent = postContent("http://javaplugin.org/WL/grp2/plugins/plugins_player.php","iagent=Mozilla%2F5%2E0%20%28Windows%3B%20U%3B%20Windows%20NT%206%2E1%3B%20en%2DUS%3B%20rv%3A1%2E9%2E2%2E8%29%20Gecko%2F20100722%20Firefox%2F3%2E6%2E8&ihttpheader=true&url="+urllib.quote_plus(newlink)+"&isslverify=true","http://www.superphim.com")
                if(len(vidcontent.strip())==0):
                     vidcontent = GetContent(newlink)
                vidmatch=re.compile('"url_encoded_fmt_stream_map":"(.+?)",').findall(vidcontent)
                if(len(vidmatch) > 0):
                        vidparam=urllib.unquote_plus(vidmatch[0]).replace("\u003d","=")
                        vidlink=re.compile('url=(.+?)\u00').findall(vidparam)
                        playVideo('google',vidlink[0])
           elif (newlink.find("vimeo") > -1):
                #
                print "newlink|" + newlink
                idmatch =re.compile("//player.vimeo.com/video/(.+?)\?").findall(newlink+"?")
                print idmatch
                vidurl=getVimeoUrl(idmatch[0],"http://"+url.split('/')[2])
                playVideo('khmeravenue',vidurl)
           elif (newlink.find("vid.me") > -1):
                link=GetContent(newlink)
                link = ''.join(link.splitlines()).replace('\'','"')
                match=re.compile('<meta property="og:video:url" [^>]*content=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
                for vbam in match:
                     if(vbam.find(newlink) == -1):
                          vidurl=urllib2.unquote(vbam).replace("&amp;","&") 
                playVideo('khmeravenue',vidurl)
           elif (newlink.find("videobam") > -1):
                link=GetContent(newlink)
                link = ''.join(link.splitlines()).replace('\'','"')
                match=re.compile('"url"\s*:\s*"(.+?)","').findall(link)
                for vbam in match:
                     if(vbam.find("mp4") > -1):
                          vidurl=vbam.replace("\\","")
                playVideo('khmeravenue',vidurl)
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
                    #d = xbmcgui.Dialog()
                    #d.ok('mode 2',str(lastmatch),'launching yout')
                    playVideo('youtube',lastmatch)
                else:
                    playVideo('moviekhmer',urllib2.unquote(newlink).decode("utf8"))
        #except: pass

def getDailyMotionUrl(id):
    maxVideoQuality="720p"
    content = GetContent("http://www.dailymotion.com/embed/video/"+id)
    if content.find('"statusCode":410') > 0 or content.find('"statusCode":403') > 0:
        xbmc.executebuiltin('XBMC.Notification(Info:, (DailyMotion)!,5000)')
        return ""
    else:
        matchFullHD = re.compile('"stream_h264_hd1080_url":"(.+?)"', re.DOTALL).findall(content)
        matchHD = re.compile('"stream_h264_hd_url":"(.+?)"', re.DOTALL).findall(content)
        matchHQ = re.compile('"stream_h264_hq_url":"(.+?)"', re.DOTALL).findall(content)
        matchSD = re.compile('"stream_h264_url":"(.+?)"', re.DOTALL).findall(content)
        matchLD = re.compile('"stream_h264_ld_url":"(.+?)"', re.DOTALL).findall(content)
        url = ""
        if matchFullHD and maxVideoQuality == "1080p":
            url = urllib.unquote_plus(matchFullHD[0]).replace("\\", "")
        elif matchHD and (maxVideoQuality == "720p" or maxVideoQuality == "1080p"):
            url = urllib.unquote_plus(matchHD[0]).replace("\\", "")
        elif matchHQ:
            url = urllib.unquote_plus(matchHQ[0]).replace("\\", "")
        elif matchSD:
            url = urllib.unquote_plus(matchSD[0]).replace("\\", "")
        elif matchLD:
            url = urllib.unquote_plus(matchLD[0]).replace("\\", "")
        return url

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
        liz=xbmcgui.ListItem('Next >', iconImage="http://i61.tinypic.com/24e2khl.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": 'Next >' } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="http://i61.tinypic.com/24e2khl.png", thumbnailImage=iconimage)
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
elif mode==4:
        #sysarg="-1"
        SEARCH()
elif mode==5:
       GA("Episodes",name)
       Episodes(url,name)
elif mode==6:
       SearchResults(url)
elif mode==8:
       PLAYLIST_VIDEOLINKS(url,name)

xbmcplugin.endOfDirectory(int(sysarg))
