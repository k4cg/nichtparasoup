from typing import List

import pytest

from .._mocks.mockable_imagecrawler import MockableImageCrawler, YetAnotherImageCrawler


class TestBaseImageCrawlerEqual:

    def test_equal(self) -> None:
        # arrange
        c01 = MockableImageCrawler()
        c02 = MockableImageCrawler()
        c11 = MockableImageCrawler(foo='bar', baz=1)
        c12 = MockableImageCrawler(foo='bar', baz=1)
        # assert
        assert c01 == c01
        assert c02 == c02
        assert c01 == c02
        assert c11 == c11
        assert c12 == c12
        assert c11 == c12

    def test_unequal(self) -> None:
        # arrange
        c1 = MockableImageCrawler()
        c2 = YetAnotherImageCrawler()
        c3 = MockableImageCrawler(foo='bar', baz=1)
        c4 = YetAnotherImageCrawler(foo='b4r', baz=1)
        c5 = MockableImageCrawler(baz=1)
        # assert
        assert c1 != c2
        assert c1 != c3
        assert c1 != c4
        assert c1 != c5
        assert c2 != c3
        assert c2 != c4
        assert c2 != c5
        assert c3 != c4
        assert c3 != c5
        assert c4 != c5


class TestBaseImageCrawlerReset:

    def test_reset_set(self) -> None:
        # arrange
        c = MockableImageCrawler()
        c._reset_before_next_crawl = False
        # act
        c.reset()
        # assert
        assert True is c._reset_before_next_crawl

    def test_reset_released(self) -> None:
        # arrange
        c = MockableImageCrawler()
        c._reset_before_next_crawl = True
        # act
        c.crawl()
        # assert
        assert False is c._reset_before_next_crawl


class TestBaseImageCrawlerGetConfig:

    def test_public(self) -> None:
        # arrange
        c = MockableImageCrawler(foo='bar')
        # act
        config = c.get_config()
        # assert
        assert {'foo': 'bar'} == config

    def test_empty_key(self) -> None:
        # arrange
        c = MockableImageCrawler(**{'': 'bar'})
        # act
        config = c.get_config()
        # assert
        assert {'': 'bar'} == config

    def test_protected(self) -> None:
        # arrange
        c = MockableImageCrawler(_foo='bar')
        # act
        config = c.get_config()
        # assert
        assert {} == config

    def test_private(self) -> None:
        # arrange
        c = MockableImageCrawler(__foo='bar')
        # act
        config = c.get_config()
        # assert
        assert {} == config


class TestExhaustedCrawling:

    @pytest.mark.parametrize(
        ('is_exhausted', 'expected_call_craw'),
        [
            (False, [True]),
            (True, []),
        ],
        ids=[
            'exhausted',
            'not-exhausted',
        ]
    )
    def test_exhausted(self, is_exhausted: bool, expected_call_craw: List[bool]) -> None:
        # arrange
        c = MockableImageCrawler()
        did_call_craw = []

        def fake_exhausted() -> bool:
            return is_exhausted

        def fake_crawl() -> None:
            did_call_craw.append(True)
            raise NotImplementedError()

        c.is_exhausted = fake_exhausted  # type: ignore[assignment]
        c._crawl = fake_crawl  # type: ignore[assignment]
        # act
        c.crawl()
        # assert
        assert expected_call_craw == did_call_craw
