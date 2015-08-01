from xbmcswift2 import Plugin, xbmcgui
from resources.lib.api import SiteApi


plugin = Plugin()
api = SiteApi()


@plugin.cached_route('/')
def index():
    '''
    Get movie categories
    '''
    plugin.log.debug('Get category menu')

    c = api.get_menu_category()

    items = [{
        'label': item['label'],
        'path': plugin.url_for(
            'browse_category', menuid=item.get('pk', '0'),
            page=1, url=item['url'])
    } for item in c]

    return items


@plugin.cached_route('/<menuid>/page/<page>')
def browse_category(menuid, page='1'):
    '''
    Get list of movies from category
    '''
    plugin.log.debug('Get movies menu')

    url = plugin.request.args['url'][0]
    movies = api.get_menu_movies(url)

    items = [{
        'label': item['label'],
        'thumbnail': item['thumb'],
        'icon': item['thumb'],
        'info': {
            'plot': item['info']
        },
        'path': plugin.url_for(
            'browse_movie', menuid=menuid, page=page,
            movieid=item.get('pk', '0'), url=item['url'])
    } for item in movies]

    # build next link
    next_link = api.get_next_link(url)
    if next_link:
        items.append({
            'label': next_link['label'],
            'path': plugin.url_for(
                'browse_category', menuid=item.get('pk', '0'),
                page=next_link['pk'], url=next_link['url'])
        })

    return items


@plugin.route('/<menuid>/page/<page>/movie/<movieid>/')
def browse_movie(menuid, page, movieid):
    '''
    Get links for movie
    '''
    plugin.log.debug('Get movie links')

    page_url = plugin.request.args['url'][0]
    links = api.get_movie_links(page_url)

    items = [{
        'label': item['label'],
        'is_playable': item['is_playable'],
        'path': plugin.url_for(
            'resolve_movie', menuid=menuid, page=page,
            movieid=movieid, linkid=item.get('pk', '0'), 
            url=item['url'])
    } for item in links]

    return items

@plugin.route('/<menuid>/page/<page>/movie/<movieid>/<linkid>')
def resolve_movie(menuid, page, movieid, linkid):
    '''
    Play movie
    '''
    page_url = plugin.request.args['url'][0]
    url = api.resolve_redirect(page_url)

    print 'resolve video: {url}'.format(url=url)
    plugin.log.debug('resolve video: {url}'.format(url=url))

    if url:
        media = __resolve_item(url, movieid)

        print 'resolved to: {url}'.format(url=media)

        if media:
            plugin.set_resolved_url(media)
        else:
            msg = ['cannot play video stream']
            plugin.log.error(msg[0])
            dialog = xbmcgui.Dialog()
            dialog.ok(api.LONG_NAME, *msg)
    else:
        msg = ['video url not found']
        plugin.log.error(msg[0])
        dialog = xbmcgui.Dialog()
        dialog.ok(api.LONG_NAME, *msg)


def __resolve_item(url, title):
    import urlresolver

    media = urlresolver.HostedMediaFile(
        url=url, title=title)
    return media.resolve()


###############################################


if __name__ == '__main__':
    try:
        plugin.run()
    except Exception, e:
        print e
        plugin.log.error(e)
        plugin.notify(msg=e)
