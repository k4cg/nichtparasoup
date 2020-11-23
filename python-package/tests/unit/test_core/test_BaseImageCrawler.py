from typing import Any
from unittest.mock import Mock, patch

import pytest

from nichtparasoup.core.image import ImageCollection
from nichtparasoup.core.imagecrawler import BaseImageCrawler as Sut, ImageCrawlerConfig, ImageCrawlerInfo


class _MockImageCrawler(Sut):

    def __init__(self, **config: Any) -> None:
        super().__init__(**config)

    info = Mock(return_value=Mock(ImageCrawlerInfo))

    check_config = Mock(side_effect=lambda config: ImageCrawlerConfig(**config))

    is_exhausted = Mock(return_value=False)

    _reset = Mock(return_value=None)

    _crawl = Mock(return_value=Mock(ImageCollection))


def test_eq_based_on_config() -> None:
    # arrange
    class OtherImageCrawler(_MockImageCrawler):
        ...
    imagecrawler1 = _MockImageCrawler(test='a')
    imagecrawler2 = _MockImageCrawler(test='a')
    imagecrawler3 = _MockImageCrawler(test='c')
    imagecrawler4 = OtherImageCrawler(test='a')
    # act
    eq11 = imagecrawler1 == imagecrawler1
    eq12 = imagecrawler1 == imagecrawler2
    eq13 = imagecrawler1 == imagecrawler3
    eq14 = imagecrawler1 == imagecrawler4
    # assert
    assert eq11
    assert eq12
    assert not eq13
    assert not eq14


def test_ne_based_on_config() -> None:
    # arrange
    class OtherImageCrawler(_MockImageCrawler):
        ...
    imagecrawler1 = _MockImageCrawler(test='a')
    imagecrawler2 = _MockImageCrawler(test='a')
    imagecrawler3 = _MockImageCrawler(test='c')
    imagecrawler4 = OtherImageCrawler(test='a')
    # act
    eq11 = imagecrawler1 != imagecrawler1
    eq12 = imagecrawler1 != imagecrawler2
    eq13 = imagecrawler1 != imagecrawler3
    eq14 = imagecrawler1 != imagecrawler4
    # assert
    assert not eq11
    assert not eq12
    assert eq13
    assert eq14


@pytest.mark.parametrize('must_reset', [False, True], ids=['must_not_reset', 'must_reset'])
def test_reset(must_reset: bool) -> None:
    # arrange
    sut = _MockImageCrawler()
    if must_reset:
        sut.reset()
    reset = Mock()
    with patch.object(sut, '_reset', reset):
        # act
        Sut.crawl(sut)
    # assert
    assert reset.call_count == (1 if must_reset else 0)
