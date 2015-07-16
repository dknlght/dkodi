'''
Created on Dec 23, 2011

@author: ajju
'''
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD
from common import HttpUtils, AddonUtils
import re

def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://www.vidbux.com/images/vid_bux_logo_small.png')
    video_hosting_info.set_video_hosting_name('VidBux')
    return video_hosting_info
    
def retrieveVideoInfo(video_id):
    
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        HttpUtils.HttpClient().enableCookies()
        video_info_link = 'http://www.vidbux.com/' + str(video_id)
        html = HttpUtils.HttpClient().getHtmlContent(url=video_info_link)
        if re.search(r'Video bandwidth is expensive. We appreciate Your patience!', html):
            data = {'method_free': 'Continue to Video', 'op' : 'download1', 'usr_login' : '', 'id':str(video_id)}
            html = HttpUtils.HttpClient().getHtmlContent(url=video_info_link, params=data)
        
        HttpUtils.HttpClient().disableCookies()
        paramSet = re.compile("return p\}\(\'(.+?)\',(\d\d),(\d\d),\'(.+?)\'").findall(html)
        video_info_link = AddonUtils.parsePackedValue(paramSet[0][0], int(paramSet[0][1]), int(paramSet[0][2]), paramSet[0][3].split('|')).replace('\\', '').replace('"', '\'')
        
        img_data = re.compile(r"addVariable\(\'image\',\'(.+?)\'\);").findall(video_info_link)
        if len(img_data) == 1:
            video_info.set_video_image(img_data[0])
        video_link = re.compile("addVariable\(\'file\',\'(.+?)\'\);").findall(video_info_link)[0]
        
        video_info.set_video_stopped(False)
        video_info.add_video_link(VIDEO_QUAL_SD, video_link)
        
    except: 
        video_info.set_video_stopped(True)
    return video_info

