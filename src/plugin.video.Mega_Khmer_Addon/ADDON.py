import urllib,urllib2,re
import os,sys
import base64
import xml.dom.minidom
import xbmcaddon,xbmcplugin,xbmcgui,xbmc
import json #For VIMEO
PLUGIN = xbmcaddon.Addon(id='plugin.video.Mega_Khmer_Addon')
addon_name = 'plugin.video.Mega_Khmer_Addon'
KHMERAVE ='http://www.khmeravenue.com/'
KHMERSTREAM ='http://www.khmerstream.net/'
MERLKON ='http://www.merlkon.net/'
JOLCHET7 ='http://www.khmotion.com/'
JOLCHETC ='http://7khmerch.blogspot.com/'
VIDEO4U ='http://www.video4khmer1.com/'
FILM4KH ='http://www.myvideokhmer.com/' ###### Film2US
KHDRAMA ='http://www.drama4khmers.com/'
HOTKHMER ='http://www.khmerkomsan24.com/'
KHMERALL = 'http://www.khmer6.com/'#'http://www.konkhmerall.com/'
K8MER = 'http://k8mer.co/'
TUBE_KHMER ='http://www.tubekhmer24.com/'
PHUMIKHMER = 'http://www.phumikhmer9.com/'
LAKORNKHMER = 'http://asialakorn.com/'
USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1"
datapath = xbmc.translatePath('special://profile/addon_data/'+addon_name)
cookiejar = os.path.join(datapath,'khmerstream.lwp')
ADDON_PATH = PLUGIN.getAddonInfo('path')
#append lib directory
sys.path.append( os.path.join( ADDON_PATH, 'resources', 'lib' ) )
from net import Net
from BeautifulSoup import BeautifulSoup
import CommonFunctions #For VIMEO
common = CommonFunctions
net = Net()

pluginhandle = int(sys.argv[1])

