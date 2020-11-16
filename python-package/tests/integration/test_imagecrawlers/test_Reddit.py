import pytest

from nichtparasoup.imagecrawlers.reddit import Reddit
from nichtparasoup.testing.imagecrawler import ImageCrawlerLoaderTest


@pytest.mark.no_cover
def test_loader() -> None:
    assert ImageCrawlerLoaderTest().check('Reddit', Reddit)
