__all__ = ["Pr0gramm"]

from typing import Any, Dict

from nichtparasoup.imagecrawler import BaseImageCrawler, ImageCollection, ImageCrawlerConfig, ImageCrawlerInfo


class Pr0gramm(BaseImageCrawler):

    # TODO plan the features
    # support nsfl/nsfw ? - currently not, cause it would need a login... maybe later
    # support tags? (multiple at once?)
    # support top?
    # support new?

    # TODO analyse the API
    # website uses lazy loading - this means there is some kind of data api that can be used for crawling.
    # also see the https://github.com/mopsalarm/Pr0 - the have mocs and docs!elf :-)

    @classmethod
    def info(cls) -> ImageCrawlerInfo:
        return ImageCrawlerInfo(
            description='A Crawler for https://pr0gramm.com',
            config=dict(),  # TODO
            icon_url='https://pr0gramm.com/media/pr0gramm-favicon.png',
        )

    @classmethod
    def check_config(cls, config: Dict[Any, Any]) -> ImageCrawlerConfig:
        # TODO
        return ImageCrawlerConfig()

    def _reset(self) -> None:
        # TODO
        pass

    def _crawl(self) -> ImageCollection:
        return ImageCollection()
