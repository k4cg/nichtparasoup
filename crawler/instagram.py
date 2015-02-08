
try:
    import urllib.request as urllib2  # py3
except:
    import urllib2  # py2

try:
    import urllib.parse as urlparse  # py3
except:
    import urlparse  # py2

import re
import json

from bs4 import BeautifulSoup

from . import Crawler, CrawlerError


class Instagram(Crawler):
    """ instagram image provider """

    __uri = ""
    __last = ""

    ## class methods

    @classmethod
    def __build_uri(cls, uri):
        return uri +"/media/"

    ## instance methods

    def _restart_at_front(self):
        self.__last = ""

    def __init__(self, uri):
        self.__uri = self.__class__.__build_uri(uri)
        self._restart_at_front()

    def _crawl(self):
        uri = urlparse.urljoin(self.__uri, "?max_id="+self.__last)
        self.__class__._log("debug", "%s crawls url: %s" % (self.__class__.__name__, uri))

        request = urllib2.Request(uri, headers=self.__class__.headers())
        response = urllib2.urlopen(request, timeout=self.__class__.timeout())

        charset = 'utf8'
        try:  # py3
            charset = response.info().get_param('charset', charset)
        except:
            pass

        data = json.loads(response.read().decode(charset))
        if data["status"] != "ok":
            raise CrawlerError()

        for item in data['items']:
            if item["type"] == "image":
                self.__last = item['id']
                image = item['images']['standard_resolution']['url']
                self._add_image(image)

