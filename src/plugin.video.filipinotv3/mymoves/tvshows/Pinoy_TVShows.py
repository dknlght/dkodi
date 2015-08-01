'''
Created on Dec 24, 2011

@author: ajju
'''
from TurtleContainer import AddonContext
from common import AddonUtils, XBMCInterfaceUtils
from common.DataObjects import ListItem
import xbmcgui #@UnresolvedImport
import BeautifulSoup
from common.HttpUtils import HttpClient
import re
from moves import SnapVideo
from snapvideo import YouTube
from t0mm0.common.net import Net

def displayTVShowsMenu(request_obj, response_obj):
    # GMA
    item = ListItem()
    item.set_next_action_name('TV_Channel_GMA')
    item.add_request_data('tvChannelUrl', 'http://mypinoytvonline.blogspot.com/search/label/GMA')
    xbmcListItem = xbmcgui.ListItem(label='GMA', iconImage='http://www.lyngsat-logo.com/logo/tv/gg/gma.jpg', thumbnailImage='http://www.lyngsat-logo.com/logo/tv/gg/gma.jpg')
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    # ABS-CBN
    item = ListItem()
    item.set_next_action_name('TV_Channel_ABS_CBN')
    item.add_request_data('tvChannelUrl', 'http://mypinoytvonline.blogspot.com/search/label/ABS-CBN')
    xbmcListItem = xbmcgui.ListItem(label='ABS-CBN', iconImage='http://www.lyngsat-logo.com/logo/tv/aa/abs_cbn.jpg', thumbnailImage='http://www.lyngsat-logo.com/logo/tv/aa/abs_cbn.jpg')
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    # TV5
    item = ListItem()
    item.set_next_action_name('TV_Channel_TV5')
    item.add_request_data('tvChannelUrl', 'http://mypinoytvonline.blogspot.com/search/label/TV%205')
    xbmcListItem = xbmcgui.ListItem(label='TV 5', iconImage='http://www.lyngsat-logo.com/logo/tv/tt/tv5_ph.jpg', thumbnailImage='http://www.lyngsat-logo.com/logo/tv/tt/tv5_ph.jpg')
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # ALL
    tvshows_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='tvShows.png')
    item = ListItem()
    item.set_next_action_name('TV_Channel_ALL')
    item.add_request_data('tvChannelUrl', 'http://mypinoytvonline.blogspot.com/')
    xbmcListItem = xbmcgui.ListItem(label='All TV Shows', iconImage=tvshows_icon_filepath, thumbnailImage=tvshows_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # Search TV
    search_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='search.png')
    item = ListItem()
    item.set_next_action_name('TV_Channel_Search')
    item.add_request_data('tvChannelUrl', 'http://mypinoytvonline.blogspot.com/search?q=')
    xbmcListItem = xbmcgui.ListItem(label='Search TV', iconImage=search_icon_filepath, thumbnailImage=search_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)

def GetContent(url):

       net = Net()
       second_response = net.http_GET(url)
       return second_response.content

def displayTVShowEpisodes(request_obj, response_obj):
    url = request_obj.get_data()['tvChannelUrl']
    contentDiv = GetContent(url)
    newcontent = ''.join(contentDiv.encode("utf-8").splitlines()).replace('\t','')
    contentDiv = BeautifulSoup.SoupStrainer('div', {'id':'content'})
    soup = HttpClient().getBeautifulSoup(url=url, parseOnlyThese=contentDiv)
    videoBoxes =re.compile("<div id='videobox'>(.+?)</h3><div style='clear: both;'>").findall(newcontent)
    for videoBox in videoBoxes:
        #imgTag = videoBox.findChild('img')
        imageUrl = re.compile('<img [^>]*src=["\']?([^>^"^\']+)["\']?[^>]*>').findall(str(videoBox))[0]
        match=re.compile('createSummaryThumb\("(.+?)","(.+?)","(.+?)",').findall(str(videoBox))
        if(len(match)>0):
            episodeName = match[0][1]
            episodeUrl = str(match[0][2])
            
            item = ListItem()
            item.add_request_data('episodeName', episodeName)
            item.add_request_data('episodeUrl', episodeUrl)
            item.set_next_action_name('Show_Episode_VLinks')
            xbmcListItem = xbmcgui.ListItem(label=episodeName, iconImage=imageUrl, thumbnailImage=imageUrl)
            item.set_xbmc_list_item_obj(xbmcListItem)
            response_obj.addListItem(item)
    pageTag = soup.findChild('div', {'class':'postnav'})
    if(pageTag !=None):
        olderPageTag = pageTag.findChild('a', {'class':'blog-pager-older-link'})
    else:
        olderPageTag = None
    if olderPageTag is not None:
        item = ListItem()
        item.add_request_data('tvChannelUrl', str(olderPageTag['href']))
        pageName = AddonUtils.getBoldString('              ->              Next Page')
        item.set_next_action_name('Show_Episodes_Next_Page')
        xbmcListItem = xbmcgui.ListItem(label=pageName)
        item.set_xbmc_list_item_obj(xbmcListItem)
        response_obj.addListItem(item)
    
    
def displayAllTVShows(request_obj, response_obj):
    url = request_obj.get_data()['tvChannelUrl']
    contentDiv = BeautifulSoup.SoupStrainer('div', {'class':'rightwidget'})
    soup = HttpClient().getBeautifulSoup(url=url, parseOnlyThese=contentDiv)
    tvshows = soup.findChildren('a')
    for tvshow in tvshows:
        tvshowName = tvshow.getText()
        tvshowUrl = str(tvshow['href'])
        
        item = ListItem()
        item.add_request_data('tvshowName', tvshowName)
        item.add_request_data('tvshowUrl', tvshowUrl)
        item.add_request_data('tvChannelUrl', tvshowUrl)
        item.set_next_action_name('Show_Episodes')
        xbmcListItem = xbmcgui.ListItem(label=tvshowName)
        item.set_xbmc_list_item_obj(xbmcListItem)
        response_obj.addListItem(item)


