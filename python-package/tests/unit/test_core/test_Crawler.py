import sys
from random import uniform as randfloat
from typing import Any, Union
from unittest.mock import Mock

import pytest

from nichtparasoup.core import Crawler as Sut

if sys.version_info[:2] >= (3, 7):
    from contextlib import nullcontext as does_not_raise
else:
    from contextlib import contextmanager

    @contextmanager
    def does_not_raise() -> None:
        yield


@pytest.mark.parametrize(
    ('weight', 'expectation'),
    [
        (-randfloat(1.0, 99999.0), pytest.raises(ValueError, match='weight')),
        (0, pytest.raises(ValueError, match='weight')),
        (+randfloat(1.0, 99999.0), does_not_raise()),
    ],
    ids=[
        'negative',
        'zero',
        'positive',
    ],
)
def test_weight(weight: Union[int, float], expectation: Any) -> None:
    # arrange
    sut = Mock(Sut)
    sut._weight = old_weight = None
    # act
    with expectation as ex:
        Sut.set_weight(sut, weight)
    # assert
    assert Sut.get_weight(sut) == (weight if ex is None else old_weight)
