'''
Created on Dec 27, 2011

@author: ajju
'''

import TurtleService
import TurtlePlugin

if __name__ == '__main__':
    
    __addon_id__ = 'plugin.video.filipinotv3'
    __is_type_service__ = False
    
    if __is_type_service__:
        TurtleService.start(__addon_id__)
    else:
        TurtlePlugin.start(__addon_id__)
