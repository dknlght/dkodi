'''
    Plugin for URLResolver
    Copyright (C) 2020 gujal

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

from urlresolver import common
from urlresolver.resolver import UrlResolver, ResolverError
from urlresolver.plugins.lib import helpers
import re
import json


class PlayTubeResolver(UrlResolver):
    name = "playtube"
    domains = ["playtube.ws"]
    pattern = r'(?://|\.)(playtube\.ws)/(?:embed-)?([0-9a-zA-Z]+)'

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {'User-Agent': common.RAND_UA}
        html = self.net.http_GET(web_url, headers=headers).content
        html = helpers.get_packed_data(html)
        r = re.search(r"op:\s*'([^']+)',\s*file_code:\s*'([^']+)',\s*hash:\s*'([^']+)'", html)
        if r:
            url = 'https://playtube.ws/dl'
            data = {'op': r.group(1),
                    'file_code': r.group(2),
                    'hash': r.group(3)}
            headers.update({'Referer': url[:-2],
                            'Origin': url[:-3]})

            vfile = seed = None
            tries = 0
            while tries < 3 and vfile is None and seed is None:
                resp = self.net.http_POST(url, form_data=data, headers=headers).content
                resp = json.loads(resp)[0]
                vfile = resp.get('file')
                seed = resp.get('seed')
                tries += 1
            source = helpers.tear_decode(vfile, seed)
            if source:
                return source + helpers.append_headers(headers)
        raise ResolverError('File not found')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://{host}/embed-{media_id}.html')
