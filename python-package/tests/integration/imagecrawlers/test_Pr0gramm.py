import pytest

from nichtparasoup.imagecrawlers.pr0gramm import Pr0gramm
from nichtparasoup.testing.imagecrawler import ImageCrawlerLoaderTest


@pytest.mark.no_cover
def test_loader() -> None:
    assert ImageCrawlerLoaderTest().check('Pr0gramm', Pr0gramm)
