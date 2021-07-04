import pytest

from nichtparasoup.imagecrawlers.picsum import Picsum
from nichtparasoup.testing.imagecrawler import ImageCrawlerLoaderTest


@pytest.mark.no_cover
def test_loader() -> None:
    ImageCrawlerLoaderTest().check('Picsum', Picsum)
