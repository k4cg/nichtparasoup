from unittest.mock import Mock

import pytest

from nichtparasoup.core.server import Server as Sut


@pytest.mark.skip(reason='TODO')
def test_has_image() -> None:
    # arrange
    sut = Mock()
    # act
    has_image = Sut.has_image(sut)
    # assert
    assert has_image is True
