
__all__ = ['Crawler']


import sys
import random





class Crawler(object):
    """
        abstract class Crawler
    """

    # clas constants

    __CFtimeout_ = 'timeout'
    __CFheaders_ = 'headers'

    # class vars

    __configuration = {
        __CFtimeout_: 2,  # needs to be greater 0
        __CFheaders_: {}  # additional headers
    }

    __blacklist = []
    __images = []

    __logger = None

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
        return cls.__config_setter_and_getter(cls.__CFheaders_, value)

    @classmethod
    def timeout(cls, value=None):
        return cls.__config_setter_and_getter(cls.__CFtimeout_, value)

    # general functions

    @classmethod
    def _blacklist(cls, uri):
        cls.__blacklist.append(uri)

    @classmethod
    def _is_blacklisted(cls, uri):
        if any(uri in s for s in cls.__blacklist):
            return True
        return False

    @classmethod
    def _add_image(cls, uri):
        if not cls._is_blacklisted(uri):
            cls.__images.append(uri)
            cls._blacklist(uri)  # add it to the blacklist to detect duplicates
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
    def _log(cls, logtype, message):
        if cls.__logger:
            getattr(cls.__logger, logtype)(message)

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

    def crawl(self):
        Crawler._log("debug", "class %s starts crawling" % self.__class__.__name__)
        try:
            self._crawl()
        except CrawlerError as e:
            Crawler._log("exception", "crawler error:" + repr(e))
        except:
            e = sys.exc_info()[0]
            Crawler._log("exception", "unexpected crawler error: " + repr(e))


    # abstract functions

    def __init__(self): #abstractmethod
        raise NotImplementedError("Should have implemented this")

    def _crawl(self): #abstractmethod
        raise NotImplementedError("Should have implemented this")


class CrawlerError(Exception):
    pass