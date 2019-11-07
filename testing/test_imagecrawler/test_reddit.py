import unittest

from nichtparasoup.imagecrawler import get_class as get_imagecrawler_class
from nichtparasoup.imagecrawler.reddit import Reddit

_reddit_right_config = dict(TODO=True)


class PicsumConfigCorrect(unittest.TestCase):

    def test__check_config_right_value(self) -> None:
        # arrange
        config_in = _reddit_right_config.copy()
        # act
        config_out = Reddit.check_config(config_in)
        # assert
        self.assertDictEqual(config_in, config_out)


class DummyResetTest(unittest.TestCase):

    def test_reset_done(self) -> None:
        # TODO
        self.assertTrue(False)


class RedditCrawlTest(unittest.TestCase):

    def test_crawl(self) -> None:
        # TODO
        self.assertTrue(False)


class RedditDescriptionTest(unittest.TestCase):
    def test_description_config(self) -> None:
        # act
        # TODO
        # assert
        self.assertTrue(False)


class RedditLoaderTest(unittest.TestCase):
    def test_get_imagecrawler_class(self) -> None:
        # act
        imagecrawler_class = get_imagecrawler_class("Reddit")
        # assert
        self.assertIs(imagecrawler_class, Reddit)
