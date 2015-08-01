'''
Created on Oct 29, 2011

@author: ajju
'''
import urllib
from common.Singleton import SingletonClass
import urllib2
from BeautifulSoup import BeautifulSoup
import cookielib

def getUrlParams(url):
    params = {}
    if url is None:
        return params
    paramstring = url
    if len(paramstring) >= 2:
        paramstring = paramstring.replace('?', '')
        if (paramstring[len(paramstring) - 1] == '/'):
            paramstring = paramstring[0:len(paramstring) - 2]
        pairsofparams = paramstring.split('&')
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                params[splitparams[0]] = urllib.unquote_plus(splitparams[1])
    return params

def getRedirectedUrl(url, data=None):
    opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
    if data == None:
        return opener.open(url).url
    else:
        return opener.open(url, data).url

def unescape(url):
    htmlCodes = [
                 ['&', '&amp;'],
                 ['<', '&lt;'],
                 ['>', '&gt;'],
                 ['"', '&quot;'],
                 ]
    for code in htmlCodes:
        url = url.replace(code[1], code[0])
    return url

def getUserAgentForXBMCPlay():
    return 'User-Agent=' + urllib.quote_plus('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_1) AppleWebKit/534.48.3 (KHTML, like Gecko) Version/5.1 Safari/534.48.3' + '&Accept=' + urllib.quote_plus('text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8') + '&Accept_Encoding=' + urllib.quote_plus('gzip, deflate'))

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_1) AppleWebKit/534.48.3 (KHTML, like Gecko) Version/5.1 Safari/534.48.3'}
#, 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept_Encoding':'gzip, deflate'
#HttpClient
class HttpClient(SingletonClass):
    
    def __initialize__(self):
        self.__cookiejar = cookielib.LWPCookieJar()
        
    def enableCookies(self, cookieJar=None, cookiesFilePath=None):
        if cookieJar is not None:
            self.__cookiejar = cookieJar
        elif cookiesFilePath is not None:
            self.loadCookiesToFile(cookiesFilePath)
        else:
            cookieJar = self.__cookiejar
        http_cookiejar = urllib2.HTTPCookieProcessor(cookieJar)
        opener = urllib2.build_opener(http_cookiejar)
        urllib2.install_opener(opener)
        
    def disableCookies(self):
        urllib2.install_opener(None)
        
    def saveCookiesToFile(self, filepath):
        self.__cookiejar.save(filename=filepath, ignore_discard=True, ignore_expires=True)
        
    def loadCookiesToFile(self, filepath):
        self.__cookiejar.load(filename=filepath, ignore_discard=True, ignore_expires=True)
    
    def get_cookiejar(self):
        return self.__cookiejar
    
    def get_cookie_string(self):
        cookies = ''
        if self.__cookiejar is not None:
            for cookie in self.__cookiejar:
                cookies = cookies + cookie.name + '=' + cookie.value + '; '
        return cookies
    
    def getHtmlContent(self, url, params=None, headers=None):
        if headers is None:
            headers = HEADERS
        data = None
        if params is not None:
            data = urllib.urlencode(params)
        req = urllib2.Request(url, data, headers)
        
        response = urllib2.urlopen(req)
        html = response.read()
        response.close()
        return html
    
    def getBeautifulSoup(self, url, params=None, headers=None, parseOnlyThese=None):
        return BeautifulSoup(self.getHtmlContent(url, params, headers), parseOnlyThese)
        
    def addHttpCookiesToUrl(self, url, addHeaders=True, addCookies=True, extraExtraHeaders={}):
        url = url + '|'
        if addHeaders:
            url = url + getUserAgentForXBMCPlay() + '&'
        if addCookies:
            url = url + 'Cookie=' + urllib.quote_plus(self.get_cookie_string()) + '&'
        for extraHeaderName in extraExtraHeaders:
            url = url + extraHeaderName + '=' + urllib.quote_plus(extraExtraHeaders[extraHeaderName])
        return url
