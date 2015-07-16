import os,sys,string,StringIO,logging,random,array,time,datetime,re
import xbmc,urllib,urllib2,xbmcaddon,xbmcplugin,xbmcgui,xbmcvfs
import requests
import cookielib
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
from BeautifulSoup import SoupStrainer
try: import simplejson as json
except ImportError: import json
from urlparse import urlparse

addon_id = "plugin.video.sitetosite"
ADDON = __settings__ = xbmcaddon.Addon(id=addon_id)
datapath = xbmc.translatePath(ADDON.getAddonInfo('profile'))  

cookie_path = os.path.join(datapath, 'cookies')
cookiefile = os.path.join(cookie_path, "cookiejar.lwp")
cj = None
strUsername = ADDON.getSetting('Username')
strpwd = ADDON.getSetting('Password')#.replace("@","%40")
AxelPath= ADDON.getSetting('axel-folder')
axelconnection = ADDON.getSetting('axel-connections')
axelkeepfile = ADDON.getSetting('axel-keepfile')
axelusename= ADDON.getSetting('axel-usename')
url_login = "https://accounts.google.com/ServiceLogin"
url_auth = "https://accounts.google.com/ServiceLoginAuth"
ballloonauth="http://ballloon.com/auth/google"
service_list = ["googleDrive", "box", "oneDrive", "dropbox"]
defaultservice=service_list[int(ADDON.getSetting('cloudservice'))]

if not os.path.exists(datapath):
        os.makedirs(datapath)
if not os.path.exists(cookie_path):
        os.makedirs(cookie_path)
IpSpecifichost=['daclips',
'happystreams',
'filehoot',
'cloudyvideos',
'realvid',
'letwatch',
'2gb-hostin..',
'playhd',
'divxstage',
'donevideo',
'ecostream',
'entroupload',
'exashare',
'facebook',
'filebox',
'filenuke',
'flashx',
'gorillavid',
'hostingbulk',
'hostingcup',
'hugefiles',
'jumbofiles',
'lemuploads',
'limevideo',
'megarelease',
'megavids',
'mightyupload',
'mooshare_biz',
'movdivx',
'movpod',
'movreel',
'movshare',
'movzap',
'mp4stream',
'mp4upload',
'mrfile',
'muchshare',
'nolimitvideo',
'nosvideo',
'novamov',
'nowvideo',
'ovfile',
'play44_net',
'played',
'playwire',
'premiumize_me',
'primeshare',
'promptfile',
'purevid',
'putlocker',
'rapidvideo',
'rpnet',
'seeon',
'sharedsx',
'sharefiles',
'sharerepo',
'sharesix',
'sharevid',
'skyload',
'slickvid',
'sockshare',
'stagevu',
'stream2k',
'streamcloud',
'teramixer',
'thefile',
'thevideo',
'trollvid',
'tubeplus',
'tunepk',
'ufliq',
'uploadcrazynet',
'veeHD',
#'vidbull',
'vidcrazynet',
'videoboxone',
'videomega',
'videoraj',
'videotanker',
'videovalley',
'videoweed',
'videozed',
'videozer',
'vidhog',
'vidpe',
'vidplay',
'vidspot',
'vidstream',
'vidto',
'vidup',
'vidxden',
'vidzi',
'vidzur',
'vk',
'vodlocker',
'vureel',
'watchfreeinhd',
'watchfreei..',
'xvidstage',
'yourupload',
'youwatch',
'zalaa',
'zooupload',
'zshare',
'bestreams',
'vidx',
'streamin',
'vidpaid',
'uploadnetwork',
'divxpress',
'videopremium',
'faststream',
'v-vids',
'topvideo',
'gamovideo',
'bonanzashare',
'clicktoview',
'flashx.tv',
'speedvid',
'vreer',
'allmyvideos',
'cyberlocker',
'veervid',
'nowdownloa',
'videoslash',
'sharebees',
'23',
'speedyshare',
'putlocker']