# example of how to get path to an image
Film2usImage = os.path.join(ADDON_PATH, 'resources', 'images','film2us.jpg')
JolchetImage = os.path.join(ADDON_PATH, 'resources', 'images','7khmer.png')
KHdramaImage = os.path.join(ADDON_PATH, 'resources', 'images','khdram.jpg')
K8merImage = os.path.join(ADDON_PATH, 'resources', 'images','K8mer.png')
TubekhmerImage = os.path.join(ADDON_PATH, 'resources', 'images','TubeKhmer.gif')
fanart = os.path.join(ADDON_PATH, 'resources', 'images','Angkor4.jpg')
def OpenURL(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.3')
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    return link 

def OpenSoup(url):
    req = urllib2.Request(url)
    req.add_unredirected_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0')
    response = urllib2.urlopen(req).read()
    return response

def LOGIN():
		khmerstream_account = PLUGIN.getSetting('khmerstream-account')
		hide_message = PLUGIN.getSetting('hide-successful-login-messages')
		if khmerstream_account == 'true':
				loginurl = 'http://www.khmerstream.net/wp-login.php'
				#loginurl = 'http://www.khmerstream.com/wp-login.php?redirect_to=http%3A%2F%2Fwww.khmerstream.com%2Fwp-admin%2F&reauth=1'
				login = PLUGIN.getSetting('khmerstream-username')
				password = PLUGIN.getSetting('khmerstream-password')
				form = {'log' : login, 'pwd' : password, 'wp-submit' : 'Log In'}				
				net.http_POST(loginurl, form)
				print 'Cookiess: %s' % net
				net.save_cookies(cookiejar)        
				CHECKUSER(KHMERSTREAM)
def CHECKUSER(url):
		hide_message = PLUGIN.getSetting('hide-successful-login-messages')
		net.set_cookies(cookiejar)
		#print 'Cookiesss: %s' % net
		req = urllib2.Request(url)
		req.add_header('User-Agent', USER_AGENT)
		response = urllib2.urlopen(req)
		link=response.read()
		#print 'Links: %s' % link
		response.close()
		match=re.compile('<li id="wp-admin-bar-logout"><a class="ab-item"  href="(.+?)">(.+?)</a>').findall(link)
		#print 'LinkMatchs: %s' % match
		if match:
				if hide_message == 'false':
						print 'Khmerstream Account: login successful'
						xbmc.executebuiltin("XBMC.Notification('small','Khmerstream Account login successful.')")
						
		if not match:
				print 'Khmerstream Account: login failed'
				xbmc.executebuiltin("XBMC.Notification('small,'Login failed: check your username and password')")
				
		pass
def HOME():
        addDir('[B][COLOR orange]MERLKON[/B][/COLOR]',MERLKON,10,'http://www.merlkon.net/wp-contents/uploads/logo.jpg')
        addDir('[B][COLOR orange]JOLCHET[/B][/COLOR]',JOLCHET7,20,'http://1.bp.blogspot.com/-eYngwVMs7wk/VbIiF42BlDI/AAAAAAAAMpc/APh97n98Vy4/s1600/7khmer%2Blogo.png')
        addDir('[B][COLOR orange]VIDEO4U[/B][/COLOR]',VIDEO4U,30,'http://www.video4khmer3.com/templates/kulenkiri/images/header/logo.png')
        addDir('[B][COLOR orange]FILM2US[/B][/COLOR]',FILM4KH,40,'http://www.film4kh.com/images/Film2us.png')
        addDir('[B][COLOR orange]KHDRAMA[/B][/COLOR]',KHDRAMA,50,'http://www.drama2khmer.com/img/logo/khdram.jpg')
        addDir('[B][COLOR orange]HOTKHMER[/B][/COLOR]',HOTKHMER,60,K8merImage+'')
        addDir('[B][COLOR orange]KHMERALL[/B][/COLOR]',KHMERALL,130,'')
        addDir('[B][COLOR orange]K8MERHD[/B][/COLOR]',K8MER,80,K8merImage+'')
        addDir('[B][COLOR orange]TUBEKHMER[/B][/COLOR]',TUBE_KHMER,90,TubekhmerImage+'')
        addDir('[B][COLOR orange]LAKORNKHMER[/B][/COLOR]',LAKORNKHMER,100,'')
        addDir('[B][COLOR red]KARAOKE[/B][/COLOR]','KARAOKE(MUSIC_MENU)',110,'')
        addDir('[B][COLOR red]KARAOKE[/B][/COLOR]','http://www.khmerlovesong.com/',120,'http://www.khmerlovesong.com/images/khmer-love-song.jpg')
########## START MERLKON ***********
def MERLKONS():#10
        LOGIN()
        khmerstream_account = PLUGIN.getSetting('khmerstream-account')
        HomeImage = 'http://www.merlkon.net/wp-contents/uploads/logo.jpg'
        addDir('[B][COLOR blue]Home[/B][/COLOR]',KHMERSTREAM+'',12,'%s' % HomeImage)
        addDir('[B][COLOR orange]Chinese Modern (KA)[/B][/COLOR]',KHMERAVE+'genre/modern-series/',13,'http://www.khmeravenue.com/wp-content/uploads/2015/06/tiger-of-macau-150x150.jpg')
        addDir('[B][COLOR orange]Chinese Ancient (KA)[/B][/COLOR]',KHMERAVE+'genre/ancient-series/',13,'http://www.khmeravenue.com/wp-content/uploads/2012/07/sevenswordsmen-150x150.jpg')
        addDir('[B][COLOR orange]Chinese Modern (KS)[/B][/COLOR]',KHMERSTREAM+'genre/modern-chinese/',12,'http://www.khmerstream.com/wp-content/uploads/2015/08/255px-LookingBackinAngerTVB-150x150.jpg')
        addDir('[B][COLOR orange]Chinese Ancient (KS)[/B][/COLOR]',KHMERSTREAM+'genre/ancient-chinese/',12,'http://www.khmerstream.com/wp-content/uploads/2012/11/5094daac360df-150x150.jpg')
        addDir('[B][COLOR blue]Korean Drama[/B][/COLOR]',KHMERSTREAM+'genre/korean/',12,'http://www.khmerstream.com/wp-content/uploads/2014/09/mylovefrom.png')
        addDir('[B][COLOR blue]Bollywood[/B][/COLOR]',MERLKON+'genre/bollywood-videos/',11,'http://www.merlkon.net/wp-content/uploads/2012/10/bol-150x150.jpg')
        #addDir('[B][COLOR green]Khmer Drama[/B][/COLOR]',MERLKON+'albumcategory/khmer-media/',11,'http://www.merlkon.com/wp-content/uploads/2013/01/komlos-300x200.jpg')
        #addDir('[B][COLOR green]Khmer Drama_V[/B][/COLOR]',VIDEO4U+'khmer-movie-category/khmer-drama-watch-online-free-catalogue-504-page-1.html',6,'http://www.vdokhmer.com/images/subcat/504/3159.jpg')        
        addDir('Thai Drama',MERLKON+'genre/modern-thai/',11,'http://www.merlkon.net/wp-content/uploads/2015/08/dang-150x150.jpg')
        #addDir('[B][COLOR blue]Korean Drama [/B][/COLOR]',VIDEO4U+'/khmer-movie-category/korean-drama-watch-online-free-catalogue-507-page-1.html',6,'http://www.vdokhmer.com/images/subcat/507/2687.jpg')
        addDir('Thai boran',MERLKON+'genre/thai-boran/',11,'http://www.merlkon.net/wp-content/uploads/2014/10/kkk-150x150.jpg')
        addDir('Thai Horror',MERLKON+'genre/horror/',11,'http://www.merlkon.net/wp-content/uploads/2012/12/chiet-150x150.jpg')
        addDir('Philippines Drama',MERLKON+'genre/philippines-videos/',11,'http://www.merlkon.net/wp-content/uploads/2015/01/e-150x150.jpg')
        #addLink('Login',MERLKON+'',9,'http://www.merlkon.com/wp-content/uploads/2012/11/bol.jpg')
        if khmerstream_account == 'true':            
            net.set_cookies(cookiejar)
            link = OpenURL(KHMERSTREAM)
            match=re.compile('<li id="wp-admin-bar-logout"><a class="ab-item"  href="(.+?)">(.+?)</a>').findall(link)
		#print 'LinkMatchs: %s' % match
            for vurl,vname in match:
                    addDir('[B][COLOR red]%s[/B][/COLOR]'% vname,vurl,HOME,'')
        xbmcplugin.endOfDirectory(pluginhandle)

def INDEX_MERLKON(url):
    
        html = OpenSoup(url)
        try:   
           html =html.encode("UTF-8")
        except: pass
        soup = BeautifulSoup(html.decode('utf-8'))
        #div_index = soup('div',{'style':"width:120px; height:120px;padding:1px;background-color:#444444"})
        div_index = soup('div',{'style':"width:140px; height:115px;padding:4px;border: 1px solid silver; background-color:#ffffff"})
        for link in div_index:
            vLink = BeautifulSoup(str(link))('a')[0]['href']
            vTitle = BeautifulSoup(str(link))('a')[0]['title']
            vImage = BeautifulSoup(str(link))('img')[0]['src']
            addDir(vTitle,vLink,15,vImage)
        match5=re.compile('<div class=\'wp-pagenavi\'>\n(.+?)\n</div>').findall(html)
        if(len(match5)):
           pages=re.compile('<a class=".+?" href="(.+?)">(.+?)</a>').findall(match5[0])
           for pageurl,pagenum in pages:
               addDir(" Page " + pagenum,pageurl.encode("utf-8"),11,"")                        
    
        xbmcplugin.endOfDirectory(pluginhandle)

def INDEX_KHMERSTREAM(url):
     
        html = OpenSoup(url)
        try:   
           html =html.encode("UTF-8")
        except: pass
        soup = BeautifulSoup(html.decode('utf-8'))
        #div_index = soup('div',{"style":"width:120px; height:120px;padding:1px;background-color:#444444"})
        div_index = soup('div',{'style':"width:140px; height:115px;padding:4px;border: 1px solid silver; background-color:#ffffff"})
        for link in div_index:
            vLink = BeautifulSoup(str(link))('a')[0]['href']
            vTitle = BeautifulSoup(str(link))('a')[0]['title']
            vImage = BeautifulSoup(str(link))('img')[0]['src']
            addDir(vTitle,vLink,15,vImage)
        match5=re.compile('<div class=\'wp-pagenavi\'>\n(.+?)\n</div>').findall(html)
        if(len(match5)):
           pages=re.compile('<a class=".+?" href="(.+?)">(.+?)</a>').findall(match5[0])
           for pageurl,pagenum in pages:
               addDir(" Page " + pagenum,pageurl.encode("utf-8"),12,"")                        
    
        xbmcplugin.endOfDirectory(pluginhandle)

def INDEX_KHMERAVE(url):    
        link = OpenURL(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        match=re.compile('<a href="(.+?)" title="(.+?)"><img src="(.+?)" alt=".+?"').findall(link)
        for vurl,vname,vimage in match:
            addDir(vname,vurl,15,vimage)
        match5=re.compile('<div class=\'wp-pagenavi\'>\n(.+?)\n</div>').findall(link)
        if(len(match5)):
            pages=re.compile('<a class=".+?" href="(.+?)">(.+?)</a>').findall(match5[0])
            for pageurl,pagenum in pages:
                addDir(" Page " + pagenum,pageurl.encode("utf-8"),13,"")
        xbmcplugin.endOfDirectory(pluginhandle)

def EPISODE_MERLKON(url,name):
        link = OpenURL(url)
        addLink(name,url,3,'')
        match=re.compile('<a href="(.+?)"><span class="part">(.+?)</span></a>').findall(link)     
        if(len(match) == 0):
          match=re.compile('<a href="(.+?)"><span style=".+?">(.+?)</span></a>').findall(link)
        for vLink, vLinkName in match:
            addLink(vLinkName,vLink,3,'')
        xbmcplugin.endOfDirectory(pluginhandle)
######## END MERLKON *****************        
        
         
######## START VIDEO4U ***************
def VIDEO4YOU():#30
        #addDir('[B][COLOR blue]Home[/B][/COLOR]',VIDEO4U+'',31,'%s' % HomeImage)
        addDir('[B][COLOR orange]Chinese Drama[/B][/COLOR]',VIDEO4U+'khmer-movie-category/chinese-series-drama-watch-online-free-catalogue-506-page-1.html',31,'http://www.vdokhmer.com/images/subcat/506/3363.jpg')   
        addDir('[B][COLOR green]Khmer Drama[/B][/COLOR]',VIDEO4U+'khmer-movie-category/khmer-drama-watch-online-free-catalogue-504-page-1.html',31,'http://www.vdokhmer.com/images/subcat/504/3159.jpg')
        addDir('[B][COLOR blue]Korean Drama[/B][/COLOR]',VIDEO4U+'/khmer-movie-category/korean-drama-watch-online-free-catalogue-507-page-1.html',31,'http://www.vdokhmer.com/images/subcat/507/2687.jpg')
        addDir('[B][COLOR purple]Thai Drama[/B][/COLOR]',VIDEO4U+'khmer-movie-category/thai-lakorn-drama-watch-online-free-catalogue-537-page-1.html',31,'http://www.vdokhmer.com/images/subcat/537/3323.jpg')
        addDir('Chinese Movie',VIDEO4U+'khmer-movie-category/chinese-movie-watch-online-free-catalogue-505-page-1.html',31,'http://www.vdokhmer.com/images/subcat/505/3283.jpg')  
        addDir('Thai Movie',VIDEO4U+'khmer-movie-category/thai-movie-watch-online-free-catalogue-525-page-1.html',31,'http://www.vdokhmer.com/images/subcat/525/3326.jpg')
        addDir('Khmer Movie',VIDEO4U+'khmer-movie-category/thai-movie-watch-online-free-catalogue-503-page-1.html',31,'')
def INDEX_VIDEO4U(url):
     
     #try:
        html = OpenSoup(url)
        try:   
           html =html.encode("UTF-8")
        except: pass
        soup = BeautifulSoup(html.decode('utf-8'))
        div_index = soup('div',{'class':"cat-thumb"})
        for link in div_index:
            vImage = BeautifulSoup(str(link))('img')[0]['src']
            vLink = BeautifulSoup(str(link))('a')[0]['href']
            vTitle = BeautifulSoup(str(link))('img')[0]['title']
            vTitle = vTitle.encode("UTF-8",'replace')
            addDir(vTitle,vLink,35,vImage)
        try:
           paging = soup('div',{'class':'pagination'})
           pages = BeautifulSoup(str(paging[0]))('a')
           for p in pages:
             psoup = BeautifulSoup(str(p))
             pageurl = psoup('a')[0]['href']
             pagenum = psoup('a')[0].contents[0]
             addDir(" Page " + pagenum.encode("utf-8") ,pageurl,31,"")
        except:pass
     #except: pass
     #xbmcplugin.endOfDirectory(pluginhandle)        
def EPISODE_VIDEO4U(url,name):
    #try:
        html = OpenSoup(url)
        try:   
           html =html.encode("UTF-8")
        except: pass
        soup = BeautifulSoup(html.decode("utf-8"))
        div_index = soup('div',{'class':"movie-thumb"})
        for episode in div_index:
            vLink = BeautifulSoup(str(episode))('a')[0]['href']
            vImage = BeautifulSoup(str(episode))('img')[0]['src']
            vTitle = BeautifulSoup(str(episode))('img')[0]['title']#('a')[1].contents[0]#['title']            
            addLink(vTitle,vLink,3,vImage)
        
        paging = soup('div',{'class':'pagination'})
        pages = BeautifulSoup(str(paging[0]))('a')
        for p in pages:
             psoup = BeautifulSoup(str(p))
             pageurl = psoup('a')[0]['href']
             pagenum = psoup('a')[0].contents[0]
             addDir(" Page " + pagenum.encode("utf-8") ,pageurl,35,"")
       
    #except: pass
     #xbmcplugin.endOfDirectory(pluginhandle)
def EPISODE4U(url,name):        
        link = OpenURL(url)
        match=re.compile('<div class=".+?"><div class="movie-thumb"><a href="(.+?)"><img src="(.+?)" alt=".+?" title="(.+?)" width="180" height="170"').findall(link)
        counter = 1
        #for url,name,thumbnail in match:
        if (len(match) >= 1):
           for vLink,Vimage,vLinkName in match:
               counter += 1
               addLink(vLinkName,vLink,3,Vimage)
        match5=re.compile('<div class="pagination">(.+?)</div>').findall(link)
        if(len(match5)):
           pages=re.compile('<a href="(.+?)">(.+?)</a>').findall(match5[0])
           for pageurl,pagenum in pages:
               addDir(" Page " + pagenum.encode("utf-8"),pageurl,35,"")     
           xbmcplugin.endOfDirectory(pluginhandle)
############## END VIDEO4U **********************

############## START JOLCHET **********
def JOLCHET():####MODE===20
        addDir('[B][COLOR blue]Home[/B][/COLOR]',JOLCHET7+'',21,'%s' % JolchetImage)
        addDir('[B][COLOR orange]Chinese Drama[/B][/COLOR]',JOLCHET7+'search/label/Chinese%20Drama?&max-results=20',21,'http://movietokhmer.com/assets/img/drama_thumbnail/2/Dav_Tip_MaChas_Piphp_Koun.jpg')
        addDir('[B][COLOR orange]Chinese Drama[/B][/COLOR]',JOLCHETC,23,'http://movietokhmer.com/assets/img/drama_thumbnail/2/Dav_Tip_MaChas_Piphp_Koun.jpg')
        addDir('Chinese Movie',JOLCHET7+'search/label/Chinese%20movie?&max-results=20',22,'http://movietokhmer.com/assets/img/drama_thumbnail/8/sdach_internet.jpg')
        addDir('[B][COLOR blue]Korean Drama[/COLOR][/B]',JOLCHET7+'search/label/Korean%20Drama?&max-results=20',21,'http://movietokhmer.com/assets/img/drama_thumbnail/1/Thornbird.jpg')
        
        addDir('[B][COLOR green]Khmer Drama[/B][/COLOR]',JOLCHET7+'search/label/Khmer%20drama?&max-results=20',21,'http://movietokhmer.com/assets/img/drama_thumbnail/3/koun-ort-kan-sla.jpg')
        addDir('Thai Drama',JOLCHET7+'search/label/Thai%20Drama?&max-results=20',21,'http://movietokhmer.com/assets/img/drama_thumbnail/4/Andath_Plerng_Sneha.jpg')
        addDir('Thai Movie',JOLCHET7+'search/label/thai%20movie?&max-results=20',21,'http://vdo168.com/images/underworld-awakening-hollywood-movie-full-khmer-movie.jpg')
        addDir('Khmer Movie',JOLCHET7+'search/label/Khmer%20Movie?&max-results=20',21,'http://vdo168.com/images/sdech-asoka-india-movie-dubed-khmer-khmer-movie.jpg')
        addDir('Korean Movie',JOLCHET7+'search/label/Korean%20Movie?&max-results=20',21,'http://vdo168.com/images/thug-le-song-ladies-vs-ricky-bahl-khmer-movie.jpg')
                
        xbmcplugin.endOfDirectory(pluginhandle) 

def INDEX_J(url):     
        link = OpenURL(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        #match=re.compile('<h2 class=\'post-title entry-title index\' itemprop=\'name headline\'>\n<a href=\'(.+?)\' itemprop=\'url\'>(.+?)</a>\n</h2>\n<meta content=\'(.+?)\' itemprop=\'image_url\'/>').findall(link)
        match=re.compile('<h2 class=\'post-title entry-title index\' itemprop=\'name headline\'>\n<a href=\'(.+?)\' itemprop=\'url\'>(.+?)</a>\n</h2>\n<meta content=\'(.+?)\'').findall(link)
        for vurl,vname,vimage in match:
            addDir(vname,vurl,25,vimage)
        #match5=re.compile('<div class=\'loadingpost\'></div>\n<div class=\'blog-pager\' id=\'blog-pager\'>\n([^"]+?)\n</div>').findall(link)
        #if(len(match5)):
        pages=re.compile('<span id=\'.+?\'>\n<a class=\'.+?\' href=\'([^"]+?)\' id=\'.+?\' title=\'.+?\'>(.+?)</a>\n</span>').findall(link)
        for pageurl,pagenum in pages:
               addDir("[B][COLOR blue]<<<%s>>>[/B][/COLOR]"% pagenum,pageurl,21,"")                        
        xbmcplugin.endOfDirectory(pluginhandle)
def INDEX_JJ(url):
    #try:
        html = OpenSoup(url)
        try:
            html = html.encode("UTF-8")
        except: pass
        soup = BeautifulSoup(html.decode('utf-8'))
        video_list = soup('div',{'class':'post-outer'})
        for link in video_list:
            vLink = BeautifulSoup(str(link))('a')[0]['href']
            vLink = vLink.encode("UTF-8",'replace')
            #print vLink
            vTitle = BeautifulSoup(str(link))('a')[0].contents[0]#['title']
            vTitle = vTitle.encode("UTF-8",'replace')
            #vImage = BeautifulSoup(str(link))('img')[0]['src']
            vImage = BeautifulSoup(str(link))('a')[4]['href']
            #print vImage
            addDir(vTitle,vLink,25,vImage)
        page = soup('a',{'class':'blog-pager-older-link'})
        for Next in page:
            pageurl = BeautifulSoup(str(Next))('a')[0]['href']
            #print pageurl
            pagenum = BeautifulSoup(str(Next))('a')[0]['title']#['title']
            #print pagenum
            addDir("[B][COLOR blue]<<<%s>>>[/B][/COLOR]"% pagenum.encode("utf-8"),pageurl,21,"")
    #except: pass        
def MOVIE_J(url):     
    #try: 
        html = OpenSoup(url)
        try:
            html = html.encode("UTF-8")
        except: pass
        soup = BeautifulSoup(html.decode('utf-8'))
        video_list = soup('div',{'class':'post-outer'})
        for link in video_list:
            vLink = BeautifulSoup(str(link))('a')[0]['href']
            vLink = vLink.encode("UTF-8",'replace')
            vTitle = BeautifulSoup(str(link))('a')[0].contents[0]#['title']
            vTitle = vTitle.encode("UTF-8",'replace')
            #vImage = BeautifulSoup(str(link))('img')[0]['src']
            vImage = BeautifulSoup(str(link))('a')[1]['href']
            addDir(vTitle,vLink,25,vImage)
        pages=re.compile('<span id=\'.+?\'>\n<a class=\'.+?\' href=\'([^"]+?)\' id=\'.+?\' title=\'.+?\'>(.+?)</a>\n</span>').findall(html)
        for pageurl,pagenum in pages:
            addDir("[B][COLOR blue]<<<%s>>>[/B][/COLOR]"% pagenum,pageurl,22,"")
    #except:pass
    #xbmcplugin.endOfDirectory(pluginhandle)    
def EPISODE_J(url,name):    
        link = OpenURL(url)
        #addLink(name.encode("utf-8"),url,3,'')
        match=re.compile('{\s*"file":\s*"(.+?)",\s*"title":\s*"(.+?)",').findall(link)     
        if(len(match) > 0):      
         for vLink,vLinkName in match:                 
          addLink(vLinkName,vLink,4,'')
        else: 
         match=re.compile('<li class="v-item active" data-source=".+?" data-vid="(.+?)">').findall(link)
         if(len(match) > 0):
           counter = 0      
           for vLink in match:
               counter += 1 
               addLink(name.encode("utf-8") + " part " + str(counter),('https://vid.me/e/'+ vLink),4,'')
         else:
          match=re.compile(' playlist: "(.+?)",').findall(link)
          if(len(match) > 0):
           List = (urllib2.unquote(match[0]).decode("utf8"))
           link = OpenURL(List)
           OpenXML(link)
          else: 
           match=re.compile('<li class="v-item " data-vid="(.+?)">').findall(link)
           if(len(match) > 0):
            counter = 0      
            for vLink in match:
               counter += 1 
               addLink(name.encode("utf-8") + " part " + str(counter),('http://www.mp4upload.com/embed-%s.html'% vLink),4,'')
           else:
             addLink(name,url,3,'')
        xbmcplugin.endOfDirectory(pluginhandle)

def EPISODE_MOVIEJ(url,name):    
        link = OpenURL(url)
        #addLink(name.encode("utf-8"),url,3,'')
        match=re.compile('{\s*"file":\s*"(.+?)",\s*"title":\s*"(.+?)",').findall(link)     
        if(len(match) > 0):      
         for vLink,vLinkName in match:                 
             addLink(vLinkName,vLink,4,'')
        else:
             addLink(name,url,3,'')
def OpenXML(Doc):
    document = xml.dom.minidom.parseString(Doc)      
    items = document.getElementsByTagName('item')
    for itemXML in items:
     vname=itemXML.getElementsByTagName('title')[0].childNodes[0].data
     vpart=itemXML.getElementsByTagName('description')[0].childNodes[0].data
     vImage=itemXML.getElementsByTagName('jwplayer:image')[0].childNodes[0].data
     vurl=itemXML.getElementsByTagName('jwplayer:source')[0].getAttribute('file')     
     addLink(vpart.encode("utf-8"),vurl.encode("utf-8"),4,"")           
############## END JOLCHET ****************** 

############## START FILM2US **********           
def FILM2US():
        addDir('[B][COLOR blue]Home[/B][/COLOR]',FILM4KH+'',41,'%s' % Film2usImage)
        addDir('[B][COLOR orange]Chinese Drama[/B][/COLOR]',FILM4KH+'khmer-chinese-drama-dubbed',41,'http://movietokhmer.com/assets/img/drama_thumbnail/2/Dav_Tip_MaChas_Piphp_Koun.jpg')
        addDir('Chinese Movie',FILM4KH+'khmer-chinese-movie-dubbed',41,'http://movietokhmer.com/assets/img/drama_thumbnail/8/sdach_internet.jpg')
        addDir('[B][COLOR blue]Korean Drama[/B][/COLOR]',FILM4KH+'khmer-korean-drama-dubbed',41,'http://movietokhmer.com/assets/img/drama_thumbnail/1/Thornbird.jpg')
        addDir('Korean Movie',FILM4KH+'khmer-korean-movie-dubbed',41,'http://vdo168.com/images/baby-and-me-comedy-action-2013-korea-full-movie-with-english-subtitles-khmer-movie.jpg')
        addDir('[B][COLOR green]Khmer Drama[/B][/COLOR]',FILM4KH+'khmer-drama-dubbed',41,'http://www.film2us.com//images/cover/Rolok-Bok-Ksach.jpg')
        addDir('Khmer Movie',FILM4KH+'khmer-movie-dubbed',41,'http://www.film2us.com//images/cover/Preay-Dek-Koul.jpg')
        addDir('Thai Drama',FILM4KH+'khmer-thai-lakorn-dubbed',41,'http://movietokhmer.com/assets/img/drama_thumbnail/4/Andath_Plerng_Sneha.jpg')
        addDir('Thai Movie',FILM4KH+'khmer-thai-movie-dubbed',41,'http://www.film2us.com//images/cover/Nak-KaPea-II.jpg')
        addDir('Philippian Movie',FILM4KH+'khmer-philipian-movie-dubbed',41,'http://www.film2us.com//images/cover/Good-Times-Bad-Times.jpg')
        #addDir('Cartoon Movie',HomeURL+'khmer-cartoon-dubbed',2,'http://www.khdrama.com/photo/Kung-Fu-Panda-2.jpg')
        #addDir('[B][COLOR red]KARAOKE[/B][/COLOR]','http://www.khmerlovesong.com/',7,'http://www.khmerlovesong.com/images/khmer-love-song.jpg')                   
        xbmcplugin.endOfDirectory(pluginhandle) 

def INDEX_FILM2US(url):
    html = OpenSoup(url)
    soup = BeautifulSoup(html.decode('utf-8'))
    #video_list = soup('div',{'class':"panel-body"})
    video_list = soup('div',{'class':"col-lg-3 col-md-3 col-sm-4 col-xs-6"})
    for link in video_list:
        vLink = BeautifulSoup(str(link))('a')[1]['href']
        #vTitle = BeautifulSoup(str(link))('a')[0].contents[0]
        vTitle = BeautifulSoup(str(link))('a')[1]['title']
        vImage = BeautifulSoup(str(link))('img')[0]['src']
        addDir(vTitle,vLink,45,vImage)
    match5=re.compile('<ul class="pagination">(.+?)</ul>').findall(html)
    if(len(match5)):
        pages=re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(match5[0])
        for pageurl,pagenum in pages:
            addDir(" Page " + pagenum,pageurl.encode("utf-8"),41,"")
    xbmcplugin.endOfDirectory(pluginhandle)    

def EPISODE_FILM2US(url):    
        html =urllib2.urlopen(url).read()
        soup = BeautifulSoup(html.decode('utf-8'))
        #episodes = soup('div',{'class':"panel-body"})
        episodes = soup('div',{'class':"col-lg-3 col-md-3 col-sm-4 col-xs-6"})
        for link in episodes:
            vLink = BeautifulSoup(str(link))('a')[1]['href']
            #vTitle = BeautifulSoup(str(link))('a')[0].contents[0]
            vTitle = BeautifulSoup(str(link))('a')[1]['title']
            vImage = BeautifulSoup(str(link))('img')[0]['src']
            addLink(vTitle,vLink,3,vImage)
        match5=re.compile('<ul class="pagination">(.+?)</ul>').findall(html)
        if(len(match5)):
            pages=re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(match5[0])
            for pageurl,pagenum in pages:
                addDir(" Page " + pagenum,pageurl.encode("utf-8"),45,"")
        xbmcplugin.endOfDirectory(pluginhandle)
############## END FILM2US ******************

############## START KHDRAMA **********
def KHDRAMA2():
        addDir('[B][COLOR blue]Home[/B][/COLOR]',KHDRAMA+'',51,'%s' % KHdramaImage)
        addDir('[B][COLOR orange]Chinese Drama[/B][/COLOR]',KHDRAMA+'watch-khmer-chinese-drama-video',51,'http://movietokhmer.com/assets/img/drama_thumbnail/2/Dav_Tip_MaChas_Piphp_Koun.jpg')
        addDir('Chinese Movie',KHDRAMA+'watch-khmer-chinese-movie-video',51,'http://movietokhmer.com/assets/img/drama_thumbnail/8/sdach_internet.jpg')
        addDir('[B][COLOR blue]Korean Drama[/B][/COLOR]',KHDRAMA+'watch-khmer-korean-drama-video',51,'http://movietokhmer.com/assets/img/drama_thumbnail/1/Thornbird.jpg')
        addDir('Korean Movie',KHDRAMA+'watch-khmer-korean-movie-video',51,'http://vdo168.com/images/baby-and-me-comedy-action-2013-korea-full-movie-with-english-subtitles-khmer-movie.jpg')
        #addDir('Korean Music Video',HomeURL+'category/korea/korea-music-video/1',6,'http://vdo168.com/images/girls-generation-mv-playlist-khmer-movie.jpg')
        addDir('[B][COLOR=FF67cc33]Khmer Movie[/B][/COLOR]',KHDRAMA+'watch-khmer-movie-video',51,'http://movietokhmer.com/assets/img/drama_thumbnail/3/koun-ort-kan-sla.jpg')
        addDir('Thai Drama',KHDRAMA+'watch-khmer-thai-lakorn-video',51,'http://movietokhmer.com/assets/img/drama_thumbnail/4/Andath_Plerng_Sneha.jpg')
        addDir('Thai Movie',KHDRAMA+'watch-khmer-thai-movie-video',51,'http://www.khdrama.com/photo/Nak-KaPea-II.jpg')
        addDir('Philippian Movie',KHDRAMA+'watch-khmer-philippian-movie-video',51,'http://www.khdrama.com/photo/Sneh-Pit-Chet-Smos.jpg')
        #addDir('[B][COLOR red]KARAOKE[/B][/COLOR]','http://www.khmerlovesong.com/',7,'http://www.khmerlovesong.com/images/khmer-love-song.jpg')        
         
        xbmcplugin.endOfDirectory(pluginhandle) 
def INDEX_KHDRAMA(url):
         html = OpenSoup(url)
         try:
            html = html.encode("UTF-8")
         except: pass
         soup = BeautifulSoup(html.decode('utf-8'))
         video_list = soup('div',{'class':"thumbnail"})
         for link in video_list:
             vLink = BeautifulSoup(str(link))('a')[0]['href']
             vTitle = BeautifulSoup(str(link))('a')[0]['title']
             vImage = BeautifulSoup(str(link))('img')[0]['src']
             addDir(vTitle,vLink,55,vImage)
         match5=re.compile('<ul class="pagination catalogue-pagination">(.+?)</ul>').findall(html)
         if(len(match5)):
           pages=re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(match5[0])
           for pageurl,pagenum in pages:
               addDir(" Page " + pagenum,pageurl.encode("utf-8"),51,"")  
                        
         xbmcplugin.endOfDirectory(pluginhandle)	
def EPISODE_KHDRAMA(url,name):
         html = OpenSoup(url)
         try:
            html = html.encode("UTF-8")
         except: pass
         soup = BeautifulSoup(html.decode('utf-8'))
         video_list = soup('div',{'class':"thumbnail"})
         for link in video_list:
             vLink = BeautifulSoup(str(link))('a')[0]['href']
             vTitle = BeautifulSoup(str(link))('a')[0]['title']
             vImage = BeautifulSoup(str(link))('img')[0]['src']
             addDir(vTitle,vLink,3,vImage)
         match5=re.compile('<ul class="pagination catalogue-pagination">(.+?)</ul>').findall(html)
         if(len(match5)):
           pages=re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(match5[0])
           for pageurl,pagenum in pages:
               addDir(" Page " + pagenum,pageurl.encode("utf-8"),55,"")

         xbmcplugin.endOfDirectory(pluginhandle)        
############## END KHDRAMA ******************
#######################################
def KHMERKOMSAN():#60
        #addDir('[B][COLOR blue]Home[/B][/COLOR]',HOTKHMER+'',61,'%s' % HomeImage)
        addDir('[B][COLOR orange]Chinese Drama[/B][/COLOR]',HOTKHMER+'category.php?cat=chinese-drama-dubbed',61,'http://www.vdokhmer.com/images/subcat/506/3363.jpg')   
        addDir('[B][COLOR green]Khmer Drama[/B][/COLOR]',HOTKHMER+'category.php?cat=khmer-drama-dubbed',61,'http://www.vdokhmer.com/images/subcat/504/3159.jpg')
        #addDir('[B][COLOR blue]Korean Drama[/B][/COLOR]',HOTKHMER+'',61,'http://www.vdokhmer.com/images/subcat/507/2687.jpg')
        addDir('[B][COLOR purple]Thai Lakorn[/B][/COLOR]',HOTKHMER+'category.php?cat=thai-lakorn-dubbed',61,'http://www.vdokhmer.com/images/subcat/537/3323.jpg')
        addDir('[B][COLOR purple]Thai Continued[/B][/COLOR]',HOTKHMER+'category.php?cat=thai-continued-dubbed',61,'http://www.vdokhmer.com/images/subcat/537/3323.jpg')
        addDir('Chinese Movie',HOTKHMER+'category.php?cat=chinese-movie-dubbed',61,'http://www.vdokhmer.com/images/subcat/505/3283.jpg')  
        addDir('Thai Movie',HOTKHMER+'category.php?cat=thai-movie-dubbed',61,'http://www.vdokhmer.com/images/subcat/525/3326.jpg')
        addDir('Khmer Movie',HOTKHMER+'category.php?cat=thai-movie-dubbed',61,'')
def INDEX_KHMERKOMSAN(url):
     
     #try:
        html = OpenSoup(url)
        try:   
           html =html.encode("UTF-8")
        except: pass
        soup = BeautifulSoup(html.decode('utf-8'))
        div_index = soup('div',{'class':"fra-thunmb"})
        for link in div_index:            
            vLink = BeautifulSoup(str(link))('a')[0]['href']
            vImage = BeautifulSoup(str(link))('img')[0]['src']
            vTitle = BeautifulSoup(str(link))('img')[0]['title']
            vTitle = vTitle.encode("UTF-8",'replace')
            addDir(vTitle,vLink,65,vImage)
        pages=re.compile('<li class="">\r\n\s*<a href="(.+?)">&raquo;</a>').findall(html)
        if(len(pages)):
          for pageurl in pages:
              addDir("[B][COLOR blue]<< Next Page >>[/B][/COLOR]",('http://www.khmerkomsan24.com/' + pageurl.encode("utf-8")),61,"")
def INDEX_KHMERKOMSAN_MOVIE(url):
     
     #try:
        html = OpenSoup(url)
        try:   
           html =html.encode("UTF-8")
        except: pass
        soup = BeautifulSoup(html.decode('utf-8'))
        div_index = soup('div',{'class':"fra-thunmb"})
        for link in div_index:            
            vLink = BeautifulSoup(str(link))('a')[0]['href']
            vImage = BeautifulSoup(str(link))('img')[0]['src']
            vTitle = BeautifulSoup(str(link))('img')[0]['title']
            vTitle = vTitle.encode("UTF-8",'replace')
            addDir(vTitle,vLink,65,vImage)
        pages=re.compile('<li class="">\r\n\s*<a href="(.+?)">&raquo;</a>').findall(html)
        if(len(pages)):
          for pageurl in pages:
              addDir("[B][COLOR blue]<< Next Page >>[/B][/COLOR]",('http://www.khmerkomsan24.com/' + pageurl.encode("utf-8")),62,"")
def EPISODE_KHMERKOMSAN(url,name):    
        link = OpenURL(url)        
        match=re.compile('{\s*"file":\s*"(.+?)",\s*"title":\s*"(.+?)",').findall(link)     
        if(len(match) > 0):      
         for vLink,vLinkName in match:                 
             addLink(vLinkName,vLink,4,'')
        else: 
         match=re.compile('[^>]*{"idGD":\s*"([^"]+?)"').findall(link)
         print 'MATCHIFRAM: %s' % match
         if(len(match) > 0):
           EPlink = match[0].replace("0!?^0!?A"," ")       
           match = EPlink.split(' ')   
           counter = 0      
           for vLink in match:
               counter += 1 
               addLink(name.encode("utf-8") + " part " + str(counter), 'https://docs.google.com/file/d/%s' % vLink,4,'')
         else:
           match=re.compile('<div id="Playerholder">\r\n\t\t\t<iframe [^>]*src="([^"]+?)"').findall(link)
           print 'MATCHPLAY: %s' % match
           if(len(match) > 0):      
            for vLink in match:
              addLink(name.encode("utf-8"),vLink,4,'')

def KONKHMERALL():
        addDir('[B][COLOR orange]Chinese Drama[/B][/COLOR]',KHMERALL+'search/label/China%20Drama',131,'http://movietokhmer.com/assets/img/drama_thumbnail/2/Dav_Tip_MaChas_Piphp_Koun.jpg')
        addDir('Chinese Movie',KHMERALL+'search/label/China%20Movie',131,'http://movietokhmer.com/assets/img/drama_thumbnail/8/sdach_internet.jpg')
        #addDir('[B][COLOR blue]Korean Drama[/B][/COLOR]',KHMERALL+'category/home/korea-drama/',101,'http://movietokhmer.com/assets/img/drama_thumbnail/1/Thornbird.jpg')
        #addDir('Korean Movie',K8MER+'type-korean-movies',81,'http://vdo168.com/images/baby-and-me-comedy-action-2013-korea-full-movie-with-english-subtitles-khmer-movie.jpg')
        #addDir('[B][COLOR green]Khmer Drama[/B][/COLOR]',LAKORNKHMER+'type-khmer-drama',101,'http://www.film2us.com//images/cover/Rolok-Bok-Ksach.jpg')
        #addDir('Khmer Movie',K8MER+'type-khmer-movies',81,'http://www.film2us.com//images/cover/Preay-Dek-Koul.jpg')
        addDir('Thai Drama',KHMERALL+'search/label/Thai%20Drama',131,'http://movietokhmer.com/assets/img/drama_thumbnail/4/Andath_Plerng_Sneha.jpg')
        addDir('Thai Movie',KHMERALL+'search/label/Thai%20Movie',131,'http://www.film2us.com//images/cover/Nak-KaPea-II.jpg')
        #addDir('Philippines Drama',LAKORNKHMER+'category/philippines-drama/',101,'')

def INDEX_KONKHMERALL(url):
         html = OpenSoup(url)
         try:
             html = html.encode("UTF-8")
         except: pass
         soup = BeautifulSoup(html.decode('utf-8'))
         div_index = soup('div',{"class":'post-outer'})
         for link in div_index:
             vLink = BeautifulSoup(str(link))('a')[0]['href']
             vLink = vLink.encode("UTF-8",'replace')
             print vLink
             vTitle = BeautifulSoup(str(link))('a')[0].contents[0]
             vTitle = vTitle.encode("UTF-8",'replace')
             print vTitle
             vImage = BeautifulSoup(str(link))('a')[1]['href']
             print vImage
             addDir(vTitle,vLink,135,vImage)             
         pages=re.compile('<span id=\'blog-pager-older-link\'>\n<a class=\'blog-pager-older-link\' href=\'([^"]+?)\' ').findall(html)
         for pageurl in pages:
               addDir("[B][COLOR blue]%s >>[/B][/COLOR]"% 'NEXT PAGE',pageurl,131,"")

def EPISODE_KONKHMERALL(url,name):    
        link = OpenURL(url)
        try:
             link = link.encode("UTF-8")
        except: pass
        #addLink(name.encode("utf-8"),url,3,'')
        match=re.compile('{\s*"file":\s*"(.+?)",\s*"title":\s*"(.+?)",').findall(link)     
        if(len(match) > 0):      
         for vLink,vLinkName in match:                 
          addLink(vLinkName,vLink,4,'')
####################################
def K8MERHD():
        addDir('[B][COLOR orange]Chinese Drama[/B][/COLOR]',K8MER+'category/home-feather/chinese/',81,'http://movietokhmer.com/assets/img/drama_thumbnail/2/Dav_Tip_MaChas_Piphp_Koun.jpg')
        #addDir('Chinese Movie',K8MER+'type-chinese-movies',81,'http://movietokhmer.com/assets/img/drama_thumbnail/8/sdach_internet.jpg')
        addDir('[B][COLOR blue]Korean Drama[/B][/COLOR]',K8MER+'category/home-feather/korea/',81,'http://movietokhmer.com/assets/img/drama_thumbnail/1/Thornbird.jpg')
        #addDir('Korean Movie',K8MER+'type-korean-movies',81,'http://vdo168.com/images/baby-and-me-comedy-action-2013-korea-full-movie-with-english-subtitles-khmer-movie.jpg')
        #addDir('[B][COLOR green]Khmer Drama[/B][/COLOR]',K8MER+'type-khmer-drama',81,'http://www.film2us.com//images/cover/Rolok-Bok-Ksach.jpg')
        #addDir('Khmer Movie',K8MER+'type-khmer-movies',81,'http://www.film2us.com//images/cover/Preay-Dek-Koul.jpg')
        addDir('Thai Drama',K8MER+'category/home-feather/thai/',81,'http://movietokhmer.com/assets/img/drama_thumbnail/4/Andath_Plerng_Sneha.jpg')
        #addDir('Thai Movie',K8MER+'type-thai-movies',81,'http://www.film2us.com//images/cover/Nak-KaPea-II.jpg')
        

def INDEX_K8MERHD(url):
         html = OpenSoup(url)
         try:
             html = html.encode("UTF-8")
         except: pass
         soup = BeautifulSoup(html.decode('utf-8'))
         div_index = soup('div',{"class":"item-thumbnail"})
         for link in div_index:
             vLink = BeautifulSoup(str(link))('a')[0]['href']
             print vLink
             vTitle = BeautifulSoup(str(link))('img')[0]['alt']
             vTitle = vTitle.encode("UTF-8",'replace')
             print vTitle
             vImage = BeautifulSoup(str(link))('img')[0]['src']
             vImage = vImage.encode("UTF-8").replace(" ", "%20")
             print vImage
             addDir(vTitle,vLink,85,vImage)
         match5=re.compile('<div class=\'wp-pagenavi\'>\n(.+?)\n</div>').findall(html)
         if(len(match5)):
            pages=re.compile('<a class=".+?" href="(.+?)">(.+?)</a>').findall(match5[0])
            for pageurl,pagenum in pages:
                addDir(" Page " + pagenum,pageurl.encode("utf-8"),81,"")    
def EPISODE_K8MERHD(url,name):
         html = OpenSoup(url)
         addLink(name,url,3,'')
         try:
             html = html.encode("UTF-8")
         except: pass
         soup = BeautifulSoup(html.decode('utf-8'))
         epis = soup('a',{"class":"btn btn-sm btn-default "})
         for link in epis:
             vLink = BeautifulSoup(str(link))('a')[0]['href']
             #vLink = BeautifulSoup(str(link))('a')[0]['data-url']
             print vLink
             vTitle = BeautifulSoup(str(link))('a')[0]['title']
             print vTitle
             #vImage = BeautifulSoup(str(link))('img')[0]['src']
             #print vImage
             addLink(vTitle,vLink,3,'')
##########################################################
def TUBEKHMER():
        addDir('[B][COLOR orange]Chinese Drama[/B][/COLOR]',TUBE_KHMER+'search/label/Chinese%20Series',91,'http://movietokhmer.com/assets/img/drama_thumbnail/2/Dav_Tip_MaChas_Piphp_Koun.jpg')
        #addDir('Chinese Movie',HomeURL+'movie/load/8',2,'http://movietokhmer.com/assets/img/drama_thumbnail/8/sdach_internet.jpg')
        #addDir('Chinese Drama_V',HomeURL+'khmer-movie-category/chinese-series-drama-watch-online-free-catalogue-506-page-1.html',6,'http://www.vdokhmer.com/images/subcat/506/3363.jpg')       
        #addDir('[B][COLOR blue]Korean Drama[/B][/COLOR]',HomeURL+'search/label/Korean%20Series',2,'http://movietokhmer.com/assets/img/drama_thumbnail/1/Thornbird.jpg')
        addDir('Thai Lakorn',PHUMIKHMER+'search/label/Thai%20Lakorn?&max-results=16',92,'http://movietokhmer.com/assets/img/drama_thumbnail/1/Thornbird.jpg')
        #addDir('[B][COLOR green]Khmer Drama[/B][/COLOR]',HomeURL+'search/label/Khmer%20Drama',2,'http://movietokhmer.com/assets/img/drama_thumbnail/3/koun-ort-kan-sla.jpg')
        addDir('Thai Drama',TUBE_KHMER+'search/label/Thai%20Lakorn?&max-results=15',91,'http://movietokhmer.com/assets/img/drama_thumbnail/4/Andath_Plerng_Sneha.jpg')
        #addDir('HOME',PHUMIKHMER+'',2,'%s' % HomeImage)
        xbmcplugin.endOfDirectory(pluginhandle)

def INDEX_PHUMIKHMER(url):     
    try:
        html = OpenSoup(url)
        try:
            html =html.encode("UTF-8")
        except: pass
        #html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html.decode('utf-8'))
        video_list = soup('div',{'class':'cutter'})
        for link in video_list:
            vLink = BeautifulSoup(str(link))('a')[0]['href']
            vTitle = BeautifulSoup(str(link))('a')[0]['title']
            vTitle = vTitle.encode("UTF-8",'replace')
            vImage = BeautifulSoup(str(link))('img')[0]['src']
            addDir(vTitle,vLink,95,vImage)
        label=re.compile("/label/(.+?)\?").findall(url)[0]
        print label
        pagenum=re.compile("PageNo=(.+?)").findall(url)
        print pagenum
        prev="0"
        if(len(pagenum)>0):
              prev=str(int(pagenum[0])-1)
              pagenum=str(int(pagenum[0])+1)

        else:
              pagenum="2"
        nexurl=buildNextPage(pagenum,label)

        if(int(pagenum)>2 and prev=="1"):
              urlhome=url.split("?")[0]+"?"
              addDir("[B][COLOR blue]<< Back Page >>[/B][/COLOR]",urlhome,92,"")
        elif(int(pagenum)>2):
              addDir("[B][COLOR blue]<< Back Page >>[/B][/COLOR]",buildNextPage(prev,label),92,"")
        if(nexurl!=""):
              addDir("[B][COLOR green]<< Next Page >>[/B][/COLOR]",nexurl,92,"")
        
    except:pass
    #xbmc.executebuiltin('Container.SetViewMode(500)')
    xbmcplugin.endOfDirectory(pluginhandle)	
def INDEX_TUBEKHMER(url):     
    
        html = OpenURL(url)
        try:
            html =html.encode("UTF-8")
        except: pass
        soup = BeautifulSoup(html.decode('utf-8'))
        video_list = soup('div',{'class':'post-outer'})
        for link in video_list:
            vImage = BeautifulSoup(str(link))('a')[1]['href']    
            vLink = BeautifulSoup(str(link))('a')[0]['href']
            vTitle = BeautifulSoup(str(link))('a')[2]['title']
            vTitle = vTitle.encode("UTF-8",'replace')
            addDir(vTitle,vLink,95,vImage)
        label=re.compile("/label/(.+?)\?").findall(url)[0]
        print label
        pagenum=re.compile("PageNo=(.+?)").findall(url)
        print pagenum
        prev="0"
        if(len(pagenum)>0):
              prev=str(int(pagenum[0])-1)
              pagenum=str(int(pagenum[0])+1)

        else:
              pagenum="2"
        nexurl=buildNextPage(pagenum,label)

        if(int(pagenum)>2 and prev=="1"):
              urlhome=url.split("?")[0]+"?"
              addDir("[B][COLOR blue]<< Back Page >>[/B][/COLOR]",urlhome,91,"")
        elif(int(pagenum)>2):
              addDir("[B][COLOR blue]<< Back Page >>[/B][/COLOR]",buildNextPage(prev,label),91,"")
        if(nexurl!=""):
              addDir("[B][COLOR green]<< Next Page >>[/B][/COLOR]",nexurl,91,"")
        #Page= soup('a',{"class":"blog-pager-older-link"})
        #for Next in Page:
         #pageurl = BeautifulSoup(str(Next))('a')[0]['href']
         #print vLink
         #pagenum = BeautifulSoup(str(Next))('a')[0]['title'] 
         #addDir("[B][COLOR blue]<<<%s>>>[/B][/COLOR]"% pagenum,pageurl,91,"")    
                         
       # xbmcplugin.endOfDirectory(pluginhandle)

def buildNextPage(pagenum,label):
	pagecount=str((int(pagenum) - 1) * 18)
	url=TUBE_KHMER+"feeds/posts/summary/-/"+label+"?start-index="+pagecount+"&max-results=1&alt=json-in-script&callback=finddatepost"
	link = OpenURL(url)
	try:
		link =link.encode("UTF-8")
	except: pass
	match=re.compile('"published":\{"\$t":"(.+?)"\}').findall(link)
	print match
	if(len(match)>0):
		tsvalue=urllib.quote_plus(match[0][0:19]+match[0][23:29])
		newurl=PHUMIKHMER+"search/label/"+label+"?updated-max="+tsvalue+"&max-results=18#PageNo="+pagenum
	else:
		newurl=""
	return newurl
def EPISODE_TUBEKHMER(url,name):
        link = OpenURL(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        #addLink(name.encode("utf-8"),url,3,'')
        match=re.compile('{\s*"file":\s*"(.+?)",\s*"title":\s*"(.+?)",\s*"description": "",').findall(link)
        if(len(match)>0):
         for vLink,vLinkName in match:
          addLink(vLinkName,vLink,4,'')
        else:#if(len(match)==0):
         match=re.compile('href="(.+?)" target="_blank">(.+?)</a>').findall(link)
         if(len(match)>0):
          for vLink,vLinkName in match:
           addLink(vLinkName,vLink,4,'')
         else:#if(len(match)==0):
          match=re.compile('<li class="v-item active" data-vid="(.+?)"><img /><span class="v-title">(.+?)</span>').findall(link)
          if(len(match)>0):
           for vLink,vLinkName in match:
            addLink(vLinkName,('https://player.vimeo.com/video/'+vLink),4,'')
          else:
           #match=re.compile('{\s*"file":\s*"(.+?)",\s*"title":\s*".+?",\s*"description":\s*"(.+?)",').findall(link)
           match=re.compile('{\s*"file":\s*"(.+?)",\s*"title":\s*"(.+?)",').findall(link)
           if(len(match)>0):
            for vLink,vLinkName in match:
             addLink(vLinkName,vLink,4,'')
           else:
            #match=re.compile('{\s*"file":\s*"(.+?)",\s*"title":\s*"(.+?)",\s*"description":\s*"",').findall(link)
            match=re.compile('{\s*"file":\s*"(.+?)",\s*"title":\s*".+?",\s*"description":\s*"(.+?)",').findall(link)
            if(len(match)>0):
             for vLink,vLinkName in match:
              addLink(vLinkName,vLink,4,'')
            else:
             match=re.compile('{\s*"file":\s*"(.+?)",\s*"title":\s*"",\s*"description":\s*"(.+?"),').findall(link)
             if(len(match)>0):
              for vLink,vLinkName in match:
               addLink(vLinkName,vLink,4,'')  
        xbmcplugin.endOfDirectory(pluginhandle)
             
##########################################################
def LAKORNKHMERS():
        addDir('[B][COLOR orange]Chinese Drama[/B][/COLOR]',LAKORNKHMER+'category/home/chinese-series/',101,'http://movietokhmer.com/assets/img/drama_thumbnail/2/Dav_Tip_MaChas_Piphp_Koun.jpg')        
        addDir('[B][COLOR blue]Korean Drama[/B][/COLOR]',LAKORNKHMER+'category/home/korea-drama/',101,'http://movietokhmer.com/assets/img/drama_thumbnail/1/Thornbird.jpg')        
        addDir('Thai Lakorn',LAKORNKHMER+'category/home/thai-lakorn/',101,'http://movietokhmer.com/assets/img/drama_thumbnail/4/Andath_Plerng_Sneha.jpg')
        

def INDEX_LAKORNKHMER(url):
         html = OpenSoup(url)
         try:
             html = html.encode("UTF-8")
         except: pass
         soup = BeautifulSoup(html.decode('utf-8'))
         div_index = soup('div',{"class":"item-thumbnail"})
         for link in div_index:
             vLink = BeautifulSoup(str(link))('a')[0]['href']
             vLink = vLink.encode("UTF-8",'replace')
             print vLink
             vTitle = BeautifulSoup(str(link))('img')[0]['title']
             vTitle = vTitle.encode("UTF-8",'replace')
             print vTitle
             vImage = BeautifulSoup(str(link))('img')[0]['src']
             print vImage
             addDir(vTitle,vLink,105,vImage)
         pages=re.compile('"nextLink":"(.+?)",').findall(html)
         for pageurl in pages:
            addDir("[B][COLOR blue]%s >>[/B][/COLOR]"% 'NEXT PAGE',pageurl.replace("\/",'/'),101,"")
def EPISODE1_LAKORNKHMER(url,name):
         html = OpenSoup(url)
         addLink(name,url,3,'')
         try:
             html = html.encode("UTF-8")
         except: pass
         soup = BeautifulSoup(html.decode('utf-8'))
         div_index = soup('a',{"class":"btn btn-sm btn-default "})
         for link in div_index:
             vLink = BeautifulSoup(str(link))('a')[0]['href']
             vLink = vLink.encode("UTF-8",'replace')
             print vLink
             vTitle = BeautifulSoup(str(link))('a')[0]['title']
             vTitle = vTitle.encode("UTF-8",'replace')
             print vTitle
             #vImage = BeautifulSoup(str(link))('img')[0]['src']
             #print vImage
             addLink(vTitle,vLink,3,'')
def EPISODE_LAKORNKHMER(url,name):
         html = OpenURL(url)
         addLink(name,url,3,'')
         try:
             html = html.encode("UTF-8")
         except: pass
         match = re.compile('<a class="btn btn-sm btn-default " href="(.+?)" title="(.+?)"><i class="fa fa-play"></i> .+?</a>').findall(html)
         for vLink,vTitle in match:
             addLink(vTitle,vLink,3,'')


################ KARAOKE ************ START #################
def MUSIC_MENU(url,name):
        addDir('phleng production',VIDEO4U +'khmer-movie-category/phleng-production-khmer-video-karaoke-catalogue-2845-page-1.html',111,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Hang Meas Karaoke',VIDEO4U +'khmer-movie-category/hang-meas-khmer-video-karaoke-catalogue-509-page-1.html',111,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Sunday Khmer Karaoke',VIDEO4U +'khmer-movie-category/sunday-khmer-video-karaoke-catalogue-510-page-1.html',111,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Town Production Karaoke',VIDEO4U +'khmer-movie-category/town-production-khmer-video-karaoke-catalogue-514-page-1.html',111,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Big Man Khmer Karaoke',VIDEO4U +'khmer-movie-category/big-man-khmer-video-karaoke-catalogue-512-page-1.html',111,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('M Production Karaoke',VIDEO4U +'khmer-movie-category/m-production-khmer-video-karaoke-catalogue-511-page-1.html',111,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Rock Production Karaoke',VIDEO4U +'khmer-movie-category/rock-production-khmer-video-karaoke-catalogue-513-page-1.html',111,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Spark Production Karaoke',VIDEO4U +'khmer-movie-category/spark-production-khmer-video-karaoke-catalogue-516-page-1.html',111,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')
        addDir('Chenla Brother Karaoke',VIDEO4U +'khmer-movie-category/chenla-brother-khmer-video-karaoke-catalogue-518-page-1.html',111,'http://moviekhmer.com/wp-content/uploads/2012/04/Khmer-Movie-Korng-Kam-Korng-Keo-180x135.jpg')

def MUSIC_VIDEO(url):     
        link = OpenURL(url)
        match=re.compile('<div class=".+?"><div class="cat-thumb"><a href="(.+?)"><img src="(.+?)" alt=".+?" title="(.+?)"').findall(link)
        for vtitle in match:
                (vurl,vimage,vname)=vtitle
                addDir(vname,vurl,115,vimage)
                match5=re.compile('<div class="pagination">(.+?)</div>').findall(link)
        if(len(match5)):
                pages=re.compile('<a href="(.+?)">(.+?)</a>').findall(match5[0])
                for pcontent in pages:
                        (pageurl,pagenum)=pcontent
                        addDir(" Page " + pagenum.encode("utf-8"),pageurl,111,"")
        xbmcplugin.endOfDirectory(pluginhandle)        
def MUSIC_EP(url,name):        
        link = OpenURL(url)
        match=re.compile('<div class=".+?"><div class="movie-thumb"><a href="(.+?)"><img src="(.+?)" alt=".+?" title="(.+?)" width="180" height="170"').findall(link)
        videolist=''
        counter = 0
        for vLink,vImage,vLinkName in match:
            counter += 1
            addLink(vLinkName,vLink,3,vImage)
            videolist=videolist+vLink+';#'
            if(counter==len(match) and (len(videolist.split(';#'))-1) > 1):
              addLink("[B][COLOR blue]-------Play the "+ str(len(videolist.split(';#'))-1)+" videos above--------[/B][/COLOR]",videolist,200,vImage)
                 
        xbmcplugin.endOfDirectory(pluginhandle)

def PLAYLIST_VIDEOLINKS(url):
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
                PLAYLISTVIDEOLINKS(videoLink)
                #VIDEOLINKS(videoLink,name)
                loadedLinks = loadedLinks + 1
                percent = (loadedLinks * 100)/totalLinks
                #print percent
                remaining_display = 'Videos loaded :: [B]'+str(loadedLinks)+' / '+str(totalLinks)+'[/B] into XBMC player playlist.'
                pDialog.update(percent,'Please wait for the process to retrieve video link.',remaining_display)
                if (pDialog.iscanceled()):
                        return False   
        playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playList.clear()
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playList)
        if not xbmcPlayer.isPlayingVideo():
                d = xbmcgui.Dialog()
                d.ok('videourl: ' + str(playList), 'One or more of the playlist items','Check links individually.')
        return ok
        pDialog.close()
        del pDialog

def PLAYLISTVIDEOLINKS(url):       
           link=OpenURL(url)
           #match=re.compile("'file': '(.+?)',").findall(link)
           match=re.compile('<iframe src="(.+?)" [^>]*').findall(link)
           if(len(match) == 0):
                match=re.compile('<iframe frameborder="0" [^>]*src="(.+?)">').findall(link)
                if(len(match)==0):
                   #match=re.compile('<iframe src="(.+?)" [^>]*').findall(link)
                   match=re.compile("'file': '(.+?)',").findall(link)
                   if(len(match) == 0):
                    match=re.compile('<div class="video_main">\s*<iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
                    if(len(match) == 0):
                     match = re.compile("var flashvars = {file: '(.+?)',").findall(link)        
                     if(len(match) == 0):       
                      match = re.compile('swfobject\.embedSWF\("(.+?)",').findall(link)
                      if(len(match) == 0):
                       match = re.compile("'file':\s*'(.+?)'").findall(link)
                       if(len(match) == 0):                    
                        match = re.compile('<iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
                        if(len(match) == 0):
                         match = re.compile('<source [^>]*src="([^"]+?)"').findall(link)       
           PLAYLIST_VIDEO_HOSTING(match[0])
           xbmcplugin.endOfDirectory(pluginhandle)
def PLAYLIST_VIDEO_HOSTING(vlink):
          
           if 'dailymotion' in vlink:                
                VideoURL = DAILYMOTION(vlink)
                print 'VideoURL: %s' % VideoURL
                PlayLIST_VIDEO(VideoURL)
           elif 'facebook.com' in vlink:
                VideoURL = FACEBOOK(vlink)
                print 'VideoURL: %s' % VideoURL
                PlayLIST_VIDEO(VideoURL)      
           elif 'google.com' in vlink:
                VideoURL = DOCS_GOOGLE(vlink)
                print 'VideoURL: %s' % VideoURL
                PlayLIST_VIDEO(VideoURL)
                
           elif 'vimeo' in vlink:
                 VideoURL = VIMEO(vlink)
                 print 'VideoURL: %s' % VideoURL
                 PlayLIST_VIDEO(VideoURL)

           elif 'vid.me' in vlink:                   
                VideoURL = VIDDME(vlink)
                print 'VideoURL: %s' % VideoURL
                #Play_VIDEO(urllib2.unquote(VideoURL).decode("utf8"))
                PlayLIST_VIDEO(VideoURL)
           elif 'sendvid.com' in vlink:
                VideoURL = SENDVID(vlink)
                print 'VideoURL: %s' % VideoURL
                xbmc.executebuiltin("XBMC.Notification(Please Wait!,Vidme Loading selected video)")
                #Play_VIDEO(urllib2.unquote(VideoURL[0]).decode("utf8"))
                PlayLIST_VIDEO(VideoURL)
           elif 'viddme' in vlink:
                VideoURL = vlink
                print 'VideoURL: %s' % VideoURL
                PlayLIST_VIDEO(VideoURL)
           
           elif 'az665436' in vlink:
                VideoURL = vlink
                print 'VideoURL: %s' % VideoURL
                PlayLIST_VIDEO(VideoURL)

           elif 'd1wst0behutosd' in vlink:
                VideoURL = vlink
                print 'VideoURL: %s' % VideoURL
                xbmc.executebuiltin("XBMC.Notification(Please Wait!,d1wst0behutosd Loading selected video)")
                PlayLIST_VIDEO(urllib2.unquote(VideoURL).decode("utf8"))
                #PlayLIST_VIDEO(VideoURL)

           elif 'videobam' in vlink:                
                VideoURL = vlink
                print 'VideoURL: %s' % VideoURL                
                PlayLIST_VIDEO(VideoURL)   

           elif 'youtube' in vlink:                   
                match=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(vlink)
                URL = match[0][len(match[0])-1].replace('v/','')                
                VideoURL = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + URL.replace('?','')               
                PlayLIST_VIDEO(VideoURL)

           elif 'youtu.be' in vlink:                   
                match=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(vlink)
                URL = match[0][len(match[0])-1].replace('v/','')
                VideoURL = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' + URL.replace('?','')               
                PlayLIST_VIDEO(VideoURL)     

           elif 'sharevids.net' in vlink:
                VideoURL = vlink
                print 'VideoURL: %s' % VideoURL
                PlayLIST_VIDEO(VideoURL)                     
           else:
                if 'vk.com' in vlink:
                       d = xbmcgui.Dialog()
                       d.ok('Not Implemented','Sorry videos on linksend.net does not work','Site seem to not exist')                
               
                else:
                    PlayLIST_VIDEO(urllib2.unquote(vlink).decode("utf8"))
                    #PlayLIST_VIDEO(vlink)

def PlayLIST_VIDEO(VideoURL):
    print 'PLAY VIDEO: %s' % VideoURL    
    item = xbmcgui.ListItem(path=VideoURL)
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.add(url=VideoURL, listitem=item)
    return xbmcplugin.setResolvedUrl(pluginhandle, True, item)
################### KARAOKE ********* END #######################


############# KORAOKE ####### START #########
def KHMERLOVES_MENU(url):     
        link = OpenURL(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        match=re.compile(' <li><a href="(.+?)" title=".+?"><span class="menu-title">(.+?)</span></a></li>').findall(link)
        for vurl,vname in match:
            addDir(vname,vurl,121,'')                
            match5=re.compile('<ul id="pagination-digg">(.+?)</ul>').findall(link)
        if(len(match5)):
            pages=re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(match5[0])
            for pageurl,pagenum in pages:
                addDir(" Page " + pagenum,pageurl.encode("utf-8"),120,"")                        
        xbmcplugin.endOfDirectory(pluginhandle)

def INDEX_KHMERLOVES(url):     
        link = OpenURL(url)
        try:
            link =link.encode("UTF-8")
        except: pass
        match=re.compile('<a title=".+?" href="(.+?)"><h4>(.+?)</h4></a>\n                <a title=".+?" href=".+?"><img src="(.+?)" width="175px" height="183px" /></a>').findall(link)
        for vurl,vname,vimage in match:                
            addDir(vname,vurl,125,vimage)
            match5=re.compile('<ul id="pagination-digg">(.+?)</ul>').findall(link)
        if(len(match5)):
            pages=re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(match5[0])
            for pageurl,pagenum in pages:
                addDir(" Page " + pagenum,pageurl.encode("utf-8"),121,"")                        
        xbmcplugin.endOfDirectory(pluginhandle)

def EPISODE_KHMERLOVES(url,name):    
        link = OpenURL(url)       
        match=re.compile('<a title="(.+?)" href="(.+?)"><img class="vimg120-jtmodule" src="(.+?)" border="0" width="120" height="90" /></a>').findall(link)     
        counter = 0
        videolist =''
        for vLinkName,vLink,vImage in match:                   
            counter +=1
            addLink(vLinkName,vLink,3,vImage)
            videolist=videolist+vLink+';#'
            if(counter==len(match) and (len(videolist.split(';#'))-1) > 0):
              addLink("[B][COLOR blue]-------Play the "+ str(len(videolist.split(';#'))-1)+" videos above--------[/B][/COLOR]",videolist,200,vImage)
              #videolist =''                 
        xbmcplugin.endOfDirectory(pluginhandle)

################ KORAOKE ########### END #########

def VIDEOLINKS(url):       
           
           link=OpenNET(url)
           url = re.compile('Base64.decode\("(.+?)"\)').findall(link)
           if(len(url) > 0):
            host=url[0].decode('base-64')
            match=re.compile('<iframe frameborder="0" [^>]*src="(.+?)"[^>]*>').findall(host)[0]
            VIDEO_HOSTING(match)
            #Play_VIDEO(match)
           else:
           #match=re.compile("'file': '(.+?)',").findall(link)
            match=re.compile('<IFRAME SRC="\r\n(.+?)" [^>]*').findall(link)
            if(len(match) == 0):
             match=re.compile('file:\s*"([^"]+?)"').findall(link)# Good Link
             if(len(match) == 0):
              match=re.compile('<iframe [^>]*src="(.+?)"').findall(link)
              if(len(match) == 0):
                match=re.compile('<iframe frameborder="0" [^>]*src="(.+?)">').findall(link)
                if(len(match)==0):
                 match=re.compile('<IFRAME SRC="(.+?)" [^>]*').findall(link)
                 if(len(match) == 0):   
                   #match=re.compile('<iframe [^>]*src="(.+?)" [^>]*').findall(link)
                   match=re.compile("'file': '(.+?)',").findall(link)
                   if(len(match) == 0):
                    match=re.compile('<div class="video_main">\s*<iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
                    if(len(match) == 0):
                     match = re.compile("var flashvars = {file: '(.+?)',").findall(link)        
                     if(len(match) == 0):       
                      match = re.compile('swfobject\.embedSWF\("(.+?)",').findall(link)
                      if(len(match) == 0):
                       match = re.compile("'file':\s*'(.+?)'").findall(link)
                       if(len(match) == 0):                    
                        match = re.compile('<iframe [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(link)
                        if(len(match)== 0):
                         match = re.compile('<source [^>]*src="([^"]+?)"').findall(link)
                         if(len(match) == 0):                    
                          match = re.compile('<script>\nvidId = \'(.+?)\'; \n</script>').findall(link)
                          for url in match:
                           vid = url[0].replace("['']", "")       
                           match ='https://docs.google.com/file/d/'+ (vid)+'/preview'
                           #REAL_VIDEO_HOST(match)
                           VIDEO_HOSTING(match)
                           print match
           VIDEO_HOSTING(match[0])
           print match
           xbmcplugin.endOfDirectory(pluginhandle)
   
def VIDEO_HOSTING(vlink):
          
           if 'dailymotion' in vlink:                
                VideoURL = DAILYMOTION(vlink)
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Dailymotion Loading selected video)")
                Play_VIDEO(VideoURL)
           elif 'facebook.com' in vlink:   
                VideoURL = FACEBOOK(vlink)
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Facebook Loading selected video)")
                Play_VIDEO(VideoURL)
                
           elif 'google.com' in vlink:   
                VideoURL = DOCS_GOOGLE(vlink)
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Google Loading selected video)")
                Play_VIDEO(VideoURL)
                
           elif 'vimeo' in vlink:
                 VideoURL = VIMEO(vlink)
                 print 'VideoURL: %s' % VideoURL
                 xbmc.executebuiltin("XBMC.Notification(Please Wait!,Vimeo Loading selected video)")
                 Play_VIDEO(VideoURL)

           elif 'vid.me' in vlink:                   
                VideoURL = VIDDME(vlink)
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Vid.me Loading selected video)")
                Play_VIDEO(VideoURL)
           elif 'sendvid.com' in vlink:
                VideoURL = SENDVID(vlink)
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Sendvid Loading selected video)")
                Play_VIDEO(VideoURL)
           elif 'viddme' in vlink:
                VideoURL = vlink
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Viddme Loading selected video)")
                Play_VIDEO(VideoURL)

           elif 'az665436' in vlink:
                VideoURL = vlink
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,AZ Loading selected video)")
                Play_VIDEO(VideoURL)

           elif 'd1wst0behutosd' in vlink:
                #link = OpenURL(vlink)   
                VideoURL = vlink
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,d1wst0behutosd Loading selected video)")
                Play_VIDEO(urllib2.unquote(VideoURL).decode("utf8"))# MP4
           #     Play_VIDEO(VideoURL)

           elif 'mp4upload.com' in vlink:
                VideoURL = MP4UPLOAD(vlink)
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,MP4UPLOAD Loading selected video)")
                Play_VIDEO(VideoURL)
           elif 'videobam' in vlink:  
                VideoURL = VIDEOBAM(vlink)
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Videobam Loading selected video)")                                
                Play_VIDEO(VideoURL)     

           elif 'sharevids.net' in vlink:
                VideoURL = vlink
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Sharevids Loading selected video)")
                Play_VIDEO(VideoURL)   
                    # d = xbmcgui.Dialog()
                    # d.ok('Not Implemented','Sorry videos on linksend.net does not work','Site seem to not exist')                
           elif 'videos4share.com' in vlink:
                VideoURL = vlink
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,videos4share Loading selected video)")
                #Play_VIDEO(VideoURL)
                Play_VIDEO(urllib2.unquote(VideoURL).decode("utf8"))# MP4
           elif 'youtu.be' in vlink:                   
                VideoURL = YOUTUBE(vlink)
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Youtube Loading selected video)")            
                Play_VIDEO(VideoURL)     

           elif 'youtube' in vlink:                   
                VideoURL = YOUTUBE(vlink)
                print 'VideoURL: %s' % VideoURL
                #xbmc.executebuiltin("XBMC.Notification(Please Wait!,Youtube Loading selected video)")
                Play_VIDEO(VideoURL)
           else:
                #if 'grayshare.net' in vlink:
                if 'share.net' in vlink:    
                    VideoURL = vlink
                    print 'VideoURL: %s' % VideoURL
                    Play_VIDEO(urllib2.unquote(VideoURL).decode("utf8"))    
                      # d = xbmcgui.Dialog()
                      # d.ok('Not Implemented','Sorry videos on linksend.net does not work','Site seem to not exist')                
               
                else:
                    print 'VideoURL: %s' % vlink
                    xbmc.executebuiltin("XBMC.Notification(Please Wait!,Let Try to Play These Video)")
                    Play_VIDEO(urllib2.unquote(vlink).decode("utf8"))
                    #VideoURL = urlresolver.HostedMediaFile(url=vlink).resolve()
                    #Play_VIDEO(VideoURL)

