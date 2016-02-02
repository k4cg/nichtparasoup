
try:
    from urllib.parse import urljoin    # py3
except ImportError:
    from urlparse import urljoin        # py2

import re


from . import Crawler, CrawlerError



class NineGag(Crawler):
    """ 9gag image provider """

    __uri = ""
    __next = ""
    __site = ""

    __RE_post_container = re.compile("badge-post-container")

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
        _more = page.find("div", {"class": "loading"})
        _next = None
        if _more:
            _more = _more.find("a", {"class": "btn badge-load-more-post", "href": True})
            if _more:
                _next = urljoin(base, _more["href"])
        if _next:
            self.__next = _next
        else:
            self.__class__._log("debug", "%s found no `next` on url: %s" % (self.__class__.__name__, uri))


        # for every found imageContainer
        # add img-src to map if not blacklisted
        images_added = 0
        for con in page.find_all("div", {"class": self.__class__.__RE_post_container}):
            image = None

            image_inline = con.find("div", {"class": "badge-animated-container-animated", "data-image": True})
            if image_inline:
                image = image_inline['data-image']

            image_src = con.find('img', {"class": "badge-item-img", "src": True})
            if image_src:
                image = image_src['src']

            if image:
                if self._add_image(urljoin(base, image), self.__site):
                    images_added += 1

        if not images_added:
            self.__class__._log("debug", "%s found no images on url: %s" % (self.__class__.__name__, uri))
