__all__ = ["ImageCrawler", "Images", "Image", "ImageUri", "ImageSource"]

from abc import ABC, abstractmethod
from typing import Set, Optional, Any

ImageUri = str  # maybe this becomes ab own class, later

ImageSource = str  # maybe this becomes an own class, later


class Image(object):

    def __init__(self, uri: ImageUri, source: Optional[ImageSource] = None, **more: Any) -> None:
        self.uri = uri
        self.source = source
        self.more = more

    def __hash__(self) -> int:
        """ the uri is the identifier of Image. uri determines the hash """
        return hash(self.uri)


class Images(Set[Image]):
    pass


class ImageCrawler(ABC):

    def __init__(self, site: str) -> None:
        self.site = site

    @abstractmethod
    def crawl(self) -> Images:
        pass  # pragma: no cover
