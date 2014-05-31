
try:
    import urllib.request as urllib2  # py3
except:
    import urllib2  # py2

try:
    import urllib.parse as urlparse  # py3
except:
    import urlparse  # py2

import json


from . import Crawler, CrawlerError







class Reddit(Crawler):
    """ class def: a crawler for Reddit image threads """

    __uri = ""
    __next = ""

    @staticmethod
    def __build_uri(uri):
        return uri + ".json"

    def __init__(self, uri):
        self.__uri = Reddit.__build_uri(uri)
        self.__next = ""

    def _crawl(self):
        uri = urlparse.urljoin(self.__uri, "?after="+self.__next)
        Crawler._log("debug", "Reddit crawls url: " + uri)

        request = urllib2.Request(uri, headers=Crawler.headers())
        response = urllib2.urlopen(request, timeout=Crawler.timeout())

        charset = 'utf8'
        try:  # py3
            charset = response.info().get_param('charset', charset)
        except:
            pass

        data = json.loads(response.read().decode(charset))

        self.__next = data['data']['after']

        for child in data['data']['children']:
            image = child['data']['url']
            Crawler._add_image(image)
