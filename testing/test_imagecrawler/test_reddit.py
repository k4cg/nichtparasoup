import unittest

from nichtparasoup.imagecrawler import get_class as get_imagecrawler_class
from nichtparasoup.imagecrawler.reddit import Reddit

_reddit_right_config = dict(subreddit='aww')


class RedditConfigCorrect(unittest.TestCase):

    def test__check_config_right_value(self) -> None:
        # arrange
        config_in = _reddit_right_config.copy()
        # act
        config_out = Reddit.check_config(config_in)
        # assert
        self.assertDictEqual(config_in, config_out)


class RedditConfigSubredditTest(unittest.TestCase):

    def setUp(self) -> None:
        self._reddit_right_config_wo_subreddit = _reddit_right_config.copy()
        del self._reddit_right_config_wo_subreddit["subreddit"]

    def tearDown(self) -> None:
        del self._reddit_right_config_wo_subreddit

    def test_check_config_missing_value(self) -> None:
        # assert
        with self.assertRaises(KeyError):
            Reddit.check_config(self._reddit_right_config_wo_subreddit)

    def test_check_config_wrong_type(self) -> None:
        wrong_types = [None, True, 1, 0.1, [], (), {}, self]  # type: ignore
        for wrong_type in wrong_types:
            # arrange
            config_in = self._reddit_right_config_wo_subreddit
            config_in["subreddit"] = wrong_type  # type: ignore
            # assert
            with self.assertRaises(TypeError):
                Reddit.check_config(config_in)

    def test_check_config_wrong_value(self) -> None:
        wrong_values = [""]
        for wrong_value in wrong_values:
            # arrange
            config_in = self._reddit_right_config_wo_subreddit
            config_in["subreddit"] = wrong_value
            # assert
            with self.assertRaises(ValueError):
                Reddit.check_config(config_in)

    def test_check_config_not_existing(self) -> None:
        self.skipTest('TODO do we need this tested or even coded?')
        pass


class RedditResetTest(unittest.TestCase):

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
        description = Reddit.info()
        # assert
        for config_key in _reddit_right_config.keys():
            self.assertTrue(config_key in description.config)


class RedditLoaderTest(unittest.TestCase):
    def test_get_imagecrawler_class(self) -> None:
        # act
        imagecrawler_class = get_imagecrawler_class("Reddit")
        # assert
        self.assertIs(imagecrawler_class, Reddit)
