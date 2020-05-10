import unittest

import pytest  # type: ignore

from nichtparasoup.config import DEFAULTS_FILE
from nichtparasoup.testing.configfile import ConfigFileTest


class DefaultConfigFileTest(unittest.TestCase, ConfigFileTest):

    @pytest.mark.online  # type: ignore  # probing goes over the internet
    @pytest.mark.slow  # type: ignore  # probing might be slow
    def test_default(self) -> None:
        self.check_file(DEFAULTS_FILE)
