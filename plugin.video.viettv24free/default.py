#!/usr/bin/python
#coding=utf-8
import xbmc , xbmcaddon , xbmcplugin , xbmcgui , sys , urllib , urllib2 , re , os , base64 , json , shutil , zipfile
from math import radians , sqrt , sin , cos , atan2
from operator import itemgetter
import xmltodict
if 64 - 64: i11iIiiIii
OO0o = 'plugin.video.viettv24free'
Oo0Ooo = xbmcaddon . Addon ( OO0o )
O0O0OO0O0O0 = xbmc . translatePath ( Oo0Ooo . getAddonInfo ( 'profile' ) )
iiiii = int ( sys . argv [ 1 ] )
if 64 - 64: iIIi1iI1II111 + ii11i / oOooOoO0Oo0O
def iI1 ( ) :
 i1I11i = xbmc . translatePath ( xbmcaddon . Addon ( ) . getAddonInfo ( 'path' ) ) . decode ( "utf-8" )
 i1I11i = xbmc . translatePath ( os . path . join ( i1I11i , "temp.jpg" ) )
 folderpath=Oo0Ooo.getAddonInfo('path')
 mainfile = xbmc.translatePath(os.path.join(folderpath, 'resources', 'main.txt'))
 Oo = I1ii11iIi11i (mainfile)
 if "xml" in Oo :
  o0OOO = Oo
  for iIiiiI , Iii1ii1II11i in eval ( o0OOO ) :
   Iii1ii1II11i=xbmc.translatePath(os.path.join(folderpath, 'resources', Iii1ii1II11i))
   iI111iI ( iIiiiI , Iii1ii1II11i , 'indexgroup' , i1I11i . replace ( "temp.jpg" , "icon.png" ) )
  IiII = xbmc . getSkinDir ( )
  if IiII == 'skin.xeebo' :
   xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 else :
  iI1Ii11111iIi = xbmcgui . Dialog ( )
  iI1Ii11111iIi . ok ( "ID: %s" % O0O , Oo )
  if 41 - 41: I1II1
def Ooo0OO0oOO ( url ) :
 oooO0oo0oOOOO = I1ii11iIi11i ( url )
 O0oO = re . compile ( '<name>(.+?)</name>' ) . findall ( oooO0oo0oOOOO )
 if len ( O0oO ) == 1 :
  o0oO0 = re . compile ( '<item>(.+?)</item>' ) . findall ( oooO0oo0oOOOO )
  for oo00 in o0oO0 :
   o00 = ""
   Oo0oO0ooo = ""
   o0oOoO00o = ""
   if "/title" in oo00 :
    Oo0oO0ooo = re . compile ( '<title>(.+?)</title>' ) . findall ( oo00 ) [ 0 ]
   if "/link" in oo00 :
    o0oOoO00o = re . compile ( '<link>(.+?)</link>' ) . findall ( oo00 ) [ 0 ]
   if "/thumbnail" in oo00 :
    o00 = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( oo00 ) [ 0 ]
   i1 ( O0oO [ 0 ] + "/" + Oo0oO0ooo , o0oOoO00o , 'play' , o00 )
  IiII = xbmc . getSkinDir ( )
  if IiII == 'skin.xeebo' :
   xbmc . executebuiltin ( 'Container.SetViewMode(52)' )
 else :
  for oOOoo00O0O in O0oO :
   iI111iI ( oOOoo00O0O , url + "&n=" + oOOoo00O0O , 'index' , '' )
   if 15 - 15: I11iii11IIi
