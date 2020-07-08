from typing import Dict, Type

import pytest

from nichtparasoup.imagecrawler import BaseImageCrawler
from nichtparasoup.imagecrawlers import KnownImageCrawlers
from nichtparasoup.testing.imagecrawler import ImageCrawlerLoaderTest

from .._mocks.loadable_imagecrawlers import LoadableImageCrawlerA, LoadableImageCrawlerB


class TestImageCrawlerLoaderTest:

    @pytest.mark.parametrize(
        ('got_class', 'got_name', 'expected'),
        [
            (False, False, False),
            (False, True, False),
            (True, False, False),
            (True, True, True),
        ],
        ids=[
            'not-class, not-name',
            'not-class, got-name',
            'got-class, not-name',
            'got-class, got-name',
        ]
    )
    def test_check(self, got_class: bool, got_name: bool, expected: bool) -> None:
        # arrange
        iclt = ImageCrawlerLoaderTest()
        iclt.check_get_imagecrawler_class = lambda *_, **__: got_class  # type: ignore[assignment]
        iclt.check_get_imagecrawler_name = lambda *_, **__: got_name  # type: ignore[assignment]
        # act
        res = iclt.check('', LoadableImageCrawlerA)
        # assert
        assert res is expected

    @pytest.mark.parametrize(
        ('ic_name', 'ic_class', 'kics', 'expected_error'),
        [
            ('Foo', LoadableImageCrawlerA, {}, r'Unknown name .*'),
            ('LoadableImageCrawlerA', LoadableImageCrawlerA, {'LoadableImageCrawlerA': LoadableImageCrawlerB},
             r'.* is not .*'),
        ],
        ids=[
            'not-found',
            'mismatch',
        ]
    )
    def test_check_get_imagecrawler_class_fail(self,
                                               ic_name: str, ic_class: Type[BaseImageCrawler],
                                               kics: Dict[str, Type[BaseImageCrawler]],
                                               expected_error: str) -> None:
        # arrange
        iclt = ImageCrawlerLoaderTest()
        kic = KnownImageCrawlers([])
        kic._list = kics
        iclt._get_imagecrawlers = lambda: kic  # type: ignore[assignment]
        # act & assert
        with pytest.raises(ValueError, match=expected_error):
            iclt.check_get_imagecrawler_class(ic_name, ic_class)

    def test_check_get_imagecrawler_class_pass(self) -> None:
        # arrange
        iclt = ImageCrawlerLoaderTest()
        kic = KnownImageCrawlers([])
        ic_name = 'Foo'
        ic_class = LoadableImageCrawlerA
        kic._list = {ic_name: ic_class}
        iclt._get_imagecrawlers = lambda: kic  # type: ignore[assignment]
        # act
        res = iclt.check_get_imagecrawler_class(ic_name, ic_class)
        # assert
        assert res is True

    @pytest.mark.parametrize(
        ('ic_name', 'ic_class', 'kics', 'expected_error'),
        [
            ('Foo', LoadableImageCrawlerA, {}, r'Unknown class .*'),
            ('LoadableImageCrawlerA', LoadableImageCrawlerA, {'LoadableImageCrawlerB': LoadableImageCrawlerA},
             r'.* is not .*'),
        ],
        ids=[
            'not-found',
            'mismatch',
        ]
    )
    def test_check_get_imagecrawler_name_fail(self,
                                              ic_name: str, ic_class: Type[BaseImageCrawler],
                                              kics: Dict[str, Type[BaseImageCrawler]],
                                              expected_error: str) -> None:
        # arrange
        iclt = ImageCrawlerLoaderTest()
        kic = KnownImageCrawlers([])
        kic._list = kics
        iclt._get_imagecrawlers = lambda: kic  # type: ignore[assignment]
        # act & assert
        with pytest.raises(ValueError, match=expected_error):
            iclt.check_get_imagecrawler_name(ic_name, ic_class)

    def test_check_get_imagecrawler_name_pass(self) -> None:
        # arrange
        iclt = ImageCrawlerLoaderTest()
        kic = KnownImageCrawlers([])
        kic._list = {'Bar': LoadableImageCrawlerA}
        iclt._get_imagecrawlers = lambda: kic  # type: ignore[assignment]
        # act
        res = iclt.check_get_imagecrawler_name('Bar', LoadableImageCrawlerA)
        # assert
        assert res is True
