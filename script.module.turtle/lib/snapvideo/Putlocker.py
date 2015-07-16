'''
Created on Nov 21, 2012

@author: ajju
'''
from common.DataObjects import VideoHostingInfo
from snapvideo import UrlResolverDelegator

def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://www.mundopremium.com/imagem/index/1261870/M/putlocker_logo_300.gif')
    video_hosting_info.set_video_hosting_name('PutLocker')
    return video_hosting_info

def retrieveVideoInfo(video_id):
    videoUrl = "http://www.putlocker.com/file/" + video_id
    return UrlResolverDelegator.retrieveVideoInfo(videoUrl)