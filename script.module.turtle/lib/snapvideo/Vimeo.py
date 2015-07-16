'''
Created on Dec 24, 2011

@author: ajju
'''
from BeautifulSoup import BeautifulStoneSoup
from common import HttpUtils
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD, \
    VIDEO_QUAL_HD_720

def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://cdn1.iconfinder.com/data/icons/Social_Networking_Icons_PNG/PNG/Vimeo.png')
    video_hosting_info.set_video_hosting_name('Vimeo')
    return video_hosting_info
    
def retrieveVideoInfo(video_id):
    
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        video_info_link = 'http://www.vimeo.com/moogaloop/load/clip:' + str(video_id)
        soup = BeautifulStoneSoup(HttpUtils.HttpClient().getHtmlContent(url=video_info_link), convertEntities=BeautifulStoneSoup.XML_ENTITIES)
        
        referrerObj = soup.findChild(name='referrer')
        req_sig = referrerObj.findChild(name='request_signature').getText()
        req_sig_exp = referrerObj.findChild(name='request_signature_expires').getText()
        
        videoObj = soup.findChild(name='video')
        img_link = videoObj.findChild(name='thumbnail').getText()
        video_title = videoObj.findChild(name='caption').getText()
        
        qual = 'sd'
        video_link = "http://player.vimeo.com/play_redirect?clip_id=%s&sig=%s&time=%s&quality=%s&codecs=H264,VP8,VP6&type=moogaloop_local&embed_location=" % (video_id, req_sig, req_sig_exp, qual)
        video_info.add_video_link(VIDEO_QUAL_SD, video_link)
        
        if(videoObj.findChild(name='ishd').getText() == '1'):
            qual = 'hd'
            video_link = "http://player.vimeo.com/play_redirect?clip_id=%s&sig=%s&time=%s&quality=%s&codecs=H264,VP8,VP6&type=moogaloop_local&embed_location=" % (video_id, req_sig, req_sig_exp, qual)
            video_info.add_video_link(VIDEO_QUAL_HD_720, video_link)
            
        video_info.set_video_stopped(False)
        video_info.set_video_image(img_link)
        video_info.set_video_name(video_title)
        
    except: 
        video_info.set_video_stopped(True)
    return video_info
