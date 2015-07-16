'''
Created on Nov 26, 2011

@author: ajju
'''
from common.DataObjects import VideoHostingInfo, VideoInfo, VIDEO_QUAL_SD
from common import HttpUtils
import re
import urllib

def getVideoHostingInfo():
    video_hosting_info = VideoHostingInfo()
    video_hosting_info.set_video_hosting_image('http://media.handywebapps.com/2011/08/megavideo.png')
    video_hosting_info.set_video_hosting_name('Megavideo')
    return video_hosting_info

def retrieveVideoInfo(video_id):
    video_info = VideoInfo()
    video_info.set_video_hosting_info(getVideoHostingInfo())
    video_info.set_video_id(video_id)
    try:
        video_link = 'http://www.megavideo.com/xml/videolink.php?v=' + str(video_id)
        html = HttpUtils.HttpClient().getHtmlContent(url=video_link)
        html = ''.join(html.splitlines()).replace('\t', '').replace('\'', '"')
        
        un = re.compile(' un="(.+?)"').findall(html)
        k1 = re.compile(' k1="(.+?)"').findall(html)
        k2 = re.compile(' k2="(.+?)"').findall(html)
        hashresult = decrypt(un[0], k1[0], k2[0])
        
        s = re.compile(' s="(.+?)"').findall(html)
        
        title = re.compile(' title="(.+?)"').findall(html)
        videoTitle = urllib.unquote_plus(title[0].replace('+', ' ').replace('.', ' '))
        
        video_link = "http://www" + s[0] + ".megavideo.com/files/" + hashresult + "/" + videoTitle.replace('www.apnajoy.com', '') + ".flv";
        video_info.set_video_stopped(False)
        video_info.set_video_name(videoTitle)
        video_info.add_video_link(VIDEO_QUAL_SD, video_link)
    except:
        video_info.set_video_stopped(True)
    return video_info


def ajoin(arr):
        strtest = ''
        for num in range(len(arr)):
                strtest = strtest + str(arr[num])
        return strtest

def asplit(mystring):
        arr = []
        for num in range(len(mystring)):
                arr.append(mystring[num])
        return arr
                

def decrypt(str1, key1, key2):

        __reg1 = []
        __reg3 = 0
        while (__reg3 < len(str1)):
                __reg0 = str1[__reg3]
                holder = __reg0
                if (holder == "0"):
                        __reg1.append("0000")
                else:
                        if (__reg0 == "1"):
                                __reg1.append("0001")
                        else:
                                if (__reg0 == "2"): 
                                        __reg1.append("0010")
                                else: 
                                        if (__reg0 == "3"):
                                                __reg1.append("0011")
                                        else: 
                                                if (__reg0 == "4"):
                                                        __reg1.append("0100")
                                                else: 
                                                        if (__reg0 == "5"):
                                                                __reg1.append("0101")
                                                        else: 
                                                                if (__reg0 == "6"):
                                                                        __reg1.append("0110")
                                                                else: 
                                                                        if (__reg0 == "7"):
                                                                                __reg1.append("0111")
                                                                        else: 
                                                                                if (__reg0 == "8"):
                                                                                        __reg1.append("1000")
                                                                                else: 
                                                                                        if (__reg0 == "9"):
                                                                                                __reg1.append("1001")
                                                                                        else: 
                                                                                                if (__reg0 == "a"):
                                                                                                        __reg1.append("1010")
                                                                                                else: 
                                                                                                        if (__reg0 == "b"):
                                                                                                                __reg1.append("1011")
                                                                                                        else: 
                                                                                                                if (__reg0 == "c"):
                                                                                                                        __reg1.append("1100")
                                                                                                                else: 
                                                                                                                        if (__reg0 == "d"):
                                                                                                                                __reg1.append("1101")
                                                                                                                        else: 
                                                                                                                                if (__reg0 == "e"):
                                                                                                                                        __reg1.append("1110")
                                                                                                                                else: 
                                                                                                                                        if (__reg0 == "f"):
                                                                                                                                                __reg1.append("1111")

                __reg3 = __reg3 + 1

        mtstr = ajoin(__reg1)
        __reg1 = asplit(mtstr)
        __reg6 = []
        __reg3 = 0
        while (__reg3 < 384):
        
                key1 = (int(key1) * 11 + 77213) % 81371
                key2 = (int(key2) * 17 + 92717) % 192811
                __reg6.append((int(key1) + int(key2)) % 128)
                __reg3 = __reg3 + 1
        
        __reg3 = 256
        while (__reg3 >= 0):

                __reg5 = __reg6[__reg3]
                __reg4 = __reg3 % 128
                __reg8 = __reg1[__reg5]
                __reg1[__reg5] = __reg1[__reg4]
                __reg1[__reg4] = __reg8
                __reg3 = __reg3 - 1
        
        __reg3 = 0
        while (__reg3 < 128):
        
                __reg1[__reg3] = int(__reg1[__reg3]) ^ int(__reg6[__reg3 + 256]) & 1
                __reg3 = __reg3 + 1

        __reg12 = ajoin(__reg1)
        __reg7 = []
        __reg3 = 0
        while (__reg3 < len(__reg12)):

                __reg9 = __reg12[__reg3:__reg3 + 4]
                __reg7.append(__reg9)
                __reg3 = __reg3 + 4
                
        
        __reg2 = []
        __reg3 = 0
        while (__reg3 < len(__reg7)):
                __reg0 = __reg7[__reg3]
                holder2 = __reg0
        
                if (holder2 == "0000"):
                        __reg2.append("0")
                else: 
                        if (__reg0 == "0001"):
                                __reg2.append("1")
                        else: 
                                if (__reg0 == "0010"):
                                        __reg2.append("2")
                                else: 
                                        if (__reg0 == "0011"):
                                                __reg2.append("3")
                                        else: 
                                                if (__reg0 == "0100"):
                                                        __reg2.append("4")
                                                else: 
                                                        if (__reg0 == "0101"): 
                                                                __reg2.append("5")
                                                        else: 
                                                                if (__reg0 == "0110"): 
                                                                        __reg2.append("6")
                                                                else: 
                                                                        if (__reg0 == "0111"): 
                                                                                __reg2.append("7")
                                                                        else: 
                                                                                if (__reg0 == "1000"): 
                                                                                        __reg2.append("8")
                                                                                else: 
                                                                                        if (__reg0 == "1001"): 
                                                                                                __reg2.append("9")
                                                                                        else: 
                                                                                                if (__reg0 == "1010"): 
                                                                                                        __reg2.append("a")
                                                                                                else: 
                                                                                                        if (__reg0 == "1011"): 
                                                                                                                __reg2.append("b")
                                                                                                        else: 
                                                                                                                if (__reg0 == "1100"): 
                                                                                                                        __reg2.append("c")
                                                                                                                else: 
                                                                                                                        if (__reg0 == "1101"): 
                                                                                                                                __reg2.append("d")
                                                                                                                        else: 
                                                                                                                                if (__reg0 == "1110"): 
                                                                                                                                        __reg2.append("e")
                                                                                                                                else: 
                                                                                                                                        if (__reg0 == "1111"): 
                                                                                                                                                __reg2.append("f")
                                                                                                                                        
                __reg3 = __reg3 + 1

        endstr = ajoin(__reg2)
        return endstr
