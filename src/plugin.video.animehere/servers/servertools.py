# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Utilidades para detectar vídeos de los diferentes conectores
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
#LvX Edited Patched
import re,sys

from core import scrapertools
from core import config
from core import logger

# Listas de servidores empleadas a la hora de reproducir para explicarle al usuario por qué no puede ver un vídeo

# Lista de los servidores que se pueden ver sin cuenta premium de ningún tipo
FREE_SERVERS = []
FREE_SERVERS.extend(['directo','allmyvideos','adnstream','bliptv','divxstage','downupload','facebook','fourshared', 'hulkshare', 'twitvid'])
FREE_SERVERS.extend(['googlevideo','gigabyteupload','hdplay','filebox','mediafire','moevideos','movshare','novamov','ovfile','putlocker'])
FREE_SERVERS.extend(['rapidtube','royalvids','sockshare','stagevu','stagero','tutv','userporn','veoh','videobam'])
FREE_SERVERS.extend(['vidbux','videoweed','vimeo','vk','watchfreeinhd','youtube','nowdownload'])#,'videobeer'
FREE_SERVERS.extend(['jumbofiles','nowvideo','allbox4','streamcloud', 'zinwa', 'dailymotion','justintv', 'vidbull'])
FREE_SERVERS.extend(['vureel','nosvideo','videopremium','one80upload','movreel','flashx','magnovideo','upafile','rapidvideo','fileflyer','playedto'])
# YA NO FUNCIONAN
# rutube

# Lista de TODOS los servidores que funcionan con cuenta premium individual
PREMIUM_SERVERS = ['uploadedto','nowvideo']

# Lista de TODOS los servidores soportados por Filenium
FILENIUM_SERVERS = []
FILENIUM_SERVERS.extend(['linkto','uploadedto','gigasize','youtube','filepost','hotfile','rapidshare','turbobit','mediafire','bitshare','depositfiles'])
FILENIUM_SERVERS.extend(['oron','downupload','allmyvideos','novamov','videoweed','movshare','fooget','letitbit','shareonline','shareflare','rapidgator'])
FILENIUM_SERVERS.extend(['filebox','filefactory','netload','nowdownload','filevelocity','freakshare','userporn','divxstage','putlocker','extabit','vidxden'])
FILENIUM_SERVERS.extend(['vimeo','dailymotion','jumbofiles','zippyshare','glumbouploads','bayfiles','twoshared', 'fourshared','crocko','fiberupload','filereactor'])
FILENIUM_SERVERS.extend(['ifile','megashares','slingfile','uploading','vipfile','filenium','movreel','one80upload','flashx','uploaz','nowvideo','vk','moevideos'])
#wupload,fileserve

# Lista de TODOS los servidores soportados por Real-Debrid
REALDEBRID_SERVERS = ['one80upload','tenupload','onefichier','onehostclick','twoshared','fourfastfile','fourshared','abc','asfile','badongo','bayfiles','bitshare','cbscom','cramit','crocko','cwtv','dailymotion','dateito',
                    'dengee','diglo','extabit','fiberupload','filebox','filedino','filefactory','fileflyer','filekeen','filemade','filemates','fileover','filepost',
                   'filereactor','filesend','filesmonster','filevelocity','freakshare','free','furk','fyels','gigasize','gigaup','glumbouploads','goldfile','hitfile','hipfile','hostingbulk',
                   'hotfile','hulkshare','hulu','ifile','jakfile','jumbofiles','justintv','letitbit','loadto','mediafire','megashare','megashares','mixturevideo','muchshare','netload',
                   'novafile','nowdownload','purevid','putbit','putlocker','redtube','rapidshare','rutube','ryushare','scribd','sendspace','sharebees','shareflare','shragle','slingfile','sockshare',
                   'soundcloud','speedyshare','turbobit','unibytes','uploadc','uploadedto','uploading','uploadspace','uptobox',
                   'userporn','veevr','vidbux','vidhog','vidxden','vimeo','vipfile','wattv','xfileshare','youporn','youtube','yunfile','zippyshare','justintv']
#wupload,fileserve

