import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
import base64
import xbmc
import datetime
import time
import json
import jsunpack
from bs4 import BeautifulSoup as BS
from urlparse import urljoin
import urlresolver

def BeautifulSoup(markup):
    return BS(markup, 'html5lib')

ADDON = xbmcaddon.Addon(id='plugin.video.azdrama')
if ADDON.getSetting('ga_visitor')=='':
    from random import randint
    ADDON.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))
GA_PRIVACY = ADDON.getSetting('ga_privacy') == "true"
DISPLAY_MIRRORS = ADDON.getSetting('display_mirrors') == "true"

UASTR = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0"
PATH = "AzDrama"  #<---- PLUGIN NAME MINUS THE "plugin.video"
UATRACK = "UA-76815405-1"
VERSION = "1.0.18.1" #<---- PLUGIN VERSION
domainlist = ["azdrama.net", "www.azdrama.info", "www1.azdrama.net", "icdrama.se", "azdrama.se"]
domain = domainlist[int(ADDON.getSetting('domainurl'))]
def __init__(self):
    self.playlist=sys.modules["__main__"].playlist
def HOME():
        #addDir('Search','http://www.khmeravenue.com/',4,'http://yeuphim.net/images/logo.png')
        if ADDON.getSetting('list_recent_updates') == "true":
            addDir(ADDON.getLocalizedString(30202),'http://'+domain+'/recently-updated/',5,'')
        if ADDON.getSetting('list_hk_dramas') == "true":
            addDir(ADDON.getLocalizedString(30204),'http://'+domain+'/hk-drama/',2,'')
        if ADDON.getSetting('list_hk_movies') == "true":
            addDir(ADDON.getLocalizedString(30205),'http://'+domain+'/hk-movie/',2,'')
        if ADDON.getSetting('list_hk_shows') == "true":
            addDir(ADDON.getLocalizedString(30206),'http://'+domain+'/hk-show/',2,'')
        if ADDON.getSetting('list_korean_dramas') == "true":
            addDir(ADDON.getLocalizedString(30207),'http://'+domain+'/korean-drama/',2,'')
        if ADDON.getSetting('list_mainlan_dramas') == "true":
            addDir(ADDON.getLocalizedString(30208),'http://'+domain+'/chinese-drama/',2,'')
        if ADDON.getSetting('list_taiwanese_dramas') == "true":
            addDir(ADDON.getLocalizedString(30209),'http://'+domain+'/taiwanese-drama/',2,'')
        if ADDON.getSetting('list_korean_shows') == "true":
            addDir(ADDON.getLocalizedString(30210),'http://'+domain+'/korean-show/',2,'')
        if ADDON.getSetting('list_japanese_dramas') == "true":
            addDir(ADDON.getLocalizedString(30211),'http://'+domain+'/japanese-drama/',2,'')
        if ADDON.getSetting('list_movies') == "true":
            addDir(ADDON.getLocalizedString(30212),'http://'+domain+'/movies/',2,'')

def INDEX(url):
    content = GetContent(url)
    soup = BeautifulSoup(content)

    tiles = soup.select('a.movie-image')
    for t in tiles:
        imageurl = re.search(r'url\((.+?)\)', t['style']).group(1)
        vidurl = urljoin(url, t['href'])
        displayname = t['title']
        names = displayname.split(' - ')

        title_lang_option = ADDON.getSetting('title_language')
        if title_lang_option == '1':
            displayname = names[0]
        elif title_lang_option == '2':
            displayname = names[-1]

        addDir(displayname, vidurl, 5, imageurl)

    pages = soup.select('ul.pager > li > span > a')
    for p in pages:
        pagename = p['title']
        pageurl = urljoin(url, p['href'])
        addDir(pagename, pageurl, 2, '')

def SEARCH():
    try:
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        #searchText = '01'
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        url = 'http://yeuphim.net/movie-list.php?str='+ searchText
        INDEX(url)
    except: pass

