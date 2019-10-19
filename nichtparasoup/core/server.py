__all__ = ["BaseServer", "ServerStatistics", "ServerStatus", "ServerRefiller"]

from abc import ABC
from copy import copy
from random import uniform
from sys import getsizeof
from threading import Thread
from time import sleep
from typing import Any, Dict, List, Optional, Set, Union
from weakref import ref as waek_ref

from nichtparasoup import __version__
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

    def get_image(self) -> Optional[Dict[str, Any]]:
        crawler = self.np_core.crawlers.get_random()
        if not crawler:
            return None
        image = copy(crawler.pop_random_image())
        if not image:
            return None
        self.stats.count_images_served += 1
        return dict(
            uri=image.uri,
            is_generic=image.is_generic,
            source=image.source,
            more=image.more,
            crawler=id(crawler),
        )

    # TODO: write the other needed server functions

    def setUp(self) -> None:
        self.refiller.refill()  # initial fill
        self.refiller.start()  # start threaded periodical refill

    def tearDown(self) -> None:
        pass


class ServerRefiller(Thread):
    def __init__(self, server: BaseServer, keep: int, sleep: Union[int, float]) -> None:
        super().__init__(daemon=True)
        self._wr_server = waek_ref(server)
        self._keep = keep
        self._sleep = sleep

    def refill_crawler(self, crawler: Crawler) -> None:
        crawled = 1
        while crawled > 0 and len(crawler.images) < self._keep:
            crawled = crawler.crawl()

    def refill(self) -> bool:
        fillers = set()  # type: Set[Thread]
        server = self._wr_server()
        if not server:
            return False
        crawlers = server.np_core.crawlers.copy()
        del server
        for crawler in crawlers:
            filler = Thread(target=self.refill_crawler, args=(crawler,), daemon=True)
            fillers.add(filler)
            filler.start()
        del crawlers
        for filler in fillers:
            filler.join()
        return True

    def run(self) -> None:
        while self.refill():
            # each service worker has some delay from time to time
            sleep(uniform(self._sleep * 0.9001, self._sleep * 1.337))


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