ALLDEBRID_SERVERS = ['one80upload','onefichier','twoshared','fourfastfile','fourshared','albafile','bayfiles','bitshare','cloudzer','cramit','crocko','cyberlocker','dailymotion','dengee',
                   'depfile','dlfree','extabit','extmatrix','filebox','filefactory','fileflyer','filegag','filehost','fileover','filepost','filerio','filesabc',
                   'filesend','filesmonster','filestay','freakshare','gigasize','hotfile','hulkshare','jumbofiles','letitbit','loadto','mediafire','megashares','mixturevideo','netload',
                   'nitrobits','oteupload','purevid','putlocker','rapidgator','rapidshare','redtube','scribd','secureupload','sharebees','shareflare','slingfile','sockshare',
                   'soundcloud','speedload','speedyshare','turbobit', 'uloadto', 'uploadc','uploadedto','uploading','uptobox',
                   'userporn','vimeo','vipfile','youporn','youtube','yunfile','zippyshare','lumfile']               
               
#Resultado de http://alldebrid.com/api.php?action=get_host
#"10upload.com", "1fichier.com", "180upload.com", "2shared.com", "4fastfile.com", "4shared.com", "asfile.com", "badongo.com", "bayfiles.com", "bitshare.com", "buckshare.com", "bulletupload.com", "cloudnator.com", 
#"cloudnxt.net", "cramit.in", "crocko.com", "datei.to", "ddlstorage.com", "dengee.net", "diglo.com", "easybytez.com", "enterupload.com", "exoshare.com", "extabit.com", "fiberupload.com", "fileape.com", "filebox.com",
# "filebase.com", "fileden.com", "filedino.com", "filefactory.com", "fileflyer.com", "filefrog.com", "fileforth.com", "filegag.com", "filejungle.com", "filekeen.com", "filelaser.com", "filemade.com", "filemates.com", 
# "fileover.com", "filepost.com", "files-save.com", "filesend.com", "fileserve.com", "filesmonster.net", "filevelocity.com", "filemarkets.com", "filereactor.com", "freakshare.com", "free.fr", "furk.net", "fyels.com",
# "gigapeta.com", "gigasize.com", "gigaup.fr", "glumbouploads.com", "goldfile.eu", "grupload", "hitfile.net", "hotfile.com", "hu.lk", "ifile.com", "jumbofiles.com", "keepfile.com", "letitbit.net", "load.to", "mediafire.com",
# "MegaShare.com", "megashares.com", "mixturevideo.com", "movbay.com", "muchshare.net", "novafile.com", "nowdownload.eu", "netload.in", "piggyshare.com", "pigsonic.com", "przeklej.pl", "purevid.com", "putlocker.com", 
# "pyramidfiles.com", "rapidgator.net", "rapidshare.com", "ryushare.com", "scribd.com", "sendspace.com", "shareflare.net", "share-online.biz", "shragle.com", "simpleupload.com", "slingfile.com", "sockshare.com", 
# "soundcloud.com", "speedy.sh", "speedyshare.com", "squillion.com", "turbobit.net", "turboupload".com, "ugotfile.com", "unibytes.com", "uploadbox.com", "uploadc.com", "uploaded.to", "uploadhere.com", "uploadhero.com", 
# "uploading.com", "uploadking.com", "uploadspace.pl", "uploadstation.com", "uptobox.com", "userporn.com", "usershare.com", "vidbux.com", "videobb.com", "videozer.com", "vidxden.com", "vip-file.com", "wupload.com", 
# "x7.com", "youtube.com", "yunfile.com", "zippyshare.com", "zshare.net"               
               
# Lista completa de todos los servidores soportados por pelisalacarta, usada para buscar patrones
ALL_SERVERS = list( set(FREE_SERVERS) | set(FILENIUM_SERVERS) | set(REALDEBRID_SERVERS) | set(ALLDEBRID_SERVERS) )
ALL_SERVERS.sort()

# Función genérica para encontrar vídeos en una página
def find_video_items(item=None, data=None, channel=""):
    logger.info("[launcher.py] findvideos")

    # Descarga la página
    if data is None:
        from core import scrapertools
        data = scrapertools.cache_page(item.url)
        #logger.info(data)
    
    # Busca los enlaces a los videos
    from core.item import Item
    from servers import servertools
    listavideos = servertools.findvideos(data)

    if item is None:
        item = Item()

    itemlist = []
    for video in listavideos:
        scrapedtitle = item.title.strip() + " - " + video[0].strip()
        scrapedurl = video[1]
        server = video[2]
        
        itemlist.append( Item(channel=item.channel, title=scrapedtitle , action="play" , server=server, page=item.page, url=scrapedurl, thumbnail=item.thumbnail, show=item.show , plot=item.plot , folder=False) )

    return itemlist

