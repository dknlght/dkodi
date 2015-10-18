#!/usr/bin/python
#coding=utf-8
import xbmc , xbmcaddon , xbmcplugin , xbmcgui , sys , urllib , urllib2 , re , os , base64 , json , shutil , zipfile
from math import radians , sqrt , sin , cos , atan2
from operator import itemgetter
import xmltodict
import random
if 64 - 64: i11iIiiIii
OO0o = 'plugin.video.viettv24free'
Oo0Ooo = xbmcaddon . Addon ( OO0o )
O0O0OO0O0O0 = xbmc . translatePath ( Oo0Ooo . getAddonInfo ( 'profile' ) )
iiiii = int ( sys . argv [ 1 ] )
if 64 - 64: iIIi1iI1II111 + ii11i / oOooOoO0Oo0O
def iI1 ( ) :
 i1I11i = xbmc . translatePath ( xbmcaddon . Addon ( ) . getAddonInfo ( 'path' ) ) . decode ( "utf-8" )
 i1I11i = xbmc . translatePath ( os . path . join ( i1I11i , "temp.jpg" ) )
 '''urllib . urlretrieve ( 'https://googledrive.com/host/0B-ygKtjD8Sc-S04wUUxMMWt5dmM/images/viettv24.jpg' , i1I11i )
 OoOoOO00 = xbmcgui . WindowDialog ( )
 I11i = xbmcgui . ControlImage ( 0 , 0 , 1280 , 720 , i1I11i )
 OoOoOO00 . addControl ( I11i )
 OoOoOO00 . doModal ( )'''
 #O0O = ""
 Oo = ( "Busy" , "Bận" , "Band" , "Beschäftigt" , "Bezig" , "忙" , "忙碌" )
 while True :
  sys = urllib . quote ( xbmc . getInfoLabel ( "" ) . strip ( ) )
  if not any ( b in sys for b in Oo ) : break
 while True :
  I1ii11iIi11i = urllib . quote ( xbmc . getInfoLabel ( "" ) . strip ( ) )
  if not any ( b in I1ii11iIi11i for b in Oo ) : break
 try :
  O0O = open ( '' ) . read ( ) . strip ( )
 except :
  while True :
   #O0O = '00:1A:79:55:55:66' 
   #O0O = '00:1A:79:55:55:55'
   #mac = ['00:1A:79:55:55:66', '00:1A:79:55:56:77', '00:1A:79:55:58:77', '02:1A:79:55:55:77', '03:1A:79:55:55:77', '09:1A:79:55:55:77', '00:1A:79:55:55:66']
   #O0O = random.choice(mac)
   '''mac = [ 0x00, 0x24, 0x81,
    random.randint(0x00, 0x7f),
    random.randint(0x00, 0xff),
    random.randint(0x00, 0xff) ]
   O0O = ':'.join(map(lambda x: "%02x" % x, mac))'''
   mac = [ random.randint(0x00, 0xff),
    random.randint(0x00, 0xff),
    random.randint(0x00, 0xff),
    random.randint(0x00, 0x7f),
    random.randint(0x00, 0xff),
    random.randint(0x00, 0xff) ]
   O0O = ':'.join(map(lambda x: "%02x" % x, mac))
   if ( "" , '' ) : break
 I1IiI = o0OOO ( iIiiiI ( "ghjl" , "z9ze3KGXmeDP19jTld7T0dvc4J6bls3b1Jfd29zazdHGztPYzJmgq9TRzqmM25Df4NunkdqOztHdpY_f" ) % ( O0O , sys , I1ii11iIi11i ) )
 
 if "mxl=" in I1IiI :
  Iii1ii1II11i = I1IiI
  for iI111iI , IiII in eval ( Iii1ii1II11i ) :
   iI1Ii11111iIi ( iI111iI , IiII , 'indexgroup' , i1I11i . replace ( "temp.jpg" , "icon.png" ) )
  i1i1II = xbmc . getSkinDir ( )
  if i1i1II == 'skin.xeebo' :
   xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 elif "//" in I1IiI :
  Iii1ii1II11i = I1IiI
  for iI111iI , IiII in eval ( Iii1ii1II11i ) :
   iI1Ii11111iIi ( iI111iI , IiII , 'indexgroup' , i1I11i . replace ( "temp.jpg" , "icon.png" ) )
  i1i1II = xbmc . getSkinDir ( )
  if i1i1II == 'skin.xeebo' :
   xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 else :
  I1IiI = o0OOO ( iIiiiI ( "ghjl" , "z9ze3KGXmeDP19jTld7T0dvc4J6bls3b1Jfd29zazdHGztPYzJmgq9TRzqmM25Df4NunkdqOztHdpY_f" ) % ( O0O , sys , I1ii11iIi11i ) ) 
  #i1i1II = xbmc . getSkinDir ( )
  #xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
  #O0oo0OO0 = xbmcgui . Dialog ( )
  #O0oo0OO0 . ok ( "ID: %s" % O0O , I1IiI )
  if 6 - 6: oooO0oo0oOOOO - ooO0oo0oO0 - i111I * II1Ii1iI1i
