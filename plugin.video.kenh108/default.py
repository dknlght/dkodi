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
import urlresolver
import datetime

ADDON = xbmcaddon.Addon(id='plugin.video.kenh108')
if ADDON.getSetting('ga_visitor')=='':
    from random import randint
    ADDON.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))
    
PATH = "Kenh108"  #<---- PLUGIN NAME MINUS THE "plugin.video"          
UATRACK="UA-40129315-1" #<---- GOOGLE ANALYTICS UA NUMBER   
VERSION = "1.0.2" #<---- PLUGIN VERSION
Rcon = [1,2,4,8,16,32,64,128,27,54,108,216,171,77,154,47,94,188,99,198,151,53,106,212,179,125,250,239,197,145];
SBox = [99,124,119,123,242,107,111,197,48,1,103,43,254,215,171,118,202,130,201,125,250,89,71,240,173,212,162,175,156,164,114,192,183,253,147,38,54,63,247,204,52,165,229,241,113,216,49,21,4,199,35,195,24,150,5,154,7,18,128,226,235,39,178,117,9,131,44,26,27,110,90,160,82,59,214,179,41,227,47,132,83,209,0,237,32,252,177,91,106,203,190,57,74,76,88,207,208,239,170,251,67,77,51,133,69,249,2,127,80,60,159,168,81,163,64,143,146,157,56,245,188,182,218,33,16,255,243,210,205,12,19,236,95,151,68,23,196,167,126,61,100,93,25,115,96,129,79,220,34,42,144,136,70,238,184,20,222,94,11,219,224,50,58,10,73,6,36,92,194,211,172,98,145,149,228,121,231,200,55,109,141,213,78,169,108,86,244,234,101,122,174,8,186,120,37,46,28,166,180,198,232,221,116,31,75,189,139,138,112,62,181,102,72,3,246,14,97,53,87,185,134,193,29,158,225,248,152,17,105,217,142,148,155,30,135,233,206,85,40,223,140,161,137,13,191,230,66,104,65,153,45,15,176,84,187,22];
shiftOffsets = [0,0,0,0,[0,1,2,3],0,[0,1,2,3],0,[0,1,3,4]];
Nb = 4;
Nk = 6;
Nr = 12;

strdomain ='http://www.lsb-movies.net/kenh108/'
def HOME():
        addDir('Search',strdomain,8,'')
        addDir('Recently Updated Videos',strdomain+'index.php?do=list&type=recently_updated',2,'')
        addDir('Recently Added Videos',strdomain+'index.php?do=list&type=more',2,'')

def ListHost(url):
        link = postContent(url,"","http://www.luongson.net/kenh108/index.php")
        try:
            link =link.encode("UTF-8")
        except: pass
        link  = ''.join(link.splitlines()).replace('\t','')
        serverlist= re.compile('<div class="noidung_servername">(.+?)</div>').findall(link)
        lcount = 0
        for (vname) in serverlist:
                TAG_RE = re.compile(r'<[^>]+>')
                addDir(TAG_RE.sub('', vname),url+"|"+str(lcount),5,"")
                lcount=lcount+1

def INDEX(url):
        link = postContent(url,"","http://www.luongson.net/kenh108/index.php")
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        vidcontent=re.compile('<div class="listmovies"><ul>(.+?)</ul>').findall(newlink)
        showlist=re.compile('<li>(.+?)</li>').findall(vidcontent[0])
        for showcontent in showlist:
                (vimg,vlink)=re.compile('<div class="movie_pix" [^>]*url\(["\)]?([^>^"^\)]+)["\)]?[^>]*><a href="(.+?)">').findall(showcontent)[0]
                (vlink,vname)=re.compile('<div class="movietitle"><a href="(.+?)">(.+?)<').findall(showcontent)[0]
                TAG_RE = re.compile(r'<[^>]+>')
                addDir(TAG_RE.sub('', vname),strdomain+vlink,10,vimg)
        pagelist=re.compile('<a class="paginate" title="(.+?)" href="(.+?)">').findall(newlink)
        for (vname,vlink) in pagelist:
                addDir(vname,strdomain+vlink.replace("/kenh108/",""),2,"")

