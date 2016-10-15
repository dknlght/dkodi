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
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
from BeautifulSoup import SoupStrainer

strDomain ='http://www.video4khmer5.com/'


ADDON = xbmcaddon.Addon(id='plugin.video.video4Khmer')
if ADDON.getSetting('ga_visitor')=='':
    from random import randint
    ADDON.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))
    
PATH = "video4khmer"  #<---- PLUGIN NAME MINUS THE "plugin.video"          
UATRACK="UA-40129315-1" #<---- GOOGLE ANALYTICS UA NUMBER   
VERSION = "1.0.10" #<---- PLUGIN VERSION
def HOME():
        addDir('Search','http://www.video4khmers.com/',4,'http://www.video4khmers.com/templates/3column/images/header/logo.png')
        addDir('Thai Lakorns','http://www.video4khmers.com/khmer-movie-category/thai-lakorn-drama-watch-online-free-catalogue-537-page-1.html',2,'http://moviekhmer.com/wp-content/uploads/2012/03/lbach-sneah-prea-kai-180x135.jpg')
        addDir('Thai Movies','http://www.video4khmers.com/khmer-movie-category/thai-movie-watch-online-free-catalogue-525-page-1.html',2,'http://moviekhmer.com/wp-content/uploads/2012/03/lbach-sneah-prea-kai-180x135.jpg')
        addDir('Korean Videos','http://www.video4khmers.com/khmer-movie-category/korean-drama-watch-online-free-catalogue-507-page-1.html',2,'http://www.khmeravenue.com/wp-content/uploads/2012/04/lietome.jpg')
        #addDir('Korean Movies','http://www.video4khmers.com/browse-khmer-korean-movie-videos-1-date.html',2,'http://www.khmeravenue.com/wp-content/uploads/2012/04/lietome.jpg')
        addDir('Chinese Drama','http://www.video4khmers.com/khmer-movie-category/chinese-series-drama-watch-online-free-catalogue-506-page-1.html',2,'http://www.khmeravenue.com/wp-content/uploads/2012/05/rosemartial.jpg')
        addDir('Chinese Movies','http://www.video4khmers.com/khmer-movie-category/chinese-movie-watch-online-free-catalogue-505-page-1.html',2,'http://www.khmeravenue.com/wp-content/uploads/2012/05/rosemartial.jpg')
        addDir('Khmer Videos','http://www.video4khmers.com/khmer-movie-category/khmer-drama-watch-online-free-catalogue-504-page-1.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Khmer Movies','http://www.video4khmers.com/khmer-movie-category/khmer-movies-watch-online-free-catalogue-503-page-1.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Khmer Comedy','http://www.video4khmers.com/khmer-movie-category/khmer-comedy-watch-online-free-catalogue-502-page-1.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('phleng production','http://www.video4khmers.com/khmer-movie-category/phleng-production-khmer-video-karaoke-catalogue-2845-page-1.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Hang Meas Karaoke','http://www.video4khmers.com/khmer-movie-category/hang-meas-khmer-video-karaoke-catalogue-509-page-1.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Sunday Khmer Karaoke','http://www.video4khmers.com/khmer-movie-category/sunday-khmer-video-karaoke-catalogue-510-page-1.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Town Production Karaoke','http://www.video4khmers.com/khmer-movie-category/town-production-khmer-video-karaoke-catalogue-514-page-1.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Big Man Khmer Karaoke','http://www.video4khmers.com/khmer-movie-category/big-man-khmer-video-karaoke-catalogue-512-page-1.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('M Production Karaoke','http://www.video4khmers.com/khmer-movie-category/m-production-khmer-video-karaoke-catalogue-511-page-1.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Rock Production Karaoke','http://www.video4khmers.com/khmer-movie-category/rock-production-khmer-video-karaoke-catalogue-513-page-1.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Spark Production Karaoke','http://www.video4khmers.com/khmer-movie-category/spark-production-khmer-video-karaoke-catalogue-516-page-1.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Chenla Brother Karaoke','http://www.video4khmers.com/khmer-movie-category/chenla-brother-khmer-video-karaoke-catalogue-518-page-1.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Khmer Radio','http://www.video4khmers.com/khmerradio.php?rname=rfi',9,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Khmer video clip','http://www.video4khmers.com/khmer-movie-category/khmer-clips-watch-online-free-catalogue-1366-page-1.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        #addDir('MISC','http://www.video4khmers.com/browse-this-and-that-accident-society-misc-videos-1-date.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Khmer Tv show','http://www.video4khmers.com/khmer-movie-category/watch-cambodia-tv-shows-online-catalogue-1278-page-1.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        #addDir('Funney Videos','http://www.video4khmers.com/browse-funny-video-clips-videos-1-date.html',2,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')		
def INDEX(url):
    #try:
        link = GetContent(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        soup = BeautifulSoup(newlink)
        listcontent=soup.findAll('div', {"id" : "content-center"})
        for item in listcontent[0].findAll('div', {"class" : "cat-thumb"}):
			vname=item.a.img["alt"]
			vurl=item.a["href"]
			vimg=item.a.img["src"]
			addDir(vname.encode('utf-8', 'ignore'),vurl,5,vimg)

        for item in listcontent[0].findAll('li'):
             if(item.a!=None):
				pageurl=item.a["href"]
				pagenum=item.a.contents[0].replace("&gt;",">").replace("&lt;","<")
				addDir("Page " + pagenum,pageurl,2,"")
    #except: pass
def KhmerRadio():
        addDir('RADIO FRANCE INTERNATIONALE','http://www.video4khmers.com/khmerradio.php?rname=rfi',10,'http://www.video4khmers.com/images/radio/small/rfi.gif')
        addDir('RADIO FREE ASIA','http://www.video4khmers.com/khmerradio.php?rname=rfa',10,'http://www.video4khmers.com/images/radio/small/rfa.gif')
        addDir('ABC RADIO AUSTRALIA','http://www.video4khmers.com/khmerradio.php?rname=abc',10,'http://www.video4khmers.com/images/radio/big/abc.png')
        addDir('VOICE OF AMERICA','http://www.video4khmers.com/khmerradio.php?rname=voa',10,'http://www.video4khmers.com/images/radio/big/voa.png')
        addDir('Latest New Khmer mp3','http://www.video4khmers.com/khmer-mp3/latest-new-khmer-mp3-1-1.html',10,'http://www.video4khmers.com/templates/3column/images/menu/new_mp3_play.png')
        addDir('Khmer Oldies Male Singers mp3','http://www.video4khmers.com/khmer-mp3/khmer-oldies-male-singers-from-50s-60s-70s-mp3-2-1.html',10,'http://www.video4khmers.com/templates/3column/images/menu/old_mp3.png')
        addDir('Khmer Oldies Male and FeMale Singers mp3','http://www.video4khmers.com/khmer-mp3/khmer-oldies-male-and-female-singers-from-50s-60s-70s-mp3-3-1.html',10,'http://www.video4khmers.com/templates/3column/images/menu/old_mp3_feat.png')

def RadioList(url):
        link = GetContent(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile("\{\s*title:\s*'(.+?)'\s*,\s*mp3:\s*'(.+?)'\}").findall(newlink)
        for vcontent in match:
              addSong(vcontent[0],vcontent[1],"","",[], 1)
def SEARCH():
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        #searchText = '01'
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        url = 'http://www.video4khmers.com/search.php?keywords='+ searchText +'&btn=Search'
        INDEX(url)
        
def SearchResults(url):
        link = GetContent(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        soup = BeautifulSoup(newlink)
        listcontent=soup.findAll('div', {"id" : "content-center"})
        for item in listcontent[0].findAll('div', {"class" : "cat-thumb"}):
			vname=item.a.img["alt"]
			vurl=item.a["href"]
			vimg=item.a.img["src"]
			addDir(vname.encode('utf-8', 'ignore'),vurl,5,vimg)
        for item in listcontent[0].findAll('li'):
             if(item.a!=None):
				pageurl=item.a["href"]
				pagenum=item.a.contents[0].replace("&gt;",">").replace("&lt;","<")
				addDir("Page " + pagenum,pageurl,2,"")
			
def Episodes_old(url,name):
    #try:
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<ul><li class="video"><div class="video_i"><a href="(.+?)">').findall(newlink)
        vidseries = re.compile('-video_(.+?).html').findall(url)
        if(len(match[0])):
                vidseries = re.compile('-video_(.+?).html').findall(match[0])
                vidseries=vidseries[0]
                addLink(name,match[0],3,"")
        elif (len(vidseries)):
                vidseries=vidseries[0]
                addLink(name,url,3,"")
        try:
                lastvidseries = ParseXml("http://www.video4khmers.com/relatedclips.php?vid=" + vidseries)
                if(len(lastvidseries)):
                        lastvidseries = ParseXml("http://www.video4khmers.com/relatedclips.php?vid=" + lastvidseries)
                        if(len(lastvidseries)):
                                addDir("Next >>","http://www.video4khmers.com/relatedclips.php?vid=" + lastvidseries,7,"")
                else:
                        raise Exception("Didn't fine listing")
        except:
                match=re.compile('<div id="browse_results" (.+?)<ul>(.+?)</ul></div>').findall(newlink)
                if(len(match) >= 1):
                        linkmatch=re.compile('<img src="(.+?)"  alt=[^>]*').findall(match[0][1])
                        counter = 0
                        for vpic in linkmatch:
                            counter += 1
                            youtubeid = re.compile('/vi/(.+?)/').findall(vpic)
                            addLink(name + " " + str(counter),"http://www.youtube.com/watch?v="+youtubeid[0],3,vpic)
    #except: pass
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
        if result["status"] == 200:
            html = result["content"]
            html = html[html.find('={')+1:]
            html = html[:html.find('}};')]+"}}"
            try:
                  collection = json.loads(html)
                  if(collection["request"]["files"]["progressive"]!=None):
					return collection["request"]["files"]["progressive"][0]["url"]
                  else:
					return collection["request"]["files"]["hls"]["url"]
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
        soup = BeautifulSoup(newlink)
        listcontent=soup.findAll('div', {"id" : "content-center"})
        for item in listcontent[0].findAll('div', {"class" : "movie-thumb"}):
			vname=item.a.img["alt"]
			vurl=item.a["href"]
			vimg=item.a.img["src"]
			addLink(vname,vurl,3,vimg)

        for item in listcontent[0].findAll('li'):
             if(item.a!=None):
				pageurl=item.a["href"]
				pagenum=item.a.contents[0].replace("&gt;",">").replace("&lt;","<")
				addDir("Page " + pagenum,pageurl,5,"")
				

    #except: pass    

def ParseXml(url):
        newcontent=GetContent(url)
        vurl=""
        xmlcontent=xml.dom.minidom.parseString(newcontent.encode('utf-8'))
        items=xmlcontent.getElementsByTagName('video')
        if(len(items)>=1 and len(items[0].getElementsByTagName('url')[0].childNodes)):
                for itemXML in items:
                        vname=itemXML.getElementsByTagName('title')[0].childNodes[0].data
                        vurl=itemXML.getElementsByTagName('url')[0].childNodes[0].data
                        vimg=itemXML.getElementsByTagName('thumb')[0].childNodes[0].data
                        youtubeid = re.compile('/vi/(.+?)/').findall(vimg)
                        if(len(youtubeid)):
                                addLink(vname,"http://www.youtube.com/watch?v="+youtubeid[0],3,vimg)
                        else:
                                addLink(vname,vurl,3,vimg)
        if(len(vurl) >= 1):
                vidseries = re.compile('-video_(.+?).html').findall(vurl)[0]
        else:
                vidseries =""
        return vidseries

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
	
def GetContent(url):
    #try:
       net = Net()
       headers = {}
       headers['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
       headers['Accept-Encoding'] = 'gzip, deflate'
       headers['Accept-Charset']='ISO-8859-1,utf-8;q=0.7,*;q=0.7'
       #headers['Referer'] = strDomain
       #headers['Content-Type'] = 'application/x-www-form-urlencoded'
       headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1'
       headers['Connection'] = 'keep-alive'
       #headers['Host']='www.vdokhmer.com'
       headers['Accept-Language']='en-us,en;q=0.5'
       headers['Pragma']='no-cache'
       formdata={}   
       second_response = net.http_GET(url,headers=headers)
       return second_response.content
    #except:	
    #   d = xbmcgui.Dialog()
    #   d.ok(url,"Can't Connect to site",'Try again in a moment')

def playVideo(videoType,videoId):
    url = videoId
    if (videoType == "youtube"):
        try:
                url = getYoutube(videoId)
                xbmcPlayer = xbmc.Player()
                xbmcPlayer.play(url)
        except:
                url = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + videoId.replace('?','')
                xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
    elif (videoType == "vimeo"):
        url = getVimeoUrl(videoId,strDomain)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(url)
    elif (videoType == "tudou"):
        url = 'plugin://plugin.video.tudou/?mode=3&url=' + videoId	
    else:
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
                loadPlaylist(videoLink,name)
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

def CreateList(videoType,videoLink):
    url1 = ""
    if (videoType == "youtube"):
        url1 = getYoutube(videoLink)
    elif (videoType == "vimeo"):
        url1 = getVimeoUrl(videoLink,strDomain)
    elif (videoType == "tudou"):
        url1 = 'plugin://plugin.video.tudou/?mode=3&url=' + videoId	
    else:
        url1=videoLink

    if(len(videoLink) >0):
        liz = xbmcgui.ListItem('[B]PLAY VIDEO[/B]', thumbnailImage="")
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.add(url=url1, listitem=liz)
        
def loadPlaylist(newlink,name):
        #try:
           if (newlink.find("video4khmer") > -1 or newlink.find("vdokhmer.com") > -1 ):
                print "currenturl" + newlink
                linkcontent = GetContent(newlink)
                newContent = ''.join(linkcontent.splitlines()).replace('\t','')
                titlecontent = re.compile("var flashvars = {file: '(.+?)',").findall(newContent)
                if(len(titlecontent) == 0):
                        titlecontent = re.compile('<source type="video/mp4" [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(newContent)
                if(len(titlecontent) == 0):
                        titlecontent = re.compile('swfobject\.embedSWF\("(.+?)",').findall(newContent)
                if(len(titlecontent) == 0):
                        titlecontent = re.compile("'file':\s*'(.+?)'").findall(newContent)
                if(len(titlecontent) == 0):
                        titlecontent = re.compile('<iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(newContent)
                newlink=titlecontent[0]

           if (newlink.find("dailymotion") > -1):
                match=re.compile('(dailymotion\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(newlink)
                if(len(match) == 0):
                        match = re.compile('http://www.dailymotion.com/swf/(.+?)&').findall(newlink)
                if(len(match[0])>1):
                     link = 'http://www.dailymotion.com/video/'+str(match[0][-1].replace("video/",""))
                else: 
                     link = 'http://www.dailymotion.com/video/'+str(match[0])
                req = urllib2.Request(link)
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                sequence=re.compile('<param name="flashvars" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
                newseqeunce = urllib.unquote(sequence[0]).decode('utf8').replace('\\/','/')
                #print 'in dailymontion:' + str(newseqeunce)
                imgSrc=re.compile('"videoPreviewURL":"(.+?)"').findall(newseqeunce)
                if(len(imgSrc[0]) == 0):
                	imgSrc=re.compile('/jpeg" href="(.+?)"').findall(link)
                dm_low=re.compile('"video_url":"(.+?)",').findall(newseqeunce)
                dm_high=re.compile('"hqURL":"(.+?)"').findall(newseqeunce)
                CreateList('dailymontion',urllib2.unquote(dm_low[0]).decode("utf8"))
           elif (newlink.find("docs.google.com") > -1):  
                docid=re.compile('/d/(.+?)/preview').findall(newlink)[0]
                vidcontent = GetContent("https://docs.google.com/get_video_info?docid="+docid) 
                html = urllib2.unquote(vidcontent)
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
					CreateList('googledocs',url)
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
                idmatch =re.compile("http://player.vimeo.com/video/([^\?&\"\'>]+)\?").findall(newlink+"?")
                if(len(idmatch) > 0):
                        CreateList('vimeo',idmatch[0])
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
			
def parseVideos(url,name):
        link = GetContent(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        url = ''.join(link.splitlines()).replace('\t','')
        soup = BeautifulSoup(url)
        playercontent=soup.findAll('div', {"id" : "Playerholder"})
        if(len(playercontent)>0):
			viditem=playercontent[0].findAll('iframe')
			newlink=viditem[0]["src"]
			print newlink
			loadVideos(newlink,name)
        else:
			match=re.compile("'file':\s*'(.+?)'").findall(url)
			loadVideos(match[0],name)
		
def loadVideos(newlink,name):
        try:
           GA("LoadVideo",name)
           if (newlink.find("video4khmer") > -1 or newlink.find("vdokhmer.com") > -1 ):
                print "currenturl" + newlink
                linkcontent = GetContent(newlink)
                newContent = ''.join(linkcontent.splitlines()).replace('\t','')
                titlecontent = re.compile("var flashvars = {file: '(.+?)',").findall(newContent)
                if(len(titlecontent) == 0):
                        titlecontent = re.compile('<source type="video/mp4" [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(newContent)
                if(len(titlecontent) == 0):
                        titlecontent = re.compile('swfobject\.embedSWF\("(.+?)",').findall(newContent)
                if(len(titlecontent) == 0):
                        titlecontent = re.compile("'file':\s*'(.+?)'").findall(newContent)
                if(len(titlecontent) == 0):
                        titlecontent = re.compile('<iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(newContent)
                newlink=titlecontent[0]
           if (newlink.find("dailymotion") > -1):
                match=re.compile('http://www.dailymotion.com/embed/video/(.+?)\?').findall(newlink)
                if(len(match) == 0):
                        match=re.compile('http://www.dailymotion.com/video/(.+?)&dk;').findall(newlink+"&dk;")
                if(len(match) == 0):
                        match=re.compile('http://www.dailymotion.com/swf/(.+?)\?').findall(newlink)
                link = 'http://www.dailymotion.com/video/'+str(match[0])
                vidlink=getDailyMotionUrl(match[0])
                playVideo('dailymontion',vidlink)
           elif (newlink.find("docs.google.com") > -1):  
                docid=re.compile('/d/(.+?)/preview').findall(newlink)[0]
                vidcontent = GetContent("https://docs.google.com/get_video_info?docid="+docid) 
                html = urllib2.unquote(vidcontent)
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
					playVideo('google',url)
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
                        playVideo('google',gcontent[0])
           elif (newlink.find("vimeo") > -1):
                print "newlink|" + newlink
                idmatch =re.compile("http://player.vimeo.com/video/([^\?&\"\'>]+)\?").findall(newlink+"?")
                if(len(idmatch) > 0):
                        playVideo('vimeo',idmatch[0])
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
                    playVideo('youtube',lastmatch)
                else:
                    playVideo('other',urllib2.unquote(newlink).decode("utf8"))
        except: pass
		
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

def addSong(songname,songurl,songImg,album,artist, totalsong):
        cm = []

        trackLabel =   album + " - " + songname
        item = xbmcgui.ListItem(label = trackLabel, thumbnailImage=songImg, iconImage=songImg)
        item.setPath(songurl)
        item.setInfo( type="Video", infoLabels={ "title": name, "album": album, "artist": artist} )
        item.setProperty('mimetype', 'audio/mpeg')
        item.setProperty("IsPlayable", "true")
        item.setProperty('title', songname)
        item.setProperty('album', album)
        item.addContextMenuItems(cm, replaceItems=False)
        u=sys.argv[0]+"?url="+urllib.quote_plus(songurl)+"&mode=3&name="+urllib.quote_plus(songname)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=songurl,listitem=item,isFolder=False, totalItems=totalsong)
def addLink(name,url,mode,iconimage):
        try:
            name =name.encode("UTF-8")
        except: pass
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
        liz=xbmcgui.ListItem('Next >', iconImage="http://www.video4khmers.com/templates/3column/images/header/logo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": 'Next >' } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addDir(name,url,mode,iconimage):
        try:
            name =name.encode("UTF-8")
        except: pass
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="http://www.video4khmers.com/templates/3column/images/header/logo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
		
def addPlayListLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok
		
def LOAD_AND_PLAY_VIDEO(url,name):
        xbmc.executebuiltin("XBMC.Notification(PLease Wait!, Loading video link into XBMC Media Player,5000)")
        ok=True
        print "playlist url="+url
        videoUrl = loadVideos(url,name,True,False)
        if videoUrl == None:
                d = xbmcgui.Dialog()
                d.ok('look',str(url),'Check other links.')
                return False
        elif videoUrl == 'skip':
                return False				
        elif videoUrl == 'ERROR':
                return False
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoUrl)
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
        GA("HOME","Home")
        HOME()
       
elif mode==2:
        #d = xbmcgui.Dialog()
        #d.ok('mode 2',str(url),' ingore errors lol')
        GA("INDEX",name)
        INDEX(url)
elif mode==3:
        #sysarg="-1"
        print url
        parseVideos(url,name)
elif mode==4:
        #sysarg="-1"
        SEARCH()
elif mode==5:
       GA("Episodes",name)
       Episodes(url,name)
elif mode==6:
       SearchResults(url)
elif mode==7:
       ParseXml(url)
elif mode==8:
       PLAYLIST_VIDEOLINKS(url,name)
elif mode==9:
       KhmerRadio()
elif mode==10:
       RadioList(url)

	   
xbmcplugin.endOfDirectory(int(sysarg))
