
import re
try:
    import urllib.request as urllib2  # py3
except:
    import urllib2  # py2

try:
    import urllib.parse as urlparse  # py3
except:
    import urlparse  # py2


from . import Crawler, CrawlerError


class Pr0gramm(Crawler):
    """ pr0gramm.com image provider"""

    ## class constants

    __base = "http://pr0gramm.com"

    ## properties

    __uri = ""
    __filter = re.compile('^/static/[\d]+')

    ## functions

    @staticmethod
    def __build_uri(uri):
        return uri

    def _restart_at_front(self):
        pass  # nothing to do - since we have no paging, yet

    def __init__(self, uri):
        self.__uri = self.__class__.__build_uri(uri)
        self._restart_at_front()

    def _crawl(self):
        uri = self.__uri  # @todo add paging
        self.__class__._log("debug", "%s crawls url: %s" % (self.__class__.__name__, uri))

        (page_container, _) = self.__class__._fetch_remote_html(uri)
        if not page_container:
            self.__class__._log("debug", "%s crawled EMPTY url: %s" % (self.__class__.__name__, uri))
            return

        pages = page_container.findAll("a", href=self.__filter)
        images_added = 0
        for page in pages:
            if self.__crawl_page(urllib2.quote(page["href"])):
                images_added += 1

        if not images_added:
            self.__class__._log("debug", "%s found no images on url: %s" % (self.__class__.__name__, uri))

    def __crawl_page(self, uri):
        uri = urlparse.urljoin(self.__base, uri)

        (page, _) = self.__class__._fetch_remote_html(uri)
        if not page:
            self.__class__._log("debug", "%s sub-crawled EMPTY url: %s" % (self.__class__.__name__, uri))
            return False

        image = page.find("img", {"src": True})
        if not image:
            return False

        return self._add_image(urlparse.urljoin(self.__base, image["src"]))