def iiI1iIiI ( url ) :
 OOo = o0OOO ( url )
 Ii1IIii11 = re . compile ( '<name>(.+?)</name>' ) . findall ( OOo )
 if len ( Ii1IIii11 ) == 1 :
  Oooo0000 = re . compile ( '<item>(.+?)</item>' ) . findall ( OOo )
  for i11 in Oooo0000 :
   I11 = ""
   Oo0o0000o0o0 = ""
   oOo0oooo00o = ""
   if "/title" in i11 :
    Oo0o0000o0o0 = re . compile ( '<title>(.+?)</title>' ) . findall ( i11 ) [ 0 ]
   if "/link" in i11 :
    oOo0oooo00o = re . compile ( '<link>(.+?)</link>' ) . findall ( i11 ) [ 0 ]
   if "/thumbnail" in i11 :
    I11 = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( i11 ) [ 0 ]
   oO0o0o0ooO0oO ( Ii1IIii11 [ 0 ] + "/" + Oo0o0000o0o0 , oOo0oooo00o , 'play' , I11 )
  i1i1II = xbmc . getSkinDir ( )
  if i1i1II == 'skin.xeebo' :
   xbmc . executebuiltin ( 'Container.SetViewMode(52)' )
 else :
  for oo0o0O00 in Ii1IIii11 :
   iI1Ii11111iIi ( oo0o0O00 , url + "&n=" + oo0o0O00 , 'index' , '' )
   if 68 - 68: o00oo . iI1OoOooOOOO + i11iiII
def I1iiiiI1iII ( url ) :
 IiIi11i = url . split ( "&n=" ) [ 1 ]
 OOo = o0OOO ( url )
 iIii1I111I11I = re . compile ( '<channel>(.+?)</channel>' ) . findall ( OOo )
 for OO00OooO0OO in iIii1I111I11I :
  if IiIi11i in OO00OooO0OO :
   Oooo0000 = re . compile ( '<item>(.+?)</item>' ) . findall ( OO00OooO0OO )
   for i11 in Oooo0000 :
    I11 = ""
    Oo0o0000o0o0 = ""
    oOo0oooo00o = ""
    if "/title" in i11 :
     Oo0o0000o0o0 = re . compile ( '<title>(.+?)</title>' ) . findall ( i11 ) [ 0 ]
    if "/link" in i11 :
     oOo0oooo00o = re . compile ( '<link>(.+?)</link>' ) . findall ( i11 ) [ 0 ]
    if "/thumbnail" in i11 :
     I11 = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( i11 ) [ 0 ]
    oO0o0o0ooO0oO ( IiIi11i + "/" + Oo0o0000o0o0 , oOo0oooo00o , 'play' , I11 )
 i1i1II = xbmc . getSkinDir ( )
 if i1i1II == 'skin.xeebo' :
  xbmc . executebuiltin ( 'Container.SetViewMode(52)' )
  if 28 - 28: iIii1
def iIiiiI ( k , e ) :
 oOOoO0 = [ ]
 e = base64 . urlsafe_b64decode ( e )
 for O0OoO000O0OO in range ( len ( e ) ) :
  iiI1IiI = k [ O0OoO000O0OO % len ( k ) ]
  II = chr ( ( 256 + ord ( e [ O0OoO000O0OO ] ) - ord ( iiI1IiI ) ) % 256 )
  oOOoO0 . append ( II )
 return "" . join ( oOOoO0 )
 if 57 - 57: ooOoo0O
