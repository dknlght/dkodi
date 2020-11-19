# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import os,sys

# Appends the main plugin dir to the PYTHONPATH if an internal package cannot be imported.
# Examples: In Plex Media Server all modules are under "Code.*" package, and in Enigma2 under "Plugins.Extensions.*"
try:
    #from core import logger
    import core
except:
    sys.path.append( os.path.abspath( os.path.join( os.path.dirname(__file__) , ".." ) ) )