def decodeurl(encodedurl):
    tempp9 =""
    tempp4="100108100114971099749574853495756564852485749575656"
    strlen = len(encodedurl)
    temp5=int(encodedurl[strlen-4:strlen],10)
    encodedurl=encodedurl[0:strlen-4]
    strlen = len(encodedurl)
    temp6=""
    temp7=0
    temp8=0
    while temp8 < strlen:
        temp7=temp7+2
        temp9=encodedurl[temp8:temp8+4]
        temp9i=int(temp9,16)
        partlen = ((temp8 / 4) % len(tempp4))
        partint=int(tempp4[partlen:partlen+1])
        temp9i=((((temp9i - temp5) - partint) - (temp7 * temp7)) -16)/3
        temp9=chr(temp9i)
        temp6=temp6+temp9
        temp8=temp8+4
    return temp6

def SearchResults(url):
        link = GetContent(url)
        newlink = ''.join(link.splitlines()).replace('\t','')
        match=re.compile('<aclass="widget-title" href="(.+?)"><imgsrc="(.+?)" alt="(.+?)"').findall(newlink)
        if(len(match) >= 1):
                for vLink,vpic,vLinkName in match:
                    addDir(vLinkName,vLink,5,vpic)
        match=re.compile('<strong>&raquo;</strong>').findall(link)
        if(len(match) >= 1):
            startlen=re.compile("<strongclass='on'>(.+?)</strong>").findall(newlink)
            url=url.replace("/page/"+startlen[0]+"/","/page/"+ str(int(startlen[0])+1)+"/")
            addDir("Next >>",url,6,"")

def Mirrors(url,name):
    try:
        if(CheckRedirect(url)):
                MirrorsThe(name,url)
        else:
                link = GetContent(url)
                newlink = ''.join(link.splitlines()).replace('\t','')
                match=re.compile('<b>Episode list </b>(.+?)</table>').findall(newlink)
                mirrors=re.compile('<div style="margin: 10px 0px 5px 0px">(.+?)</div>').findall(match[0])
                if(len(mirrors) >= 1):
                        for vLinkName in mirrors:
                            if DISPLAY_MIRRORS:
                                addDir(vLinkName,url,5,'')
                            else:
                               loadVideos(url, vLinkName.encode("utf-8"))

    except: pass

def Parts(url,name):
        content = GetContent(url)
        soup = BeautifulSoup(content)

        tites = soup.select('span.tite')
        uldefs = soup.select('ul.tn-uldef')

        zipped = zip(tites, uldefs)

        total = 0
        for t, u in zipped:
            mirror = t.string
            parts = u.find_all('a', recursive=False)

            numparts = len(parts)
            for index, part in enumerate(parts):
                link = part['href']
                name = 'Full' if part.string.strip().lower() == 'full' else ' Part %s/%s' % (index+1, numparts)
                if DISPLAY_MIRRORS:
                    addDir('%s@%s' % (name, mirror), link, 3, '')
                else:
                    loadVideos(link, '@%s %s' % (mirror, name))
                total += 1

        return total

def CheckParts(url,name):
	if(Parts(url,name) < 2):
		loadVideos(url,name)