def searchTVShows(request_obj, response_obj):
    search_text = XBMCInterfaceUtils.getUserInput(heading='Enter search text')
    newtvChannelUrl = request_obj.get_data()['tvChannelUrl'] + search_text
    request_obj.get_data()['tvChannelUrl'] = newtvChannelUrl
    response_obj.set_redirect_action_name('Search_Episodes')


def retrieveVideoLinks(request_obj, response_obj):
    
    video_source_id = 1
    video_source_img = None
    video_part_index = 0
    video_playlist_items = []
    #ignoreAllLinks = False
    
    url = request_obj.get_data()['episodeUrl']
    contentDiv = BeautifulSoup.SoupStrainer('div', {'class':'entry'})
    soup = HttpClient().getBeautifulSoup(url=url, parseOnlyThese=contentDiv)
    soup = soup.findChild('div')
    for child in soup.findChildren():
        if child.name == 'img' or child.name == 'param' or child.name == 'object' or child.name == 'b' or child.name == 'font' or child.name == 'br':
            pass
        elif child.name == 'span' and re.search('ALTERNATIVE VIDEO', child.getText(), re.IGNORECASE):
            if len(video_playlist_items) > 0:
                response_obj.addListItem(__preparePlayListItem__(video_source_id, video_source_img, video_playlist_items))
                
            video_source_id = video_source_id + 1
            video_source_img = None
            video_part_index = 0
            video_playlist_items = []
            #ignoreAllLinks = False
        elif child.name == 'embed' or child.name == 'iframe':
            
            if re.search('http://gdata.youtube.com/feeds/api/playlists/', str(child)) or re.search('http://www.youtubereloaded.com/playlists/', str(child)):
                playlistId = re.compile('/playlists/(.+?)(\&|\.xml)').findall(str(child))[0][0]
                
                videoUrls = YouTube.retrievePlaylistVideoItems(playlistId)
                for videoUrl in videoUrls:
                    try:
                        video_part_index = video_part_index + 1
                        video_link = {}
                        video_link['videoTitle'] = 'Source #' + str(video_source_id) + ' | ' + 'Part #' + str(video_part_index)
                        video_link['videoLink'] = videoUrl
                        print "myvidlink"+videoUrl
                        video_hosting_info = SnapVideo.findVideoHostingInfo(video_link['videoLink'])
                        video_link['videoSourceImg'] = video_hosting_info.get_video_hosting_image()
                        
                        video_playlist_items.append(video_link)
                        video_source_img = video_link['videoSourceImg']
                        
                        item = ListItem()
                        item.add_request_data('videoLink', video_link['videoLink'])
                        item.add_request_data('videoTitle', video_link['videoTitle'])
                        item.set_next_action_name('SnapAndPlayVideo')
                        xbmcListItem = xbmcgui.ListItem(label='Source #' + str(video_source_id) + ' | ' + 'Part #' + str(video_part_index) , iconImage=video_source_img, thumbnailImage=video_source_img)
                        item.set_xbmc_list_item_obj(xbmcListItem)
                        response_obj.addListItem(item)
                    except:
                        print 'Unable to recognize a source = ' + video_link['videoLink']
                        video_source_img = None
                        video_part_index = 0
                        video_playlist_items = []
                        #ignoreAllLinks = True
                    
            else:

                videoUrl = str(child['src'])
                
                try:
                    video_part_index = video_part_index + 1
                    video_link = {}
                    video_link['videoTitle'] = 'Source #' + str(video_source_id) + ' | ' + 'Part #' + str(video_part_index)
                    video_link['videoLink'] = videoUrl
                    print "myvidlink"+videoUrl
                    video_hosting_info = SnapVideo.findVideoHostingInfo(video_link['videoLink'])
                    video_link['videoSourceImg'] = video_hosting_info.get_video_hosting_image()
                    
                    video_playlist_items.append(video_link)
                    video_source_img = video_link['videoSourceImg']
                    
                    item = ListItem()
                    item.add_request_data('videoLink', video_link['videoLink'])
                    item.add_request_data('videoTitle', video_link['videoTitle'])
                    item.set_next_action_name('SnapAndPlayVideo')
                    xbmcListItem = xbmcgui.ListItem(label='Source #' + str(video_source_id) + ' | ' + 'Part #' + str(video_part_index) , iconImage=video_source_img, thumbnailImage=video_source_img)
                    item.set_xbmc_list_item_obj(xbmcListItem)
                    response_obj.addListItem(item)
                except:
                    print 'Unable to recognize a source = ' + video_link['videoLink']
                    video_source_img = None
                    video_part_index = 0
                    video_playlist_items = []
                    #ignoreAllLinks = True
        else:
            print 'UNKNOWN child name'
            print child
            
    if len(video_playlist_items) > 0:
        response_obj.addListItem(__preparePlayListItem__(video_source_id, video_source_img, video_playlist_items))
            
    
def __preparePlayListItem__(video_source_id, video_source_img, video_playlist_items):
    item = ListItem()
    item.add_request_data('videoPlayListItems', video_playlist_items)
    item.set_next_action_name('SnapAndDirectPlayList')
    xbmcListItem = xbmcgui.ListItem(label=AddonUtils.getBoldString('DirectPlay') + ' | ' + 'Source #' + str(video_source_id) + ' | ' + 'Parts = ' + str(len(video_playlist_items)) , iconImage=video_source_img, thumbnailImage=video_source_img)
    item.set_xbmc_list_item_obj(xbmcListItem)
    return item


