'''
Created on Nov 12, 2011

@author: ajju
'''
import xbmcgui, xbmcplugin, xbmc #@UnresolvedImport
import urllib
from common.Singleton import SingletonClass
from common import AddonUtils, ExceptionHandler
import sys
import logging

SUPPRESS_DIALOG_MSG = False

def setSuppressDialogMsg(suppressMsg=False):
    global SUPPRESS_DIALOG_MSG
    if suppressMsg:
        SUPPRESS_DIALOG_MSG = True
    else:
        SUPPRESS_DIALOG_MSG = False


def updateListItem_With_VideoHostingInfo(video_hosting_info, xbmc_list_item):
    new_label = video_hosting_info.get_video_hosting_name()
    if new_label is not None and new_label != '':
        new_label = xbmc_list_item.getLabel()
    xbmc_list_item.setLabel(new_label)
    xbmc_list_item.setThumbnailImage(video_hosting_info.get_video_hosting_image())


def updateListItem_With_VideoInfo(video_info, xbmc_list_item):
    new_label = video_info.get_video_hosting_info().get_video_hosting_name()
    if new_label is not None and new_label != '':
        new_label = video_info.get_video_name()
    xbmc_list_item.setLabel(new_label)
    xbmc_list_item.setThumbnailImage(video_info.get_video_image())
    
    
def callBackDialogProgressBar(function_obj, function_args, heading, failure_message, line1='Please wait...', line2='Retrieved $current_index of $total_it items', line3='To go back, press the Cancel button'):
    total_iteration = len(function_args)
    current_index = 0
    ProgressDisplayer().end()
    pDialog = None
    if not SUPPRESS_DIALOG_MSG:
        pDialog = xbmcgui.DialogProgress()
        pDialog.create(heading, line1, line2.replace('$total_it', str(total_iteration)).replace('$current_index', str(current_index)), line3)
        pDialog.update(1)
    print 'Total Iterations = ' + str(total_iteration)
    function_returns = []
    isCanceled = False
    for arg in function_args:
        try:
            returnedObj = function_obj(arg)
            if returnedObj is not None and type(returnedObj) is list:
                function_returns.extend(returnedObj)
            elif returnedObj is not None:
                function_returns.append(returnedObj)
            if not SUPPRESS_DIALOG_MSG and pDialog is not None:
                current_index = current_index + 1
                percent = (current_index * 100) / total_iteration
                pDialog.update(percent, line1, line2.replace('$total_it', str(total_iteration)).replace('$current_index', str(current_index)), line3)
                if (pDialog.iscanceled()):
                    isCanceled = True
                    break
        except Exception, e:
            if not SUPPRESS_DIALOG_MSG and pDialog is not None:
                pDialog.close()
                dialog = xbmcgui.Dialog()
                dialog.ok('Process Failed', failure_message, 'You may like to try again later or use other source if available')
            print 'ERROR OCCURRED :: ' + str(e)
            logging.exception(e)
            raise Exception(ExceptionHandler.DONOT_DISPLAY_ERROR, '')
        if isCanceled:
            raise Exception(ExceptionHandler.PROCESS_STOPPED, 'It looks like you don\'t want wait more|Process was stopped in between')
    return function_returns
    
def sortItems(xbmc_sort_method):
    xbmcplugin.addSortMethod(handle=int(sys.argv[1]), sortMethod=xbmc_sort_method)
    
def setContentType(content_type):
    xbmcplugin.setContent(handle=int(sys.argv[1]), content=content_type)

def addFolderItem(item, item_next_action_id, is_folder=True):
    u = sys.argv[0] + '?actionId=' + urllib.quote_plus(item_next_action_id) + '&data=' + urllib.quote_plus(AddonUtils.encodeData(item.get_request_data()))
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=item.get_xbmc_list_item_obj(), isFolder=is_folder)

def addPlayListItem(item):
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.add(url=item.get_moving_data()['videoStreamUrl'], listitem=item.get_xbmc_list_item_obj())
    
def clearPlayList():
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    playlist.clear()
    
def play(videoSrc=None):
    if videoSrc == None:
        videoSrc = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(videoSrc)
    #if not xbmcPlayer.isPlayingVideo():
    #        d = xbmcgui.Dialog()
    #        d.ok('Playback Failed!', 'XBMC player failed to play the playlist items', 'Please check again later or look for other options')
    
def isPlayingVideo():
    return xbmc.Player().isPlayingVideo()        

class ProgressDisplayer(SingletonClass):
    
    def __initialize__(self):
#        self.pDialog = xbmcgui.DialogProgress()
        pass
        
        
    def start(self, heading='', line1='', line2='', line3=''):
#        self.pDialog.create(heading, line1, line2, line3)
#        self.pDialog.update(1)
        pass
        
        
    def displayMessage(self, percent=1, line1='', line2='', line3='', pmessage=None):
#        if pmessage is not None:
#            lines = pmessage.split('|')
#            if len(lines) == 3:
#                line1 = lines[0]
#                line2 = lines[1]
#                line3 = lines[2]
#            elif len(lines) == 2:
#                line1 = lines[0]
#                line2 = lines[1]
#            elif len(lines) == 1:
#                line1 = lines[0]
#        self.pDialog.update(percent, line1, line2, line3)
        pass

    
    def end(self):
#        self.pDialog.close()
        pass

def displayDialogMessage(heading='', line1='', line2='', line3='', dmessage=None):
    ProgressDisplayer().end()
    if dmessage is not None:
        lines = dmessage.split('|')
        if len(lines) == 3:
            line1 = lines[0]
            line2 = lines[1]
            line3 = lines[2]
        elif len(lines) == 2:
            line1 = lines[0]
            line2 = lines[1]
        elif len(lines) == 1:
            line1 = lines[0]
    if not SUPPRESS_DIALOG_MSG:
        dialog = xbmcgui.Dialog()
        dialog.ok('Process Failed: ' + heading, line1, line2, line3)

def getUserInput(heading='Input', isPassword=False):
    keyb = xbmc.Keyboard()
    if isPassword:
        keyb.setDefault('password')
        keyb.setHiddenInput(True)
    keyb.setHeading(heading)
    keyb.doModal()
    text = None
    if (keyb.isConfirmed()):
        text = urllib.quote_plus(keyb.getText())
    return text

def displayNotification(header, message='', time='3000', iconimage=''):
    notification = "XBMC.Notification(%s,%s,%s,%s)" % (header, message, time, iconimage)
    xbmc.executebuiltin(notification)
