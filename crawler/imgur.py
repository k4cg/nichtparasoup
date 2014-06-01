
try:
    import urllib.request as urllib2  # py3
except:
    import urllib2  # py2

from bs4 import BeautifulSoup


from . import Crawler, CrawlerError







class Imgur(Crawler):

    def __init__(self, uri):
        self.__uri = uri

    def _crawl(self):  # @todo make the crawler more efficient
        uri = self.__uri
        Crawler._log("debug", "Imgur crawls url: " + uri)

        request = urllib2.Request(uri, headers=Crawler.headers())
        response = urllib2.urlopen(request, timeout=Crawler.timeout())

        image = BeautifulSoup(response.read()).find("div", {"id" : "image"}).find("img")["src"]

        Crawler._add_image(image)