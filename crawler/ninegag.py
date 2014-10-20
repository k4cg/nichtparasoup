
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





class Ninegag(Crawler):
    """ 9gag image provider """

    ___uri = ""
    __next = ""


    @staticmethod
    def __build_uri(uri):
        return uri

    def _restart_at_front(self):
        self.__next = ""

    def __init__(self, uri):
        self.__uri = Ninegag.__build_uri(uri)
        self._restart_at_front()

    def _crawl(self):
        uri = urlparse.urljoin(self.__uri, self.__next)
        Crawler._log("debug", "9gag crawls url: " + uri)

        request = urllib2.Request(uri, headers=Crawler.headers())
        response = urllib2.urlopen(request, timeout=Crawler.timeout())

        page = BeautifulSoup(response.read())

        # get more content ("scroll down")
        # to know what page to parse next
        # update new last URI when we're not on first run
        self.__next = page.find("div", {"class" : "loading"}).find("a", {"class": "btn badge-load-more-post"})["href"]

        # for every found imageContainer
        # add img-src to map if not blacklisted
        for con in page.find_all("div", {"class": "badge-post-container post-container "}):
            image = con.find('img')['src']
            self._add_image(image)
