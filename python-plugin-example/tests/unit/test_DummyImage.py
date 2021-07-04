from random import randint, random
from typing import Any
from unittest.mock import Mock
from urllib.parse import urlparse

import pytest

from nichtparasoup_imagecrawler_dummyimage import DummyImage as Sut

_DUMMYIMAGE_RIGHT_CONFIG = {'width': randint(1, 999), 'height': randint(1, 999)}


class TestDummyImageConfigCorrect:

    @staticmethod
    def test_right_value() -> None:
        # arrange
        config_in = _DUMMYIMAGE_RIGHT_CONFIG.copy()
        # act
        config_out = Sut.check_config(config_in)
        # assert
        assert config_out == _DUMMYIMAGE_RIGHT_CONFIG

    @staticmethod
    def test_unknown_ignored() -> None:
        # arrange
        config_in = _DUMMYIMAGE_RIGHT_CONFIG.copy()
        config_in['unknown'] = 42
        # act
        config_out = Sut.check_config(config_in)
        # assert
        assert config_out == _DUMMYIMAGE_RIGHT_CONFIG


class TestDummyImageConfigWidth:

    @staticmethod
    def test_missing_value() -> None:
        # arrange
        config_in = _DUMMYIMAGE_RIGHT_CONFIG.copy()
        del config_in['width']
        # assert
        with pytest.raises(KeyError):
            # act
            Sut.check_config(config_in)

    @staticmethod
    @pytest.mark.parametrize('wrong_type',
                             [None, True, '', random(), list(), set(), dict(), tuple(), object()],
                             ids=type)
    def test_wrong_type(wrong_type: Any) -> None:
        # arrange
        config_in = _DUMMYIMAGE_RIGHT_CONFIG.copy()
        config_in['width'] = wrong_type
        # assert
        with pytest.raises(TypeError):
            # act
            Sut.check_config(config_in)

    @staticmethod
    @pytest.mark.parametrize('wrong_value', [0, -randint(1, 999)], ids=['zero', 'negative'])
    def test_wrong_value(wrong_value: int) -> None:
        # arrange
        config_in = _DUMMYIMAGE_RIGHT_CONFIG.copy()
        config_in['width'] = wrong_value
        # assert
        with pytest.raises(ValueError):
            # act
            Sut.check_config(config_in)


class TestDummyImageConfigHeight:

    @staticmethod
    def test_missing_value() -> None:
        # arrange
        config_in = _DUMMYIMAGE_RIGHT_CONFIG.copy()
        del config_in['height']
        # assert
        with pytest.raises(KeyError):
            # act
            Sut.check_config(config_in)

    @staticmethod
    @pytest.mark.parametrize('wrong_type',
                             [None, True, '', random(), list(), set(), dict(), tuple(), object()],
                             ids=type)
    def test_wrong_type(wrong_type: Any) -> None:
        # arrange
        config_in = _DUMMYIMAGE_RIGHT_CONFIG.copy()
        config_in['height'] = wrong_type
        # assert
        with pytest.raises(TypeError):
            # act
            Sut.check_config(config_in)

    @staticmethod
    @pytest.mark.parametrize('wrong_value', [0, -randint(1, 999)], ids=['zero', 'negative'])
    def test_wrong_value(wrong_value: int) -> None:
        # arrange
        config_in = _DUMMYIMAGE_RIGHT_CONFIG.copy()
        config_in['height'] = wrong_value
        # assert
        with pytest.raises(ValueError):
            # act
            Sut.check_config(config_in)


def test_always_exhausted() -> None:
    # act
    exhausted = Sut.is_exhausted(Mock())
    # assert
    assert not exhausted


def test_get_image_uri() -> None:
    width = randint(1, 999)
    height = randint(1, 999)
    # act
    url = Sut._get_image_uri(width=width, height=height)
    url_parts = urlparse(url)
    # assert
    assert url_parts.hostname == 'dummyimage.com'
    assert url_parts.path.startswith(f'/{width}x{height}/')


def test_crawl() -> None:
    # arrange
    crawler = Sut(**_DUMMYIMAGE_RIGHT_CONFIG)
    # act
    images_crawled = crawler._crawl()
    # assert
    assert len(images_crawled) == crawler._BUNCH, 'crawler did not finish'
    for image_crawled in images_crawled:
        assert image_crawled.is_generic is True, 'this is not generic'


def test_description_config() -> None:
    # act
    description = Sut.info()
    # assert
    assert isinstance(description.config, dict)
    assert _DUMMYIMAGE_RIGHT_CONFIG.keys() == description.config.keys()
