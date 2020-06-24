import pytest

from nichtparasoup.config import DEFAULTS_FILE
from nichtparasoup.testing.configfile import ConfigFileTest


@pytest.mark.no_cover
class TestDefaultConfigFile:

    @pytest.mark.online  # probing goes over the internet
    @pytest.mark.slow  # probing might be slow
    def test_default(self) -> None:
        ConfigFileTest(DEFAULTS_FILE).check_file()
