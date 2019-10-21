__all__ = ["BaseServer", "ServerStatistics", "ServerStatus", "ServerRefiller", "BaseServerLocks"]

from abc import ABC
from copy import copy
from random import uniform
from sys import getsizeof
from threading import Lock, Thread
from time import sleep, time
from typing import Any, Dict, List, Optional, Union
from weakref import ref as weak_ref

from nichtparasoup import __version__
from nichtparasoup._internals import _log, _logger_date_time_string
from nichtparasoup.core import Crawler, NPCore


class BaseServer(ABC):
    """
    this class intended to be a stable interface.
    its public methods return base types only.
    """

    def __init__(self, np_core: NPCore, crawler_upkeep: int = 30,
                 reset_delay: int = 60 * 60) -> None:  # pragma: no cover
        self._np_core = np_core
        self._keep = crawler_upkeep
        self._stats = ServerStatistics()
        self._refiller = ServerRefiller(self, 1.337)
        self._trigger_reset = False
        self._reset_delay = reset_delay
        self._locks = BaseServerLocks()

    def get_image(self) -> Optional[Dict[str, Any]]:
        crawler = self._np_core.crawlers.get_random()
        if not crawler:
            return None
        image = copy(crawler.pop_random_image())
        if not image:
            return None
        self._locks.stats_get_image.acquire()
        self._stats.count_images_served += 1
        self._locks.stats_get_image.release()
        return dict(
            uri=image.uri,
            is_generic=image.is_generic,
            source=image.source,
            more=image.more,
            crawler=id(crawler),
        )

    def _refill_crawler(self, crawler: Crawler) -> int:
        cum_refilled = crawler.fill_up_to(self._keep)
        if cum_refilled > 0:
            _log("info", "{} refilled {}({}) by {}".format(
                _logger_date_time_string(),
                type(crawler.imagecrawler).__name__, id(crawler.imagecrawler),
                cum_refilled))
        return cum_refilled

    def _reset(self) -> bool:
        self._locks.reset.acquire()
        reset_treads = list()  # type: List[Thread]
        for crawler in self._np_core.crawlers.copy():
            reset_tread = Thread(target=crawler.reset, daemon=True)
            reset_treads.append(reset_tread)
            reset_tread.start()
        self._stats.cum_blacklist_on_flush += len(self._np_core.blacklist)
        self._np_core.blacklist.clear()
        self._stats.count_reset += 1
        self._stats.time_last_reset = int(time())
        for reset_tread in reset_treads:
            reset_tread.join()
        self._locks.reset.release()
        return True

    def refill(self) -> Dict[str, bool]:
        self._locks.refill.acquire()
        fill_treads = list()  # type: List[Thread]
        for crawler in self._np_core.crawlers.copy():
            fill_tread = Thread(target=self._refill_crawler, args=(crawler,), daemon=True)
            fill_treads.append(fill_tread)
            fill_tread.start()
        for fill_tread in fill_treads:
            fill_tread.join()
        self._locks.refill.release()
        return dict(refilled=True)

    def reset(self) -> Union[bool, int]:
        # TODO write proper json Dict return
        time_started = self._stats.time_started
        if time_started is not None:
            delay = self._reset_delay
            now = int(time())
            time_last_reset = self._stats.time_last_reset
            reset_after = delay + (time_started if time_last_reset is None else time_last_reset)
            if reset_after > now:
                return reset_after - now
        return self._reset()

    def setUp(self) -> None:
        self._locks.run.acquire()
        _log("info", " * setting up {}".format(type(self).__name__))
        self._stats.time_started = int(time())
        self.refill()  # initial fill
        self._refiller.start()  # start threaded periodical refill
        self._locks.run.release()

    def tearDown(self) -> None:
        self._locks.run.acquire()
        _log("info", "\r\n * tearing down {}".format(type(self).__name__))
        self._refiller.stop()
        self._locks.run.release()


class ServerRefiller(Thread):
    def __init__(self, server: BaseServer, sleep: Union[int, float]) -> None:  # pragma: no cover
        super().__init__(daemon=True)
        self._wr_server = weak_ref(server)
        self._sleep = sleep
        self._stopped = False

    def run(self) -> None:
        while not self._stopped:
            server = self._wr_server()
            if server:
                server.refill()
            else:
                _log("info", " * server gone. stopping {}".format(type(self).__name__))
                self._stopped = True
            if not self._stopped:
                # each service worker has some delay from time to time
                sleep(uniform(self._sleep * 0.9001, self._sleep * 1.337))

    def start(self) -> None:
        _log("info", " * starting {}".format(type(self).__name__))
        self._stopped = False
        super().start()

    def stop(self) -> None:
        _log("info", " * stopping {}".format(type(self).__name__))
        self._stopped = True


class ServerStatus(ABC):
    """
    this class intended to be a stable interface.
    all methods are like this: Callable[[Server], Union[List[SomeBaseType], Dict[str, SomeBaseType]]]
    all methods must be associated with stat(u)s!
    """

    @staticmethod
    def server(server: BaseServer) -> Dict[str, Any]:
        stats = copy(server._stats)
        now = int(time())
        uptime = (now - stats.time_started) if stats.time_started else 0
        return dict(
            version=__version__,
            uptime=uptime,
            reset=dict(
                count=stats.count_reset,
                since=(now - stats.time_last_reset) if stats.time_last_reset else uptime,
            ),
            images=dict(
                served=stats.count_images_served,
                crawled=stats.cum_blacklist_on_flush + len(server._np_core.blacklist),
            ),
        )

    @staticmethod
    def blacklist(server: BaseServer) -> Dict[str, Any]:
        blacklist = server._np_core.blacklist.copy()
        return dict(
            len=len(blacklist),
            size=getsizeof(blacklist),
        )

    @staticmethod
    def crawlers(server: BaseServer) -> Dict[int, Dict[str, Any]]:
        status = dict()
        for crawler in server._np_core.crawlers.copy():
            crawler_id = id(crawler)
            crawler = copy(crawler)
            images = crawler.images.copy()
            status[crawler_id] = dict(
                type=str(type(crawler.imagecrawler).__name__),
                weight=crawler.weight,
                config=crawler.imagecrawler.get_config().copy(),
                images=dict(
                    len=len(images),
                    size=getsizeof(images),
                ),
            )
        return status


class ServerStatistics(object):
    def __init__(self) -> None:  # pragma: no cover
        self.time_started = None  # type: Optional[int]
        self.count_images_served = 0  # type: int
        self.count_reset = 0  # type: int
        self.time_last_reset = None  # type: Optional[int]
        self.cum_blacklist_on_flush = 0  # type: int


class BaseServerLocks(object):
    def __init__(self) -> None:
        self.stats_get_image = Lock()
        self.reset = Lock()
        self.refill = Lock()
        self.run = Lock()
