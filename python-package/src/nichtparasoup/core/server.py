__all__ = ["Server", "ImageResponse", "ResetResponse",
           "ServerStatistics",
           "StatusLike", "ServerStatus", "BlacklistStatus", "CrawlerStatus",
           "ServerRefiller",
           ]

import sys
from copy import copy
from threading import Event, Lock, Thread
from time import sleep, time
from typing import Any, Dict, List, Optional, Set, Type, TypeVar, Union
from weakref import ref as weak_ref

from .._internals import _log, _type_module_name_str
from . import Crawler, NPCore
from .image import Image

if sys.version_info >= (3, 8):
    from typing import Protocol
else:
    from typing_extensions import Protocol

_Timestamp = int
"""Time in seconds since the Epoch
"""


class ServerStatistics:
    def __init__(self) -> None:  # pragma: no cover
        self.time_started: Optional[_Timestamp] = None
        self.count_images_served: int = 0
        self.count_reset: int = 0
        self.time_last_reset: Optional[_Timestamp] = None
        self.cum_blacklist_on_flush: int = 0


class ImageResponse:
    def __init__(self, image: Image, crawler: Crawler) -> None:  # pragma: no cover
        self.image = image
        self.crawler = crawler


class ResetResponse:
    def __init__(self, requested: bool, timeout: int) -> None:  # pragma: no cover
        self.requested = requested
        self.timeout = timeout


class Server:
    """

    This class is intended to be thread save.
    This class intended to be a stable interface.
    Its public methods return base types only.

    :param core: the core
    :param crawler_upkeep: number of images the server must keep at all time
    :param reset_timeout: number of seconds the server must nt be reset
    """

    def __init__(self, core: NPCore, *,
                 crawler_upkeep: int = 30,
                 reset_timeout: int = 60 * 60
                 ) -> None:  # pragma: no cover
        self.core = core
        self.keep = max(crawler_upkeep, 10)
        self.reset_timeout = max(reset_timeout, 600)
        self.stats = ServerStatistics()
        self._refiller: Optional[ServerRefiller] = None
        self._trigger_reset = False
        self._locks = _ServerLocks()
        self.__running = False

    def get_image(self) -> Optional[ImageResponse]:
        crawler = self.core.crawlers.get_random()
        if not crawler:
            return None
        image = copy(crawler.pop_random_image())
        if not image:
            return None
        with self._locks.stats_get_image:
            self.stats.count_images_served += 1
        return ImageResponse(image, crawler)

    @staticmethod
    def _log_refill_crawler(crawler: Crawler, refilled: int) -> None:
        # must be compatible to nichtparasoup.core._OnFill
        if refilled > 0:
            _log('info', 'refilled by %d via %s', refilled, crawler.imagecrawler)

    def refill(self) -> None:
        with self._locks.refill:
            self.core.fill_up_to(self.keep, on_refill=self._log_refill_crawler)

    def _reset(self) -> None:
        with self._locks.reset:
            self.stats.cum_blacklist_on_flush += self.core.reset()
            self.stats.count_reset += 1
            self.stats.time_last_reset = int(time())

    def request_reset(self) -> ResetResponse:
        if not self.is_alive():
            request_valid = True
            timeout = 0
        else:
            now = int(time())
            time_started = self.stats.time_started or now
            timeout_base = self.reset_timeout
            time_last_reset = self.stats.time_last_reset
            reset_after = timeout_base + (time_last_reset or time_started)
            request_valid = now > reset_after
            timeout = timeout_base if request_valid else (reset_after - now)
        if request_valid:
            self._reset()
        return ResetResponse(request_valid, timeout)

    def start(self) -> None:
        with self._locks.run:
            if self.__running:
                raise RuntimeError('already running')
            _log('info', ' * starting %s', type(self).__name__)
            _log('info', ' * fill all crawlers up to %d', self.keep)
            self.refill()  # initial fill
            if not self._refiller:
                self._refiller = ServerRefiller(self, 1.0)
                self._refiller.start()  # start threaded periodical refill
            self.stats.time_started = int(time())
            self.__running = True

    def is_alive(self) -> bool:
        return self.__running

    def stop(self) -> None:
        with self._locks.run:
            if not self.__running:
                raise RuntimeError('not running')
            _log('info', "\r\n * stopping %s", type(self).__name__)
            if self._refiller:
                self._refiller.stop()
                self._refiller = None
            self.__running = False


