import pytest

from nichtparasoup.config import _DEFAULTS_FILE
from nichtparasoup.testing.config import ConfigFileTest


class DefaultConfigFileTest(ConfigFileTest):

    @pytest.mark.online  # probing goes over the internet
    @pytest.mark.slow  # probing might be slow
    def test_default(self) -> None:
        self.validate(_DEFAULTS_FILE)
        self.probe(_DEFAULTS_FILE)