def O00o0o0000o0o ( url ) :
 O0Oo = url . split ( "&n=" ) [ 1 ]
 oooO0oo0oOOOO = I1ii11iIi11i ( url )
 oo = re . compile ( '<channel>(.+?)</channel>' ) . findall ( oooO0oo0oOOOO )
 for IiII1I1i1i1ii in oo :
  if O0Oo in IiII1I1i1i1ii :
   o0oO0 = re . compile ( '<item>(.+?)</item>' ) . findall ( IiII1I1i1i1ii )
   for oo00 in o0oO0 :
    o00 = ""
    Oo0oO0ooo = ""
    o0oOoO00o = ""
    if "/title" in oo00 :
     Oo0oO0ooo = re . compile ( '<title>(.+?)</title>' ) . findall ( oo00 ) [ 0 ]
    if "/link" in oo00 :
     o0oOoO00o = re . compile ( '<link>(.+?)</link>' ) . findall ( oo00 ) [ 0 ]
    if "/thumbnail" in oo00 :
     o00 = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( oo00 ) [ 0 ]
    i1 ( O0Oo + "/" + Oo0oO0ooo , o0oOoO00o , 'play' , o00 )
 IiII = xbmc . getSkinDir ( )
 if IiII == 'skin.xeebo' :
  xbmc . executebuiltin ( 'Container.SetViewMode(52)' )
  if 44 - 44: OOo0o0 / OOoOoo00oo - iI1OoOooOOOO + i1iiIII111ii + i1iIIi1
def I1IiI ( k , e ) :
 ii11iIi1I = [ ]
 e = base64 . urlsafe_b64decode ( e )
 for iI111I11I1I1 in range ( len ( e ) ) :
  OOooO0OOoo = k [ iI111I11I1I1 % len ( k ) ]
  iIii1 = chr ( ( 256 + ord ( e [ iI111I11I1I1 ] ) - ord ( OOooO0OOoo ) ) % 256 )
  ii11iIi1I . append ( iIii1 )
 return "" . join ( ii11iIi1I )
 if 71 - 71: IiI1I1
def OoO000 ( source , dest_dir ) :
 with zipfile . ZipFile ( source ) as IIiiIiI1 :
  for iiIiIIi in IIiiIiI1 . infolist ( ) :
   ooOoo0O = iiIiIIi . filename . split ( '/' )
   i1I11i = dest_dir
   for OooO0 in ooOoo0O [ : - 1 ] :
    II11iiii1Ii , OooO0 = os . path . splitdrive ( OooO0 )
    OO0oOoo , OooO0 = os . path . split ( OooO0 )
    if OooO0 in ( os . curdir , os . pardir , '' ) : continue
    i1I11i = os . path . join ( i1I11i , OooO0 )
   IIiiIiI1 . extract ( iiIiIIi , i1I11i )
   if 68 - 68: oOo00Oo00O + I11i1I + o0o0OOO0o0 % IIII % o0O0 . o0
def I11II1i ( url ) :
 i1I11i = xbmc . translatePath ( xbmcaddon . Addon ( ) . getAddonInfo ( 'path' ) ) . decode ( "utf-8" )
 IIIII = xbmc . translatePath ( os . path . join ( i1I11i , "tmp" ) )
 if os . path . exists ( IIIII ) :
  shutil . rmtree ( IIIII )
 os . makedirs ( IIIII )
 if ".zip" in url :
  ooooooO0oo = xbmc . translatePath ( os . path . join ( IIIII , "temp.zip" ) )
  urllib . urlretrieve ( url , ooooooO0oo )
  OoO000 ( ooooooO0oo , IIIII )
 else :
  IIiiiiiiIi1I1 = xbmc . translatePath ( os . path . join ( IIIII , "temp.jpg" ) )
  urllib . urlretrieve ( url , IIiiiiiiIi1I1 )
 xbmc . executebuiltin ( "SlideShow(%s,recursive)" % IIIII )
 if 13 - 13: OOoo0O0 + Ii + OOo0o0 - ii11i * oOo00Oo00O % IIII
