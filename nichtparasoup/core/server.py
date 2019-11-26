__all__ = ["Server", "ServerStatistics", "ServerStatus", "ServerRefiller"]

from abc import ABC
from copy import copy
from sys import getsizeof
from threading import Lock, Thread
from time import time
from typing import Any, Dict, Optional, Union
from weakref import ref as weak_ref

from nichtparasoup import __version__
from nichtparasoup._internals import _log
from nichtparasoup.core import Crawler, NPCore


class Server(object):
    """
    this class is intended to be thread save.
    this class intended to be a stable interface.
    its public methods return base types only.
    """

    def __init__(self, core: NPCore, crawler_upkeep: int = 30,
                 reset_timeout: int = 60 * 60) -> None:  # pragma: no cover
        self.core = core
        self.keep = crawler_upkeep
        self.reset_timeout = reset_timeout
        self._stats = ServerStatistics()
        self._refiller = None  # type: Optional[ServerRefiller]
        self._trigger_reset = False
        self._locks = _ServerLocks()
        self.__running = False

    def get_image(self) -> Optional[Dict[str, Any]]:
        crawler = self.core.crawlers.get_random()
        if not crawler:
            return None
        image = copy(crawler.pop_random_image())
        if not image:
            return None
        with self._locks.stats_get_image:
            self._stats.count_images_served += 1
        return dict(
            uri=image.uri,
            is_generic=image.is_generic,
            source=image.source,
            more=image.more,
            crawler=dict(
                id=id(crawler),
                type=type(crawler.imagecrawler).__name__,
            ),
        )

    @staticmethod
    def _log_refill_crawler(crawler: Crawler, refilled: int) -> None:
        # must be compatible to nichtparasoup.core._OnFill
        if refilled > 0:
            _log('info', "refilled by {} via {!r}".format(refilled, crawler.imagecrawler))

    def refill(self) -> Dict[str, bool]:
        with self._locks.refill:
            self.core.fill_up_to(self.keep, self._log_refill_crawler)
            return dict(refilled=True)

    def _reset(self) -> None:
        with self._locks.reset:
            self._stats.cum_blacklist_on_flush += self.core.reset()
            self._stats.count_reset += 1
            self._stats.time_last_reset = int(time())

    def request_reset(self) -> Dict[str, Any]:
        if not self.is_alive():
            request_valid = True
            timeout = 0
        else:
            now = int(time())
            time_started = self._stats.time_started or now
            timeout_base = self.reset_timeout
            time_last_reset = self._stats.time_last_reset
            reset_after = timeout_base + (time_last_reset or time_started)
            request_valid = now > reset_after
            timeout = timeout_base if request_valid else (reset_after - now)
        if request_valid:
            self._reset()
        return dict(
            requested=request_valid,
            timeout=timeout,
        )

    def start(self) -> None:
        with self._locks.run:
            if self.__running:
                raise RuntimeError('already running')
            _log('info', " * starting {}".format(type(self).__name__))
            _log('info', ' * fill all crawlers up to {}'.format(self.keep))
            self.refill()  # initial fill
            if not self._refiller:
                self._refiller = ServerRefiller(self, 1)
                self._refiller.start()  # start threaded periodical refill
            self._stats.time_started = int(time())
            self.__running = True

    def is_alive(self) -> bool:
        return self.__running

    def stop(self) -> None:
        with self._locks.run:
            if not self.__running:
                raise RuntimeError('not running')
            _log('info', "\r\n * stopping {}".format(type(self).__name__))
            if self._refiller:
                self._refiller.stop()
                self._refiller = None
            self.__running = False


class ServerStatus(ABC):
    """
    this class intended to be a stable interface.
    all methods are like this: Callable[[Server], Union[List[SomeBaseType], Dict[str, SomeBaseType]]]
    all methods must be associated with stat(u)s!
    """

    @staticmethod
    def server(server: Server) -> Dict[str, Any]:
        stats = copy(server._stats)
        now = int(time())
        uptime = (now - stats.time_started) if server.is_alive() and stats.time_started else 0
        return dict(
            version=__version__,
            uptime=uptime,
            reset=dict(
                count=stats.count_reset,
                since=(now - stats.time_last_reset) if stats.time_last_reset else uptime,
            ),
            images=dict(
                served=stats.count_images_served,
                crawled=stats.cum_blacklist_on_flush + len(server.core.blacklist),
            ),
        )

    @staticmethod
    def blacklist(server: Server) -> Dict[str, Any]:
        blacklist = server.core.blacklist.copy()
        return dict(
            len=len(blacklist),
            size=getsizeof(blacklist),
        )

    @staticmethod
    def crawlers(server: Server) -> Dict[int, Dict[str, Any]]:
        status = dict()
        for crawler in server.core.crawlers.copy():
            crawler_id = id(crawler)
            crawler = copy(crawler)
            images = crawler.images.copy()
            status[crawler_id] = dict(
                type=type(crawler.imagecrawler).__name__,
                weight=crawler.weight,
                config=crawler.imagecrawler.get_config(),  # just a dict
                images=dict(
                    len=len(images),
                    size=getsizeof(images),
                ),
            )
        return status


class ServerRefiller(Thread):
    def __init__(self, server: Server, sleep: Union[int, float]) -> None:  # pragma: no cover
        from threading import Event
        super().__init__(daemon=True)
        self._server_wr = weak_ref(server)
        self._sleep = sleep
        self._stop_event = Event()
        self._run_lock = Lock()

    def run(self) -> None:
        from time import sleep
        while not self._stop_event.is_set():
            server = self._server_wr()  # type: Optional[Server]
            if server:
                server.refill()
            else:
                _log('info', " * server gone. stopping {}".format(type(self).__name__))
                self._stop_event.set()
            if not self._stop_event.is_set():
                sleep(self._sleep)

    def start(self) -> None:
        self._run_lock.acquire()
        try:
            if self.is_alive():
                raise RuntimeError('already running')
            _log('info', " * starting {}".format(type(self).__name__))
            self._stop_event.clear()
            super().start()
        finally:
            self._run_lock.release()

    def stop(self) -> None:
        self._run_lock.acquire()
        try:
            if not self.is_alive():
                raise RuntimeError('not running')
            _log('info', " * stopping {}".format(type(self).__name__))
            self._stop_event.set()
        finally:
            self._run_lock.release()


class ServerStatistics(object):
    def __init__(self) -> None:  # pragma: no cover
        self.time_started = None  # type: Optional[int]
        self.count_images_served = 0  # type: int
        self.count_reset = 0  # type: int
        self.time_last_reset = None  # type: Optional[int]
        self.cum_blacklist_on_flush = 0  # type: int


class _ServerLocks(object):
    def __init__(self) -> None:  # pragma: no cover
        self.stats_get_image = Lock()
        self.reset = Lock()
        self.refill = Lock()
        self.run = Lock()