def SEARCH():
        keyb = xbmc.Keyboard('', 'Enter search text')
        keyb.doModal()
        #searchText = '01'
        if (keyb.isConfirmed()):
                searchText = urllib.quote_plus(keyb.getText())
        link = postContent(strdomain+"index.php?do=timkiem","search_this="+searchText,"http://www.lsb-movies.net/kenh108/index.php")
        try:
            link =link.encode("UTF-8")
        except: pass
        link = ''.join(link.splitlines()).replace('\t','')
        vidcontent=re.compile('<div class="searchresults_image" [^>]*url\(["\)]?([^>^"^\)]+)["\)]?[^>]*>(.+?)<').findall(link)
        for (vimg,moviecontent) in vidcontent:
            (vlink,vimg,vname)=re.compile('<a href="(.+?)&image=(.+?)" alt=(.+?)>').findall(moviecontent)[0]
            addDir(vname,strdomain+vlink,10,vimg)
		

def GetVideoLinks(url):
        link = postContent(url,"","http://www.luongson.net/kenh108/index.php")
        link = ''.join(link.splitlines()).replace('\'','"')
        frmsrc1=re.compile('<iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>', re.IGNORECASE).findall(link)
        if(len(frmsrc1) ==0):
                frmsrc1=re.compile('"file":\s*"(.+?)"', re.IGNORECASE).findall(link)
                if(len(frmsrc1) ==0):
                        frmsrc1=re.compile('http://youtube.googleapis.com/v/(.+?)\?', re.IGNORECASE).findall(link)
                        if(len(frmsrc1) ==0):
                              frmsrc1=re.compile('proxy.link=kenh108\*(.+?)&', re.IGNORECASE).findall(link)
                              if(len(frmsrc1) ==0):
                                    frmsrc1=re.compile('<embed [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>', re.IGNORECASE).findall(link)
                                    if(len(frmsrc1) ==0):
                                             frmsrc1=re.compile('<param name="flashvars" [^>]*value=["\']?([^>^"^\']+)["\']?[^>]*>', re.IGNORECASE).findall(link)
                                             frmsrc1=re.compile('file=(.+?)&', re.IGNORECASE).findall(frmsrc1[0])
                                             frmsrc1[0]=urllib.unquote_plus(frmsrc1[0])
                              else:
                                             frmsrc1[0] = decrypt(frmsrc1[0])

                        else:
                              frmsrc1[0]="http://www.youtube.com/watch?v="+frmsrc1[0] 
        loadVideos(frmsrc1[0],"")
def Episodes(url,name,itemno):
        link = postContent(url,"","http://www.luongson.net/kenh108/index.php")
        try:
            link =link.encode("UTF-8")
        except: pass
        link  = ''.join(link.splitlines()).replace('\t','')
        match = re.compile('<div class="noidung_servers">(.+?)</div></div>').findall(link)
        serverlist=re.compile('</div>(.+?)</div>').findall(match[0].replace("</div>","</div></div>")+"</div></div>")
        itemno=int(itemno)
        episodelist=re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>(.+?)</a>').findall(serverlist[itemno])
        for (vlink,vname) in episodelist:
                addLink("Part " + vname,strdomain+vlink,4,"")


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
        url = 'plugin://plugin.video.vimeo/?action=play_video&videoID=' + videoId
    elif (videoType == "tudou"):
        url = 'plugin://plugin.video.tudou/?mode=3&url=' + videoId	
    else:
        #xbmc.executebuiltin("xbmc.PlayMedia("+videoId+")")
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoId)

