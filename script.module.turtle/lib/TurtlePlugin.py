'''
Created on Oct 16, 2011

@author: ajju
'''
from TurtleContainer import Container
import xbmcplugin #@UnresolvedImport
import sys
from common import ExceptionHandler
import logging

__addon_id__ = None

def start(addon_id):
    try:
        global __addon_id__
        __addon_id__ = addon_id
        
        containerObj = Container(addon_id=addon_id)
        action_id = containerObj.getTurtleRequest().get_action_id()
        containerObj.performAction(action_id)
    except Exception, e:
        logging.exception(e)
        ExceptionHandler.handle(e)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


        
