from unittest.mock import Mock

from nichtparasoup.core.image import ImageCollection


def test_copy() -> None:
    # arrange
    image1 = Mock()
    image2 = Mock()
    images = ImageCollection([image1, image2])
    # act
    copy = images.copy()
    # assert
    assert isinstance(copy, ImageCollection)
    assert copy is not images
    assert copy == images
    for image in images:
        assert image in copy
