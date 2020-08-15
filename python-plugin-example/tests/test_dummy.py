import sys

import pytest


def test_dummy() -> None:
    v = sys.version_info[:2]
    if v == (3, 6):
        pytest.skip(v)
    assert v == (3, 8), v
