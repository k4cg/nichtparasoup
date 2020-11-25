from unittest.mock import Mock

from nichtparasoup.core.image import ImageCollection as Sut


def test_copy() -> None:
    # arrange
    image1 = Mock()
    image2 = Mock()
    images = Sut([image1, image2])
    # act
    copy = images.copy()
    # assert
    assert isinstance(copy, Sut)
    assert copy is not images
    assert copy == images
    for image in images:
        assert image in copy