def resolve_180upload(url,inhtml=None):
    net = Net()
    try:
        dialog = xbmcgui.DialogProgress()
        dialog.create('Resolving', 'Resolving 180Upload Link...')
        dialog.update(0)
        
        print '180Upload - Requesting GET URL: %s' % url
        if(inhtml==None):
               html = net.http_GET(url).content
        else:
               html = inhtml
        
        op = 'download1'
        id = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
        rand = re.search('<input type="hidden" name="rand" value="(.+?)">', html).group(1)
        method_free = ''
        
        data = {'op': op, 'id': id, 'rand': rand, 'method_free': method_free}
        
        dialog.update(33)
        
        print '180Upload - Requesting POST URL: %s' % url
        html = net.http_POST(url, data).content
        
        op = 'download2'
        id = re.search('<input type="hidden" name="id" value="(.+?)">', html).group(1)
        rand = re.search('<input type="hidden" name="rand" value="(.+?)">', html).group(1)
        method_free = ''

        data = {'op': op, 'id': id, 'rand': rand, 'method_free': method_free, 'down_direct': 1}

        dialog.update(66)

        print '180Upload - Requesting POST URL: %s' % url
        html = net.http_POST(url, data).content
        link = re.search('<span style="background:#f9f9f9;border:1px dotted #bbb;padding:7px;">.+?<a href="(.+?)">', html,re.DOTALL).group(1)
        print '180Upload Link Found: %s' % link
    
        dialog.update(100)
        dialog.close()
        return link
    except Exception, e:
        print '**** 180Upload Error occured: %s' % e
        raise
def get_match(data,patron,index=0):
    matches = re.findall( patron , data , flags=re.DOTALL )
    return matches[index]
	
def unpackjs4(texto):

    matches = texto.split("return p}")
    if len(matches)>0:
        data = matches[1].replace(".split(\"|\")))","")
    else:
        return ""

    patron = "(.*)\"([^\"]+)\""
    matches = re.compile(patron,re.DOTALL).findall(data)
    cifrado = matches[0][0]
    
    descifrado = ""
    
    claves = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","1g","1h","1i","1j","1k","1l","1m","1n","1o","1p","1q","1r","1s","1t","1u","1v","1w","1x","1y","1z"]
    palabras = matches[0][1].split("|")
    diccionario = {}
   
    i=0
    for palabra in palabras:
        if palabra!="":
            diccionario[claves[i]]=palabra
        else:
            diccionario[claves[i]]=claves[i]
        i=i+1


    def lookup(match):
        return diccionario[match.group(0)]


    claves.reverse()
    cadenapatron = '|'.join(claves)
    compiled = re.compile(cadenapatron)
    descifrado = compiled.sub(lookup, cifrado)

    return descifrado

def unpackjs3(texto,tipoclaves=1):

    
    patron = "return p\}(.*?)\.split"
    matches = re.compile(patron,re.DOTALL).findall(texto)

    if len(matches)>0:
        data = matches[0]
    else:
        patron = "return p; }(.*?)\.split"
        matches = re.compile(patron,re.DOTALL).findall(texto)
        if len(matches)>0:
            data = matches[0]
        else:
            return ""

    patron = "(.*)'([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    cifrado = matches[0][0]

    descifrado = ""
    
    # Create the Dictionary with the conversion table
    claves = []
    if tipoclaves==1:
        claves.extend(["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"])
        claves.extend(["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"])
    else:
        claves.extend(["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"])
        claves.extend(["10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","1g","1h","1i","1j","1k","1l","1m","1n","1o","1p","1q","1r","1s","1t","1u","1v","1w","1x","1y","1z"])
        claves.extend(["20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","2g","2h","2i","2j","2k","2l","2m","2n","2o","2p","2q","2r","2s","2t","2u","2v","2w","2x","2y","2z"])
        claves.extend(["30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","3g","3h","3i","3j","3k","3l","3m","3n","3o","3p","3q","3r","3s","3t","3u","3v","3w","3x","3y","3z"])
        
    palabras = matches[0][1].split("|")
    diccionario = {}

    i=0
    for palabra in palabras:

        if palabra!="":
            diccionario[claves[i]]=palabra
        else:
            diccionario[claves[i]]=claves[i]
        i=i+1

     # Substitute the words of the conversion table
     # Retrieved from http://rc98.net/multiple_replace
    def lookup(match):
        try:
            return diccionario[match.group(0)]
        except:
            return ""

     # Reverse key priority for having the longest
    claves.reverse()
    cadenapatron = '|'.join(claves)

    compiled = re.compile(cadenapatron)
    descifrado = compiled.sub(lookup, cifrado)

    descifrado = descifrado.replace("\\","")


    return descifrado
	
