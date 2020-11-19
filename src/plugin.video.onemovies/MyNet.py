'''
    common XBMC Module
    Copyright (C) 2011 t0mm0

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import cookielib
import gzip
import re
import StringIO
import urllib
import urllib2
import socket
from urlparse import urlparse
from urlparse import urlunparse
import time

class HeadRequest(urllib2.Request):
    '''A Request class that sends HEAD requests'''
    def get_method(self):
        return 'HEAD'

class MyNet:
    '''
    This class wraps :mod:`urllib2` and provides an easy way to make http
    requests while taking care of cookies, proxies, gzip compression and 
    character encoding.
    
    Example::
    
        from addon.common.net import Net
        net = Net()
        response = net.http_GET('http://xbmc.org')
        print response.content
    '''
    IE_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'
    FF_USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'
    IOS_USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25'
    ANDROID_USER_AGENT = 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 4 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.114 Mobile Safari/537.36'

    _cj = cookielib.LWPCookieJar()

    _proxy = None
    _user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'
    _accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    _http_debug = False
    _socket_timeout = 60
    
    def __init__(self, cookie_file='', proxy='', user_agent='', 
                 http_debug=False, accept=_accept, socket_timeout=_socket_timeout, cloudflare=False):
        '''
        Kwargs:
            cookie_file (str): Full path to a file to be used to load and save
            cookies to.
            
            proxy (str): Proxy setting (eg. 
            ``'http://user:pass@example.com:1234'``)
            
            user_agent (str): String to use as the User Agent header. If not 
            supplied the class will use a default user agent (chrome)
            
            http_debug (bool): Set ``True`` to have HTTP header info written to
            the XBMC log for all requests.
            
            accept (str) : String to use as HTTP Request Accept header.
            
            socket_timeout (int): time in seconds for socket connections to wait until time out

            cloudflare (bool): Set ``True`` to check all requests that raise HTTPError 503 for Cloudflare challenge and solve
            This can be changed per request as well, see http_GET, http_PUSH
        '''
        
        #Set socket timeout - Useful for slow connections
        socket.setdefaulttimeout(socket_timeout)

        # empty jar for each instance rather than scope of the import
        self._cloudflare_jar = cookielib.LWPCookieJar()

        self.cloudflare = cloudflare
        if cookie_file:
            self.set_cookies(cookie_file)
        if proxy:
            self.set_proxy(proxy)
        if user_agent:
            self.set_user_agent(user_agent)
        self._http_debug = http_debug
        self._update_opener()
        
    
    def set_cookies(self, cookie_file):
        '''
        Set the cookie file and try to load cookies from it if it exists.
        
        Args:
            cookie_file (str): Full path to a file to be used to load and save
            cookies to.
        '''
        try:
            self._cj.load(cookie_file, ignore_discard=True)
            self._update_opener()
            return True
        except:
            return False
        
    
    def get_cookies(self):
        '''Returns A dictionary containing all cookie information by domain.'''
        return self._cj._cookies


    def save_cookies(self, cookie_file):
        '''
        Saves cookies to a file.
        
        Args:
            cookie_file (str): Full path to a file to save cookies to.
        '''
        self._cj.save(cookie_file, ignore_discard=True)        

        
    def set_proxy(self, proxy):
        '''
        Args:
            proxy (str): Proxy setting (eg. 
            ``'http://user:pass@example.com:1234'``)
        '''
        self._proxy = proxy
        self._update_opener()

        
    def get_proxy(self):
        '''Returns string containing proxy details.'''
        return self._proxy
        
        
    def set_user_agent(self, user_agent):
        '''
        Args:
            user_agent (str): String to use as the User Agent header.
        '''
        self._user_agent = user_agent

        
    def get_user_agent(self):
        '''Returns user agent string.'''
        return self._user_agent


    def _update_opener(self, cloudflare_jar=False):
        """
        Builds and installs a new opener to be used by all future calls to
        :func:`urllib2.urlopen`.
        """
        if self._http_debug:
            http = urllib2.HTTPHandler(debuglevel=1)
        else:
            http = urllib2.HTTPHandler()

        if cloudflare_jar:
            self._cloudflare_jar = cookielib.LWPCookieJar()
            jar = self._cloudflare_jar
        else:
            jar = self._cj

        if self._proxy:
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar),
                                          urllib2.ProxyHandler({'http':
                                                                self._proxy}),
                                          urllib2.HTTPBasicAuthHandler(),
                                          http)

        else:
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar),
                                          urllib2.HTTPBasicAuthHandler(),
                                          http)
        urllib2.install_opener(opener)


    def _parseJSString(self, s):
        """
        lambda
        plugin.video.genesis\resources\lib\libraries\cloudflare.py
        https://offshoregit.com/lambda81/
        """
        try:
            offset=1 if s[0]=='+' else 0
            val = int(eval(s.replace('!+[]','1').replace('!![]','1').replace('[]','0').replace('(','str(')[offset:]))
            return val
        except:
            raise Exception


    def _cloudflare_challenge(self, url, challenge, form_data={}, headers={}, compression=True):
        """
        Use _set_cloudflare to call this, not intended to be called directly.
        Solve challenge and make request with cloudflare cookie jar

        Part from:
        lambda
        plugin.video.genesis\resources\lib\libraries\cloudflare.py
        https://offshoregit.com/lambda81/
        """
        jschl = re.compile('name="jschl_vc" value="(.+?)"/>').findall(challenge)[0]
        init = re.compile('setTimeout\(function\(\){\s*.*?.*:(.*?)};').findall(challenge)[0]
        builder = re.compile(r"challenge-form\'\);\s*(.*)a.v").findall(challenge)[0]
        decrypt_val = self._parseJSString(init)
        lines = builder.split(';')

        for line in lines:
            if len(line)>0 and '=' in line:
                sections=line.split('=')
                line_val = self._parseJSString(sections[1])
                decrypt_val = int(eval(str(decrypt_val)+sections[0][-1]+str(line_val)))

        path = urlparse(url).path
        netloc = urlparse(url).netloc
        if not netloc:
            netloc = path

        answer = decrypt_val + len(netloc)

        url = url.rstrip('/')
        query = '%s/cdn-cgi/l/chk_jschl?jschl_vc=%s&jschl_answer=%s' % (url, jschl, answer)

        if 'type="hidden" name="pass"' in challenge:
            passval = re.compile('name="pass" value="(.*?)"').findall(challenge)[0]
            query = '%s/cdn-cgi/l/chk_jschl?pass=%s&jschl_vc=%s&jschl_answer=%s' % \
                    (url, urllib.quote_plus(passval), jschl, answer)
            time.sleep(9)

        self._update_opener(cloudflare_jar=True)
        req = urllib2.Request(query)
        if form_data:
            form_data = urllib.urlencode(form_data)
            req = urllib2.Request(query, form_data)
        req.add_header('User-Agent', self._user_agent)
        for k, v in headers.items():
            req.add_header(k, v)
        if compression:
            req.add_header('Accept-Encoding', 'gzip')
        try:
            response = urllib2.urlopen(req)
        except urllib2.HTTPError as e:
            pass


    def _set_cloudflare(self, url, challenge, form_data={}, headers={}, compression=True):
        """
        Entry Point for _cloudflare_challenge
        Calls cloudflare_challenge on netloc, not full url w/ path
        Puts any cloudflare cookies in the main cookie jar
        Args:
            url (str): The URL to site of potential Cloudflare IUA.

            challenge (str): html contents of the page that raised 503, containing potential Cloudflare IUA Challenge
        Kwargs:
            form_data (dict): A dictionary of form data if pass-through from POST.

            headers (dict): A dictionary describing any headers you would like
            to add to the request. (eg. ``{'X-Test': 'testing'}``)

            compression (bool): If ``True`` (default), try to use gzip
            compression.
        """
        netloc = urlparse(url).netloc
        if not netloc:
            netloc = urlparse(url).path
        cloudflare_url = urlunparse((urlparse(url).scheme, netloc, '', '', '', ''))
        try:
            self._cloudflare_challenge(cloudflare_url, challenge, form_data, headers, compression)
            for c in self._cloudflare_jar:
                self._cj.set_cookie(c)
            self._update_opener()
        except:
            # make sure we update to main jar
            self._update_opener()
            raise Exception


    def url_with_headers(self, url, referer=None, user_agent=None, cookies=None, proxy=None, connection_timeout=None,
                         encoding='', accept_charset='', sslcipherlist='', noshout='false', seekable='1'):
        '''
        Return url with Referer, User-Agent, Cookies, Proxy, Connection-Timeout, Encoding, Accept-Charset,
        SSLCipherList, NoShout and Seekable
        Based on: https://github.com/xbmc/xbmc/blob/master/xbmc/filesystem/CurlFile.cpp#L782
        Args:
            url (str): The URL to append headers to.

        Kwargs:
            referer (str): If None (default), urlunparse((urlparse(url).scheme, netloc, path, '', '', '')) is used and append if set

            user_agent (str): If None (default), self._user_agent is used and append if set

            cookies (bool): If ``None`` (default), use self.cloudflare as bool (False as default)
            Append cookies to URL as well

            proxy (str): If None (default), self.proxy is used and append if set

            connection_timeout (str): If None (default), self._socket_timeout is used and append if set

            encoding (str): append if set

            accept_charset (str): append if set

            sslcipherlist (str): append if set

            noshout (str): 'true'/'false', skip shout, append if 'true' ('false' is kodi default)

            seekable (str): '0'/'1', append if 0 ('1' is kodi default)
        Returns:
            http://example.com/myimage.png|Referer=%%%%%&User-Agent=%%%%%...
        '''
        kodi_schemes = ('special', 'plugin', 'script', 'profile')
        if ('://' not in url) or (url.startswith(kodi_schemes)):
            # don't waste time and return url
            return url

        _tmp = re.search('(.+?)(?:\|.*|$)', url)
        if _tmp:
            # trim any headers that may already be attached to url
            url = _tmp.group(1)

        if referer is not None:
            try:
                referer = str(referer)
            except:
                referer = None
        if referer is None:
            path = urlparse(url).path
            netloc = urlparse(url).netloc
            if not netloc:
                netloc = path
                path = ''
            referer = urlunparse((urlparse(url).scheme, netloc, path, '', '', ''))
            if referer == url:
                index = path.rfind('/')
                if index >= 0:
                    referer = urlunparse((urlparse(url).scheme, netloc, path[:index], '', '', ''))
        if user_agent is None:
            user_agent = self._user_agent
        else:
            try:
                user_agent = str(user_agent)
            except:
                user_agent = self._user_agent
        if cookies is None:
            cookies = self.cloudflare
        if proxy is None:
            proxy = self._proxy
        if connection_timeout is None:
            connection_timeout = self._socket_timeout
        try:
            connection_timeout = str(connection_timeout)
        except:
            connection_timeout = None
        try:
            if str(seekable) != '0':
                seekable = None
        except:
            seekable = None
        try:
            if str(noshout).lower() != 'true':
                noshout = None
        except:
            noshout = None

        url += '|Referer=' + urllib.quote_plus(referer) + '&User-Agent=' + urllib.quote_plus(user_agent)
        if proxy:
            try:
                url += '&HTTPProxy=' + urllib.quote_plus(str(proxy))
            except:
                pass
        if connection_timeout:
            url += '&Connection-Timeout=' + urllib.quote_plus(connection_timeout)
        if encoding:
            try:
                url += '&Encoding=' + urllib.quote_plus(str(encoding))
            except:
                pass
        if accept_charset:
            try:
                url += '&Accept-Charset=' + urllib.quote_plus(str(accept_charset))
            except:
                pass
        if sslcipherlist:
            try:
                url += '&SSLCipherList=' + urllib.quote_plus(str(sslcipherlist))
            except:
                pass
        if noshout:
            url += '&NoShout=' + urllib.quote_plus(str(noshout).lower())
        if seekable:
            url += '&Seekable=' + urllib.quote_plus(str(seekable))
        if cookies:
            cookie_string = ''
            for c in self._cj:
                if c.domain and (c.domain.lstrip('.') in url):
                    cookie_string += '%s=%s;' % (c.name, c.value)
            if cookie_string:
                url += '&Cookie=' + urllib.quote_plus(cookie_string)
        return url


    def http_GET(self, url, headers={}, compression=True, cloudflare=None):
        '''
        Perform an HTTP GET request.
        
        Args:
            url (str): The URL to GET.
            
        Kwargs:
            headers (dict): A dictionary describing any headers you would like
            to add to the request. (eg. ``{'X-Test': 'testing'}``)

            compression (bool): If ``True`` (default), try to use gzip 
            compression.

            cloudflare (bool): If ``None`` (default), use self.cloudflare as bool (False as default)
            On HTTPError 503 check for Cloudflare challenge and solve
        Returns:
            An :class:`HttpResponse` object containing headers and other 
            meta-information about the page and the page content.
        '''
        if cloudflare is None:
            cloudflare = self.cloudflare
        return self._fetch(url, headers=headers, compression=compression, cloudflare=cloudflare)
        

    def http_POST(self, url, form_data, headers={}, compression=True, cloudflare=None):
        '''
        Perform an HTTP POST request.
        
        Args:
            url (str): The URL to POST.
            
            form_data (dict): A dictionary of form data to POST.
            
        Kwargs:
            headers (dict): A dictionary describing any headers you would like
            to add to the request. (eg. ``{'X-Test': 'testing'}``)

            compression (bool): If ``True`` (default), try to use gzip 
            compression.

            cloudflare (bool): If ``None`` (default), use self.cloudflare as bool (False as default)
            On HTTPError 503 check for Cloudflare challenge and solve
        Returns:
            An :class:`HttpResponse` object containing headers and other 
            meta-information about the page and the page content.
        '''
        if cloudflare is None:
            cloudflare = self.cloudflare
        return self._fetch(url, form_data, headers=headers,
                           compression=compression, cloudflare=cloudflare)

    
    def http_HEAD(self, url, headers={}):
        '''
        Perform an HTTP HEAD request.
        
        Args:
            url (str): The URL to GET.
        
        Kwargs:
            headers (dict): A dictionary describing any headers you would like
            to add to the request. (eg. ``{'X-Test': 'testing'}``)
        
        Returns:
            An :class:`HttpResponse` object containing headers and other 
            meta-information about the page.
        '''
        req = HeadRequest(url)
        req.add_header('User-Agent', self._user_agent)
        req.add_header('Accept', self._accept)
        for k, v in headers.items():
            req.add_header(k, v)
        response = urllib2.urlopen(req)
        return HttpResponse(response)


    def _fetch(self, url, form_data={}, headers={}, compression=True, cloudflare=None):
        '''
        Perform an HTTP GET or POST request.
        
        Args:
            url (str): The URL to GET or POST.
            
            form_data (dict): A dictionary of form data to POST. If empty, the 
            request will be a GET, if it contains form data it will be a POST.
            
        Kwargs:
            headers (dict): A dictionary describing any headers you would like
            to add to the request. (eg. ``{'X-Test': 'testing'}``)

            compression (bool): If ``True`` (default), try to use gzip 
            compression.

            cloudflare (bool): If ``None`` (default), use self.cloudflare as bool (False as default)
            On HTTPError 503 check for Cloudflare challenge and solve
        Returns:
            An :class:`HttpResponse` object containing headers and other 
            meta-information about the page and the page content.
        '''
        if cloudflare is None:
            cloudflare = self.cloudflare
        encoding = ''
        req = urllib2.Request(url)
        if form_data:
            form_data = urllib.urlencode(form_data)
            req = urllib2.Request(url, form_data)
        req.add_header('User-Agent', self._user_agent)
        for k, v in headers.items():
            req.add_header(k, v)
        if compression:
            req.add_header('Accept-Encoding', 'gzip')
        if not cloudflare:
            response = urllib2.urlopen(req)
            return HttpResponse(response)
        else:
            try:
                response = urllib2.urlopen(req)
                return HttpResponse(response)
            except urllib2.HTTPError as e:
                if e.code == 503:
                    try:
                        self._set_cloudflare(url, e.read(), form_data, headers, compression)
                    except:
                        raise urllib2.HTTPError, e
                    req = urllib2.Request(url)
                    if form_data:
                        form_data = urllib.urlencode(form_data)
                        req = urllib2.Request(url, form_data)
                    req.add_header('User-Agent', self._user_agent)
                    for k, v in headers.items():
                        req.add_header(k, v)
                    if compression:
                        req.add_header('Accept-Encoding', 'gzip')
                    response = urllib2.urlopen(req)
                    return HttpResponse(response)
                else:
                    raise urllib2.HTTPError, e


class HttpResponse:
    '''
    This class represents a response from an HTTP request.
    
    The content is examined and every attempt is made to properly encode it to
    Unicode.
    
    .. seealso::
        :meth:`Net.http_GET`, :meth:`Net.http_HEAD` and :meth:`Net.http_POST` 
    '''
    
    content = ''
    '''Unicode encoded string containing the body of the response.'''
    
    
    def __init__(self, response):
        '''
        Args:
            response (:class:`mimetools.Message`): The object returned by a call
            to :func:`urllib2.urlopen`.
        '''
        self._response = response
        html = response.read()
        try:
            if response.headers['content-encoding'].lower() == 'gzip':
                html = gzip.GzipFile(fileobj=StringIO.StringIO(html)).read()
        except:
            pass
        
        try:
            content_type = response.headers['content-type']
            if 'charset=' in content_type:
                encoding = content_type.split('charset=')[-1]
        except:
            pass

        r = re.search('<meta\s+http-equiv="Content-Type"\s+content="(?:.+?);' +
                      '\s+charset=(.+?)"', html, re.IGNORECASE)
        if r:
            encoding = r.group(1) 
                   
        try:
            html = unicode(html, encoding)
        except:
            pass
        
        #try:
        #    if response.headers['content-encoding'].lower() == 'gzip':
        #        r = re.search('<meta\s+http-equiv="Content-Type"\s+content="(?:.+?);' + '\s+charset=(.+?)"', html, re.IGNORECASE)
        #        if r:
        #        	encoding = r.group(1) 
        #        	try:
        #        		html = unicode(html, encoding)
        #        	except:
        #        		pass
        #except:
        #    pass
            
        self.content = html
    
    
    def get_headers(self):
        '''Returns a List of headers returned by the server.'''
        return self._response.info().headers
    
        
    def get_url(self):
        '''
        Return the URL of the resource retrieved, commonly used to determine if 
        a redirect was followed.
        '''
        return self._response.geturl()