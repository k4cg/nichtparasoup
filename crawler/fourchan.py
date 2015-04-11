
try:
    import urllib.request as urllib2  # py3
except:
    import urllib2  # py2

try:
    import urllib.parse as urlparse  # py3
except:
    import urlparse  # py2

from bs4 import BeautifulSoup

from . import Crawler, CrawlerError


class Fourchan(Crawler):
    """ Fourchan image provider """

    __uri = ""
    __next = ""

    @staticmethod
    def __build_uri(uri):
        return uri

    def _restart_at_front(self):
        self.__next = ""

    def __init__(self, uri):
        self.__uri = self.__class__.__build_uri(uri)
        self._restart_at_front()

    def _crawl(self):
        self.__class__._log("debug", "uri is: %s, next is: %s" % (self.__uri, self.__next))
        uri = self.__uri+'/'+self.__next
        self.__class__._log("debug", "%s crawls url: %s" % (self.__class__.__name__, uri))

        request = urllib2.Request(uri, headers=self.__class__.headers())
        response = urllib2.urlopen(request, timeout=self.__class__.timeout())

        page = BeautifulSoup(response.read())

        # get more content ("scroll down")
        # to know what page to parse next
        # update new last URI when we're not on first run
        self.__next =page.find_all("a", {"class": "button"})[-1]["href"]

        for con in page.find_all("a", {"class": "fileThumb"}):
          self._add_image(con["href"])