class SessionGoogle:
    def __init__(self, url_login, url_auth, login, pwd):
		requests.packages.urllib3.disable_warnings()
		self.ses = requests.session()
		self.email=login
		self.passwd=pwd
		if os.path.exists(cookiefile):
			cj = cookielib.LWPCookieJar()
			cj.load(cookiefile, ignore_discard=True)
			self.ses.cookies=cj
		else:
			self.Relogin()

    def get(self, URL):
        return self.ses.get(URL).text
		
    def post(self, URL,postdata):
		return self.ses.post(URL, data=postdata)
    def Relogin(self):
			print "logging in again"
			self.ses.cookies=cookielib.LWPCookieJar()
			login_html = self.ses.get(url_login)
			soup = BeautifulSoup(login_html.content).findAll('form')
			soup_login = soup[0].findAll('input')
			dico = {}
			for u in soup_login:
				if u.has_key('value'):
					dico[u['name']] = u['value']
			dico['Email'] = self.email
			dico['Passwd'] = self.passwd
			self.ses.post(url_auth, data=dico)
			resp=self.ses.get(ballloonauth).text
			self.ses.cookies.save(cookiefile, ignore_discard=True)
		
def BackuptoBallloon(html,destination):
	fileparam=re.compile('var buttton\s*=\s*(.+?);', re.IGNORECASE).findall(html)
	folderparam=re.compile('var lastUseFolder\s*=\s*(.+?);', re.IGNORECASE).findall(html)
	filedic=json.loads(fileparam[0])
	try:
		folderdic=json.loads(folderparam[0])
	except: 
		folderdic={}
	postparam = {}
	if(len(folderdic) <2):
		session = SessionGoogle(url_login, url_auth, strUsername, strpwd)
		folderinfo=session.get("http://ballloon.com/api/"+destination+"?method=getFolders&path=%2F&folderId=")
		folderdic=json.loads(folderinfo)
		if(folderdic[0].has_key('name')):
			postparam["cusFolderPath"]="/%s/" % folderdic[0]["name"]
		postparam["cusFolderId"]=folderdic[0]["id"]
		postparam["cusIds"]="#**ballloon-sep**#%s" % folderdic[0]["id"]
	else:
		postparam["cusFolderPath"]=folderdic["path"]
		postparam["cusFolderId"]=folderdic["ids"].replace("#**ballloon-sep**#","")
		postparam["cusIds"]=folderdic["ids"]
	postparam["pageUrl"]=filedic["pageUrl"]
	postparam["url"]=filedic["url"]
	postparam["destination"]=destination
	postparam["cusName"]=filedic["fileName"]

	postparam["butttonId"]=filedic["id"]
	postparam["type"]=filedic["mimeType"]
	postparam["flag"]="a"
	return postparam

#oneDrive
#googleDrive
def GetDecision():
        dialog = xbmcgui.Dialog()
        choices = ["Cancel backup","Try anyway","Backup offline"]
        index = dialog.select('File might not save remotely, what do you want to do?', choices)
        return index
		
def startStreambackup(destination="googleDrive"):
	if(destination==None):
		destination=defaultservice
	session = SessionGoogle(url_login, url_auth, strUsername, strpwd)
	vName=''; 
	vPath=''; 
	p=xbmc.Player();
	if(p.isPlayingVideo()==True or p.isPlaying()==True):
		vurl=p.getPlayingFile()
		xbmc.executebuiltin("XBMC.Notification(Backing up, Saving selected video to the cloud,5000)")
		fileInfoHtml=session.get("http://ballloon.com/plugins/download?key=direct&url="+urllib.quote_plus(vurl)+"&cloud="+destination)
		postparam=BackuptoBallloon(fileInfoHtml.encode('utf-8', 'ignore'),destination)
		parsed_uri = urlparse(postparam["url"])
		if(str(parsed_uri.netloc).split('.')[0].lower() in IpSpecifichost):
			userchoice=GetDecision()
			if(userchoice==1):
				session.post("http://ballloon.com/api/ballloons/new",postparam)
			elif(userchoice==2):
				DoDownloader(postparam["url"],postparam["cusName"],AxelPath,False)
		else:
			session.post("http://ballloon.com/api/ballloons/new",postparam)

