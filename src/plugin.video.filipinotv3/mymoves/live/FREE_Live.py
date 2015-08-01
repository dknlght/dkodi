'''
Created on Dec 10, 2011

@author: ajju
'''
from TurtleContainer import AddonContext
from common import AddonUtils, ExceptionHandler
from common.DataObjects import ListItem
import xbmcgui, xbmcplugin #@UnresolvedImport


CHANNELS_JSON_FILE = 'Free-Channels.json'
    

def selectChannelsCategory(request_obj, response_obj):
    filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_SRC_DATA_FOLDER, filename=CHANNELS_JSON_FILE)
    freeChannels = AddonUtils.getJsonFileObj(filepath)
    if len(freeChannels.keys()) > 1:
        d = xbmcgui.Dialog()
        catSelect = d.select('SELECT Category', freeChannels.keys())
    else:
        catSelect = 0
    if catSelect == -1:
        raise Exception(ExceptionHandler.CATEGORY_NOT_SELECTED, 'Please select the category correctly')
    category = freeChannels.keys()[catSelect]
    request_obj.set_data({'channels': freeChannels[category]})


def displayChannels(request_obj, response_obj):
    channels = request_obj.get_data()['channels']
    for channelName in channels:
        channelInfo = channels[channelName]
        channelUrl = channelInfo['channelUrl']
        channelLogo = channelInfo['channelLogo']
        item = ListItem()
        item.set_next_action_name('play_Live_Channel')
        item.add_request_data('channelName', channelName)
        item.add_request_data('channelLogo', channelLogo)
        item.add_request_data('channelUrl', channelUrl)
        xbmcListItem = xbmcgui.ListItem(label=channelName, iconImage=channelLogo, thumbnailImage=channelLogo)
        item.set_xbmc_list_item_obj(xbmcListItem)
        response_obj.addListItem(item)
    response_obj.set_xbmc_sort_method(xbmcplugin.SORT_METHOD_LABEL)
    

def playChannel(request_obj, response_obj):
    item = ListItem()
    item.set_next_action_name('Play')
    item.add_moving_data('videoStreamUrl', request_obj.get_data()['channelUrl'])
    xbmcListItem = xbmcgui.ListItem(label=request_obj.get_data()['channelName'], iconImage=request_obj.get_data()['channelLogo'], thumbnailImage=request_obj.get_data()['channelLogo'])
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
