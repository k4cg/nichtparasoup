from typing import Optional

import pytest

from nichtparasoup.imagecrawler import Image, ImageCollection
from nichtparasoup.testing.imagecrawler import ImagecrawlerProbeResult


class TestImagecrawlerProbeResultAdd:

    def test_type_mismatch(self) -> None:
        # arrange
        one = ImagecrawlerProbeResult(None, [])
        other = 1337
        # act & assert
        with pytest.raises(TypeError, match='unsupported operand'):
            one + other

    def test_errors(self) -> None:
        # arrange
        errors = [BaseException(), Exception(), TypeError(), BrokenPipeError()]
        one = ImagecrawlerProbeResult(None, errors[:2])
        other = ImagecrawlerProbeResult(None, errors[2:])
        # act
        res = one + other
        # assert
        assert errors == res.errors

    @pytest.mark.parametrize(
        ('one_images', 'other_images', 'expected_images'),
        [
            [None, None, None],
            [None, ImageCollection([Image(uri='1', source='1')]), ImageCollection([Image(uri='1', source='1')])],
            [ImageCollection([Image(uri='1', source='1')]), None, ImageCollection([Image(uri='1', source='1')])],
            [
                ImageCollection([Image(uri='1', source='1')]), ImageCollection([Image(uri='2', source='2')]),
                ImageCollection([Image(uri='1', source='1'), Image(uri='2', source='2')])
            ],
        ],
        ids=[
            'both None',
            'one None',
            'other None',
            'no None',
        ]
    )
    def test_images(self,
                    one_images: Optional[ImageCollection],
                    other_images: Optional[ImageCollection],
                    expected_images: Optional[ImageCollection]) -> None:
        # arrange
        one = ImagecrawlerProbeResult(one_images, [])
        other = ImagecrawlerProbeResult(other_images, [])
        # act
        res = one + other
        # assert
        assert expected_images == res.images


class TestImagecrawlerProbeResultIsFailure:

    def test_failure_no_errors(self) -> None:
        # arrange
        res = ImagecrawlerProbeResult(None, [])
        # act & assert
        assert res.is_failure
        assert not res.is_erroneous

    def test_failure_with_error(self) -> None:
        # arrange
        res = ImagecrawlerProbeResult(None, [Exception()])
        # act & assert
        assert res.is_failure
        assert res.is_erroneous

    def test_success_no_errors(self) -> None:
        # arrange
        res = ImagecrawlerProbeResult(ImageCollection(), [])
        # act & assert
        assert not res.is_failure
        assert not res.is_erroneous

    def test_success_with_errors(self) -> None:
        # arrange
        res = ImagecrawlerProbeResult(ImageCollection(), [Exception()])
        # act & assert
        assert not res.is_failure
        assert res.is_erroneous
