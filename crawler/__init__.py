
__all__ = ['Crawler', 'CrawlerError']


import sys
import random
import time
import re

try:
    from urllib.request import Request, urlopen     # py3
except ImportError:
    from urllib2 import Request, urlopen            # py2

try:
    from urllib.parse import urljoin    # py3
except ImportError:
    from urlparse import urljoin        # py2


from bs4 import BeautifulSoup


class Crawler(object):
    """
        abstract class Crawler
    """

    ## class constants

    __C_timeout_ = 'timeout'
    __C_headers_ = 'headers'
    __C_resetDelay_ = 'resetDelay'

    __refresh_uri_RE = re.compile("^(?:\d*;)?url=(.+)$", flags=re.IGNORECASE)

    __image_RE = re.compile(".*\.(?:jpeg|jpg|png|gif)(?:\?.*)?(?:#.*)?$", flags=re.IGNORECASE)

    ## class vars

    __configuration = {
        __C_timeout_: 10,  # needs to be greater 0
        __C_headers_: {},  # additional headers
        __C_resetDelay_: 10800  # value in seconds
    }

    __blacklist = []
    __images = {}

    __factors = None
    __logger = None

    ## properties

    __crawlingStarted = 0.0

    ## config methods

    @classmethod
    def configure(cls, config=None, key=None, value=None):
        if isinstance(config, dict):
            cls.__configuration += config
        elif key and value:
            cls.__configuration[key] = value

    @classmethod
    def __config_setter_and_getter(cls, key, value=None):
        if value is None:
            return cls.__configuration[key]
        cls.configure(key=key, value=value)

    ## wellknown config accessors

    @classmethod
    def request_headers(cls, value=None):
        return cls.__config_setter_and_getter(cls.__C_headers_, value)

    @classmethod
    def request_timeout(cls, value=None):
        return cls.__config_setter_and_getter(cls.__C_timeout_, value)

    @classmethod
    def reset_delay(cls, value=None):
        return cls.__config_setter_and_getter(cls.__C_resetDelay_, value)

    ## basic document fetcher

    @classmethod
    def __html_find_meta_refresh(cls, document):
        """
        :type document: BeautifulSoup
        :rtype: str | None
        """
        refresh_uri = None

        # <meta content="0;url=/images?foo=bar&amp;you=awesome" http-equiv="refresh">
        meta_refresh = document.find("meta", {"http-equiv": "refresh", "content": cls.__refresh_uri_RE})
        if meta_refresh:
            # @fixme html-decode !
            refresh_uri = cls.__refresh_uri_RE.match(meta_refresh["content"]).group(1)

        return refresh_uri

    @staticmethod
    def __html_find_base(document):
        """
        :type document: BeautifulSoup
        :rtype: str | None
        """
        base_uri = None

        # <base href="http://www.w3schools.com/images/" target="_blank">
        base_tag = document.find("base", {"href": True})
        if base_tag:
            # @fixme html-decode !
            base_uri = base_tag["href"]

        return base_uri

    @classmethod
    def _fetch_remote(cls, uri, depth_indicator=1):
        """
        return remote document and actual remote uri
        :type uri: str
        :type depth_indicator: int
        :rtype: (document: str | None, uri)
        """

        cls._log("debug", "fetch remote(%d): %s" % (depth_indicator, uri))
        request = Request(uri, headers=cls.request_headers())
        response = urlopen(request, timeout=cls.request_timeout())

        if not response:
            return None

        uri = response.geturl()

        charset = 'utf8'
        try:
            charset = response.info().get_param('charset', charset)     # py3
        except AttributeError:
            pass

        return response.read().decode(charset), uri

    @classmethod
    def _fetch_remote_html(cls, uri, follow_meta_refresh=True, follow_meta_refresh_max=5, bs4features="html5lib"):
        """
        returns remote HTML document, actual remote uri and base uri
        :type uri: str
        :type follow_meta_refresh: bool
        :type follow_meta_refresh_max: int
        :rtype: ( document: BeautifulSoup | None , base: str,  uri: str )
        """

        document = None
        follow_meta_refresh_depth = 1

        while True:
            (response, uri) = cls._fetch_remote(uri, follow_meta_refresh_depth)

            if not response:
                break

            document = BeautifulSoup(response, features=bs4features)

            if not follow_meta_refresh:
                break

            refresh_uri = cls.__html_find_meta_refresh(document)
            if not refresh_uri:
                break
            refresh_uri = urljoin(uri, refresh_uri)

            if refresh_uri == uri:
                break

            cls._log("debug", "fetch remote HTML(%d): %s meta-refreshes to %s" %
                     (follow_meta_refresh_depth, uri, refresh_uri))
            uri = refresh_uri

            follow_meta_refresh_depth += 1
            if follow_meta_refresh_depth >= follow_meta_refresh_max:
                break

        if not document:
            cls._log("debug", "fetch remote HTML: %s is empty" % uri)

        base = uri

        doc_base = cls.__html_find_base(document)
        if doc_base:
            base = urljoin(base, doc_base)

        return document, base, uri

    ## general functions

    @classmethod
    def __blacklist_clear(cls):
        cls.__blacklist = []  # alternative: cls.__blacklist[:] = [] # be aware: list.clean() is not available in py2

    @classmethod
    def _blacklist(cls, uri):
        cls.__blacklist.append(uri)

    @classmethod
    def _is_blacklisted(cls, uri):
        return uri in cls.__blacklist

    @classmethod
    def _is_image(cls, uri):
        return cls.__image_RE.match(uri) is not None

    @classmethod
    def __images_clear(cls):
        cls.__images = {}  # alternative: cls.__images[:] = [] # be aware: list.clean() is not available in py2

    @classmethod
    def __add_image(cls, uri, crawler, site):
        """
        :type uri: str
        :type crawler: str
        :type site: str
        :return: bool
        """
        if not cls._is_image(uri):
            # self._log("info", uri + " is no image ")
            return False

        if cls._is_blacklisted(uri):
            return False

        if crawler not in cls.__images:
            cls.__images[crawler] = {}

        if site not in cls.__images[crawler]:
            cls.__images[crawler][site] = []

        cls._blacklist(uri)  # add it to the blacklist to detect duplicates
        cls.__images[crawler][site].append("%s#%s" % (uri, crawler))
        cls._log("debug", "added %s-%s: %s" % (crawler, site, uri))
        return True

    @classmethod
    def get_image(cls):
        images = cls.__images
        factors = cls.__factors
        if images:
            # return image respecting factors:
            # Summing up the Factors till reaching a random number

            max = 0
            for crawler in images:
                for site in images[crawler]:
                    factor = 1
                    if crawler in factors and site in factors[crawler]:
                        factor = factors[crawler][site]

                    max += factor

            rnd = random.uniform(0, max)

            count = 0
            for crawler in images:
                for site in images[crawler]:
                    factor = 1
                    if crawler in factors and site in factors[crawler]:
                        factor = factors[crawler][site]

                    count += factor
                    if count > rnd:
                        image = random.choice(images[crawler][site])
                        images[crawler][site].remove(image)
                        cls._log("debug", "delivered %s-%s: %s - remaining: %d"
                                 % (crawler, site, image, len(images[crawler][site])))
                        return image
        return None

    @classmethod
    def set_logger(cls, logger):
        cls.__logger = logger

    @classmethod
    def set_factors(cls, factors):
        cls.__factors = factors

    @classmethod
    def _log(cls, log_type, message):
        if cls.__logger:
            getattr(cls.__logger, log_type)(message)

    @classmethod
    def _debug(cls):
        return "<Crawler config:%s info:%s>" % (cls.__configuration, cls.info())

    @classmethod
    def info(cls):
        images = cls.__images
        blacklist = cls.__blacklist

        info = {
            "blacklist": len(blacklist),
            "blacklist_size": sys.getsizeof(blacklist, 0),
            "images_per_site": {}
        }

        images_count = 0
        images_size = 0
        for crawler in images:
            for site in images[crawler]:
                site_image_count = len(images[crawler][site])
                images_count += site_image_count
                images_size += sys.getsizeof(images[crawler][site])
                info["images_per_site"][crawler + "_" + site] = site_image_count

        info["images_size"] = images_size
        info["images"] = images_count

        return info

    @classmethod
    def show_imagelist(cls):
        images = []
        for crawler in cls.__images:
            for site in cls.__images[crawler]:
                images.append(cls.__images[crawler][site])

        return images

    @classmethod
    def show_blacklist(cls):
        return cls.__blacklist

    @classmethod
    def flush(cls):
        cls.__images_clear()
        cls._log("info", "flushed. cache is now empty")

    @classmethod
    def reset(cls):
        cls.__images_clear()
        cls.__blacklist_clear()
        cls._log("info", "reset. cache and blacklist are now empty")

    def crawl(self):
        now = time.time()
        if not self.__crawlingStarted:
            self.__crawlingStarted = now
        elif self.__crawlingStarted <= now - self.__class__.reset_delay():
            self.__class__._log("debug", "instance %s starts at front" % (repr(self)))
            self.__crawlingStarted = now
            self._restart_at_front()

        self.__class__._log("debug", "instance %s starts crawling" % (repr(self)))
        try:
            self._crawl()
        except CrawlerError as e:
            self.__class__._log("exception", "crawler error: %s" % (repr(e)))
        except:
            e = sys.exc_info()[0]
            self.__class__._log("exception", "unexpected crawler error: %s" % (repr(e)))

    def _add_image(self, uri, site):
        """
        :type uri: str
        :type site: str
        :rtype: bool
        """
        return self.__class__.__add_image(uri, self.__class__.__name__, site)

    ## abstract functions

    def __init__(self):
        # call every abstract method to be sure it is there
        self._restart_at_front()
        self._crawl()
        raise NotImplementedError("Should have implemented this")

    def _crawl(self):
        raise NotImplementedError("Should have implemented this")

    def _restart_at_front(self):
        raise NotImplementedError("Should have implemented this")


class CrawlerError(Exception):
    pass
