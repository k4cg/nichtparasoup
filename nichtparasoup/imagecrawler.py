"""For convenience, all classes that are needed to implement an ImageCrawler are exported, here.
"""

__all__ = [
    "BaseImageCrawler", "ImageCrawlerConfig", "ImageCrawlerInfo",
    "Image", "ImageCollection",
    "RemoteFetcher", "ImageRecognizer",
]


from .core.image import Image, ImageCollection
from .core.imagecrawler import BaseImageCrawler, ImageCrawlerConfig, ImageCrawlerInfo, ImageRecognizer, RemoteFetcher