def OpenNET(url):
    try:
       net = Net(cookie_file=cookiejar)
       #net = Net(cookiejar)
       try:
            second_response = net.http_GET(url)
       except:
            second_response = net.http_GET(url.encode("utf-8"))
       return second_response.content
    except:
       d = xbmcgui.Dialog()
       d.ok(url,"Can't Connect to site",'Try again in a moment')
	

def Play_VIDEO(VideoURL):

    print 'PLAY VIDEO: %s' % VideoURL    
    item = xbmcgui.ListItem(path=VideoURL)
    return xbmcplugin.setResolvedUrl(pluginhandle, True, item)

###################### Resolver Start  ###################
def DAILYMOTION(SID):
        match=re.compile('(dailymotion\.com\/(watch\?(.*&)?v=|(embed|v|user|video)\/))([^\?&"\'>]+)').findall(SID)                
        SID = match[0][len(match[0])-1]
        vlink = 'http://www.dailymotion.com/embed/' + str(SID)
        link = OpenURL(vlink)
        matchFullHD = re.compile('"1080":.+?"url":"(.+?)"', re.DOTALL).findall(link)
        matchHD = re.compile('"720":.+?"url":"(.+?)"', re.DOTALL).findall(link)
        matchHQ = re.compile('"480":.+?"url":"(.+?)"', re.DOTALL).findall(link)
        matchSD = re.compile('"380":.+?"url":"(.+?)"', re.DOTALL).findall(link)
        matchLD = re.compile('"240":.+?"url":"(.+?)"', re.DOTALL).findall(link)
        if matchFullHD:
            VideoURL = urllib.unquote_plus(matchFullHD[0]).replace("\\", "/")
        elif matchHD:
            VideoURL = urllib.unquote_plus(matchHD[0]).replace("\\/", "/")
        elif matchHQ:
            VideoURL = urllib.unquote_plus(matchHQ[0]).replace("\\/", "/")
        elif matchSD:
            VideoURL = urllib.unquote_plus(matchSD[0]).replace("\\/", "/")
        elif matchLD:
            VideoURL = urllib.unquote_plus(matchLD[0]).replace("\\/", "/")
        return VideoURL

