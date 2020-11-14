import pytest
from nichtparasoup.testing.imagecrawler import ImageCrawlerLoaderTest

from nichtparasoup_imagecrawler_dummyimage import DummyImage


@pytest.mark.no_cover
def test_loader() -> None:
    assert ImageCrawlerLoaderTest().check('DummyImage', DummyImage)
