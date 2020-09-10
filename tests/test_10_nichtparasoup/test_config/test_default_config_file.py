import pytest

from nichtparasoup.config import _DEFAULTS_FILE
from nichtparasoup.testing.config import ConfigFileTest


class DefaultConfigFileTest(ConfigFileTest):

    @pytest.mark.online  # type: ignore  # probing goes over the internet
    @pytest.mark.slow  # type: ignore  # probing might be slow
    def test_default(self) -> None:
        self.validate(_DEFAULTS_FILE)
        self.probe(_DEFAULTS_FILE)
