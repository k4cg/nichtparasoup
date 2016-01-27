

try:
    from urllib.parse import urljoin    # py3
except ImportError:
    from urlparse import urljoin        # py2


from . import Crawler, CrawlerError


class Fourchan(Crawler):
    """ Fourchan image provider """

    __uri = ""
    __next = ""
    __site = ""

    @staticmethod
    def __build_uri(uri):
        return uri

    def _restart_at_front(self):
        self.__next = self.__uri

    def __init__(self, uri, site):
        self.__site = site
        self.__uri = self.__class__.__build_uri(uri)
        self._restart_at_front()

    def _crawl(self):
        uri = self.__next
        self.__class__._log("debug", "%s crawls url: %s" % (self.__class__.__name__, uri))

        (page, base, _) = self.__class__._fetch_remote_html(uri)
        if not page:
            self.__class__._log("debug", "%s crawled EMPTY url: %s" % (self.__class__.__name__, uri))
            return

        # get more content ("scroll down")
        # to know what page to parse next
        # update new last URI when we're not on first run
        _buttons = page.find_all("a", {"class": "button", "href": True})
        if _buttons:
            self.__next = urljoin(base, _buttons[-1]["href"])
        else:
            self.__class__._log("debug", "%s found no `next` on url: %s" % (self.__class__.__name__, uri))

        images_added = 0
        for con in page.find_all("a", {"class": "fileThumb", "href": True}):
            if self._add_image(urljoin(base, con["href"])):
                images_added += 1

        if not images_added:
            self.__class__._log("debug", "%s found no images on url: %s" % (self.__class__.__name__, uri))