class _CollectionStatus:
    def __init__(self, *, length: int, size: int) -> None:  # pragma: no cover
        self.len = length
        self.size = size

    @classmethod
    def of_collection(cls: Type['_CS'], collection: Union[List[Any], Set[Any]]) -> '_CS':
        return cls(
            length=len(collection),
            size=sys.getsizeof(collection)
        )


_CS = TypeVar('_CS', bound=_CollectionStatus)


class StatusLike(Protocol):  # pragma: no cover
    """A snapshot of server's metrics.

    Basically a data class alike.
    """

    @classmethod
    def of_server(cls: Type['_SL'], server: Server) -> '_SL':
        raise NotImplementedError()


_SL = TypeVar('_SL')


class ServerStatus(StatusLike):
    class _Reset:
        def __init__(self, count: int, since: int) -> None:  # pragma: no cover
            self.count = count
            self.since = since

    class _Images:
        def __init__(self, served: int, crawled: int) -> None:  # pragma: no cover
            self.served = served
            self.crawled = crawled

    def __init__(self, *, uptime: int, reset: _Reset, images: _Images) -> None:  # pragma: no cover
        self.uptime = uptime
        self.reset = reset
        self.images = images

    @classmethod
    def of_server(cls, server: Server) -> 'ServerStatus':
        now = int(time())
        stats = server.stats
        uptime = (now - stats.time_started) if server.is_alive() and stats.time_started else 0
        return cls(
            uptime=uptime,
            reset=cls._Reset(
                stats.count_reset,
                (now - stats.time_last_reset) if stats.time_last_reset else uptime
            ),
            images=cls._Images(
                stats.count_images_served,
                stats.cum_blacklist_on_flush + len(server.core.blacklist)
            )
        )


class BlacklistStatus(_CollectionStatus, StatusLike):

    @classmethod
    def of_server(cls: Type['BlacklistStatus'], server: Server) -> 'BlacklistStatus':
        return super().of_collection(server.core.blacklist)


class CrawlerStatus(Dict[int, 'CrawlerStatus._Crawler'], StatusLike):
    class _Crawler:
        def __init__(self, crawler: Crawler) -> None:  # pragma: no cover
            self.name = crawler.imagecrawler.internal_name
            self.weight = crawler.weight
            self.type = _type_module_name_str(type(crawler.imagecrawler))
            self.config = crawler.imagecrawler.get_config()
            self.images = _CollectionStatus.of_collection(crawler.images)

    def __init__(self, *args: Any, **kwargs: Any) -> None:  # pragma: no cover
        super().__init__(*args, **kwargs)

    @classmethod
    def of_server(cls, server: Server) -> 'CrawlerStatus':
        return cls(
            (id(crawler), cls._Crawler(crawler))
            for crawler
            in server.core.crawlers
        )


class ServerRefiller(Thread):

    def __init__(self, server: Server, delay: float) -> None:  # pragma: no cover
        super().__init__(daemon=True)
        self._server_wr = weak_ref(server)
        self._delay = delay
        self._stop_event = Event()
        self._run_lock = Lock()

    def run(self) -> None:
        while not self._stop_event.is_set():
            server: Optional[Server] = self._server_wr()
            if server:
                server.refill()
            else:
                _log('info', ' * server gone. stopping %s', type(self).__name__)
                self._stop_event.set()
            if not self._stop_event.is_set():
                sleep(self._delay)

    def start(self) -> None:
        with self._run_lock:
            if self.is_alive():
                raise RuntimeError('already running')
            _log('info', ' * starting %s', type(self).__name__)
            self._stop_event.clear()
            super().start()

    def stop(self) -> None:
        with self._run_lock:
            if not self.is_alive():
                raise RuntimeError('not running')
            _log('info', ' * stopping %s', type(self).__name__)
            self._stop_event.set()


class _ServerLocks:
    def __init__(self) -> None:  # pragma: no cover
        self.stats_get_image = Lock()
        self.reset = Lock()
        self.refill = Lock()
        self.run = Lock()