def Home():
	addDir('Backup Queue','test',"viewQueue",'')

def ViewQueue():
	session = SessionGoogle(url_login, url_auth, strUsername, strpwd)
	html=session.get("http://ballloon.com/categories/departures")
	soup = BeautifulSoup(html).findAll('div', {"id" : "history-list"})
	for item in soup[0].findAll('div', {"class":re.compile('list-row status-*')}):
		vfile=item.findAll('div', {"class" : "cell-title arrived-title"})
		if(len(vfile)>0 ):
			vfile=vfile[0].contents[0]
			vstatus=item.findAll('div', {"class" : "cell-status"})[0].contents[0]
			vcloudservice=item.findAll('div', {"class" : "cell-destination"})[0].a.contents[0]
			varrivetime=item.findAll('div', {"class" : "cell-time time-date"})[0].contents[0]
		displaytext=("[COLOR green]Filename:[/COLOR]%s     [COLOR green]Status[/COLOR]:%s     [COLOR green]Backup Time[/COLOR]:%s     [COLOR green]Cloud Service[/COLOR]:%s" %(vfile,vstatus,varrivetime,vcloudservice))
		if(displaytext.find("{{fileName}}") == -1 and displaytext.find("[COLOR green]Filename:[/COLOR][]") == -1):
			addLink(displaytext,"","delete","")
		
def startDownload():
	p=xbmc.Player()
	if(p.isPlayingVideo()==True or p.isPlaying()==True):
		vurl=p.getPlayingFile()
		xbmc.executebuiltin("XBMC.Notification(Backing up, Saving selected video offline,5000)")
		vFilename=xbmc.getInfoLabel('VideoPlayer.Title')
		DoDownloader(vurl,vFilename,AxelPath,False)
def DoDownloader(url,destfile="",destpath="",useResolver=False):
	destpath=xbmc.translatePath(destpath); 
	if useResolver==True:
		try: 
			import urlresolver; 
			link=urlresolver.HostedMediaFile(url).resolve();  
		except: link=url
	else: 
		link=url 
		import axelproxy as proxy; 
		axelhelper=proxy.ProxyHelper(); 
	AxelConnections=axelconnection; 
	AxelUseName=(axelusename==True); 
	AxelKeepFile=(axelkeepfile==True); 
	if (AxelConnections.lower()=='default') or (len(AxelConnections)==0):
		if AxelUseName==True: 
			download_id=axelhelper.download(link,name=destfile,dest_path=destpath); 
		else: 
			download_id=axelhelper.download(link,dest_path=destpath); 
	else: 
		if AxelUseName==True: 
			download_id=axelhelper.download(link,name=destfile,connections=AxelConnections,dest_path=destpath); 
		else: 
			download_id=axelhelper.download(link,connections=AxelConnections,dest_path=destpath); 

def addLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="", infoLabels={ "Title": name } )
        contextMenuItems = []
        liz.addContextMenuItems(contextMenuItems, replaceItems=True)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok
		
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
		
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
params = get_params()
url = None
name = None
mode = None

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode = urllib.unquote_plus(params["mode"])
except:
    pass
	
sysarg=str(sys.argv[1]) 
if mode == None:
	Home()
elif mode == "backuptocloud":
    startStreambackup()
elif mode == "backuptogdrive":
    startStreambackup("googleDrive")
elif mode == "backuptoonedrive":
    startStreambackup("oneDrive")
elif mode == "backuptoboxnet":
    startStreambackup("box")
elif mode == "backuptodropbox":
    startStreambackup("dropbox")
elif mode == "backupoffline":
    startDownload()
elif mode == "viewQueue":
    ViewQueue()
xbmcplugin.endOfDirectory(int(sysarg))