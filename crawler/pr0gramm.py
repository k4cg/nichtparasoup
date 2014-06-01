
import re

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







class Pr0gramm(Crawler):
    """ pr0gramm.com image provider """


    __uri = ""

    __filter = re.compile('^/static/[\d]+')

    __base = "http://pr0gramm.com"

    def __init__(self, uri):
        self.__uri = uri

    def _crawl(self):
        uri = self.__uri  # @todo add paging
        Crawler._log("debug", "Pr0gramm crawls url: " + uri)

        request = urllib2.Request(uri, headers=Crawler.headers())
        response = urllib2.urlopen(request, timeout=Crawler.timeout())

        pages = BeautifulSoup(response.read()).findAll("a", href=Pr0gramm.__filter)
        for page in pages:
            self.__crawl_page(urllib2.quote(page["href"]))

    def __crawl_page(self, uri):
        uri = urlparse.urljoin(Pr0gramm.__base, uri)

        request = urllib2.Request(uri, headers=Crawler.headers())
        response = urllib2.urlopen(request, timeout=Crawler.timeout())

        image = BeautifulSoup(response.read()).find("img")["src"]

        Crawler._add_image(urlparse.urljoin(Pr0gramm.__base, image))