def OooO0 ( source , dest_dir ) :
 with zipfile . ZipFile ( source ) as II11iiii1Ii :
  for OO0oOoo in II11iiii1Ii . infolist ( ) :
   O0o0Oo = OO0oOoo . filename . split ( '/' )
   i1I11i = dest_dir
   for Oo00OOOOO in O0o0Oo [ : - 1 ] :
    O0OO00o0OO , Oo00OOOOO = os . path . splitdrive ( Oo00OOOOO )
    I11i1 , Oo00OOOOO = os . path . split ( Oo00OOOOO )
    if Oo00OOOOO in ( os . curdir , os . pardir , '' ) : continue
    i1I11i = os . path . join ( i1I11i , Oo00OOOOO )
   II11iiii1Ii . extract ( OO0oOoo , i1I11i )
   if 25 - 25: iii1I11ii1i1 - OO0oo0oOO + oo0oooooO0
def i11Iiii ( url ) :
 i1I11i = xbmc . translatePath ( xbmcaddon . Addon ( ) . getAddonInfo ( 'path' ) ) . decode ( "utf-8" )
 iI = xbmc . translatePath ( os . path . join ( i1I11i , "tmp" ) )
 if os . path . exists ( iI ) :
  shutil . rmtree ( iI )
 os . makedirs ( iI )
 if ".zip" in url :
  I1i1I1II = xbmc . translatePath ( os . path . join ( iI , "temp.zip" ) )
  urllib . urlretrieve ( url , I1i1I1II )
  OooO0 ( I1i1I1II , iI )
 else :
  i1 = xbmc . translatePath ( os . path . join ( iI , "temp.jpg" ) )
  urllib . urlretrieve ( url , i1 )
 xbmc . executebuiltin ( "SlideShow(%s,recursive)" % iI )
 if 48 - 48: Ii + I1I - II11iII % oOoo % iIIi1iI1II111
def iii11I111 ( url , title ) :
 if ( "youtube" in url ) :
  OOOO00ooo0Ooo = re . compile ( '(youtu\.be\/|youtube-nocookie\.com\/|youtube\.com\/(watch\?(.*&)?v=|(embed|v|user)\/))([^\?&"\'>]+)' ) . findall ( url )
  OOOooOooo00O0 = OOOO00ooo0Ooo [ 0 ] [ len ( OOOO00ooo0Ooo [ 0 ] ) - 1 ] . replace ( 'v/' , '' )
  url = "plugin://plugin.video.youtube/play/?video_id=%s" % OOOooOooo00O0
  xbmc . executebuiltin ( "xbmc.PlayMedia(" + url + ")" )
 else :
  if "://" not in url :
   Oo0OO = "http://www.viettv24.com/main/getStreamingServer.php"
   iIiiiI = urllib . urlencode ( { 'strname' : '%s-' % url } )
   url = urllib2 . urlopen ( Oo0OO , data = iIiiiI ) . read ( )
  title = urllib . unquote_plus ( title )
  oOOoOo00o = xbmc . PlayList ( 1 )
  oOOoOo00o . clear ( )
  o0OOoo0OO0OOO = xbmcgui . ListItem ( title )
  o0OOoo0OO0OOO . setInfo ( 'video' , { 'Title' : title } )
  iI1iI1I1i1I = xbmc . Player ( )
  oOOoOo00o . add ( url , o0OOoo0OO0OOO )
  iI1iI1I1i1I . play ( oOOoOo00o )
  if 24 - 24: iIii1
