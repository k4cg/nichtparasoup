import pytest  # type: ignore

from nichtparasoup.config import DEFAULTS_FILE
from nichtparasoup.testing.configfile import ConfigFileTest


class TestDefaultConfigFile:

    @pytest.mark.online  # type: ignore  # probing goes over the internet
    @pytest.mark.slow  # type: ignore  # probing might be slow
    def test_default(self) -> None:
        ConfigFileTest(DEFAULTS_FILE).check_file()
