import unittest
from os.path import dirname, join as path_join, realpath

from nichtparasoup.config import parse_yaml_file


class ConfigParserTest(unittest.TestCase):

    def setUp(self) -> None:
        config_root_path = realpath(path_join(dirname(__file__), 'config_files'))
        self.config_paths = dict(
            root=config_root_path,
            positive=path_join(config_root_path, 'positive'),
        )

    def tearDown(self) -> None:
        del self.config_paths

    def test_optional_crawler_weight(self) -> None:
        # arrange
        file = path_join(self.config_paths['positive'], 'crawler_weight_optional.yaml')
        # act
        config = parse_yaml_file(file)
        # assert
        for crawler in config['crawlers']:
            self.assertEqual(1, crawler['weight'])

    def test_multiple_crawlers(self) -> None:
        # arrange
        file = path_join(self.config_paths['positive'], 'multiple_crawlers.yaml')
        # act
        config = parse_yaml_file(file)
        # assert
        self.assertEqual(3, len(config['crawlers']))