def unpackjs(texto):

    # Extract the function body
    patron = "eval\(function\(p\,a\,c\,k\,e\,d\)\{[^\}]+\}(.*?)\.split\('\|'\)\)\)"
    matches = re.compile(patron,re.DOTALL).findall(texto)

    
    # Separate code conversion table
    if len(matches)>0:
        data = matches[0]

    else:
        return ""

    patron = "(.*)'([^']+)'"
    matches = re.compile(patron,re.DOTALL).findall(data)
    cifrado = matches[0][0]
    descifrado = ""
    
    # Create the Dictionary with the conversion table
    claves = []
    claves.extend(["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"])
    claves.extend(["10","11","12","13","14","15","16","17","18","19","1a","1b","1c","1d","1e","1f","1g","1h","1i","1j","1k","1l","1m","1n","1o","1p","1q","1r","1s","1t","1u","1v","1w","1x","1y","1z"])
    claves.extend(["20","21","22","23","24","25","26","27","28","29","2a","2b","2c","2d","2e","2f","2g","2h","2i","2j","2k","2l","2m","2n","2o","2p","2q","2r","2s","2t","2u","2v","2w","2x","2y","2z"])
    claves.extend(["30","31","32","33","34","35","36","37","38","39","3a","3b","3c","3d","3e","3f","3g","3h","3i","3j","3k","3l","3m","3n","3o","3p","3q","3r","3s","3t","3u","3v","3w","3x","3y","3z"])
    palabras = matches[0][1].split("|")
    diccionario = {}

    i=0
    for palabra in palabras:
        if palabra!="":
            diccionario[claves[i]]=palabra
        else:
            diccionario[claves[i]]=claves[i]
        i=i+1

    # Substitute the words of the conversion table
    # Retrieved from http://rc98.net/multiple_replace
    def lookup(match):
        try:
            return diccionario[match.group(0)]
        except:
            return ""

    # Reverse key priority for having the longest
    claves.reverse()
    cadenapatron = '|'.join(claves)
    compiled = re.compile(cadenapatron)
    descifrado = compiled.sub(lookup, cifrado)


    return descifrado
	
