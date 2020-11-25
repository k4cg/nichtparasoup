import pytest

from nichtparasoup.imagecrawlers.echo import Echo
from nichtparasoup.testing.imagecrawler import ImageCrawlerLoaderTest


@pytest.mark.no_cover
def test_loader() -> None:
    ImageCrawlerLoaderTest().check('Echo', Echo)
