
import re, json

try:
    from urllib.parse import urljoin    # py3
except ImportError:
    from urlparse import urljoin        # py2

from . import Crawler, CrawlerError


class Pr0gramm(Crawler):
    """ pr0gramm.com image provider"""

    ## class constants

    ## properties

    __uri = ""
    __next = ""
    __site = ""
    __image_base_url = "http://img.pr0gramm.com/"
    __api_base_url = ""

    __filter = re.compile('^/static/[\d]+')
    __filterNextPage = ""

    ## functions

    """
        JSON From API
        {
            atEnd: <bool>
            atStart: <bool>
            error: ?
            items: [
                        ...
                        {
                            id: <int>
                            promoted: <int>
                            up: <int>
                            down: <int>
                            created: <int>
                            image: <string> z.B.: 2016/02/18/047b2e356d059074.jpg
                            thumb: <string>
                            fullsize: <string>
                            source: <string>
                            flags: <int>
                            user: <string>
                            mark: <int>
                        }
                        ...
                    ]
            ts: <int>
            cache: <string>
            rt: <int>
            qc: <int>
        }
    """

    @staticmethod
    def __build_uri(uri):
        return uri

    def _restart_at_front(self):
        self.__next = self.__uri

    def __init__(self, uri, site):
        self.__site = site
        self.__uri = self.__class__.__build_uri(uri)
        self.__api_base_url = self.__uri
        self.__filterNextPage = re.compile('^/static/' + self.__site + '/[\d]+')
        self._restart_at_front()

    def _crawl(self):
        uri = self.__next
        self.__class__._log("debug", "%s crawls url: %s" % (self.__class__.__name__, uri))


        (remote, uri) = self.__class__._fetch_remote(uri)
        if not remote:
            self.__class__._log("debug", "%s crawled EMPTY url: %s" % (self.__class__.__name__, uri))
            return

        data = json.loads(remote)

        last_id = 0
        images_added = 0
        for item in data["items"]:

            if item["promoted"] == 0:
                continue

            if item["image"].lower().endswith(".webm"):
                continue

            last_id = item["id"]

            if self._add_image(urljoin(self.__image_base_url, item["image"]), self.__site):
                images_added += 1


        self.__next = self.__api_base_url + "?older=" + str(last_id)

        self.__class__._log("debug", "%s added %s images on url: %s" % (self.__class__.__name__, images_added, uri))
