from abc import ABC
from unittest import TestCase

from nichtparasoup.config import get_imagecrawler, parse_yaml_file
from nichtparasoup.core.imagecrawler import BaseImageCrawler


class ConfigFilesTest(TestCase, ABC):  # pragma: no cover

    def validate(self, file: str) -> None:
        config = parse_yaml_file(file)
        self.assertIsInstance(config, dict)
        for crawler_config in config['crawlers']:
            try:
                imagecrawler = get_imagecrawler(crawler_config)
            except BaseException as e:
                self.fail('Init {}\r\n{}'.format(crawler_config, e))
            self.assertIsInstance(imagecrawler, BaseImageCrawler, file)

    def probe(self, file: str) -> None:
        config = parse_yaml_file(file)
        self.assertIsInstance(config, dict)
        for crawler_config in config['crawlers']:
            imagecrawler = get_imagecrawler(crawler_config)
            try:
                imagecrawler._crawl()
            except BaseException as e:
                self.fail('Crawl {!r}\r\n{}'.format(imagecrawler, e))
