'''
Created on Oct 29, 2011

@author: ajju
'''
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_LOW, \
    VIDEO_QUAL_SD, VIDEO_QUAL_HD_720, VIDEO_QUAL_HD_1080
from common import HttpUtils
import re
import urllib
import logging

def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://www.automotivefinancingsystems.com/images/icons/socialmedia_youtube_256x256.png')
    video_hosting_info.set_video_hosting_name('YouTube')
    return video_hosting_info

def retrieveVideoInfo(video_id):
    
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        video_info.set_video_image('http://i.ytimg.com/vi/' + video_id + '/default.jpg')
        html = HttpUtils.HttpClient().getHtmlContent(url='http://www.youtube.com/get_video_info?video_id=' + video_id + '&asv=3&el=detailpage&hl=en_US')
        stream_map = None
        html = html.decode('utf8')
        html = html.replace('\n', '')
        html = html.replace('\r', '')
        html = html + '&'
        title = urllib.unquote_plus(re.compile('&title=(.+?)&').findall(html)[0]).replace('/\+/g', ' ')
        print title
        if re.search('status=fail', html):
            video_info.set_video_stopped(True)
            return video_info
        
        stream_info = re.compile('url_encoded_fmt_stream_map=(.+?)&').findall(html)
        stream_map = ''
        if(len(stream_info) == 0):
            stream_map = re.compile('fmt_stream_map": "(.+?)"').findall(html)[0].replace("\\/", "/")
        else:
            stream_map = stream_info[0]
            
        if stream_map == None:
            video_info.set_video_stopped(True)
            return video_info
        
        stream_map = urllib.unquote_plus(stream_map)

        
        formatArray = stream_map.split(',')
        for formatContent in formatArray:
            if formatContent == '':
                continue
            formatUrl = ""
            try:
                formatUrl = urllib.unquote(re.compile("url=([^&]+)").findall(formatContent)[0]) + "&title=" + urllib.quote_plus(title)   
            except:
                    print "Unexpected error"     
            if re.search("rtmpe", stream_map):
                try:
                    conn = urllib.unquote(re.compile("conn=([^&]+)").findall(formatContent)[0]);
                    host = re.compile("rtmpe:\/\/([^\/]+)").findall(conn)[0];
                    stream = re.compile("stream=([^&]+)").findall(formatContent)[0];
                    path = 'videoplayback';
                    
                    formatUrl = "-r %22rtmpe:\/\/" + host + "\/" + path + "%22 -V -a %22" + path + "%22 -f %22WIN 11,3,300,268%22 -W %22http:\/\/s.ytimg.com\/yt\/swfbin\/watch_as3-vfl7aCF1A.swf%22 -p %22http:\/\/www.youtube.com\/watch?v=" + video_id + "%22 -y %22" + urllib.unquote(stream) + "%22"
                except:
                    print "Unexpected error"
                
            if(formatUrl[0: 4] == "http" or formatUrl[0: 2] == "-r"):
                formatQual = re.compile("itag=([^&]+)").findall(formatContent)[0]
                if not re.search("signature=", formatUrl):
                    formatUrl += "&signature=" + re.compile("sig=([^&]+)").findall(formatContent)[0]
        
            qual = formatQual
            url = formatUrl
            if(qual == '13'):  # 176x144
                video_info.add_video_link(VIDEO_QUAL_LOW, url)
            elif(qual == '17'):  # 176x144
                video_info.add_video_link(VIDEO_QUAL_LOW, url)
            elif(qual == '36'):  # 320x240
                video_info.add_video_link(VIDEO_QUAL_LOW, url)
            elif(qual == '5'):  # 400\\327226
                video_info.add_video_link(VIDEO_QUAL_LOW, url)
            elif(qual == '34'):  # 480x360 FLV
                video_info.add_video_link(VIDEO_QUAL_SD, url)
            elif(qual == '6'):  # 640\\327360 FLV
                video_info.add_video_link(VIDEO_QUAL_SD, url)
            elif(qual == '35'):  # 854\\327480 HD
                video_info.add_video_link(VIDEO_QUAL_SD, url)
            elif(qual == '18'):  # 480x360 MP4
                video_info.add_video_link(VIDEO_QUAL_SD, url)
            elif(qual == '22'):  # 1280x720 MP4
                video_info.add_video_link(VIDEO_QUAL_HD_720, url)
            elif(qual == '37'):  # 1920x1080 MP4
                video_info.add_video_link(VIDEO_QUAL_HD_1080, url)
            elif(qual == '38' and video_info.get_video_link(VIDEO_QUAL_HD_1080) is None):  # 4096\\3272304 EPIC MP4
                video_info.add_video_link(VIDEO_QUAL_HD_1080, url)
            elif(qual == '43' and video_info.get_video_link(VIDEO_QUAL_SD) is None):  # 360 WEBM
                video_info.add_video_link(VIDEO_QUAL_SD, url)
            elif(qual == '44'):  # 480 WEBM
                video_info.add_video_link(VIDEO_QUAL_SD, url)
            elif(qual == '45' and video_info.get_video_link(VIDEO_QUAL_HD_720) is None):  # 720 WEBM
                video_info.add_video_link(VIDEO_QUAL_HD_720, url)
            elif(qual == '46' and video_info.get_video_link(VIDEO_QUAL_HD_1080) is None):  # 1080 WEBM
                video_info.add_video_link(VIDEO_QUAL_HD_1080, url)
            elif(qual == '120' and video_info.get_video_link(VIDEO_QUAL_HD_720) is None):  # New video qual
                video_info.add_video_link(VIDEO_QUAL_HD_720, url)
                # 3D streams - MP4
                # 240p -> 83
                # 360p -> 82
                # 520p -> 85
                # 720p -> 84
                # 3D streams - WebM
                # 360p -> 100
                # 360p -> 101
                # 720p -> 102
            else:  # unknown quality
                video_info.add_video_link(VIDEO_QUAL_SD, url)

            video_info.set_video_stopped(False)
    except Exception, e:
        logging.exception(e)
        video_info.set_video_stopped(True)
    return video_info

def retrievePlaylistVideoItems(playlistId):
    soupXml = HttpUtils.HttpClient().getBeautifulSoup('http://gdata.youtube.com/feeds/api/playlists/' + playlistId)
    videoItemsList = []
    for media in soupXml.findChildren('media:player'):
        videoUrl = str(media['url'])
        videoItemsList.append(videoUrl)
    return videoItemsList
    
def retrieveReloadedPlaylistVideoItems(playlistId):
    soupXml = HttpUtils.HttpClient().getBeautifulSoup('http://gdata.youtube.com/feeds/api/playlists/' + playlistId)
    videoItemsList = []
    for media in soupXml.findChildren('track'):
        videoUrl = media.findChild('location').getText()
        videoItemsList.append(videoUrl)
    return videoItemsList
    
