
__all__ = ['Crawler', 'CrawlerError']


import sys
import random
import time
import re


class Crawler(object):
    """
        abstract class Crawler
    """

    ## class constants

    __C_timeout_ = 'timeout'
    __C_headers_ = 'headers'
    __C_resetDelay_ = 'resetDelay'

    ## class vars

    __configuration = {
        __C_timeout_: 2,  # needs to be greater 0
        __C_headers_: {},  # additional headers
        __C_resetDelay_: 10800  # value in seconds
    }

    __blacklist = []
    __images = []

    __logger = None

    __imageRE = re.compile(".*\.(?:jpeg|jpg|png|gif)(?:\?.*)?(?:#.*)?$", flags=re.IGNORECASE)

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
    def headers(cls, value=None):
        return cls.__config_setter_and_getter(cls.__C_headers_, value)

    @classmethod
    def timeout(cls, value=None):
        return cls.__config_setter_and_getter(cls.__C_timeout_, value)

    @classmethod
    def reset_delay(cls, value=None):
        return cls.__config_setter_and_getter(cls.__C_resetDelay_, value)

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
        return cls.__imageRE.match(uri) is not None

    @classmethod
    def __images_clear(cls):
        cls.__images = []  # alternative: cls.__images[:] = [] # be aware: list.clean() is not available in py2

    @classmethod
    def __add_image(cls, uri, crawler=None):
        if not cls._is_image(uri):
            # self._log("info", uri + " is no image ")
            return False

        if cls._is_blacklisted(uri):
            return False

        cls._blacklist(uri)  # add it to the blacklist to detect duplicates
        cls.__images.append("%s#%s" % (uri, crawler))
        cls._log("debug", "added: %s" % (uri))
        return True

    @classmethod
    def get_image(cls):
        images = cls.__images
        if images:
            image = random.choice(images)
            images.remove(image)
            cls._log("debug", "delivered: %s - remaining: %d" % (image, len(images)))
            return image
        return None

    @classmethod
    def set_logger(cls, logger):
        cls.__logger = logger

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
        return {
            "images": len(images),
            "images_size": sys.getsizeof(images, 0),
            "blacklist": len(blacklist),
            "blacklist_size": sys.getsizeof(blacklist, 0)
        }

    @classmethod
    def show_imagelist(cls):
        return cls.__images

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

    def _add_image(self, uri):
        return self.__class__.__add_image(uri, crawler=self.__class__.__name__)

    ## abstract functions

    def __init__(self):
        raise NotImplementedError("Should have implemented this")

    def _crawl(self):
        raise NotImplementedError("Should have implemented this")

    def _restart_at_front(self):
        raise NotImplementedError("Should have implemented this")


class CrawlerError(Exception):
    pass
