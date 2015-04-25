


try:
    import urllib.parse as urlparse  # py3
except:
    import urlparse  # py2

import json

from . import Crawler, CrawlerError


class Giphy(Crawler):
    """ class def: a crawler for Giphy """

    __uri = ""
    __next = 0

    __limit = 50

    __api_key = "dc6zaTOxFJmzC"

    @classmethod
    def _build_uri(cls, uri):
        return uri + "&api_key=" + cls.__api_key + "&limit=" + str(cls.__limit)

    def _restart_at_front(self):
        self.__next = 0

    def __init__(self, uri):
        self.__uri = self.__class__._build_uri(uri)
        self._restart_at_front()

    def _crawl(self):
        uri = self.__uri + "&offset=" + str(self.__next)
        self.__class__._log("debug", "%s crawls url: %s" % (self.__class__.__name__, uri))

        remote = self.__class__._fetch_remote(uri)
        if not remote:
            self.__class__._log("debug", "%s crawled EMPTY url: %s" % (self.__class__.__name__, uri))
            return

        data = json.loads(remote)

        self.__next += self.__limit

        images_added = 0
        for child in data['data']:
            image = child['images']['original']['url']
            if image:
                if self._add_image(image):
                    images_added += 1

        if not images_added:
            self.__class__._log("debug", "%s found no images on url: %s" % (self.__class__.__name__, uri))