def o0Oo0O0Oo00oO ( lat1 , lon1 , lat2 , lon2 ) :
 lat1 = radians ( lat1 )
 lon1 = radians ( lon1 )
 lat2 = radians ( lat2 )
 lon2 = radians ( lon2 )
 if 39 - 39: I1I - ooO0oo0oO0 * o00oo % i11iiII * ooO0oo0oO0 % ooO0oo0oO0
 OoOOOOO = lon1 - lon2
 if 33 - 33: iIii1 % oooO0oo0oOOOO
 o00OO00OoO = 6372.8
 if 60 - 60: o00oo * iI1OoOooOOOO - o00oo % oOooOoO0Oo0O - oOoo + i111I
 O00Oo000ooO0 = sqrt (
 ( cos ( lat2 ) * sin ( OoOOOOO ) ) ** 2
 + ( cos ( lat1 ) * sin ( lat2 ) - sin ( lat1 ) * cos ( lat2 ) * cos ( OoOOOOO ) ) ** 2
 )
 OoO0O00 = sin ( lat1 ) * sin ( lat2 ) + cos ( lat1 ) * cos ( lat2 ) * cos ( OoOOOOO )
 IIiII = atan2 ( O00Oo000ooO0 , OoO0O00 )
 return o00OO00OoO * IIiII
 if 80 - 80: I1I . ooOoo0O
def o0OOO ( url ) :
 oOo0oooo00o = ""
 if os . path . exists ( url ) == True :
  oOo0oooo00o = open ( url ) . read ( )
 else :
  IIi = urllib2 . Request ( url )
  IIi . add_header ( 'User-Agent' , 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)' )
  i11iIIIIIi1 = urllib2 . urlopen ( IIi )
  oOo0oooo00o = i11iIIIIIi1 . read ( )
  i11iIIIIIi1 . close ( )
  if 20 - 20: oooO0oo0oOOOO + iIii1 - oOoo
 if ( "xml" in url ) :
  oOo0oooo00o = iIiiiI ( "umbala" , oOo0oooo00o )
 oOo0oooo00o = '' . join ( oOo0oooo00o . splitlines ( ) ) . replace ( '\'' , '"' )
 oOo0oooo00o = oOo0oooo00o . replace ( '\n' , '' )
 oOo0oooo00o = oOo0oooo00o . replace ( '\t' , '' )
 oOo0oooo00o = re . sub ( '  +' , ' ' , oOo0oooo00o )
 oOo0oooo00o = oOo0oooo00o . replace ( '> <' , '><' )
 return oOo0oooo00o
 if 30 - 30: ooO0oo0oO0 - iii1I11ii1i1 - i11iIiiIii % iI1OoOooOOOO - ooO0oo0oO0 * oo0oooooO0
def oO0o0o0ooO0oO ( name , url , mode , iconimage ) :
 oO00O0O0O = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
 i1ii1iiI = xbmcgui . ListItem ( name , iconImage = "DefaultVideo.png" , thumbnailImage = iconimage )
 i1ii1iiI . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 if ( "youtube.com/user/" in url ) or ( "youtube.com/channel/" in url ) :
  oO00O0O0O = "plugin://plugin.video.youtube/%s/%s/" % ( url . split ( "/" ) [ - 2 ] , url . split ( "/" ) [ - 1 ] )
  return xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = oO00O0O0O , listitem = i1ii1iiI , isFolder = True )
 return xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = oO00O0O0O , listitem = i1ii1iiI )
 if 98 - 98: Ii * Ii / Ii + OO0oo0oOO
def iI1Ii11111iIi ( name , url , mode , iconimage ) :
 oO00O0O0O = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name )
 ii111111I1iII = True
 i1ii1iiI = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 i1ii1iiI . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 ii111111I1iII = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = oO00O0O0O , listitem = i1ii1iiI , isFolder = True )
 return ii111111I1iII
 if 68 - 68: Ii - ii11i * i11iIiiIii / iIii1 * II11iII
def i1iIi1iIi1i ( parameters ) :
 I1I1iIiII1 = { }
 if 4 - 4: oOoo + iIIi1iI1II111 * iii1I11ii1i1
 if parameters :
  OOoo0O = parameters [ 1 : ] . split ( "&" )
  for Oo0ooOo0o in OOoo0O :
   Ii1i1 = Oo0ooOo0o . split ( '=' )
   if ( len ( Ii1i1 ) ) == 2 :
    I1I1iIiII1 [ Ii1i1 [ 0 ] ] = Ii1i1 [ 1 ]
 return I1I1iIiII1
 if 15 - 15: ooO0oo0oO0
if os . path . exists ( O0O0OO0O0O0 ) == False :
 os . mkdir ( O0O0OO0O0O0 )