def DOCS_GOOGLE(Video_ID):
        SID=re.compile('/d/(.+?)/preview').findall(Video_ID)[0]
        URL = "https://docs.google.com/get_video_info?docid="+str(SID)
        print 'VIDEO html: %s' % URL
        req = urllib2.Request(URL)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.3')
        response = urllib2.urlopen(req)
        link=response.read()
        #print 'VIDEO Link: %s' % link  
        response.close()         
        vlink = urllib2.unquote(link)
        #print 'VIDEO html: %s' % vlink 
        #vlink = 'https://docs.google.com/file/'+str(link)+ '?pli=1'
        #print 'VIDEO VLINK: %s' % vlink
        #stream_map= re.compile('fmt_stream_map","(.+?)"').findall(vlink)[0].replace("\/", "/")
        stream_map= re.compile('fmt_stream_map=(.+?)&fmt_list').findall(vlink)[0].replace("\/", "/")
        formatArray = stream_map.split(',')
        for formatContent in formatArray:
            formatContentInfo = formatContent.split('|')
            #print 'VIDEO html: %s' % formatContentInfo
            qual = formatContentInfo[0]
            #VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            if(qual == '120'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '46'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '45'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '38'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '37'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '22'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '35'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '18'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '44'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '43'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '59'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '6'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '34'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '5'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            elif(qual == '36'):
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')
            else:
               VideoURL = (formatContentInfo[1]).decode('unicode-escape')     
        return VideoURL  

