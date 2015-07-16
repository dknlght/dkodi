import httplib
import urllib,urllib2,re,sys
import cookielib,os,string,cookielib,StringIO,gzip
import os,time,base64,logging
from t0mm0.common.net import Net
import urlresolver
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui
import base64
import xbmc
import json
import datetime
import cgi
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
from BeautifulSoup import SoupStrainer


ADDON = xbmcaddon.Addon(id='plugin.video.comotin')
if ADDON.getSetting('ga_visitor')=='':
    from random import randint
    ADDON.setSetting('ga_visitor',str(randint(0, 0x7fffffff)))
    
PATH = "comotin"  #<---- PLUGIN NAME MINUS THE "plugin.video"          
UATRACK="UA-40129315-1" #<---- GOOGLE ANALYTICS UA NUMBER   
VERSION = "1.0.6" #<---- PLUGIN VERSION
homeLink="http://comotin.com/"
home = ADDON.getAddonInfo('path')
filename = xbmc.translatePath(os.path.join(home, 'resources', 'streams.xml'))
usehd = ADDON.getSetting('use-hd') == 'true'
def __init__(self): 
    self.playlist=sys.modules["__main__"].playlist
#def HOME():
#        addDir('Search','http://phim47.com/',4,'http://yeuphim.net/images/logo.png')
#        addDir('HQ Videos','http://phim47.com/list-hd.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
#        addDir('Movies','http://phim47.com/movie-list/phim-le.html',2,'http://phim47.com/skin/movie/style/images/logo.png')
#        addDir('Series','http://phim47.com/movie-list/phim-bo.html ',2,'http://phim47.com/skin/movie/style/images/logo.png')
#        addDir('Videos By Region','http://phim47.com/',8,'http://phim47.com/skin/movie/style/images/logo.png')
#        addDir('Videos By Category ','http://phim47.com/',9,'http://phim47.com/skin/movie/style/images/logo.png')
def RemoveHTML(inputstring):
    TAG_RE = re.compile(r'<[^>]+>')
    return TAG_RE.sub('', inputstring)
	
def HOME():
        GetMenu("http://www.comotin.com/")
		
