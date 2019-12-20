from unittest import TestCase

from nichtparasoup.config import get_imagecrawler, parse_yaml_file
from nichtparasoup.core.imagecrawler import BaseImageCrawler


class ConfigFilesTest(TestCase):  # pragma: no cover

    def validate(self, file: str) -> None:
        config = parse_yaml_file(file)
        self.assertIsInstance(config, dict, file)
        for crawler_config in config['crawlers']:
            try:
                imagecrawler = get_imagecrawler(crawler_config)
            except Exception as e:
                self.fail('{}\r\n{}'.format(file, e))
            self.assertIsInstance(imagecrawler, BaseImageCrawler, file)
