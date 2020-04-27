import unittest

import pytest  # type: ignore

from nichtparasoup.config import DEFAULTS_FILE, parse_yaml_file
from nichtparasoup.testing.config import ConfigTest


class DefaultConfigFileTest(unittest.TestCase):

    @pytest.mark.online  # type: ignore  # probing goes over the internet
    @pytest.mark.slow  # type: ignore  # probing might be slow
    def test_default(self) -> None:
        config = parse_yaml_file(DEFAULTS_FILE)
        tester = ConfigTest()
        tester.check_duplicates(config)
        tester.probe(config)