def Episodes(url,name,newmode):
    #try:
        link = GetContent(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        if(newmode==5):
                vidmode=11
        else:
                vidmode=9
        soup = BeautifulSoup(newlink)
        match = [(n['href'], n['title']) for n in soup.select('ul.listep > li > a')]
        if match:
            for (vurl,vname) in match:
                vname = vname.lstrip('Watch ')
                if not url.endswith('/recently-updated/'):
                    vname = vname.split('-')[-1].strip()
                addDir(vname,vurl,vidmode,"")
            pagecontent=re.compile('<div class="wp-pagenavi" align=center>(.+?)</div>').findall(newlink)
            if(len(pagecontent)>0):
                    match5=re.compile('<a href="(.+?)" class="(.+?)" title="(.+?)">(.+?)</a>').findall(pagecontent[0])
                    for vurl,vtmp,vname,vtmp2 in match5:
                        addDir(cleanPage(vname),vurl,newmode,"")
        else:
            node = soup.select('a.btnWatch')[0]
            CheckParts(node['href'], node['title'])

    #except: pass

def GetEpisodeFromVideo(url,name):
        link = GetContent(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        listcontent=re.compile('<div align="center">(.+?)<div style=[^>]*>').findall(newlink)
        if listcontent:
            match=re.compile('<a href="(.+?)"><b>(.+?)</b>').findall(listcontent[0])
            if match:
                for (vurl,vname) in match:
                    addDir("Episode: " + vname,vurl,11,"")
            else:
                listcontent=re.compile('<center><a href="(.+?)"><font style="(.+?)">(.+?)</font></a></center>').findall(newlink)
                Episodes(listcontent[0][0]+"list-episode/",name,5)
        else:
             listcontent=re.compile('<center><a href="(.+?)"><font style="(.+?)">(.+?)</font></a></center>').findall(newlink)
             Episodes(listcontent[0][0]+"list-episode/",name,5)

def Geturl(strToken):
        for i in range(20):
                try:
                        strToken=strToken.decode('base-64')
                except:
                        return strToken
                if strToken.find("http") != -1:
                        return strToken


def GetContent(url):
    try:
       net = Net()
       second_response = net.http_GET(url)
       return second_response.content
    except:
       d = xbmcgui.Dialog()
       d.ok(url,"Can't Connect to site",'Try again in a moment')

def playVideo(videoType,videoId):
    url = ""
    print videoType + '=' + videoId
    if (videoType == "youtube"):
        url = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + videoId.replace('?','')
        xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
    elif (videoType == "vimeo"):
        url = 'plugin://plugin.video.vimeo/?action=play_video&videoID=' + videoId
    elif (videoType == "tudou"):
        url = 'plugin://plugin.video.tudou/?mode=3&url=' + videoId
    else:
        if any(x in videoId for x in ['h265.se', 'uptobox.com', 'uptostream.com', 'openload.co']):
            videoId = urlresolver.resolve(videoId)

        if videoId:
            xbmcPlayer = xbmc.Player()
            xbmcPlayer.play(videoId)
        else:
            xbmc.executebuiltin('Notification(Info:,Video not playable,5000,)')

def postContent(url,data,referr):
    opener = urllib2.build_opener()
    opener.addheaders = [('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                         ('Accept-Encoding','gzip, deflate'),
                         ('Referer', referr),
                         ('Content-Type', 'application/x-www-form-urlencoded'),
                         ('User-Agent', UASTR),
                         ('Connection','keep-alive'),
                         ('Accept-Language','en-us,en;q=0.5'),
                         ('Pragma','no-cache'),
                         ('Host','videobug.se')]
    usock=opener.open(url,data)
    if usock.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(usock.read())
        f = gzip.GzipFile(fileobj=buf)
        response = f.read()
    else:
        response = usock.read()
    usock.close()
    return response

def vidbugresolver2(inputstring):
	newstring = urllib.unquote_plus(inputstring[:-1])
	t=""
	for i in range(len(newstring)):
		t=t+chr(ord(newstring[i])-int(inputstring[-1:]))
	return t

def vidbugresolver(inputstringorig):
	attempts=0
	inputstring=""
	t=""
	result=None
	while attempts < 10:
		#if True:
		print "attempts =" + str(attempts)
		try:
			if(attempts!=0):
				t=vidbugresolver1(inputstringorig,str(attempts))
			else:
				t=vidbugresolver1(inputstringorig,"")
			result= re.compile('json_allupload\d?.php",{vidID:\s*"(.+?)",vidKey:\s*"(.+?)",').findall(t)[0]
			break
		except:
			attempts += 1

	return result

def vidbugresolver1(inputstring,strcat):

	try:
		inputstring=inputstring+strcat
		newstring = urllib.unquote_plus(inputstring[1:len(inputstring)-1])
		t=""
		for i in range(len(newstring)):
			t=t+chr(ord(newstring[i])-int(inputstring[0:1]))
	except:
		t=vidbugresolver2(inputstring)
	return t

def getDailyMotionUrls(id):
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
        keys = cc.keys()
        possible_keys = ['1080', '720', '480', '380', '240', 'auto']
        urls = [(cc[q][0]['url'], q.capitalize()) for q in possible_keys if q in keys]
        if not urls:
            xbmc.executebuiltin('XBMC.Notification(Info:, No playable Link found (DailyMotion)!,5000)')

def Videosresolve(url,name):
        #try:
           newlink=url
           print "Videosresolve|" +url
           if (newlink.find("dailymotion") > -1):
                match=re.compile('www.dailymotion.com/embed/video/(.+?)\?').findall(newlink)
                if(len(match) == 0):
                        match=re.compile('http://www.dailymotion.com/video/(.+?)&dk;').findall(newlink+"&dk;")
                else:
						match=re.compile('www.dailymotion.com/video/(.+?)&dk;').findall(match[0]+"&dk;")
                if(len(match) == 0):
                        match=re.compile('http://www.dailymotion.com/swf/(.+?)\?').findall(newlink)
                if(len(match) == 0):
                	match=re.compile('www.dailymotion.com/embed/video/(.+?)\?').findall(newlink.replace("$","?"))
                vidlink=getDailyMotionUrls(match[0])
           elif (newlink.find("cloudy") > -1):
                pcontent=GetContent(newlink)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                filecode = re.compile('flashvars.file="(.+?)";').findall(pcontent)[0]
                filekey = re.compile('flashvars.filekey="(.+?)";').findall(pcontent)[0]
                vidcontent="https://www.cloudy.ec/api/player.api.php?file=%s&key=%s"%(filecode,urllib.quote_plus(filekey))
                pcontent=GetContent(vidcontent)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                urlcode = re.compile('url=(.+?)&').findall(pcontent)[0]
                vidlink=[(urllib.unquote_plus(urlcode), 'Unknown Quality')]
           elif (newlink.find("videomega") > -1):
                refkey= re.compile('\?ref=(.+?)&dk').findall(newlink+"&dk")[0]
                vidcontent="http://videomega.tv/iframe.php?ref="+refkey
                pcontent=GetContent(vidcontent)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                urlcode = re.compile('if\s*\(!validstr\){\s*document.write\(unescape\("(.+?)"\)\);\s*}').findall(pcontent)[0]
                vidcontent=urllib.unquote_plus(urlcode)
                vidlink = [(re.compile('file:\s*"(.+?)",').findall(vidcontent)[0], 'Unknown Quality')]
           elif (newlink.find("video44") > -1):
                link=GetContent(newlink)
                link=''.join(link.splitlines()).replace('\'','"')
                media_url= ""
                media_url = re.compile('file:\s*"(.+?)"').findall(link)
                if(len(media_url)==0):
                     media_url = re.compile('url:\s*"(.+?)"').findall(link)
                vidlink = [(media_url[0], 'Unknown Quality')]
           elif (newlink.find("videobug") > -1):
               content = GetContent(newlink)
               content = jsunpack.unpack(content)
               vidlink = []

               # unobscurify
               key = 5
               unobscurify = lambda s: urllib.unquote(''.join(chr(ord(c) - key) for c in urllib.unquote(s)))
               df = re.search(r"dF\(\\'(.*)\\'\)", content)
               if df:
                   script_end = content.find('</script>', df.end())
                   script_end = script_end + 9 if script_end > -1 else -1
                   content = content[:script_end] + unobscurify(df.group(1)) + content[script_end:]

               # Allupload
               # http://videobug.se/vid-a/g2S5k34-MoC2293iUaa9Hw
               json_data = re.findall(r"json_data = '(.+)';", content)
               if json_data:
                   strdecode = lambda s: base64.b64decode(urllib.unquote(s)[::-1])
                   try:
                       hashes = json.loads(json_data[0])
                       exclude = ['Subtitles', 'image', 'JS', 'ADV']
                       videos = [h for h in hashes if h['s'] not in exclude]
                       vidlink = [(strdecode(h['u']), h['s']) for h in videos]
                   except Exception:
                       pass

               # Picasaweb, Videobug
               # http://videobug.se/video/Wz3_oCoEYozRSbJFQo4fkjmuvR6LpsFHM-XZya5tuk6stTXWdUeyplq5vVvSm0Yr0MXPFUmLt2XqrbLMPnE_Mgz8NbhXMZ6XFDI4hj253Z7af95WQPPDlpizIuuUXavEJqB8-bXuKbx6HTCMb5p5FC90yg1kXJb6?
               if not vidlink:
                   soup = BeautifulSoup(content)
                   player_func = re.compile(r'(player_[^\(]+)\(\);').match
                   butts = soup.find_all('input', type='button', onclick=player_func)

                   funcs = [player_func(b['onclick']).group(1) for b in butts]
                   qualities = [b['value'] for b in butts]

                   try:
                       func_bodies = [re.findall(r'%s\(\) *{(.+)};' % f, content)[0] for f in funcs]
                       re_flash = re.compile(r"video *= *{[^:]+: *'(.*?)' *}")
                       re_html5 = re.compile(r'<source.*?src=\"(.*?)\"')

                       urls = [(re_flash.findall(fb) or re_html5.findall(fb))[0] for fb in func_bodies]
                       vidlink = zip(urls, qualities)
                   except Exception:
                       pass

               # http://videobug.se/vid-al/XNkjCT5pBx1YlndruYWdWg?&caption=-sgCv7BkuLZn41-ZxxJZhTsKYcZIDgJPGYNOuIpulC_4kcrZ9k3fGQabH5rDAKgiLMVJdesVZPs
               if not vidlink:
                   vids = re.findall(r'''{ *file *: *strdecode\('(.+?)'\).*?label *: *"(.*?)"''', content)
                   for cryptic_url, quality in vids:
                       url = base64.b64decode(urllib.unquote(cryptic_url)[::-1])
                       vidlink.append((url, quality))

           elif (newlink.find("play44") > -1):
                link=GetContent(newlink)
                link=''.join(link.splitlines()).replace('\'','"')
                media_url= ""
                media_url = re.compile('playlist:\s*\[\s*\{\s*url:\s*"(.+?)",').findall(link)[0]
                vidlink = [(urllib.unquote(media_url), 'Unknown Quality')]
           elif (newlink.find("byzoo") > -1):
                link=GetContent(newlink)
                link=''.join(link.splitlines()).replace('\'','"')
                media_url= ""
                media_url = re.compile('playlist:\s*\[\s*\{\s*url:\s*"(.+?)",').findall(link)[0]
                vidlink = [(urllib.unquote(media_url), 'Unknown Quality')]
           elif (newlink.find("vidzur") > -1 or newlink.find("videofun") > -1 or newlink.find("auengine") > -1):
                link=GetContent(newlink)
                link=''.join(link.splitlines()).replace('\'','"')
                media_url= ""
                op = re.compile('playlist:\s*\[(.+?)\]').findall(link)[0]
                urls=op.split("{")
                for rows in urls:
                     if(rows.find("url") > -1):
                          murl= re.compile('url:\s*"(.+?)"').findall(rows)[0]
                          media_url=urllib.unquote_plus(murl)
                vidlink = [(media_url, 'Unknown Quality')]
           elif (newlink.find("cheesestream") > -1 or newlink.find("yucache") > -1):
                link=GetContent(newlink)
                link=''.join(pcontent.splitlines()).replace('\'','"')
                vidlink = [(re.compile('<meta property="og:video" content="(.+?)"/>').findall(link)[0], 'Unknown Quality')]
           elif(newlink.find("picasaweb.google") > 0):
                ua = urllib.urlencode({'iagent' : UASTR})
                vidcontent=postContent("http://cache.dldrama.com/gk/43/plugins_player.php",ua+"&ihttpheader=true&url="+urllib.quote_plus(newlink)+"&isslverify=true",domain)
                vidmatch=re.compile('"application/x-shockwave-flash"\},\{"url":"(.+?)",(.+?),(.+?),"type":"video/mpeg4"\}').findall(vidcontent)
                hdmatch=re.compile('"application/x-shockwave-flash"\},\{"url":"(.+?)",(.+?),(.+?)').findall(vidmatch[-1][2])
                if(len(hdmatch) > 0):
                    vidmatch=hdmatch
                vidlink=[(vidmatch[-1][0], 'Unknown Quality')]
           elif (newlink.find("docs.google.com") > -1):
                vidcontent = GetContent(newlink)
                vidmatch=re.compile('"url_encoded_fmt_stream_map":"(.+?)",').findall(vidcontent)
                if(len(vidmatch) > 0):
                        vidparam=urllib.unquote_plus(vidmatch[0]).replace("\u003d","=")
                        vidlink=[(re.compile('url=(.+?)\u00').findall(vidparam), 'Unknown Quality')]
           elif (newlink.find("allmyvideos") > -1):
                videoid=  re.compile('http://allmyvideos.net/embed-(.+?).html').findall(newlink)
                if(len(videoid)>0):
                       newlink="http://allmyvideos.net/"+videoid[0]
                link = GetContent(newlink)
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                mfree = re.compile('<input type="hidden" name="method_free" value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","id":idkey,"fname":fname,"referer":url,"method_free":mfree})
                pcontent=postContent2(newlink,posdata,url)
                vidlink=[(re.compile('"file" : "(.+?)",').findall(pcontent)[0], 'Unknown Quality')]
           elif (newlink.find("nosvideo") > -1):
                videoid=  re.compile('http://nosvideo.com/embed/(.+?)/').findall(newlink)
                if(len(videoid)>0):
                       newlink="http://nosvideo.com/"+videoid[0]
                link = GetContent(newlink)
                idkey = re.compile('<input type="hidden" name="id" value="(.+?)">').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" value="(.+?)">').findall(link)[0]
                fname = re.compile('<input type="hidden" name="fname" value="(.+?)">').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"usr_login":"","fname":fname,"rand":"","id":idkey,"referer":url,"method_free":"Continue+to+Video","method_premium":"","down_script":"1"})
                pcontent=postContent2(newlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                scriptcontent=re.compile('<div name="placeholder" id="placeholder">(.+?)</div></div>').findall(pcontent)[0]
                packed = scriptcontent.split("</script>")[1]
                unpacked = unpackjs4(packed)
                if unpacked=="":
                        unpacked = unpackjs3(packed,tipoclaves=2)

                unpacked = unpacked.replace("\\","")

                xmlUrl=re.compile('"playlist=(.+?)&').findall(unpacked)[0]
                vidcontent = postContent2(xmlUrl,None,url)
                vidlink=[(re.compile('<file>(.+?)</file>').findall(vidcontent)[0], 'Unknown Quality')]
           elif (newlink.find("uploadpluz") > -1):
                videoid=  re.compile('http://nosvideo.com/embed/(.+?)/').findall(newlink)
                if(len(videoid)>0):
                       newlink="http://nosvideo.com/"+videoid[0]
                link = GetContent(newlink)
                pcontent=''.join(link.splitlines()).replace('\'','"')
                scriptcontent=re.compile('<div id="player_code">(.+?)</div>').findall(pcontent)[0]
                packed = scriptcontent.split("</script>")[1].replace('<script type="text/javascript">',"")
                unpacked = unpackjs4(packed)
                if unpacked=="":
                        unpacked = unpackjs3(packed,tipoclaves=2)

                unpacked = unpacked.replace("\\","")

                vidUrl=re.compile('"file","(.+?)"').findall(unpacked)[0]
                vidlink=[(vidUrl+"|Referer=http%3A%2F%2Fuploadpluz.com%3A8080%2Fplayer%2Fplayer.swf", 'Unknown Quality')]
           elif (newlink.find("yourupload") > -1):
                link = GetContent(newlink)
                link=''.join(link.splitlines()).replace('\'','"')
                vidlink=re.compile('<a class="btn btn-primary" [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                vidlink=[(vidlink.replace("download.yucache.net","stream.yucache.net"), 'Unknown Quality')]
           elif (newlink.find("nowvideo") > -1):
                link = GetContent(newlink)
                link=''.join(link.splitlines()).replace('\'','"')
                fileid=re.compile('flashvars.file="(.+?)";').findall(link)[0]
                codeid=re.compile('flashvars.cid="(.+?)";').findall(link)
                if(len(codeid) > 0):
                     codeid=codeid[0]
                else:
                     codeid=""
                keycode=re.compile('flashvars.filekey=(.+?);').findall(link)[0]
                keycode=re.compile('var\s*'+keycode+'="(.+?)";').findall(link)[0]
                vidcontent=GetContent("http://www.nowvideo.sx/api/player.api.php?codes="+urllib.quote_plus(codeid) + "&key="+urllib.quote_plus(keycode) + "&file=" + urllib.quote_plus(fileid))
                vidlink = [(re.compile('url=(.+?)\&').findall(vidcontent)[0], 'Unknown Quality')]
           elif (newlink.find("180upload") > -1):
                if(newlink.find("embed") == -1):
                      vidcode = re.compile('180upload.com/(.+?)dk').findall(newlink+"dk")[0]
                      newlink= 'http://180upload.com/embed-'+vidcode+'.html'
                link=GetContent(newlink)
                file_code = re.compile('<input type="hidden" name="file_code" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                op = re.compile('<input type="hidden" name="op" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                embed_width = re.compile('<input type="hidden" name="embed_width" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                embed_height = re.compile('<input type="hidden" name="embed_height" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                test34 = re.compile('<input type="hidden" name="nwknj3" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)[0]
                posdata=urllib.urlencode({"op":op,"file_code":file_code,"referer":url,"embed_width":embed_width,"embed_height":embed_height,"nwknj3":test34})
                pcontent=postContent2(newlink,posdata,url)
                pcontent=''.join(pcontent.splitlines()).replace('\'','"')
                packed = re.compile('/swfobject.js"></script><script type="text/javascript">(.+?)</script>').findall(pcontent)[0]
                unpacked = unpackjs4(packed)
                if unpacked=="":
                        unpacked = unpackjs3(packed,tipoclaves=2)
                unpacked=unpacked.replace("\\","")
                vidlink = [(re.compile('addVariable\("file",\s*"(.+?)"\)').findall(unpacked)[0], 'Unknown Quality')]
           elif (newlink.find("youtube") > -1) and (newlink.find("playlists") > -1):
                playlistid=re.compile('playlists/(.+?)\?v').findall(newlink)
                vidlink=[("plugin://plugin.video.youtube?path=/root/video&action=play_all&playlist="+playlistid[0], 'Unknown Quality')]
           elif (newlink.find("youtube") > -1) and (newlink.find("list=") > -1):
                playlistid=re.compile('videoseries\?list=(.+?)&').findall(newlink+"&")
                vidlink=[("plugin://plugin.video.youtube?path=/root/video&action=play_all&playlist="+playlistid[0], 'Unknown Quality')]
           elif (newlink.find("youtube") > -1) and (newlink.find("/p/") > -1):
                playlistid=re.compile('/p/(.+?)\?').findall(newlink)
                vidlink=[("plugin://plugin.video.youtube?path=/root/video&action=play_all&playlist="+playlistid[0], 'Unknown Quality')]
           elif (newlink.find("youtube") > -1) and (newlink.find("/embed/") > -1):
                playlistid=re.compile('/embed/(.+?)\?').findall(newlink+"?")
                vidlink=[(getYoutube(playlistid[0]), 'Unknown Quality')]
           elif (newlink.find("youtube") > -1):
                match=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(newlink1)
                if(len(match) == 0):
                    match=re.compile('http://www.youtube.com/watch\?v=(.+?)&dk;').findall(newlink1)
                if(len(match) > 0):
                    lastmatch = match[0][len(match[0])-1].replace('v/','')
                print "in youtube" + lastmatch[0]
                vidlink=[(getYoutube(lastmatch[0]), 'Unknown Quality')]
           else:
                import urlresolver
                sources = []
                label=name
                hosted_media = urlresolver.HostedMediaFile(url=url, title=label)
                sources.append(hosted_media)
                source = urlresolver.choose_source(sources)
                print "inresolver=" + url
                if source:
                        vidlink = [(source.resolve(), 'Unknown Quality')]
                else:
                        vidlink = []
           return vidlink

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

        video_url += " | " + UASTR


        return video_url

def getYoutube(videoid):

                code = videoid
                linkImage = 'http://i.ytimg.com/vi/'+code+'/default.jpg'
                req = urllib2.Request('http://www.youtube.com/watch?v='+code+'&fmt=18')
                req.add_header('User-Agent', UASTR)
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()

                if len(re.compile('shortlink" href="http://youtu.be/(.+?)"').findall(link)) == 0:
                        if len(re.compile('\'VIDEO_ID\': "(.+?)"').findall(link)) == 0:
                                req = urllib2.Request('http://www.youtube.com/get_video_info?video_id='+code+'&asv=3&el=detailpage&hl=en_US')
                                req.add_header('User-Agent', UASTR)
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

def loadVideos(url,name):
		GA("LoadVideo",name)
		episode_name = ""
		print "loading from video " + url
		if DISPLAY_MIRRORS == False:
			episode_name = name
		link=GetContent(url)
		newlink = ''.join(link.splitlines()).replace('\t','')
		try:
			newlink =newlink.encode("UTF-8")
		except: pass
                soup = BeautifulSoup(newlink)
                match = [m['src'] for m in soup.select('iframe')]

                if match:
                    frameurl = match[0]
                else:
                    frameurl = decodeurl(re.compile('dl.link=dll\*(.+?)&').findall(newlink)[0])

                videos = Videosresolve(frameurl, name)
                for url, quality in videos:
                    pre = episode_name + ': ' if episode_name else ''
                    addLink(pre + quality, url, 8, '', '')


def parseDate(dateString):
    try:
        return datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString.encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
    except:
        return datetime.datetime.today() - datetime.timedelta(days = 1) #force update


def checkGA():
    if GA_PRIVACY == True:
        return
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
    if GA_PRIVACY == True:
        return
    import urllib2
    try:
        req = urllib2.Request(utm_url, None,
                                    {'User-Agent':UASTR}
                                     )
        response = urllib2.urlopen(req).read()
    except:
        print ("GA fail: %s" % utm_url)
    return response

def GA(group,name):
        if GA_PRIVACY == True:
            return
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

def addLink(name,url,mode,iconimage,mirrorname):        
        name = cleanName(name)
        u=sys.argv[0]+"?url="+urllib.quote_plus(url.encode('utf-8'))+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('utf-8'))+"&mirrorname="+urllib.quote_plus(mirrorname)
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
        try:
            name = name.encode('utf-8')
        except:
            pass
        try:
            url = url.encode('utf-8')
        except:
            pass
        name = cleanName(name)
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def cleanName(name):
        strireplace = re.compile(re.escape('Watch Online '), re.IGNORECASE)
        return strireplace.sub('',name)

def cleanPage(name):
        strireplace = re.compile(re.escape('&raquo;'), re.IGNORECASE)
        name = strireplace.sub('Last',name)
        strireplace = re.compile(re.escape('&laquo; First'), re.IGNORECASE)
        name = strireplace.sub('First Page',name)
        return name

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
mirrorname=None
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
        mirrorname=urllib.unquote_plus(params["mirrorname"])
except:
        pass

sysarg=str(sys.argv[1])
print "mode is:" + str(mode)
if mode==None or url==None or len(url)<1:

        HOME()
elif mode==2:
        GA("INDEX",name)
        INDEX(url)
elif mode==3:
        loadVideos(url,mirrorname)
elif mode==4:
        SEARCH()
elif mode==5:
       GA("Episodes",name)
       Episodes(url,name,mode)
elif mode==6:
       SearchResults(url)
elif mode==7:
       Episodes(url,name,mode)
elif mode==8:
        playVideo("direct",url)
elif mode==9:
       GetEpisodeFromVideo(url,name)
elif mode==10:
       Episodes2(url,name)
elif mode==11:
       CheckParts(url,name)

xbmcplugin.endOfDirectory(int(sysarg))