def GetMenu(url):
        link = GetContent(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        menuhead = SoupStrainer('nav', {"id" : "navigation"})
        soup = BeautifulStoneSoup(newlink, parseOnlyThese=menuhead,convertEntities=BeautifulSoup.XML_ENTITIES)
        for item in soup.findAll('li'):
			mode=8
			if(item.parent.name=="div"):
				mode=2
			if(item.a.has_key("href")):
				link = item.a['href'].encode('utf-8', 'ignore')
				if(item["class"].find("menu-item-has-children")==-1):
					vname="---"+str(item.a.contents[0]).strip()
				else:
					vname=str(item.a.contents[0]).strip()
				if(vname.strip().find("Home") == -1 and vname.strip().find("Privacy Policy") == -1 and vname.strip().find("Advertising") == -1 and vname.strip().find("TV ONLINE") == -1):
					addDir(vname,link,mode,"")
				if(vname.strip().find("TV ONLINE") > -1):
					addDir(vname,link,9,"")
def SearchXml(SearchText):
    if os.path.isfile(filename)==False:
        BuildXMl()
    f = open(filename, "r")
    text = f.read()
    if SearchText=='-1':
        match=re.compile('<movie name="[^A-Za-z](.+?)" url="(.+?)" year="(.+?)"/>', re.IGNORECASE).findall(text)	
        SearchText=""
    else:
        match=re.compile('<movie name="' + SearchText + '(.+?)" url="(.+?)" year="(.+?)"/>', re.IGNORECASE).findall(text)
    for i in range(len(match)):
        (mName,mNumber,vyear)=match[i]
        addDir(SearchText+mName,mNumber,6,"")
		
def ParseXml(tagname):
        f = open(filename, "r")
        text = f.read()
        xmlcontent=xml.dom.minidom.parseString(text)
        items=xmlcontent.getElementsByTagName('channel')
        print "calling " + tagname
        for channelitem in items:
                if(len(channelitem.getElementsByTagName('item'))>=1 and channelitem.getElementsByTagName('name')[0].childNodes[0].data==tagname):
                        chitems = channelitem.getElementsByTagName('item')
                        for itemXML in chitems:
                                vname=itemXML.getElementsByTagName('title')[0].childNodes[0].data.strip()
                                vurl=itemXML.getElementsByTagName('link')[0].childNodes[0].data.strip()
                                vimg=itemXML.getElementsByTagName('thumbnail')[0].childNodes[0].data.strip()
                                addLink(vname,vurl,6,vimg,"")
	

def Episode(url):
        link = GetContent(url)
        link = ''.join(link.splitlines())
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        #menuhead = SoupStrainer('article', {"id" : "article"})
        soup = BeautifulSoup(newlink)
        episodelist=soup.findAll('ul',{"class":"partlar"})
        if(len(episodelist)>0):
			for epiitem in episodelist[0].findAll('a'):
				vname =epiitem.contents[0]
				vimg=""
				if(epiitem.has_key("href")):
					vlink =epiitem["href"]
					addLinkSub(vname.encode('utf-8', 'ignore'),vlink,3,vimg,"")
				else:
					addLinkSub(vname.encode('utf-8', 'ignore'),url,3,vimg,"")
def LoadLive(url):
			xbmc.executebuiltin("XBMC.Notification(PLease Wait!, Loading video link into XBMC Media Player,5000)")
			link = GetContent(url)
			link = ''.join(link.splitlines())
			try:
				link =link.encode("UTF-8")
			except: pass
			newlink = ''.join(link.splitlines()).replace('\t','')
			#menuhead = SoupStrainer('article', {"id" : "article"})
			soup = BeautifulSoup(newlink)
			episodelist=soup.findAll('iframe')
			livelink = GetContent(episodelist[0]["src"])
			playerlist=json.loads(re.compile('setup\((.+?)\);').findall(livelink)[0])
			playVideo(playerlist["file"],"")
 
def LiveIndex(url):
        link = GetContent(url)
        link = ''.join(link.splitlines())
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        soup = BeautifulSoup(newlink)
        for imgitem in soup.findAll('figure'):
			vimg=imgitem.img["src"]
			vurl=imgitem.previousSibling.a["href"]
			vname=imgitem.img["alt"]
			addLinkSub(vname.encode('utf-8', 'ignore'),vurl,10,vimg,"")
			
def INDEX(url,type):
        link = GetContent(url)
        link = ''.join(link.splitlines())
        try:
            link =link.encode("UTF-8")
        except: pass
        newlink = ''.join(link.splitlines()).replace('\t','')
        #menuhead = SoupStrainer('article', {"id" : "article"})
        soup = BeautifulSoup(newlink)
        for imgitem in soup.findAll('figure'):
			vname =imgitem.parent["title"]
			vimg=imgitem.img["src"]
			vlink =imgitem.parent["href"]
			if(type=="tv"):
				addDir(vname.encode('utf-8', 'ignore'),vlink,7,vimg)
			else:
				addLinkSub(vname.encode('utf-8', 'ignore'),vlink,3,vimg,"")
        navigation = soup.findAll('div', {"class" : "paGination"})
        if(len(navigation)>0):
			for item in navigation[0].findAll('a'):
				addDir("page " +(str(item.contents[0])).replace("&laquo;","<<").replace("&raquo;",">>"),item["href"],2,"")



#----------------------------------------decryption code--------------------------------------------------------
Rcon = [1,2,4,8,16,32,64,128,27,54,108,216,171,77,154,47,94,188,99,198,151,53,106,212,179,125,250,239,197,145];
SBox = [99,124,119,123,242,107,111,197,48,1,103,43,254,215,171,118,202,130,201,125,250,89,71,240,173,212,162,175,156,164,114,192,183,253,147,38,54,63,247,204,52,165,229,241,113,216,49,21,4,199,35,195,24,150,5,154,7,18,128,226,235,39,178,117,9,131,44,26,27,110,90,160,82,59,214,179,41,227,47,132,83,209,0,237,32,252,177,91,106,203,190,57,74,76,88,207,208,239,170,251,67,77,51,133,69,249,2,127,80,60,159,168,81,163,64,143,146,157,56,245,188,182,218,33,16,255,243,210,205,12,19,236,95,151,68,23,196,167,126,61,100,93,25,115,96,129,79,220,34,42,144,136,70,238,184,20,222,94,11,219,224,50,58,10,73,6,36,92,194,211,172,98,145,149,228,121,231,200,55,109,141,213,78,169,108,86,244,234,101,122,174,8,186,120,37,46,28,166,180,198,232,221,116,31,75,189,139,138,112,62,181,102,72,3,246,14,97,53,87,185,134,193,29,158,225,248,152,17,105,217,142,148,155,30,135,233,206,85,40,223,140,161,137,13,191,230,66,104,65,153,45,15,176,84,187,22];
shiftOffsets = [0,0,0,0,[0,1,2,3],0,[0,1,2,3],0,[0,1,3,4]];
Nb = 4;
Nk = 6;
Nr = 12;

def decrypt(param1):
	_loc11_ = True;
	_loc12_ = False;
	_loc10_ = None;
	_loc4_ = []
	_loc5_ = []
	_loc6_ = hexToChars(param1);
	_loc7_ = 16;
	_loc8_ = [1849252152, 1951094370, 1162557538, 2000770928, 1115308622, 0, 224016986L, 2031184952L, 1012552794L, 1260061482L, 157368676L, 157368676L, 1314641371L, 927644131L, 185658809L, 1074523795L, 1231728631L, 1074523795L, -1840054537L, -1525135596L, -1375163731L, -301775810L, -1486230583L, -413006502L, 751195284L, -1981934720L, 668383533L, -908722925L, 1857820378L, -1981934720L, -513717767L, 1757371001L, 1332339540L, -2034491833L, -402650979L, 1641945885L, 1166955638L, 758189583L, 1649995099L, -454757604L, 216333185L, 1832575132L, -1682778921L, -1232872744L, -723830909L, 809485471L, 1021001502L, 1373757314L, -2006766391L, 1054930449L, -365182574L, -637270771L]

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

#---------------------------------------------------------------------------------------------------------------

	   
def GetContent(url):
    try:
       net = Net()
       try:
            second_response = net.http_GET(url)
       except:
            second_response = net.http_GET(url.encode("utf-8"))
       return second_response.content
    except:
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
				
def playVideo(videoId,suburl):
        print videoId
        vidinfo = videoId.split("_")[0]
        win = xbmcgui.Window(10000)
        win.setProperty('1ch.playing.title', vidinfo)
        win.setProperty('1ch.playing.season', str(3))
        win.setProperty('1ch.playing.episode', str(4))
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(videoId)
        xbmcPlayer.setSubtitles(suburl) 
		

def loadVideos(url,name,suburl):
    #try:
        GA("LoadVideo","NA")
        xbmc.executebuiltin("XBMC.Notification(PLease Wait!, Loading video link into XBMC Media Player,5000)")
        if(url.find("sembunyi*") > -1):
              newlink=decrypt(url.replace("sembunyi*",""))
        elif(url.find("//")==-1):
			newlink=urllib.unquote_plus(url.replace("@","%"))
			newlink=re.compile('<iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(newlink)[0]
        else:
			urlcontent=GetContent(url)
			newlink=re.compile('proxy.link=(.+?)&').findall(urlcontent)[0]
        print newlink
        if(newlink.find("cyworld.vn") > 0):
            vidcontent=GetContent(newlink)
            vidmatch=re.compile('<meta property="og:video" content="(.+?)" />').findall(vidcontent)
            vidlink=vidmatch[0]
            playVideo(vidlink,suburl)
        elif(newlink.find("plus.google") > 0):
				print "in plus"
				vidcontent=postContent("http://www.ganoolmovie.com/wp-content/plugins/gkplugins-for-wordpres/player/plugins/plugins_player.php","iagent=Mozilla%2F5%2E0%20%28Windows%3B%20U%3B%20Windows%20NT%206%2E1%3B%20en%2DUS%3B%20rv%3A1%2E9%2E2%2E8%29%20Gecko%2F20100722%20Firefox%2F3%2E6%2E8&ihttpheader=true&url="+urllib.quote_plus(newlink)+"&isslverify=true",homeLink)
				newplusurl =re.compile('<meta property="og:url" [^>]*content=["\']?([^>^"^\']+)["\']?[^>]*>').findall(vidcontent)[0]
				vidcontent=postContent("http://www.ganoolmovie.com/wp-content/plugins/gkplugins-for-wordpres/player/plugins/plugins_player.php","iagent=Mozilla%2F5%2E0%20%28Windows%3B%20U%3B%20Windows%20NT%206%2E1%3B%20en%2DUS%3B%20rv%3A1%2E9%2E2%2E8%29%20Gecko%2F20100722%20Firefox%2F3%2E6%2E8&ihttpheader=true&url="+urllib.quote_plus(newplusurl)+"&isslverify=true",homeLink)
				print vidcontent
        elif(newlink.find("picasaweb.google") > 0):
                 print "in picasa"
                 vidcontent=postContent("http://www.cdn.comotin.com/www/plugins/plugins_player.php","iagent=Mozilla%2F5%2E0%20%28Windows%3B%20U%3B%20Windows%20NT%206%2E1%3B%20en%2DUS%3B%20rv%3A1%2E9%2E2%2E8%29%20Gecko%2F20100722%20Firefox%2F3%2E6%2E8&ihttpheader=true&url="+urllib.quote_plus(newlink)+"&isslverify=true",homeLink)
				 
                 vidid=vidlink=re.compile('picasaweb.google.com/(.+?)/').findall(newlink+"&")
                 if(len(vidid)>0 and vidcontent.find("<H1>Moved Temporarily</H1>") == -1):
					vidmatch=re.compile('feedPreload:(.+?)}}},').findall(vidcontent)[0]+"}}"
					data = json.loads(vidmatch)
					vidlink=""
					for currententry in data["feed"]["entry"]:
								for currentmedia in currententry["media"]["content"]:
									if(currentmedia["type"]=="video/mpeg4"):
										vidlink=currentmedia["url"]
										break
								if(vidlink==""):
									vidlink=currententry["media"]["content"][0]["url"]
									break
                 else:
						if(vidcontent.find("<H1>Moved Temporarily</H1>") > -1):
							newcontent =re.compile('<a [^>]*href=["\']?([^>^"^\']+)["\']?[^>]*>').findall(vidcontent.lower())[0]
							vidcontent=GetContent(newcontent)
						vidmatch=re.compile('"application/x-shockwave-flash"\},\{"url":"(.+?)",(.+?),(.+?),"type":"video/mpeg4"\}').findall(vidcontent)
						hdmatch=re.compile('"application/x-shockwave-flash"\},\{"url":"(.+?)",(.+?),(.+?)').findall(vidmatch[-1][2])
						if(len(hdmatch) > 0):
							vidmatch=hdmatch
						vidlink=vidmatch[-1][0]
                 playVideo(vidlink,suburl)
        elif (newlink.find("docs.google.com") > -1):  
                vidcontent = GetContent(newlink)
                html = vidcontent.decode('utf8')
                stream_map = re.compile('fmt_stream_map","(.+?)"').findall(html)[0].replace("\/", "/")
                formatArray = stream_map.split(',')
                for formatContent in formatArray:
                     formatContentInfo = formatContent.split('|')
                     qual = formatContentInfo[0]
                     url = (formatContentInfo[1]).decode('unicode-escape')
                     playVideo(url,suburl)
        if (newlink.find("dailymotion") > -1):
                match=re.compile('/(.+?)-').findall(newlink)
                dailyid=""
                
                if(len(match)>0):
                        dailyid=match[0].split("/")[-1]
                if(len(match) == 0):
                        match=re.compile('http://www.dailymotion.com/video/(.+?)&dk;').findall(newlink+"&dk;")
                        dailyid=match[0]
                if(len(match) == 0):
                        match=re.compile('http://www.dailymotion.com/swf/(.+?)\?').findall(newlink)
                        dailyid=match[0]
                if (newlink.find("http://www.dailymotion.com/swf/") > -1):
                        link=newlink
                else:
                        link = 'http://www.dailymotion.com/video/'+str(dailyid)
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
                vidlink=urllib2.unquote(dm_low[0]).decode("utf8")
                playVideo(vidlink,suburl)
        elif(newlink.find("youtube") > 0):
            vidmatch=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(newlink)
            vidlink=vidmatch[0][len(vidmatch[0])-1].replace('v/','')
            playVideo(getYoutube(vidlink),suburl)
        else:
            sources = []
            label=name
            hosted_media = urlresolver.HostedMediaFile(url=newlink, title=label)
            sources.append(hosted_media)
            source = urlresolver.choose_source(sources)
            print "urlrsolving" + newlink
            if source:
                vidlink = source.resolve()
            else:
                vidlink =""
            playVideo(vidlink,suburl)
    #except:
       #d = xbmcgui.Dialog()
       #d.ok(url,"Can't play video",'Try another link')
   
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

def addLink(name,url,mode,iconimage,mirrorname):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&mirrorname="+urllib.quote_plus(mirrorname)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        contextMenuItems = []
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok
		
def addLinkSub(name,url,mode,iconimage,suburl):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&suburl="+urllib.quote_plus(suburl)
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
        liz=xbmcgui.ListItem('Next >', iconImage="http://yeuphim.net/images/logo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": 'Next >' } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
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
try:
        subtitleurl=urllib.unquote_plus(params["suburl"])
except:
        pass
		
sysarg=str(sys.argv[1])
print "mode is:" + str(mode)
if mode==None or url==None or len(url)<1:

        HOME()
elif mode==2:
        GA("TV INDEX",name)
        INDEX(url,"tv")
elif mode==3:
        loadVideos(url,mirrorname,subtitleurl)
elif mode==5:
        ParseXml(name) 
elif mode==6:
        GA("PlayVideo",name)
        playVideo(url,"")
elif mode==7:
		Episode(url)
elif mode==8:
        GA("MOVIE INDEX",name)
        INDEX(url,"movie")
elif mode==9:
        GA("LIVE INDEX",name)
        LiveIndex(url)
elif mode==10:
        LoadLive(url)
xbmcplugin.endOfDirectory(int(sysarg))