def FACEBOOK (SID):
       req = urllib2.Request(SID)
       req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.3')
       response = urllib2.urlopen(req)
       link=response.read()
       response.close()
       #vlink = 'http://www.facebook.com/video/video.php?v=' + str(link)
       vlink = re.compile('"params","([\w\%\-\.\\\]+)').findall(link)[0]
       print 'VIDEO Link: %s' % vlink 
       html = urllib.unquote(vlink.replace('\u0025', '%')).decode('utf-8')
       print 'VIDEO HTML: %s' % html 
       html = html.replace('\\', '')
       videoUrl = re.compile('(?:hd_src|sd_src)\":\"([\w\-\.\_\/\&\=\:\?]+)').findall(html)
       if len(videoUrl) > 0:    
           VideoURL =  videoUrl[0]
       else:
           VideoURL =  videoUrl
       return  VideoURL  

def MP4UPLOAD(SID):
       req = urllib2.Request(SID)
       req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.3')
       response = urllib2.urlopen(req)
       link=response.read()
       response.close()    
       VideoURL=re.compile('\'file\': \'(.+?)\'').findall(link)[0]
       return VideoURL

def SENDVID(SID):
        #Video_ID = urllib.unquote_plus(SID).replace("//", "http://")
        VID = urllib2.unquote(SID).replace("//", "http://")
        req = urllib2.Request(VID)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match = re.compile('<source src="([^"]+?)"').findall(link)
        #match = re.compile('<meta property="og:video:secure_url" content="([^"]+?)"').findall(link)
        #VideoURL = (match[0]).decode("utf-8")
        VideoURL =  urllib2.unquote(match[0]).replace("//", "http://")
        return VideoURL

