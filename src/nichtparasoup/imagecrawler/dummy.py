__all__ = ["Dummy"]

from uuid import uuid4
from urllib.parse import urlencode

from . import ImageCrawler, Images, Image


class Dummy(ImageCrawler):

    def crawl(self) -> Images:
        images = Images()
        images.add(Image(
            "#" + urlencode({
                # TODO: add data url to the logo or something
                "site": self.site,
                "uuid": str(uuid4())
            }),
            source=None,
            this_is_a_dummy=True
        ))
        return images
