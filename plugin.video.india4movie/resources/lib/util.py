import requests


# allows us to get mobile version
user_agent_mobile = 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3'

user_agent_desktop = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0'

addon_id = 'plugin.video.india4movie'


def get_image_path(image):
    ''' get image path '''
    image = 'special://home/addons/{id}/resources/images/{image}'.format(
        id=addon_id, image=image)
    return image


def get_remote_data(url, ismobile=True, referer=None):
    ''' fetch website data as mobile or desktop browser'''
    user_agent = user_agent_mobile if ismobile else user_agent_desktop

    headers = {'User-Agent': user_agent}
    if referer:
        headers['Referer'] = referer

    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    return r.content


def is_site_available(url):
    ''' ping site to see if it is up '''
    print 'Checking url: {url}'.format(url=url)

    try:
        r = requests.head(url)
        return r.status_code < 400

    except:
        return False
