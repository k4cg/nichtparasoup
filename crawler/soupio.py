

try:
    import urllib.parse as urlparse  # py3
except:
    import urlparse  # py2

from . import Crawler, CrawlerError


class SoupIO(Crawler):
    """ soup.io image provider """

    __uri = ""
    __next = ""

    __base = "http://soup.io/"

    @staticmethod
    def __build_uri(uri):
        return urlparse.urljoin(uri, "?type=image")

    def _restart_at_front(self):
        self.__next = ""

    def __init__(self, uri):
        self.__uri = self.__class__.__build_uri(uri)
        self._restart_at_front()

    def _crawl(self):
        uri = urlparse.urljoin(self.__uri, self.__next)
        self.__class__._log("debug", "%s crawls url: %s" % (self.__class__.__name__, uri))

        (page, _) = self.__class__._fetch_remote_html(uri)
        if not page:
            self.__class__._log("debug", "%s crawled EMPTY url: %s" % (self.__class__.__name__, uri))
            return

        # get more content ("scroll down")
        # to know what page to parse next
        # update new last URI when we're not on first run
        _more = page.find("div", {"id": "more_loading"})
        if _more:
            _more = _more.find("a", {"href": True})
            if _more:
                self.__next = _more["href"]
        if not _more:
            self.__class__._log("debug", "%s found no `next` on url: %s" % (self.__class__.__name__, uri))

        # for every found imageContainer
        # add img-src to map if not blacklisted
        images_added = 0
        for con in page.find_all("div", {"class": "imagecontainer"}):
            image = con.find('img', {"src": True})
            if image:
                if self._add_image(urlparse.urljoin(self.__base, image['src'])):
                    images_added += 1

        if not images_added:
            self.__class__._log("debug", "%s found no images on url: %s" % (self.__class__.__name__, uri))
