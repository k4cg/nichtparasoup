import unittest
from os.path import dirname, join as path_join, realpath

from nichtparasoup.config import parse_yaml_file


class ConfigParserDefaultsTest(unittest.TestCase):

    def test_set_optional_weight(self) -> None:
        # arrange
        file = realpath(path_join(dirname(__file__), 'configs', 'positive', 'missing_weight.yaml'))
        # act
        config = parse_yaml_file(file)
        # assert
        self.assertEqual(2, len(config["crawlers"]))
        self.assertIsNone(config["crawlers"][0]["weight"])
        self.assertIsNone(config["crawlers"][1]["weight"])

    def test_set_optional_config(self) -> None:
        # arrange
        file = realpath(path_join(dirname(__file__), 'configs', 'positive', 'missing_config.yaml'))
        # act
        config = parse_yaml_file(file)
        # assert
        self.assertEqual(2, len(config["crawlers"]))
        self.assertDictEqual(config["crawlers"][0]["config"], dict())
        self.assertDictEqual(config["crawlers"][1]["config"], dict())
