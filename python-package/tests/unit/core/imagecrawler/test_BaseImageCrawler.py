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
    eq1mock = imagecrawler1 == Mock()
    # assert
    assert eq11 is True
    assert eq12 is True
    assert eq13 is False
    assert eq14 is False
    assert eq1mock is False


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
    eq1mock = imagecrawler1 != Mock()
    # assert
    assert eq11 is False
    assert eq12 is False
    assert eq13 is True
    assert eq14 is True
    assert eq1mock is True


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


@pytest.mark.parametrize('is_exhausted', [False, True], ids=['not_exhausted', 'is_exhausted'])
def test_crawl(is_exhausted: bool) -> None:
    # arrange
    sut = _MockImageCrawler()
    sut.is_exhausted.return_value = is_exhausted
    # act
    images = sut.crawl()
    # assert
    if is_exhausted:
        sut._crawl.assert_not_called()
        assert len(images) == 0
    else:
        sut._crawl.assert_called_once()
        assert images is sut._crawl.return_value


def test_crawl_errors() -> None:
    # arrange
    sut = _MockImageCrawler()
    sut.is_exhausted.return_value = False
    sut._crawl.side_effect = Exception()
    # act
    images = sut.crawl()
    # assert
    sut._crawl.assert_called_once()
    assert len(images) == 0
