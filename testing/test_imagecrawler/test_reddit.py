import unittest
from os.path import dirname, join as path_join

from nichtparasoup.core.image import Image, ImageCollection
from nichtparasoup.imagecrawler import get_class as get_imagecrawler_class
from nichtparasoup.imagecrawler.reddit import Reddit

from . import _FileFetcher

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


class RedditBuildUriTest(unittest.TestCase):

    def test__build_uri_at_front(self) -> None:
        # arrange
        crawler = Reddit(subreddit='foo')
        # act
        uri = crawler._get_uri(None)
        # assert
        self.assertEqual(uri, 'https://www.reddit.com/r/foo.json?after=')

    def test__build_uri_at_front__escape(self) -> None:
        # arrange
        crawler = Reddit(subreddit='foo/bar bazz')
        # act
        uri = crawler._get_uri(None)
        # assert
        self.assertEqual(uri, 'https://www.reddit.com/r/foo%2Fbar+bazz.json?after=')

    def test__build_uri_at_after(self) -> None:
        # arrange
        crawler = Reddit(subreddit='test')
        # act
        uri = crawler._get_uri('foobar')
        # assert
        self.assertEqual(uri, 'https://www.reddit.com/r/test.json?after=foobar')

    def test__build_uri_at_after__escape(self) -> None:
        # arrange
        crawler = Reddit(subreddit='test')
        # act
        uri = crawler._get_uri('foo/bar bazz')
        # assert
        self.assertEqual(uri, 'https://www.reddit.com/r/test.json?after=foo%2Fbar+bazz')


class RedditResetTest(unittest.TestCase):

    def test_reset_done(self) -> None:
        # arrange
        crawler = Reddit(subreddit='test')
        crawler._after = 'foo'
        # act
        crawler._reset()
        # assert
        self.assertIsNone(crawler._after)


_FILE_FETCHER = _FileFetcher({  # relative to "../testdata_instagram"
    '/r/aww.json?after=': 'aww.json',
}, base_dir=path_join(dirname(__file__), 'testdata_reddit'))


class RedditCrawlTest(unittest.TestCase):

    def setUp(self) -> None:
        self.crawler = Reddit(subreddit='aww')
        self.crawler._remote_fetcher = _FILE_FETCHER

    def tearDown(self) -> None:
        del self.crawler

    def test_crawl(self) -> None:
        # arrange
        expected_after = 't3_dqx42l'
        expected_images = ImageCollection()
        expected_images.add(Image(
            uri='https://i.redd.it/kl3dp9sy5fw31.jpg',
            source='https://www.reddit.com/r/aww/comments/dqx0z4/a_very_photogenic_noodle/'))
        expected_images.add(Image(
            uri='https://i.redd.it/4ltnvj5irdw31.jpg',
            source='https://www.reddit.com/r/aww/comments/dqud6w/3/'))
        expected_images.add(Image(
            uri='https://i.redd.it/nkfjoej8yew31.png',
            source='https://www.reddit.com/r/aww/comments/dqwp8l/left_the_house_for_10_minutes_and_came_back_to/'))
        expected_images.add(Image(
            uri='https://i.redd.it/gcxqswv8igw31.png',
            source='https://www.reddit.com/r/aww/comments/dqz6iz/blind_cutie/'))
        expected_images.add(Image(
            uri='https://i.redd.it/hywobahj9ew31.png',
            source='https://www.reddit.com/r/aww/comments/dqvgm9/i_asked_this_guy_if_he_knocked_over_the_treats/'))
        expected_images.add(Image(
            uri='https://i.redd.it/j4qda3c9scw31.jpg',
            source='https://www.reddit.com/r/aww/comments/dqrxiq/admiral_anchovies_is_two_weeks_old_and_has/'))
        expected_images.add(Image(
            uri='https://i.imgur.com/O2bVClA.jpg',
            source='https://www.reddit.com/r/aww/comments/dqsk7y/meet_our_new_3_month_old_baby_bucko_the_beagle/',
        ))
        expected_images.add(Image(
            uri='https://imgur.com/82LxoWj.jpg',
            source='https://www.reddit.com/r/aww/comments/dqtdo7/im_one_of_a_kind/',
        ))
        # act
        images = self.crawler._crawl()
        # assert
        self.assertEqual(self.crawler._after, expected_after)
        self.assertSetEqual(images, expected_images)
        for expected_image in expected_images:
            for image in images:
                if image == expected_image:
                    # sources are irrelevant for equality, need to be checked manually
                    self.assertEqual(image.source, expected_image.source)


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
