from unittest.mock import Mock

from nichtparasoup.core.image import Image, ImageCollection


def test_copy() -> None:
    # arrange
    image1 = Mock(Image)
    image2 = Mock(Image)
    images = ImageCollection([image1, image2])
    # act
    copy = images.copy()
    # assert
    assert isinstance(copy, ImageCollection)
    assert copy is not images
    assert copy == images
    assert image1 in copy
    assert image2 in copy
    assert 2 == len(copy)
