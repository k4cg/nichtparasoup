import unittest

from nichtparasoup.config import _defaults_file as config_defaults_file, parse_yaml_file


class ConfigTest(unittest.TestCase):

    def test_parse_yaml_file(self) -> None:
        """ validate the defaults (again) - this file is supposed to be correct """
        # arrange
        file = config_defaults_file
        # act
        config = parse_yaml_file(file)
        # assert
        self.assertIsNotNone(config)

    def write_test(self) -> None:
        # TODO: write tests
        self.skipTest('TODO: write the test')
