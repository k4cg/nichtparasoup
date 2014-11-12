
__all__ = ['Crawler']


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

    __crawlingStarted = None

    ## config methods

    @classmethod
    def configure(cls, config=None, key=None, value=None):
        if isinstance(config, dict):
            cls.__configuration += config
        elif key and value:
            cls.__configuration[key] = value

    @classmethod
    def __config_setter_and_getter(cls, key, value=None):
        if value is None :
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
    def _blacklist(cls, uri):
        cls.__blacklist.append(uri)

    @classmethod
    def _is_blacklisted(cls, uri):
        if any(uri in s for s in cls.__blacklist):
            return True
        return False

    @classmethod
    def _is_image(cls, uri):
        return cls.__imageRE.match(uri) is not None

    @classmethod
    def __add_image(cls, uri):
        if not cls._is_blacklisted(uri):
            cls._blacklist(uri)  # add it to the blacklist to detect duplicates
            cls.__images.append(uri)
            cls._log("debug", "added: %s" % uri)
            return True
        return False

    @classmethod
    def get_image(cls):
        images = Crawler.__images
        if images:
            image = random.choice(images)
            images.remove(image)
            cls._log("debug", "delivered: %s - remaining: %d" % (image, len(images)))
            return image

    @classmethod
    def set_logger(cls, logger):
        cls.__logger = logger

    @classmethod
    def _log(cls, log_type, message):
        if cls.__logger:
            getattr(cls.__logger, log_type)(message)

    @classmethod
    def _debug(cls):
        return "<Crawler config:%s info:%s>" % (cls.__configuration, Crawler.info())

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
        cls.__images.clear()
        cls._log("info", "flushed. cache is now empty")

    @classmethod
    def reset(cls):
        cls.__images.clear()
        cls.__blacklist.clear()
        cls._log("info", "reset. cache and blacklist are now empty")

    def crawl(self):
        now = time.time()
        if self.__crawlingStarted is None:
            self.__crawlingStarted = now
        elif self.__crawlingStarted <= now - Crawler.reset_delay():
            self._log("debug", "instance %s starts at front" % repr(self))
            self._restart_at_front()
            self.__crawlingStarted = now

        self._log("debug", "instance %s starts crawling" % repr(self))
        try:
            self._crawl()
        except CrawlerError as e:
            self._log("exception", "crawler error:" + repr(e))
        except:
            e = sys.exc_info()[0]
            self._log("exception", "unexpected crawler error: " + repr(e))

    def _add_image(self, uri):
        if not self._is_image(uri):
            # self._log("info", uri + " is no image ")
            return False
        return self.__add_image(uri + '#' + self.__class__.__name__)

    ## abstract functions

    def __init__(self):
        raise NotImplementedError("Should have implemented this")

    def _crawl(self):
        raise NotImplementedError("Should have implemented this")

    def _restart_at_front(self):
        raise NotImplementedError("Should have implemented this")


class CrawlerError(Exception):
    pass
