import pytest  # type: ignore

from nichtparasoup.config import _DEFAULTS_FILE
from nichtparasoup.testing.config import ConfigFileTest


class DefaultConfigFileTest(ConfigFileTest):

    @pytest.mark.slow  # type: ignore  # probing goes over the internet and might be slow
    def test_default(self) -> None:
        self.validate(_DEFAULTS_FILE)
        self.probe(_DEFAULTS_FILE)