def VIDDME(Video_ID):
        #req = urllib2.Request(Video_ID)
        #req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.3')
        #response = urllib2.urlopen(req)
        #link=response.read()
        #response.close()
        #match = re.compile('"(https://vid.me/[^"]+)"').findall(link)
       #for Video_ID in match:
            req = urllib2.Request(Video_ID)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.3')
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()    
            #VideoURL=re.compile('<source src="([^"]+?)"').findall(link)
            match = re.compile('<source src="([^"]+mp4[^"]+)"').findall(link)
            for URL in match:
                VideoURL =urllib2.unquote(URL).replace('&amp;','&')
            return VideoURL       

def VIDEOBAM(Video_ID):        
        req = urllib2.Request(Video_ID)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()               
        match=re.compile('"url"\s*:\s*"(.+?)","').findall(link)               
        for URL in match:
            if(URL.find("mp4") > -1):
               VideoURL = URL.replace("\\","")
        return VideoURL       

def VIMEO(Video_ID):
        HomeURL = ("http://"+Video_ID.split('/')[2])
        if 'player' in Video_ID:
            vlink =re.compile("//player.vimeo.com/video/(.+?)\?").findall(Video_ID+'?')
        elif 'vimeo' in Video_ID:
              vlink =re.compile("//vimeo.com/(.+?)\?").findall(Video_ID+'?')
        result = common.fetchPage({"link": "http://player.vimeo.com/video/%s/config?type=moogaloop&referrer=&player_url=player.vimeo.com&v=1.0.0&cdn_url=http://a.vimeocdn.com" % vlink[0],"refering": HomeURL})
        print 'Resultcommon: %s' % result
        collection = {}
        if result["status"] == 200:
            html = result["content"]
            print 'HTMLresult: %s' % html
            collection = json.loads(html)
            print 'COLLcommon: %s' % collection
            #codec = collection["request"]["files"]["codecs"][0]
            #video = collection["request"]["files"][codec]
            video = collection["request"]["files"]["progressive"]
            print 'VideoColl: %s' % video
            #if video.get("hd"):
            if(len(video) > 2):    
               #VideoURL = video['hd']['url']
               VideoURL = video[2]['url']
               print 'VideoSD: %s' % VideoURL
            else: 
               #VideoURL = video['sd']['url']
               VideoURL = video[0]['url']
               print 'VideoLD: %s' % VideoURL
        return VideoURL