def findvideosbyserver(data, serverid):
    logger.info("[servertools.py] findvideos")
    encontrados = set()
    devuelve = []
    try:
        exec "from servers import "+serverid
        exec "devuelve.extend("+serverid+".find_videos(data))"
    except ImportError:
        logger.info("No existe conector para "+serverid)
    except:
        logger.info("Error en el conector "+serverid)
        import traceback,sys
        from pprint import pprint
        exc_type, exc_value, exc_tb = sys.exc_info()
        lines = traceback.format_exception(exc_type, exc_value, exc_tb)
        for line in lines:
            line_splits = line.split("\n")
            for line_split in line_splits:
                logger.error(line_split)

    return devuelve

def findvideos(data):
    logger.info("[servertools.py] findvideos")
    encontrados = set()
    devuelve = []

    # Ejecuta el findvideos en cada servidor
    for serverid in ALL_SERVERS:
        try:
            exec "from servers import "+serverid
            exec "devuelve.extend("+serverid+".find_videos(data))"
        except ImportError:
            logger.info("No existe conector para "+serverid)
        except:
            logger.info("Error en el conector "+serverid)
            import traceback,sys
            from pprint import pprint
            exc_type, exc_value, exc_tb = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_tb)
            for line in lines:
                line_splits = line.split("\n")
                for line_split in line_splits:
                    logger.error(line_split)

    return devuelve

def get_server_from_url(url):
    encontrado = findvideos(url)
    if len(encontrado)>0:
        devuelve = encontrado[0][2]
    else:
        devuelve = "directo"

    return devuelve

