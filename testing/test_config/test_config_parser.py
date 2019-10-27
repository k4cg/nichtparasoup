import unittest

from nichtparasoup.config import _defaults_file as config_defaults_file, parse_yaml_file


class ConfigParserDefaultsTest(unittest.TestCase):

    def test_defaults(self) -> None:
        # arrange
        file = config_defaults_file
        # act
        config = parse_yaml_file(file)
        # assert
        self.assertIsInstance(config, dict)
