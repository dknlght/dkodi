'''
Created on Oct 17, 2011

'''

from common import DataObjects, XBMCInterfaceUtils, AddonUtils
from common.Singleton import SingletonClass
from common.XBMCInterfaceUtils import ProgressDisplayer
from definition.Turtle import Action, Move, Service
import sys
import xbmcaddon #@UnresolvedImport

__author__ = "ajju"
__version__ = "1.0.0"


class AddonContext(SingletonClass):
    '''
    AddonContext will provide a way for container to access the route
    '''
    def __initialize__(self, addon_id):
        
        #Addon information
        self.addon = xbmcaddon.Addon(id=addon_id)
        self.addonPath = self.addon.getAddonInfo('path')
        self.addonProfile = self.addon.getAddonInfo('profile')
        
        self.turtle_addon = xbmcaddon.Addon(id='script.module.turtle')
        self.turtle_addonPath = self.turtle_addon.getAddonInfo('path')
        self.turtle_addonProfile = self.turtle_addon.getAddonInfo('profile')
        
        turtle_filepath = AddonUtils.getCompleteFilePath(self.addonPath, 'config', 'turtle.xml')
        if not AddonUtils.doesFileExist(turtle_filepath):
            turtle_filepath = AddonUtils.getCompleteFilePath(self.turtle_addonPath, 'lib/config', 'turtle.xml')
        self.turtle_map = AddonUtils.getBeautifulSoupObj(turtle_filepath)
        
    
    def getTurtleRoute(self, actionId):
        actionTag = self.turtle_map.find(name='action', attrs={'id':actionId})
        actionObj = Action(actionTag['id'])
        if actionTag.has_key('pmessage'):
            ProgressDisplayer().displayMessage(5, pmessage=actionTag['pmessage'])
        
        for moveTag in actionTag.findAll('move'):
            modulePath = moveTag['module']
            functionName = moveTag['function']
            pmessage = None
            if moveTag.has_key('pmessage'):
                pmessage = moveTag['pmessage']
            actionObj.addMove(Move(modulePath, functionName, pmessage))
            
        for nextActionTag in actionTag.findAll('next-action'):
            actionName = nextActionTag['name']
            actionId = nextActionTag['id']
            actionObj.addNextAction(actionName, actionId)
            
        for redirectActionTag in actionTag.findAll('redirect-action'):
            actionName = redirectActionTag['name']
            actionId = redirectActionTag['id']
            actionObj.addRedirectAction(actionName, actionId)
            
        return actionObj
    
    
    def isNextActionFolder(self, actionId, nextActionName):
        actionTag = self.turtle_map.find(name='action', attrs={'id':actionId})
        nextActionTag = actionTag.find(name='next-action', attrs={'name':nextActionName})
        return (nextActionTag['isfolder'] == 'true')
        
        
    def getTurtleServices(self):
        services = []
        serviceTags = self.turtle_map.findAll(name='service')
        for serviceTag in serviceTags:
            services.append(Service(serviceTag['name'], serviceTag['action-id']))
        return services
    
        
'''CONTAINER FUNCTIONS START FROM HERE'''
#INITIALIZE CONTAINER
class Container(SingletonClass):
    
    def __initialize__(self, addon_id):
        self.addon_context = AddonContext(addon_id=addon_id)
        
    def getAddonContext(self):
        return self.addon_context
        
    def getTurtleRequest(self):
        params = None
        if len(sys.argv) >= 3:
            params = str(sys.argv[2])
        self.request_obj = DataObjects.Request(params=params)
        self.response_obj = DataObjects.Response()
        return self.request_obj
    
    def getTurtleResponse(self):
        return self.response_obj
        
    def reloadTurtleRequest(self, params):
        self.request_obj = DataObjects.Request(params=params)
        self.request_obj.__initialize__(params)
        self.response_obj = DataObjects.Response()
        self.response_obj.reset_item_list()
        
    def getTurtleRoute(self, actionId):
        return self.addon_context.getTurtleRoute(actionId)
        
    def moveTurtle(self, moveObj):
        if moveObj.get_pmessage() is not None:
            ProgressDisplayer().displayMessage(50, pmessage=moveObj.get_pmessage())
        components = moveObj.module_path.split('.')
        module = __import__(moveObj.module_path)
        if components is not None and isinstance(components, list):
            for index in range(1, len(components)):
                module = getattr(module, components[index])
        function = getattr(module, moveObj.function_name)
        function(self.request_obj, self.response_obj)
        
        
    def judgeTurtleNextAction(self, actionObj):
        ProgressDisplayer().displayMessage(80, line1='Preparing items for display or play', line2='Total items: ' + str(len(self.response_obj.get_item_list())))
        if self.response_obj.get_redirect_action_name() is None:
            isAnyVideoItem = False
            for item in self.response_obj.get_item_list():
                nextActionId = actionObj.get_next_action_map()[item.get_next_action_name()]
                if nextActionId == '__play__':
                    if not isAnyVideoItem:
                        XBMCInterfaceUtils.clearPlayList() #Clear playlist item only when at least one video item is found.
                    XBMCInterfaceUtils.addPlayListItem(item)
                    isAnyVideoItem = True
                elif nextActionId == '__service_response__':
                    #Do Nothing , get response object from container for parameters to be returned
                    pass
                else:
                    is_Folder = self.addon_context.isNextActionFolder(actionObj.get_action_id(), item.get_next_action_name())
                    XBMCInterfaceUtils.addFolderItem(item, nextActionId, is_Folder)
            if isAnyVideoItem == True:
                ProgressDisplayer().end()
                XBMCInterfaceUtils.play()
            else:
                if self.response_obj.get_xbmc_sort_method() is not None:
                    XBMCInterfaceUtils.sortItems(self.response_obj.get_xbmc_sort_method())
                if self.response_obj.get_xbmc_content_type() is not None:
                    XBMCInterfaceUtils.setContentType(self.response_obj.get_xbmc_content_type())

        else:
            redirectActionId = actionObj.get_redirect_action_map()[self.response_obj.get_redirect_action_name()]
            self.response_obj.set_redirect_action_name(None)
            return redirectActionId


    def performAction(self, actionId):
        ProgressDisplayer().start('Processing request...')
         
        while actionId is not None:
            print 'Action to be performed ::' + actionId
            turtle_route = self.getTurtleRoute(actionId)
            for move in turtle_route.moves:
                self.moveTurtle(move)
            actionId = self.judgeTurtleNextAction(turtle_route)
            
        ProgressDisplayer().end()
