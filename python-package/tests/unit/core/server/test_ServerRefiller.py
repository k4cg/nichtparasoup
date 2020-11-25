from unittest.mock import Mock

import pytest

from nichtparasoup.core.server import ServerRefiller as Sut


@pytest.mark.skip(reason='TODO')
def test_run() -> None:
    Sut(Mock(), 1.0)
    raise NotImplementedError()
