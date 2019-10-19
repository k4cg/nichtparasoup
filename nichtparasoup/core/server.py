__all__ = ["BaseServer", "ServerStatistics", "ServerStatus", "ServerRefiller"]

from abc import ABC
from copy import copy
from random import uniform
from sys import getsizeof
from threading import Lock, Thread
from time import sleep
from typing import Any, Dict, List, Optional, Set, Union
from weakref import ref as waek_ref

from nichtparasoup import __version__
from nichtparasoup._internals import _log, _logger_date_time_string
from nichtparasoup.core import Crawler, NPCore


class BaseServer(ABC):
    """
    this class intended to be a stable interface.
    its methods return base types only.
    """

    def __init__(self, np_core: NPCore, crawler_upkeep: int = 30) -> None:  # pragma: no cover
        self.np_core = np_core
        self.stats = ServerStatistics()
        self.refiller = ServerRefiller(self, crawler_upkeep, 1.0)
        self._lock_stats = Lock()

    def get_image(self) -> Optional[Dict[str, Any]]:
        crawler = self.np_core.crawlers.get_random()
        if not crawler:
            return None
        image = copy(crawler.pop_random_image())
        if not image:
            return None
        self._lock_stats.acquire()
        self.stats.count_images_served += 1
        self._lock_stats.release()
        return dict(
            uri=image.uri,
            is_generic=image.is_generic,
            source=image.source,
            more=image.more,
            crawler=id(crawler),
        )

    def flush_blacklist(self) -> int:
        old_len = len(self.np_core.blacklist)
        self.np_core.blacklist.clear()
        self._lock_stats.acquire()
        # TODO: log timestamp
        self.stats.cum_blacklist_on_flush += old_len
        self._lock_stats.release()
        return old_len

    def setUp(self) -> None:
        _log("info", " * setting up {}".format(type(self).__name__))
        self.refiller.refill()  # initial fill
        self.refiller.start()  # start threaded periodical refill

    def tearDown(self) -> None:
        _log("info", "\r\n * tearing down {}".format(type(self).__name__))
        self.refiller.stop()


class ServerRefiller(Thread):
    def __init__(self, server: BaseServer, keep: int, sleep: Union[int, float]) -> None:  # pragma: no cover
        super().__init__(daemon=False)
        self._wr_server = waek_ref(server)
        self._keep = keep
        self._sleep = sleep
        self.__stopped = False

    def refill_crawler(self, crawler: Crawler) -> int:
        cum_refilled = 0
        while len(crawler.images) < self._keep:
            refilled = crawler.crawl()
            if 0 == refilled:
                break  # while
            _log("info", "{} refilled {}({}) by {}".format(
                _logger_date_time_string(), type(crawler.imagecrawler).__name__, id(crawler.imagecrawler), refilled))
            cum_refilled += refilled
        return cum_refilled

    def refill(self) -> bool:
        fillers = set()  # type: Set[Thread]
        server = self._wr_server()
        if not server:
            return False
        crawlers = server.np_core.crawlers.copy()
        del server
        for crawler in crawlers:
            filler = Thread(target=self.refill_crawler, args=(crawler,), daemon=False)
            fillers.add(filler)
            filler.start()
        del crawlers
        for filler in fillers:
            filler.join()
        return True

    def run(self) -> None:
        while True:
            if not self.refill():
                break
            if self.__stopped:
                break
            # each service worker has some delay from time to time
            sleep(uniform(self._sleep * 0.9001, self._sleep * 1.337))

    def start(self) -> None:
        _log("info", " * starting {}".format(type(self).__name__))
        self.__stopped = False
        super().start()

    def stop(self) -> None:
        _log("info", " * stopping {}".format(type(self).__name__))
        self.__stopped = True


class ServerStatistics(object):
    def __init__(self) -> None:  # pragma: no cover
        self.count_images_served = 0
        self.cum_blacklist_on_flush = 0


class ServerStatus(ABC):
    """
    this class intended to be a stable interface.
    all methods are like this: Callable[[Server], Union[List[SomeBaseType], Dict[str, SomeBaseType]]]
    all methods must be associated with stat(u)s!
    """

    @staticmethod
    def server(server: BaseServer) -> Dict[str, Any]:
        stats = copy(server.stats)
        return dict(
            version=__version__,
            images=dict(
                served=stats.count_images_served,
                crawled=stats.cum_blacklist_on_flush + len(server.np_core.blacklist),
            ),
        )

    @staticmethod
    def blacklist(server: BaseServer) -> Dict[str, Any]:
        blacklist = server.np_core.blacklist.copy()
        return dict(
            len=len(blacklist),
            size=getsizeof(blacklist),
        )

    @staticmethod
    def crawlers(server: BaseServer) -> List[Dict[str, Any]]:
        status = list()
        for crawler in server.np_core.crawlers.copy():
            crawler = copy(crawler)
            images = crawler.images.copy()
            status.append(dict(
                id=id(crawler),
                type=str(type(crawler.imagecrawler).__name__),
                weight=crawler.weight,
                config=crawler.imagecrawler.get_config().copy(),
                images=dict(
                    len=len(images),
                    size=getsizeof(images),
                ),
            ))
        return status
