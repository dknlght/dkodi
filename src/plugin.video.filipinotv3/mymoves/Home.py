'''
Created on Dec 5, 2011

@author: ajju
'''
from TurtleContainer import AddonContext
from common.DataObjects import ListItem
import xbmcgui #@UnresolvedImport
from common import AddonUtils


def displayMenuItems(request_obj, response_obj):
    # TV Shows item
    tvshows_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='tvShows.png')
    item = ListItem()
    item.set_next_action_name('TV_Shows')
    xbmcListItem = xbmcgui.ListItem(label='TV SHOWS', iconImage=tvshows_icon_filepath, thumbnailImage=tvshows_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # Movies item
    movies_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='movies.png')
    item = ListItem()
    item.set_next_action_name('Movies')
    xbmcListItem = xbmcgui.ListItem(label='MOVIES', iconImage=movies_icon_filepath, thumbnailImage=movies_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
    
    # LIVE TV item
    live_icon_filepath = AddonUtils.getCompleteFilePath(baseDirPath=AddonContext().addonPath, extraDirPath=AddonUtils.ADDON_ART_FOLDER, filename='live.png')
    item = ListItem()
    item.set_next_action_name('Live')
    xbmcListItem = xbmcgui.ListItem(label='LIVE TV', iconImage=live_icon_filepath, thumbnailImage=live_icon_filepath)
    item.set_xbmc_list_item_obj(xbmcListItem)
    response_obj.addListItem(item)
        