def VIMEO1(Video_ID):
        HomeURL = ("http://"+Video_ID.split('/')[2])
        if 'player' in Video_ID:
            vlink =re.compile("//player.vimeo.com/video/(.+?)\?").findall(Video_ID+'?')
        elif 'vimeo' in Video_ID:
              vlink =re.compile("//vimeo.com/(.+?)\?").findall(Video_ID+'?')
        #result = common.fetchPage({"link": "http://player.vimeo.com/video/%s/config?type=moogaloop&referrer=&player_url=player.vimeo.com&v=1.0.0&cdn_url=http://a.vimeocdn.com" % vlink[0],"refering": HomeURL})
        result = common.fetchPage({"link": "http://player.vimeo.com/video/%s?title=0&byline=0&portrait=0" % vlink[0],"refering": HomeURL})        
        print 'Result: %s' % result
        collection = {}
        if result["status"] == 200:
            html = result["content"]
            html = html[html.find('={"cdn_url"')+1:]
            html = html[:html.find('}};')]+"}}"
            #print html
            collection = json.loads(html)
            print 'Collection: %s' %collection
            #codec = collection["request"]["files"]["codecs"][0]
            #print codec            
            video = collection["request"]["files"]["progressive"]#[0]
            #isHD = collection["request"]["files"][video]
            print 'VideoCOLL1: %s' % video
            if(len(video) > 2):
            #if video.get("720p"):
                VideoURL = video[2]['url']
                print 'VideoSD: %s' % VideoURL
            #elif(len(video) > 1):
            #    VideoURL = video[1]['url']
            #    print 'VideoSD: %s' % VideoURL
            else: 
               VideoURL = video[0]['url']
               print 'VideoLD: %s' % VideoURL
        return VideoURL
