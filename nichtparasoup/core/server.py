__all__ = ["BaseServer", "ServerStatistics", "ServerStatus"]

from abc import ABC
from sys import getsizeof
from typing import Any, Dict, List, Optional

from nichtparasoup import __version__
from nichtparasoup.core import NPCore


class BaseServer(ABC):
    """
    this class intended to be a stable interface.
    its methods return base types only.
    """

    def __init__(self, np_core: NPCore) -> None:  # pragma: no cover
        self.np_core = np_core
        self.stats = ServerStatistics()

    def get_image(self) -> Optional[Dict[str, Any]]:
        crawler = self.np_core.crawlers.get_random()
        if not crawler:
            return None
        image = crawler.pop_random_image()
        if not image:
            return None
        self.stats.count_images_served += 1
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

    # TODO: write the other needed server functions


class ServerStatistics(object):
    def __init__(self) -> None:  # pragma: no cover
        self.count_images_served = 0


class ServerStatus(ABC):
    """
    this class intended to be a stable interface.
    all methods are like this: Callable[[Server], Union[List[SomeBaseType], Dict[str, SomeBaseType]]]
    all methods must be associated with stat(u)s!
    """

    @staticmethod
    def server(server: BaseServer) -> Dict[str, Any]:
        return dict(
            version=__version__,
            images=dict(
                served=server.stats.count_images_served,
                crawled=len(server.np_core.blacklist),
            ),
        )

    @staticmethod
    def blacklist(server: BaseServer) -> Dict[str, Any]:
        return dict(
            len=len(server.np_core.blacklist),
            size=getsizeof(server.np_core.blacklist, 0),
        )

    @staticmethod
    def crawlers(server: BaseServer) -> List[Dict[str, Any]]:
        return list(
            dict(
                id=id(crawler),
                type=str(type(crawler.imagecrawler).__name__),
                weight=crawler.weight,
                config=crawler.imagecrawler.get_config(),
                images=dict(
                    len=len(crawler.images),
                    size=getsizeof(crawler.images),
                ),
            )
            for crawler in server.np_core.crawlers
        )