def postContent(url,data,referr):
    print referr
    opener = urllib2.build_opener()
    opener.addheaders = [('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                         ('Accept-Encoding','gzip, deflate'),
                         ('Referer', referr),
                         ('Content-Type', 'application/x-www-form-urlencoded'),
                         ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0'),
                         ('Connection','keep-alive'),
                         ('Accept-Language','en-us,en;q=0.5'),
                         ('Host','www.lsb-movies.net'),
                         ('Pragma','no-cache')]
    usock=opener.open(url,data)
    response=usock.read()
    usock.close()
    return response
	
def loadVideos(url,name):
        #try:
           GA("LoadVideos",name)
           newlink=url
           xbmc.executebuiltin("XBMC.Notification(Please Wait!,Loading selected video)")
           vidtype="direct"
           if (newlink.find("dailymotion") > -1):
                match=re.compile('http://www.dailymotion.com/embed/video/(.+?)\?').findall(url)
                if(len(match) == 0):
                        match=re.compile('http://www.dailymotion.com/video/(.+?)&dk;').findall(url+"&dk;")
                if(len(match) == 0):
                        match=re.compile('http://www.dailymotion.com/swf/(.+?)\?').findall(url)
                if(len(match) == 0):
                        match=re.compile('http://www.dailymotion.com/swf/(.+?)_').findall(url)
                if(len(match) == 0):
                        match=re.compile('http://www.dailymotion.com/video/(.+?)&dk;').findall(url+"&dk;")
                print match
                link = 'http://www.dailymotion.com/video/'+str(match[0])
                vidlink=getDailyMotionUrl(str(match[0]))
           elif(newlink.find("picasaweb.google") > 0):
                vidcontent=GetContent(newlink)
                vidmatch=re.compile('"application/x-shockwave-flash"\},\{"url":"(.+?)",(.+?),(.+?),"type":"video/mpeg4"\}').findall(vidcontent)
                vidlink=vidmatch[0][0]
           elif(newlink.find("amazon") > 0):
                vidcontent=GetContent(newlink)
                vidmatch=re.compile('sArg\s*=\s*"(.+?)";').findall(vidcontent)
                sntxt=re.compile('sNum\s*=\s*"(.+?)";').findall(vidcontent)
                directcontent=GetContent("https://www.amazon.com/gp/drive/share/downloadFile.html?_=1398898498897&sharedId="+vidmatch[0]+"&download=TRUE&deviceType=ubid&deviceSerialNumber=")
                vidmatch=re.compile('{"url":"(.+?)"').findall(directcontent)
                vidlink=vidmatch[0]
           elif(newlink.find("vk.com") > 0):
                vidcontent=GetContent(newlink)
                vidhost=re.compile("var\s*video_host\s*=\s*'(.+?)';").findall(vidcontent)[0]
                viduid=re.compile("var\s*video_uid\s*=\s*'(.+?)';").findall(vidcontent)[0]
                vidvtag=re.compile("var\s*video_vtag\s*=\s*'(.+?)';").findall(vidcontent)[0]
                vidlink=vidhost+"u"+viduid+"/videos/"+vidvtag+".360.mp4"
           elif (newlink.find("uploadpluz") > -1):
                link = GetContent(newlink)
                link = ''.join(link.splitlines()).replace('\'','"')
                scriptcontent=re.compile('<div id="player_code"><span id="flvplayer">(.+?)</div>').findall(link)[0]
                packed = scriptcontent.split("</script>")[1]
                unpacked = unpackjs4(packed)
                if unpacked=="":
                        unpacked = unpackjs3(packed,tipoclaves=2)
                        
                unpacked = unpacked.replace("\\","")
                vidlink=re.compile('"file","(.+?)"').findall(unpacked)[0]
                vidlink=vidlink+"?file="+vidlink+'&start=0|Referer="http://uploadpluz.com:8080/player/player.swf"|Host="s23.uploadpluz.com:8080"|User-Agent=Mozilla%2F5.0+%28Windows+NT+6.2%3B+Win64%3B+x64%3B+rv%3A16.0.1%29+Gecko%2F20121011+Firefox%2F16.0.1|Connection="keep-alive"|Accept="text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"|Accept-Encoding="gzip, deflate"'
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
                vidlink=re.compile('"file" : "(.+?)",').findall(pcontent)[0]
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
                vidlink=re.compile('<file>(.+?)</file>').findall(vidcontent)[0]
           elif (newlink.find("180upload") > -1):
                urlnew= re.compile('http://180upload.com/embed-(.+?).html').findall(newlink)
                print urlnew
                if(len(urlnew) > 0):
                      newlink="http://180upload.com/" + urlnew[0]
                vidlink=resolve_180upload(newlink,None)
           elif(newlink.find("playlists") > 0):
                playlistid=re.compile('http://gdata.youtube.com/feeds/api/playlists/(.+?)&', re.IGNORECASE).findall(newlink)
                vidlink="plugin://plugin.video.youtube?path=/root/video&action=play_all&playlist="+playlistid[0]
           elif(newlink.find("youtube") > 0):
                vidmatch=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(newlink)
                vidlink=vidmatch[0][len(vidmatch[0])-1].replace('v/','')
                vidtype="youtube"
                #vidlink=getYoutube(vidlink)
           else:
                sources = []
                label=name
                hosted_media = urlresolver.HostedMediaFile(url=url, title=label)
                sources.append(hosted_media)
                source = urlresolver.choose_source(sources)
                print "inresolver=" + url
                if source:
                        vidlink = source.resolve()
                else:
                        vidlink =""
           playVideo(vidtype,vidlink)
        #except: pass

def getDailyMotionUrl(id):
    maxVideoQuality="720p"
    content = GetContent("http://www.dailymotion.com/embed/video/"+id)
    if content.find('"statusCode":410') > 0 or content.find('"statusCode":403') > 0:
        xbmc.executebuiltin('XBMC.Notification(Info:,'+translation(30022)+' (DailyMotion)!,5000)')
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
		
def GetContent(url):
    try:
       net = Net()
       second_response = net.http_GET(url)
       return second_response.content
    except:	
       d = xbmcgui.Dialog()
       d.ok(url,"Can't Connect to site",'Try again in a moment')
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

#-----------------------------------------------------Decode Methods------------------------------------------------------------------------------------

def decrypt(param1):
	_loc11_ = True;
	_loc12_ = False;
	_loc10_ = None;
	_loc4_ = []
	_loc5_ = []
	_loc6_ = hexToChars(param1);
	_loc7_ = 16;
	_loc8_ = [1966101078, 1516336945, 1263424345, 1379365717, 909404232, 0, 374550836L, 1278363141L, 125572444L, 1431004681L, 1669271105L, 1669271105L, -1784093795L, -644176488L, -555306812L, -1951541555L, -388835188L, -1951541555L, 680883823L, -250620937L, 803824435L, -1539000834L, 1284926834L, -952386625L, 542348429L, -782481542L, -21683127L, 1525780919L, 375913669L, -782481542L, -93462979L, 724670791L, -712721138L, -1888146247L, -1726820228L, 1213110022L, -1790971499L, -1106351918L, 1804260828L, -452986523L, 2112694553L, 899923487L, 1437203323L, -341339223L, -2144516491L, 1691533072L, 423597577L, 748431382L, 316155343L, -109070746L, 2035478547L, 494948099L]

	_loc9_ = (len(_loc6_) / _loc7_)-1;

	while	_loc9_ > 0:
		_loc5_ = decryption(_loc6_[_loc9_ * _loc7_:(_loc9_ + 1) * _loc7_],_loc8_);
		_loc4_=_loc5_+(_loc4_)
		_loc9_-=1;

	_loc44= decryption(_loc6_[0:int(_loc7_)],_loc8_)

	_loc4_ =_loc44+_loc4_;

	_loc4_= charsToStr(_loc4_);
	
	_loop_=0;
	_patternArray=[];
	_loop_=0
	return _loc4_.split('\0')[0];   


def MyInt(x):
	x = 0xffffffff & x
	if x > 0x7fffffff :
		return - ( ~(x - 1) & 0xffffffff )
	else : return x   
	

def hexToChars(param1):

	_loc4_ = False;
	_loc5_ = True;
	_loc2_ = []
	_loc3_ =0;
	if param1[0:1] == '0x':
		_loc3_ =2;
	
	while _loc3_ < len(param1):
		_loc2_.append(int(param1[_loc3_:_loc3_+2],16));
		_loc3_ = _loc3_ + 2;

	return _loc2_;
	
def strToChars(param1):
	_loc4_ = True;
	_loc5_ = False;
	_loc2_ = []
	_loc3_ = 0;
	while(_loc3_ < len(param1)):
		_loc2_.append(ord(param1[_loc3_]));
		_loc3_+=1;
	
	return _loc2_;

def charsToStr(param1):
	_loc4_ = False;
	_loc5_ = True;
	_loc2_ = ''
	_loc3_ = 0;
	while(_loc3_ < len(param1)):
		_loc2_ = _loc2_ + chr(param1[_loc3_]);
		_loc3_+=1;
	return _loc2_;
	
def packBytes(param1):
	_loc4_ = False;
	_loc5_ = True;
	_loc2_ = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
	_loc3_ = 0;
	while(_loc3_ < len(param1)):
		_loc2_[0][_loc3_ / 4] = param1[_loc3_];
		_loc2_[1][_loc3_ / 4] = param1[_loc3_ + 1];
		_loc2_[2][_loc3_ / 4] = param1[_loc3_ + 2];
		_loc2_[3][_loc3_ / 4] = param1[_loc3_ + 3];
		_loc3_ = _loc3_ + 4;
	return _loc2_;

  
def unpackBytes(param1):
	_loc4_= False;
	_loc5_ = True;
	_loc2_ = []
	_loc3_ = 0;
	while(_loc3_ < len(param1[0])):
		_loc2_.append( param1[0][_loc3_]);
		_loc2_.append(param1[1][_loc3_]);
		_loc2_.append(param1[2][_loc3_]);
		_loc2_.append(param1[3][_loc3_]);
		_loc3_+=1;
	return _loc2_;
  
  
def InverseRound(param1, param2):
	_loc3_ = False;
	_loc4_ = True;
	addRoundKey(param1,param2);
	mixColumn(param1,'decrypt');
	shiftRow(param1,'decrypt');
	byteSub(param1,'decrypt');

def FinalRound(param1, param2):
	_loc3_ = False;
	_loc4_ = True;
	byteSub(param1,'encrypt');
	shiftRow(param1,'encrypt');
	addRoundKey(param1,param2);
  
  
def InverseFinalRound(param1, param2):
	_loc3_ = False;
	_loc4_ = True;
	addRoundKey(param1,param2);
	shiftRow(param1,'decrypt');
	byteSub(param1,'decrypt');

  
def addRoundKey(param1, param2):
	_loc4_ = True;
	_loc5_ = False;
	_loc3_ = 0;
	while(_loc3_ < Nb):
		param1[0][_loc3_] = MyInt(param1[0][_loc3_] ^ (param2[_loc3_] & 255));
		param1[1][_loc3_] = param1[1][_loc3_] ^ param2[_loc3_] >> 8 & 255;
		param1[2][_loc3_] = param1[2][_loc3_] ^ param2[_loc3_] >> 16 & 255;
		param1[3][_loc3_] = param1[3][_loc3_] ^ param2[_loc3_] >> 24 & 255;
		_loc3_+=1;
		   
  
def shiftRow(param1, param2):
	_loc4_ = True;
	_loc5_ = False;
	_loc3_ = 1;
	while(_loc3_ < 4):
		if(param2 == 'encrypt'):
			param1[_loc3_] = cyclicShiftLeft(param1[_loc3_],shiftOffsets[Nb][_loc3_]);
		else:
			param1[_loc3_] = cyclicShiftLeft(param1[_loc3_],Nb - shiftOffsets[Nb][_loc3_]);
		_loc3_+=1;
		
def cyclicShiftLeft(param1, param2):
	_loc4_ = False;
	_loc5_ = True;
	_loc3_ = param1[0:param2];
	param1=param1[param2:];
	param1.extend(_loc3_);
	return param1;
  
def decryption(param1, param2):
	_loc4_ = True;
	_loc5_ = False;
	_loc4_ = False;
	_loc5_ = True;
	_loc2_ = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

	_loc3_ = 0;

	while(_loc3_ < len(param1)):
		_loc2_[0][_loc3_ / 4] = param1[_loc3_];
		_loc2_[1][_loc3_ / 4] = param1[_loc3_ + 1];
		_loc2_[2][_loc3_ / 4] = param1[_loc3_ + 2];
		_loc2_[3][_loc3_ / 4] = param1[_loc3_ + 3];
		_loc3_ = _loc3_ + 4;
	param1=_loc2_;
	InverseFinalRound(param1,param2[Nb * Nr:]);# nb*nr=42

	_loc3_ = Nr-1;
	while(_loc3_ > 0):
		InverseRound(param1,param2[(Nb * _loc3_):Nb * (_loc3_ + 1)]);
		_loc3_-=1;

	addRoundKey(param1,param2);
	_loc4_= False;
	_loc5_ = True;
	_loc2_ = []
	_loc3_ = 0;

	while(_loc3_ < len(param1[0])):
		_loc2_.append( param1[0][_loc3_]);
		_loc2_.append(param1[1][_loc3_]);
		_loc2_.append(param1[2][_loc3_]);
		_loc2_.append(param1[3][_loc3_]);
		_loc3_+=1;
	reVal= _loc2_;
	return reVal;
  
def byteSub(param1, param2):
	_loc6_ = False;
	_loc7_ = True;
	_loc3_ = 0;
	_loc5_ = 0;
	if(param2 == 'encrypt'):
		_loc3_ = SBox;
	else:
		_loc3_ = [82,9,106,213,48,54,165,56,191,64,163,158,129,243,215,251,124,227,57,130,155,47,255,135,52,142,67,68,196,222,233,203,84,123,148,50,166,194,35,61,238,76,149,11,66,250,195,78,8,46,161,102,40,217,36,178,118,91,162,73,109,139,209,37,114,248,246,100,134,104,152,22,212,164,92,204,93,101,182,146,108,112,72,80,253,237,185,218,94,21,70,87,167,141,157,132,144,216,171,0,140,188,211,10,247,228,88,5,184,179,69,6,208,44,30,143,202,63,15,2,193,175,189,3,1,19,138,107,58,145,17,65,79,103,220,234,151,242,207,206,240,180,230,115,150,172,116,34,231,173,53,133,226,249,55,232,28,117,223,110,71,241,26,113,29,41,197,137,111,183,98,14,170,24,190,27,252,86,62,75,198,210,121,32,154,219,192,254,120,205,90,244,31,221,168,51,136,7,199,49,177,18,16,89,39,128,236,95,96,81,127,169,25,181,74,13,45,229,122,159,147,201,156,239,160,224,59,77,174,42,245,176,200,235,187,60,131,83,153,97,23,43,4,126,186,119,214,38,225,105,20,99,85,33,12,125];

	_loc4_ = 0;
	
	while(_loc4_ < 4):
		_loc5_ = 0;
		while(_loc5_ < Nb):
			param1[_loc4_][_loc5_] = _loc3_[param1[_loc4_][_loc5_]];
			_loc5_+=1;
		_loc4_+=1;
	 




def mixColumn(param1, param2):
	_loc6_ = False;
	_loc7_ = True;
	_loc4_ = 0;
	_loc3_ = [0,0,0,0];
	_loc5_ = 0;
	while(_loc5_ < Nb):
		_loc4_ = 0;
		while(_loc4_ < 4):

			if(param2 == "encrypt"):
				_loc3_[_loc4_] = mult_GF256(param1[_loc4_][_loc5_],2) ^ mult_GF256(param1[(_loc4_ + 1) % 4][_loc5_],3) ^ param1[(_loc4_ + 2) % 4][_loc5_] ^ param1[(_loc4_ + 3) % 4][_loc5_];
			else:					
				_loc3_[_loc4_] = mult_GF256(param1[_loc4_][_loc5_],14) ^ mult_GF256(param1[(_loc4_ + 1) % 4][_loc5_],11) ^ mult_GF256(param1[(_loc4_ + 2) % 4][_loc5_],13) ^ mult_GF256(param1[(_loc4_ + 3) % 4][_loc5_],9);
			_loc4_+=1;
			
		_loc4_ = 0;
		while(_loc4_ < 4):
			param1[_loc4_][_loc5_] = _loc3_[_loc4_];
			_loc4_+=1;
		
		_loc5_+=1;
	 
def xtime(param1):
	_loc2_ = False;
	_loc3_ = True;
	param1 = param1 << 1;
	if param1 & 256:
		return param1 ^ 283
	else:
		return param1;
	   
	   
def mult_GF256(param1, param2):
	_loc5_ = True;
	_loc6_ = False;
	_loc3_ = 0;
	_loc4_ = 1;

	
	while(_loc4_ < 256):
		if(param1 & _loc4_):
			_loc3_ = _loc3_ ^ param2;
		_loc4_ = _loc4_ * 2;
		param2 = xtime(param2);

	return _loc3_;
  

def hexToChars(param1):
	
 		_loc4_ = False;
		_loc5_ = True;
		_loc2_ = []
		_loc3_ =0;
		if param1[0:1] == '0x':
			_loc3_ =2;
		
		while _loc3_ < len(param1):
			_loc2_.append(int(param1[_loc3_:_loc3_+2],16));
			_loc3_ = _loc3_ + 2;

		return _loc2_;    

def arrNametoString(param1):
	_loc4_ = True;
	_loc5_ = False;
	_loc2_ = "";
	param1.reverse();
	_loc3_ = 0;
	while(_loc3_ < len(param1)):
		_loc2_ = _loc2_ + chr(param1[_loc3_]);
		_loc3_+=1;
	return _loc2_;

#-------------------------------------------------------------------------------------------------------------------------------------------------------
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
        HOME()
elif mode==2:
        GA("INDEX",name)
        INDEX(url)
elif mode==3:
       loadVideos(url,name)
elif mode==4:
       GetVideoLinks(url)
elif mode==5:
       GA("Episodes",name)
       (url,itemno)=url.split("|")
       Episodes(url,name,itemno)
elif mode==6:
       INDEX2(url)
elif mode==7:
       GetLatest(strdomain)
elif mode==8:
       SEARCH()
elif mode==9:
       SearchResults(url)
elif mode==10:
       ListHost(url)
xbmcplugin.endOfDirectory(int(sysarg))
