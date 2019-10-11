__all__ = ["Picsum"]

from uuid import uuid4

from . import ImageCrawler, Images, Image, ImageUri


class Picsum(ImageCrawler):

    _fake_crawl_len = 10

    def _build_image_uri(self) -> ImageUri:
        return "https://picsum.photos/" + self.site

    def crawl(self) -> Images:
        images = Images()
        for _ in range(self._fake_crawl_len):
            images.add(Image(
                self._build_image_uri() + "#" + str(uuid4())
            ))
        return images