Iiooo0O = os . path . join ( O0O0OO0O0O0 , 'visitor' )
if 75 - 75: i11iiII % i11iiII . II11iII
if os . path . exists ( Iiooo0O ) == False :
 from random import randint
 III1iII1I1ii = open ( Iiooo0O , "w" )
 III1iII1I1ii . write ( str ( randint ( 0 , 0x7fffffff ) ) )
 III1iII1I1ii . close ( )
 if 61 - 61: ooO0oo0oO0
def O0OOO ( utm_url ) :
 II11iIiIIIiI = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
 import urllib2
 try :
  IIi = urllib2 . Request ( utm_url , None ,
 { 'User-Agent' : II11iIiIIIiI }
 )
  i11iIIIIIi1 = urllib2 . urlopen ( IIi ) . read ( )
 except :
  print ( "GA fail: %s" % utm_url )
 return i11iIIIIIi1
 if 67 - 67: II11iII . Ii . iIIi1iI1II111
def IIIIiiII111 ( group , name ) :
 try :
  try :
   from hashlib import md5
  except :
   from md5 import md5
  from random import randint
  import time
  from urllib import unquote , quote
  from os import environ
  from hashlib import sha1
  OOoOoo = "4.2.8"
  oO0000OOo00 = open ( Iiooo0O ) . read ( )
  iiIi1IIiIi = "VietTV24"
  oOO00Oo = "UA-52209804-2"
  i1iIIIi1i = "www.viettv24.com"
  iI1iIIiiii = "http://www.google-analytics.com/__utm.gif"
  if name == "None" :
   i1iI11i1ii11 = iI1iIIiiii + "?" + "utmwv=" + OOoOoo + "&utmn=" + str ( randint ( 0 , 0x7fffffff ) ) + "&utmp=" + quote ( iiIi1IIiIi ) + "&utmac=" + oOO00Oo + "&utmcc=__utma=%s" % "." . join ( [ "1" , "1" , oO0000OOo00 , "1" , "1" , "2" ] )
   if 58 - 58: o00oo % i11iIiiIii . Ii / ooOoo0O
   if 84 - 84: Ii . iIii1 / II1Ii1iI1i - i111I / oOooOoO0Oo0O / i11iiII
   if 12 - 12: i111I * Ii % oooO0oo0oOOOO % ii11i
   if 20 - 20: iii1I11ii1i1 % oo0oooooO0 / oo0oooooO0 + oo0oooooO0
   if 45 - 45: ooOoo0O - I1I - oOooOoO0Oo0O - o00oo . ooO0oo0oO0 / iIIi1iI1II111
  else :
   if group == "None" :
    i1iI11i1ii11 = iI1iIIiiii + "?" + "utmwv=" + OOoOoo + "&utmn=" + str ( randint ( 0 , 0x7fffffff ) ) + "&utmp=" + quote ( iiIi1IIiIi + "/" + name ) + "&utmac=" + oOO00Oo + "&utmcc=__utma=%s" % "." . join ( [ "1" , "1" , oO0000OOo00 , "1" , "1" , "2" ] )
    if 51 - 51: iIIi1iI1II111 + Ii
    if 8 - 8: ooOoo0O * iI1OoOooOOOO - oo0oooooO0 - o00oo * iii1I11ii1i1 % i111I
    if 48 - 48: iIIi1iI1II111
    if 11 - 11: OO0oo0oOO + oOooOoO0Oo0O - o00oo / i11iiII + II1Ii1iI1i . ooO0oo0oO0
    if 41 - 41: oo0oooooO0 - iIIi1iI1II111 - iIIi1iI1II111
   else :
    i1iI11i1ii11 = iI1iIIiiii + "?" + "utmwv=" + OOoOoo + "&utmn=" + str ( randint ( 0 , 0x7fffffff ) ) + "&utmp=" + quote ( iiIi1IIiIi + "/" + group + "/" + name ) + "&utmac=" + oOO00Oo + "&utmcc=__utma=%s" % "." . join ( [ "1" , "1" , oO0000OOo00 , "1" , "1" , "2" ] )
    if 68 - 68: iii1I11ii1i1 % II11iII
    if 88 - 88: ii11i - oOoo + iii1I11ii1i1
    if 40 - 40: i111I * oo0oooooO0 + iii1I11ii1i1 % Ii
    if 74 - 74: ooOoo0O - II1Ii1iI1i + oOooOoO0Oo0O + II11iII / iI1OoOooOOOO
    if 23 - 23: iIIi1iI1II111
    if 85 - 85: oo0oooooO0
  print "============================ POSTING ANALYTICS ============================"
  O0OOO ( i1iI11i1ii11 )
  if 84 - 84: i111I . ii11i % oOooOoO0Oo0O + oo0oooooO0 % oOooOoO0Oo0O % o00oo
  if not group == "None" :
   IIi1 = iI1iIIiiii + "?" + "utmwv=" + OOoOoo + "&utmn=" + str ( randint ( 0 , 0x7fffffff ) ) + "&utmhn=" + quote ( i1iIIIi1i ) + "&utmt=" + "events" + "&utme=" + quote ( "5(" + iiIi1IIiIi + "*" + group + "*" + name + ")" ) + "&utmp=" + quote ( iiIi1IIiIi ) + "&utmac=" + oOO00Oo + "&utmcc=__utma=%s" % "." . join ( [ "1" , "1" , "1" , oO0000OOo00 , "1" , "2" ] )
   if 45 - 45: Ii / Ii + II11iII + oOoo
   if 47 - 47: i11iiII + oOoo
   if 82 - 82: ooO0oo0oO0 . I1I - ii11i - I1I * ooO0oo0oO0
   if 77 - 77: ii11i * o00oo
   if 95 - 95: i111I + i11iIiiIii
   if 6 - 6: oOoo / i11iIiiIii + Ii * ooOoo0O
   if 80 - 80: ooO0oo0oO0
   if 83 - 83: OO0oo0oOO . i11iIiiIii + ooO0oo0oO0 . i11iiII * OO0oo0oOO
   try :
    print "============================ POSTING TRACK EVENT ============================"
    O0OOO ( IIi1 )
   except :
    print "============================  CANNOT POST TRACK EVENT ============================"
    if 53 - 53: ooO0oo0oO0
 except :
  print "================  CANNOT POST TO ANALYTICS  ================"
  if 31 - 31: o00oo
