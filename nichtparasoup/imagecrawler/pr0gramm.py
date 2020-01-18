__all__ = ["Pr0gramm"]

from typing import Any, Dict

from nichtparasoup.imagecrawler import BaseImageCrawler, ImageCollection, ImageCrawlerConfig, ImageCrawlerInfo


class Pr0gramm(BaseImageCrawler):

    # TODO plan the features
    # support nsfl/nsfw ? - flags=(int) - binary concat; sfw=1, nsfw=2, nsfl=4 - default: 1
    # support tags? - tags=(string) - default ""
    # support top/new? promoted=(int) - top=1, new=0 - default: 1

    # understand the tags: read https://pr0gramm.com/new/2782197
    # images only = add to tags: ! -"video"

    # TODO analyse the API
    # website uses lazy loading - this means there is some kind of data api that can be used for crawling.
    # also see the https://github.com/mopsalarm/Pr0 - the have mocs and docs!elf :-)
    # * https://pr0gramm.com/api/items/get?flags=1&tags=!-%22video%22
    #   * has all non-videos, that are sfw
    #   * atEnd: bool
    #   * error: null
    #   * items: list
    #     * id: int
    #     * width:
    #     * height:
    #     * source:
    # * https://pr0gramm.com/api/items/get?older=3637805&flags=1&tags=!-%22video%22
    #    * param: "older" = id of last item

    # distinguish the source:
    # https://pr0gramm.com/(new|top)/<item.id> -- integrate nsfw|nsfl ?

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
