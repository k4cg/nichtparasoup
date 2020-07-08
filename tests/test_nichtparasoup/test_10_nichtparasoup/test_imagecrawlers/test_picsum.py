import unittest
from typing import Any, List

import pytest

from nichtparasoup.imagecrawlers.picsum import Picsum
from nichtparasoup.testing.imagecrawler import ImageCrawlerLoaderTest

_picsum_right_config = {'width': 800, 'height': 600}


class PicsumConfigCorrect(unittest.TestCase):

    def test__check_config_right_value(self) -> None:
        # arrange
        config_in = _picsum_right_config.copy()
        # act
        config_out = Picsum.check_config(config_in)
        # assert
        self.assertDictEqual(config_in, config_out)


class PicsumConfigWidthTest(unittest.TestCase):

    def setUp(self) -> None:
        self._picsum_right_config_wo_width = _picsum_right_config.copy()
        del self._picsum_right_config_wo_width["width"]

    def tearDown(self) -> None:
        del self._picsum_right_config_wo_width

    def test__check_config_missing_value(self) -> None:
        # assert
        with self.assertRaises(KeyError):
            Picsum.check_config(self._picsum_right_config_wo_width)

    def test__check_config_wrong_type(self) -> None:
        wrong_types: List[Any] = [None, True, "", [], (), {}, self]
        for wrong_type in wrong_types:
            # arrange
            config_in = self._picsum_right_config_wo_width
            config_in["width"] = wrong_type
            # assert
            with self.assertRaises(TypeError, msg=repr(config_in)):
                Picsum.check_config(config_in)

    def test__check_config_wrong_value(self) -> None:
        wrong_values = [0, -1]
        for wrong_value in wrong_values:
            # arrange
            config_in = self._picsum_right_config_wo_width
            config_in["width"] = wrong_value
            # assert
            with self.assertRaises(ValueError, msg=repr(config_in)):
                Picsum.check_config(config_in)


class PicsumConfigHeightTest(unittest.TestCase):

    def setUp(self) -> None:
        self._picsum_right_config_wo_height = _picsum_right_config.copy()
        del self._picsum_right_config_wo_height["height"]

    def tearDown(self) -> None:
        del self._picsum_right_config_wo_height

    def test__check_config_missing_value(self) -> None:
        # assert
        with self.assertRaises(KeyError):
            Picsum.check_config(self._picsum_right_config_wo_height)

    def test__check_config_wrong_type(self) -> None:
        wrong_types: List[Any] = [None, True, "", [], (), {}, self]
        for wrong_type in wrong_types:
            # arrange
            config_in = self._picsum_right_config_wo_height
            config_in["height"] = wrong_type
            # assert
            with self.assertRaises(TypeError, msg=repr(config_in)):
                Picsum.check_config(config_in)

    def test__check_config_wrong_value(self) -> None:
        wrong_values = [0, -1]
        for wrong_value in wrong_values:
            # arrange
            config_in = self._picsum_right_config_wo_height
            config_in["height"] = wrong_value
            # assert
            with self.assertRaises(ValueError, msg=repr(config_in)):
                Picsum.check_config(config_in)


class PicsumCrawlTest(unittest.TestCase):

    def test_crawl(self) -> None:
        # arrange
        crawler = Picsum(**_picsum_right_config)
        # act
        images_crawled = crawler.crawl()
        images_crawled_len = len(images_crawled)
        image_crawled = images_crawled.pop() if images_crawled_len else None
        # assert
        self.assertEqual(images_crawled_len, crawler._bunch, "crawler did not finish")
        if image_crawled:
            self.assertTrue(image_crawled.is_generic, 'this is not generic')


class PicsumDescriptionTest(unittest.TestCase):

    def test_description_config(self) -> None:
        # act
        description = Picsum.info()
        # assert
        assert isinstance(description.config, dict)
        for config_key in _picsum_right_config.keys():
            self.assertIn(config_key, description.config)


@pytest.mark.no_cover
def test_loader() -> None:
    ImageCrawlerLoaderTest().check('Picsum', Picsum)
