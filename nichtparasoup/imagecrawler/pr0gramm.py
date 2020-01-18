__all__ = ["Pr0gramm"]

from typing import Any, Dict, Optional

from nichtparasoup.imagecrawler import (
    BaseImageCrawler, Image, ImageCollection, ImageCrawlerConfig, ImageCrawlerInfo, RemoteFetcher,
)


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
    #     * width: int
    #     * height: int
    #     * source: ???
    #     * image: string (url-path)
    # * https://pr0gramm.com/api/items/get?older=3637805&flags=1&tags=!-%22video%22
    #    * param: "older" = id of last item

    # distinguish the image:
    # https://img.pr0gramm.com/<item.image>

    # distinguish the source:
    # https://pr0gramm.com/new/<item.id>

    def __init__(self, **config: Any) -> None:  # pragma: no cover
        super().__init__(**config)
        self._older = None  # type: Optional[int]
        self._remote_fetcher = RemoteFetcher()

    @classmethod
    def info(cls) -> ImageCrawlerInfo:
        return ImageCrawlerInfo(
            description='A Crawler for https://pr0gramm.com',
            config=dict(
                promoted='Show only top("beliebt") voted images or anything("neu")',
                tags='Filter. must start with "!" - see https://pr0gramm.com/new/2782197',
            ),
            icon_url='https://pr0gramm.com/media/pr0gramm-favicon.png',
        )

    @classmethod
    def check_config(cls, config: Dict[Any, Any]) -> ImageCrawlerConfig:
        # TODO promoted==Optional[bool] - default: true
        # TODO tag=str - must start with "!"
        # TODO set `tags = '({}) & -"video"'.format(tags)` to gags
        return ImageCrawlerConfig()

    def _reset(self) -> None:
        self._older = None
        pass

    def _crawl(self) -> ImageCollection:
        images = ImageCollection()
        # TODO get some info from the API
        # TODO loop over `items`, add image ...
        images.add(Image(
            uri='',
            source='https://pr0gramm.com/new/12345',
            # more: width, height, nsfw, nsfl, ...
        ))
        # TODO
        # if `atEnd` is true, then reset
        # else: set set._older to `items[last].id`
        return images