def YOUTUBE(SID):
        match=re.compile('(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)').findall(SID)
        if(len(match) > 0):
             URL = match[0][len(match[0])-1].replace('v/','')
        else:   
             match = re.compile('([^\?&"\'>]+)').findall(SID)
             URL = match[1].replace('v=','')
        VideoURL = 'plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=' +URL.replace('?','')     
        return VideoURL
###################### Resolver End  ###################        
def addLink(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultImage", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
        liz.setProperty('IsPlayable', 'true')
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
        return ok
		
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="http://www.merlkon.net/wp-contents/uploads/logo.jpg", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image', fanart)
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
play=None
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

		
sysarg=str(sys.argv[1]) 
if mode==None or url==None or len(url)<1:
        #OtherContent()
        HOME()
elif mode==3:
        VIDEOLINKS(url)
elif mode==4:
        VIDEO_HOSTING(url)
        
elif mode==10:
        MERLKONS()
elif mode==11:
        print ""+url
        INDEX_MERLKON(url)       
elif mode==12:
        INDEX_KHMERSTREAM(url)
elif mode==13:
        INDEX_KHMERAVE(url)
elif mode==15:
        EPISODE_MERLKON(url,name)

elif mode==20:
        JOLCHET()
elif mode==21:
        INDEX_J(url)
elif mode==23:
        INDEX_JJ(url)        
elif mode==22:
        MOVIE_J(url)
elif mode==25:
        EPISODE_J(url,name)
elif mode==26:
        EPISODE_MOVIEJ(url,name)

elif mode==30:
        VIDEO4YOU()
elif mode==31:
        INDEX_VIDEO4U(url)
elif mode==35:
        EPISODE_VIDEO4U(url,name)

elif mode==40:
        FILM2US()
elif mode==41:
        INDEX_FILM2US(url)        
elif mode==45:
        EPISODE_FILM2US(url)
elif mode==50:
        KHDRAMA2()
elif mode==51:
        INDEX_KHDRAMA(url)
elif mode==55:
        EPISODE_KHDRAMA(url,name)       
elif mode==80:
        K8MERHD()
elif mode==81:
        INDEX_K8MERHD(url)
elif mode==85:
        EPISODE_K8MERHD(url,name)
elif mode==90:
        TUBEKHMER()
elif mode==91:
        INDEX_TUBEKHMER(url)
elif mode==92:
        INDEX_PHUMIKHMER(url)
elif mode==95:
        EPISODE_TUBEKHMER(url,name)

elif mode==100:
        LAKORNKHMERS()
elif mode==101:
        INDEX_LAKORNKHMER(url)
elif mode==105:
        EPISODE_LAKORNKHMER(url,name)
############## START KARAOKE
elif mode==110:
        MUSIC_MENU(url,name)
elif mode==111:
        MUSIC_VIDEO(url)
elif mode==115:
        MUSIC_EP(url,name)       
elif mode==200:
        PLAYLIST_VIDEOLINKS(url)

elif mode==120:
        KHMERLOVES_MENU(url)
elif mode==121:
        INDEX_KHMERLOVES(url)
elif mode==125:
        EPISODE_KHMERLOVES(url,name)        
################ END KARAOKE
elif mode==130:
        KONKHMERALL()
elif mode==131:
        INDEX_KONKHMERALL(url)
elif mode==135:
        EPISODE_KONKHMERALL(url,name)
elif mode==60:
        KHMERKOMSAN()
elif mode==61:
        INDEX_KHMERKOMSAN(url)
elif mode==62:
        INDEX_KHMERKOMSAN_MOVIE(url)
elif mode==65:
        EPISODE_KHMERKOMSAN(url,name)         

xbmcplugin.endOfDirectory(int(sysarg))
        
