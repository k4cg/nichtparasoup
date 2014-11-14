
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

    def _restart_at_front(self):
        self.__next = ""

    def __init__(self, uri):
        self.__uri = self.__class__.__build_uri(uri)
        self._restart_at_front()

    def _crawl(self):
        uri = urlparse.urljoin(self.__uri, "?after="+self.__next)
        self.__class__._log("debug", "%s crawls url: %s" % (self.__class__.__name__, uri))

        request = urllib2.Request(uri, headers=self.__class__.headers())
        response = urllib2.urlopen(request, timeout=self.__class__.timeout())

        charset = 'utf8'
        try:  # py3
            charset = response.info().get_param('charset', charset)
        except:
            pass

        data = json.loads(response.read().decode(charset))

        self.__next = data['data']['after']

        for child in data['data']['children']:
            image = child['data']['url']
            self._add_image(image)
