from unittest.mock import Mock

import pytest

from nichtparasoup.core.imagecrawler import BaseImageCrawler as Sut

from .mock_BaseImageCrawler import _MockImageCrawler, _OtherImageCrawler


def test_eq_based_on_config() -> None:
    # arrange
    imagecrawler1 = _MockImageCrawler(test='a')
    imagecrawler2 = _MockImageCrawler(test='a')
    imagecrawler3 = _MockImageCrawler(test='c')
    imagecrawler4 = _OtherImageCrawler(test='a')
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
    imagecrawler1 = _MockImageCrawler(test='a')
    imagecrawler2 = _MockImageCrawler(test='a')
    imagecrawler3 = _MockImageCrawler(test='c')
    imagecrawler4 = _OtherImageCrawler(test='a')
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


def test_get_config() -> None:
    # arrange
    config_in = {'a': 'a', '_b': 'b', '__c': 'c'}
    sut = Mock(Sut, _config=config_in)
    # act
    config_out = Sut.get_config(sut)
    # assert
    assert config_out['a'] == config_in['a']
    assert '_b' not in config_out
    assert '_c' not in config_out


@pytest.mark.parametrize('must_reset', [False, True], ids=['must_not_reset', 'must_reset'])
def test_reset(must_reset: bool) -> None:
    # arrange
    sut = _MockImageCrawler()
    if must_reset:
        sut.reset()
    # act
    Sut.crawl(sut)
    # assert
    assert sut._reset.call_count == (1 if must_reset else 0)