o0O = i1iIi1iIi1i ( sys . argv [ 2 ] )
IiIIii1iII1II = o0O . get ( 'mode' )
Iii1I1I11iiI1 = o0O . get ( 'url' )
oo0o0O00 = o0O . get ( 'name' )
if type ( Iii1I1I11iiI1 ) == type ( str ( ) ) :
 Iii1I1I11iiI1 = urllib . unquote_plus ( Iii1I1I11iiI1 )
if type ( oo0o0O00 ) == type ( str ( ) ) :
 oo0o0O00 = urllib . unquote_plus ( oo0o0O00 )
 if 18 - 18: iii1I11ii1i1 + Ii - oo0oooooO0 . ooO0oo0oO0 + i11iIiiIii
iI1Ii1iI11iiI = str ( sys . argv [ 1 ] )
if IiIIii1iII1II == 'index' :
 IIIIiiII111 ( "Browse" , oo0o0O00 )
 I1iiiiI1iII ( Iii1I1I11iiI1 )
elif IiIIii1iII1II == 'indexgroup' :
 IIIIiiII111 ( "Browse" , oo0o0O00 )
 iiI1iIiI ( Iii1I1I11iiI1 )
elif IiIIii1iII1II == 'play' :
 IIIIiiII111 ( "Play" , oo0o0O00 + "/" + Iii1I1I11iiI1 )
 if any ( x in Iii1I1I11iiI1 for x in [ ".jpg" , ".zip" ] ) :
  i11Iiii ( Iii1I1I11iiI1 )
 else :
  OO0OO0O00oO0 = xbmcgui . DialogProgress ( )
  OO0OO0O00oO0 . create ( 'Brought to you by VietTV24.com' , 'Loading video. Please wait...' )
  iii11I111 ( Iii1I1I11iiI1 , oo0o0O00 )
  OO0OO0O00oO0 . close ( )
  del OO0OO0O00oO0
else :
 IIIIiiII111 ( "None" , "None" )
 iI1 ( )
xbmcplugin . endOfDirectory ( int ( iI1Ii1iI11iiI ) ) # dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