def II11iII ( url , title ) :
 if ( "youtube" in url ) :
  OoOo = re . compile ( '(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)' ) . findall ( url )
  iI = OoOo [ 0 ] [ len ( OoOo [ 0 ] ) - 1 ] . replace ( 'v/' , '' )
  url = "plugin://plugin.video.youtube/play/?video_id=%s" % iI
  xbmc . executebuiltin ( "xbmc.PlayMedia(" + url + ")" )
 else :
  if url . isdigit ( ) :
   o00O = "http://www.viettv24.com/main/getStreamingServer.php"
   I1IiI = urllib . urlencode ( { 'strname' : '%s-' % url } )
   url = urllib2 . urlopen ( o00O , data = I1IiI ) . read ( )
  title = urllib . unquote_plus ( title )
  OOO0OOO00oo = xbmc . PlayList ( 1 )
  OOO0OOO00oo . clear ( )
  Iii111II = xbmcgui . ListItem ( title )
  Iii111II . setInfo ( 'video' , { 'Title' : title } )
  iiii11I = xbmc . Player ( )
  OOO0OOO00oo . add ( url , Iii111II )
  iiii11I . play ( OOO0OOO00oo )
  if 96 - 96: I11iii11IIi % IIII . I11i1I + oOooOoO0Oo0O * oOo00Oo00O - i1iiIII111ii
def i11i1 ( lat1 , lon1 , lat2 , lon2 ) :
 lat1 = radians ( lat1 )
 lon1 = radians ( lon1 )
 lat2 = radians ( lat2 )
 lon2 = radians ( lon2 )
 if 29 - 29: IiI1I1 % OOo0o0 + Ii / i1iIIi1 + I11i1I * i1iIIi1
 i1I1iI = lon1 - lon2
 if 93 - 93: ii11i % oOo00Oo00O * I1II1
 Ii11Ii1I = 6372.8
 if 72 - 72: o0O0 / I1II1 * OOoOoo00oo - OOoo0O0
 Oo0O0O0ooO0O = sqrt (
 ( cos ( lat2 ) * sin ( i1I1iI ) ) ** 2
 + ( cos ( lat1 ) * sin ( lat2 ) - sin ( lat1 ) * cos ( lat2 ) * cos ( i1I1iI ) ) ** 2
 )
 IIIIii = sin ( lat1 ) * sin ( lat2 ) + cos ( lat1 ) * cos ( lat2 ) * cos ( i1I1iI )
 O0o0 = atan2 ( Oo0O0O0ooO0O , IIIIii )
 return Ii11Ii1I * O0o0
 if 71 - 71: I11i1I + Ii % i11iIiiIii + IiI1I1 - o0

def I1ii11iIi11i ( url ) :
 o0oOoO00o = ""
 if os . path . exists ( url ) == True :
  o0oOoO00o = open ( url ) . read ( )
 else :
  oO0OOoO0 = urllib2 . Request ( url )
  oO0OOoO0 . add_header ( 'User-Agent' , 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)' )
  I111Ii111 = urllib2 . urlopen ( oO0OOoO0 )
  o0oOoO00o = I111Ii111 . read ( )
  I111Ii111 . close ( )
  if 4 - 4: oOo00Oo00O
 if ( "xml" in url ) :
  o0oOoO00o = I1IiI ( "umbala" , o0oOoO00o )
 o0oOoO00o = '' . join ( o0oOoO00o . splitlines ( ) ) . replace ( '\'' , '"' )
 o0oOoO00o = o0oOoO00o . replace ( '\n' , '' )
 o0oOoO00o = o0oOoO00o . replace ( '\t' , '' )
 o0oOoO00o = re . sub ( '  +' , ' ' , o0oOoO00o )
 o0oOoO00o = o0oOoO00o . replace ( '> <' , '><' )
 return o0oOoO00o
 if 93 - 93: iI1OoOooOOOO % oOo00Oo00O . iI1OoOooOOOO * OOoo0O0 % IIII . I11iii11IIi
def i1 ( name , url , mode , iconimage ) :
 iI1ii1Ii = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
 oooo000 = xbmcgui . ListItem ( name , iconImage = "DefaultVideo.png" , thumbnailImage = iconimage )
 oooo000 . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 if ( "youtube.com/user/" in url ) or ( "youtube.com/channel/" in url ) :
  iI1ii1Ii = "plugin://plugin.video.youtube/%s/%s/" % ( url . split ( "/" ) [ - 2 ] , url . split ( "/" ) [ - 1 ] )
  return xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = iI1ii1Ii , listitem = oooo000 , isFolder = True )
 return xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = iI1ii1Ii , listitem = oooo000 )
 if 16 - 16: IiI1I1 + iI1OoOooOOOO - I11iii11IIi