def resolve_video_urls_for_playing(server,url,video_password="",muestra_dialogo=False):
    logger.info("[servertools.py] resolve_video_urls_for_playing, server="+server+", url="+url)
    video_urls = []
    torrent = False
    
    server = server.lower()

    # Si el vídeo es "directo", no hay que buscar más
    if server=="directo" or server=="local":
        logger.info("[servertools.py] server=directo, la url es la buena")
        
        try:
            import urlparse
            parsed_url = urlparse.urlparse(url)
            logger.info("parsed_url="+str(parsed_url))
            extension = parsed_url.path[-4:]
        except:
            extension = url[-4:]

        video_urls = [[ "%s [%s]" % (extension,server) , url ]]
        return video_urls,True,""

    # Averigua las URL de los vídeos
    else:
        
        if server=="torrent":
            server="filenium"
            torrent = True

        # Carga el conector
        try:
            # Muestra un diálogo de progreso
            if muestra_dialogo:
                import xbmcgui
                progreso = xbmcgui.DialogProgress()
                progreso.create( "pelisalacarta" , "Conectando con "+server)

            exec "from servers import "+server+" as server_connector"
            logger.info("[servertools.py] servidor de "+server+" importado")
            if muestra_dialogo:
                progreso.update( 20 , "Conectando con "+server)

            # Si tiene una función para ver si el vídeo existe, lo comprueba ahora
            if hasattr(server_connector, 'test_video_exists'):
                logger.info("[servertools.py] invocando a "+server+".test_video_exists")
                puedes,motivo = server_connector.test_video_exists( page_url=url )

                # Si la funcion dice que no existe, fin
                if not puedes:
                    logger.info("[servertools.py] test_video_exists dice que el video no existe")
                    if muestra_dialogo: progreso.close()
                    return video_urls,puedes,motivo
                else:
                    logger.info("[servertools.py] test_video_exists dice que el video SI existe")

            # Obtiene enlaces free
            if server in FREE_SERVERS:
                logger.info("[servertools.py] invocando a "+server+".get_video_url")
                video_urls = server_connector.get_video_url( page_url=url , video_password=video_password )
                
                # Si no se encuentran vídeos en modo free, es porque el vídeo no existe
                if len(video_urls)==0:
                    if muestra_dialogo: progreso.close()
                    return video_urls,False,"No se puede encontrar el vídeo en "+server

            # Obtiene enlaces premium si tienes cuenta en el server
            if server in PREMIUM_SERVERS and config.get_setting(server+"premium")=="true":
                video_urls = server_connector.get_video_url( page_url=url , premium=(config.get_setting(server+"premium")=="true") , user=config.get_setting(server+"user") , password=config.get_setting(server+"password"), video_password=video_password )
                
                # Si no se encuentran vídeos en modo premium directo, es porque el vídeo no existe
                if len(video_urls)==0:
                    if muestra_dialogo: progreso.close()
                    return video_urls,False,"No se puede encontrar el vídeo en "+server
    
            # Obtiene enlaces filenium si tienes cuenta
            if server in FILENIUM_SERVERS and config.get_setting("fileniumpremium")=="true":
    
                # Muestra un diálogo de progreso
                if muestra_dialogo:
                    progreso.update( 40 , "Conectando con Filenium")
    
                exec "from servers import filenium as gen_conector"
                
                video_gen = gen_conector.get_video_url( page_url=url , premium=(config.get_setting("fileniumpremium")=="true") , user=config.get_setting("fileniumuser") , password=config.get_setting("fileniumpassword"), video_password=video_password )
                extension = gen_conector.get_file_extension(video_gen)
                logger.info("[xbmctools.py] filenium url="+video_gen)
                video_urls.append( [ extension+" ["+server+"][filenium]", video_gen ] )

            # Obtiene enlaces realdebrid si tienes cuenta
            if server in REALDEBRID_SERVERS and config.get_setting("realdebridpremium")=="true":
    
                # Muestra un diálogo de progreso
                if muestra_dialogo:
                    progreso.update( 60 , "Conectando con Real-Debrid")

                exec "from servers import realdebrid as gen_conector"
                video_gen = gen_conector.get_video_url( page_url=url , premium=(config.get_setting("realdebridpremium")=="true") , user=config.get_setting("realdebriduser") , password=config.get_setting("realdebridpassword"), video_password=video_password )
                logger.info("[xbmctools.py] realdebrid url="+video_gen)
                if not "REAL-DEBRID" in video_gen:
                    video_urls.append( [ "."+video_gen.rsplit('.',1)[1]+" [realdebrid]", video_gen ] )
                else:
                    if muestra_dialogo: progreso.close()
                    # Si RealDebrid da error pero tienes un enlace válido, no te dice nada
                    if len(video_urls)==0:
                        return video_urls,False,video_gen
                  
            # Obtiene enlaces alldebrid si tienes cuenta
            if server in ALLDEBRID_SERVERS and config.get_setting("alldebridpremium")=="true":
    
                # Muestra un diálogo de progreso
                if muestra_dialogo:
                    progreso.update( 80 , "Conectando con All-Debrid")

                exec "from servers import alldebrid as gen_conector"
                video_gen = gen_conector.get_video_url( page_url=url , premium=(config.get_setting("alldebridpremium")=="true") , user=config.get_setting("alldebriduser") , password=config.get_setting("alldebridpassword"), video_password=video_password )
                logger.info("[xbmctools.py] alldebrid url="+video_gen)
                if video_gen.startswith("http"):
                    video_urls.append( [ "[alldebrid]", video_gen ] )
                else:
                    # Si Alldebrid da error pero tienes un enlace válido, no te dice nada
                    if len(video_urls)==0:
                        return [],False,video_gen.strip()

            
            if muestra_dialogo:
                progreso.update( 100 , "Proceso finalizado")

            # Cierra el diálogo de progreso
            if muestra_dialogo: progreso.close()

            # Llegas hasta aquí y no tienes ningún enlace para ver, así que no vas a poder ver el vídeo
            if len(video_urls)==0:
                # ¿Cual es el motivo?
                
                # 1) No existe -> Ya está controlado
                # 2) No tienes alguna de las cuentas premium compatibles

                # Lista de las cuentas que soportan este servidor
                listapremium = ""
                if server in ALLDEBRID_SERVERS: listapremium+="All-Debrid o "            
                if server in FILENIUM_SERVERS: listapremium+="Filenium o "
                if server in REALDEBRID_SERVERS: listapremium+="Real-Debrid o "
                if server in PREMIUM_SERVERS: listapremium+=server+" o "
                listapremium = listapremium[:-3]
    
                return video_urls,False,"Para ver un vídeo en "+server+" necesitas<br/>una cuenta en "+listapremium

        except:
            if muestra_dialogo: progreso.close()
            import traceback
            from pprint import pprint
            exc_type, exc_value, exc_tb = sys.exc_info()
            lines = traceback.format_exception(exc_type, exc_value, exc_tb)
            for line in lines:
                line_splits = line.split("\n")
                for line_split in line_splits:
                    logger.error(line_split)

            return video_urls,False,"Se ha producido un error en<br/>el conector con "+server

    return video_urls,True,""