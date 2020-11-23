from pathlib import PurePath
from random import getrandbits

import pytest

from nichtparasoup.core.imagecrawler import ImageRecognizer


def _random_case(text: str) -> str:
    return ''.join(
        (char.upper() if bool(getrandbits(1)) else char.lower())
        for char
        in text
    )


@pytest.mark.parametrize(
    'path',
    [f'https://images.com/test{ext}' for ext in ImageRecognizer._IMAGE_SUFFIXES],
    ids=lambda img: PurePath(img).suffix[1:]
)
def test_known_ext(path: str) -> None:
    # arrange
    ir = ImageRecognizer()
    path = _random_case(path)
    # act
    is_image = ir.path_is_image(path)
    # assert
    assert is_image