def iI111iI ( name , url , mode , iconimage ) :
 iI1ii1Ii = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
 oOoOO0 = True
 oooo000 = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 oooo000 . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 oOoOO0 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = iI1ii1Ii , listitem = oooo000 , isFolder = True )
 return oOoOO0
 if 30 - 30: I11iii11IIi - I11i1I - i11iIiiIii % i1iiIII111ii - I11iii11IIi * IIII
def oO00O0O0O ( parameters ) :
 i1ii1iiI = { }
 if 98 - 98: o0O0 * o0O0 / o0O0 + o0o0OOO0o0
 if parameters :
  ii111111I1iII = parameters [ 1 : ] . split ( "&" )
  for O00ooo0O0 in ii111111I1iII :
   i1iIi1iIi1i = O00ooo0O0 . split ( '=' )
   if ( len ( i1iIi1iIi1i ) ) == 2 :
    i1ii1iiI [ i1iIi1iIi1i [ 0 ] ] = i1iIi1iIi1i [ 1 ]
 return i1ii1iiI
 if 46 - 46: OOoo0O0 % o0o0OOO0o0 + iI1OoOooOOOO . i1iiIII111ii . iI1OoOooOOOO
if os . path . exists ( O0O0OO0O0O0 ) == False :
 os . mkdir ( O0O0OO0O0O0 )
oO00o0 = os . path . join ( O0O0OO0O0O0 , 'visitor' )
if 55 - 55: OOoOoo00oo + ii11i / i1iiIII111ii * oOo00Oo00O - i11iIiiIii - IIII
if os . path . exists ( oO00o0 ) == False :
 from random import randint
 ii1ii1ii = open ( oO00o0 , "w" )
 ii1ii1ii . write ( str ( randint ( 0 , 0x7fffffff ) ) )
 ii1ii1ii . close ( )
 if 91 - 91: o0
def iiIii ( utm_url ) :
 ooo0O = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
 import urllib2
 try :
  oO0OOoO0 = urllib2 . Request ( utm_url , None ,
 { 'User-Agent' : ooo0O }
 )
  I111Ii111 = urllib2 . urlopen ( oO0OOoO0 ) . read ( )
 except :
  print ( "GA fail: %s" % utm_url )
 return I111Ii111
 if 75 - 75: i1iIIi1 % i1iIIi1 . OOoo0O0

I1Ii = oO00O0O0O ( sys . argv [ 2 ] )
O0oo00o0O = I1Ii . get ( 'mode' )
i1I1I = I1Ii . get ( 'url' )
oOOoo00O0O = I1Ii . get ( 'name' )
if type ( i1I1I ) == type ( str ( ) ) :
 i1I1I = urllib . unquote_plus ( i1I1I )
if type ( oOOoo00O0O ) == type ( str ( ) ) :
 oOOoo00O0O = urllib . unquote_plus ( oOOoo00O0O )
 if 12 - 12: i11iIiiIii / iI1OoOooOOOO
o0O = str ( sys . argv [ 1 ] )
if O0oo00o0O == 'index' :
 #III1iII1I1ii ( "Browse" , oOOoo00O0O )
 O00o0o0000o0o ( i1I1I )
elif O0oo00o0O == 'indexgroup' :
 #III1iII1I1ii ( "Browse" , oOOoo00O0O )
 Ooo0OO0oOO ( i1I1I )
elif O0oo00o0O == 'play' :
 #III1iII1I1ii ( "Play" , oOOoo00O0O + "/" + i1I1I )
 if any ( x in i1I1I for x in [ ".jpg" , ".zip" ] ) :
  I11II1i ( i1I1I )
 else :
  IiIIii1iII1II = xbmcgui . DialogProgress ( )
  IiIIii1iII1II . create ( 'Brought to you by VietTV24.com' , 'Loading video. Please wait...' )
  II11iII ( i1I1I , oOOoo00O0O )
  IiIIii1iII1II . close ( )
  del IiIIii1iII1II
else :
 #III1iII1I1ii ( "None" , "None" )
 iI1 ( )
xbmcplugin . endOfDirectory ( int ( o0O ) ) # dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
