from unittest import TestCase

from nichtparasoup.config import get_imagecrawler, parse_yaml_file
from nichtparasoup.core.imagecrawler import BaseImageCrawler


class ConfigFilesTest(TestCase):

    def validate(self, file: str) -> None:
        config = parse_yaml_file(file)
        self.assertIsInstance(config, dict, file)
        for crawler_config in config['crawlers']:
            self.assertIsInstance(get_imagecrawler(crawler_config), BaseImageCrawler, file)
