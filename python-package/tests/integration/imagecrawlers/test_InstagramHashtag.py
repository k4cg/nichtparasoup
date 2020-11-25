import pytest

from nichtparasoup.imagecrawlers.instagram import InstagramHashtag
from nichtparasoup.testing.imagecrawler import ImageCrawlerLoaderTest


@pytest.mark.no_cover
def test_loader() -> None:
    ImageCrawlerLoaderTest().check('InstagramHashtag', InstagramHashtag)
