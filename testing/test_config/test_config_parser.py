import unittest

from nichtparasoup.config import _defaults_file as config_defaults_file, get_config_imagecrawler, parse_yaml_file
from nichtparasoup.core.imagecrawler import BaseImageCrawler


class ConfigParserDefaultsTest(unittest.TestCase):

    def validate(self, file: str) -> None:
        # act
        config = parse_yaml_file(file)
        # assert
        self.assertIsInstance(config, dict, file)
        for crawler_config in config['crawlers']:
            self.assertIsInstance(get_config_imagecrawler(crawler_config), BaseImageCrawler, file)

    def test_defaults(self) -> None:
        # arrange
        file = config_defaults_file
        # act & assert
        self.validate(file)

    def test_examples(self) -> None:
        from glob import glob
        from os.path import dirname, join as path_join, realpath
        from itertools import chain
        examples_base = realpath(path_join(dirname(__file__), "..", "..", 'examples'))
        files_glob = [path_join(examples_base, '*.yml'), path_join(examples_base, '**', '*.yml'),
                      path_join(examples_base, '*.yaml'), path_join(examples_base, '**', '*.yaml')]
        files = chain(*map(glob, files_glob))  # type: ignore
        for file in files:
            self.validate(file)  # type: ignore
