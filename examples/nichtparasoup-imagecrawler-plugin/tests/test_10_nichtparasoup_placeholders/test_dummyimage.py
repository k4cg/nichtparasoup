import unittest
from typing import Type

from nichtparasoup_placeholders import DummyImage

from nichtparasoup.imagecrawler import BaseImageCrawler
from nichtparasoup.testing.imagecrawler import ImageCrawlerLoaderTest

_DUMMYIMAGE_RIGHT_CONFIG = {'width': 800, 'height': 600}


class DummyImageConfigCorrect(unittest.TestCase):

    def test__check_config_right_value(self) -> None:
        # arrange
        config_in = _DUMMYIMAGE_RIGHT_CONFIG.copy()
        # act
        config_out = DummyImage.check_config(config_in)
        # assert
        self.assertDictEqual(config_in, config_out)


class DummyImageConfigWidthTest(unittest.TestCase):

    def setUp(self) -> None:
        self._dummyimage_right_config_wo_width = _DUMMYIMAGE_RIGHT_CONFIG.copy()
        del self._dummyimage_right_config_wo_width["width"]

    def tearDown(self) -> None:
        del self._dummyimage_right_config_wo_width

    def test__check_config_missing_value(self) -> None:
        # assert
        with self.assertRaises(KeyError):
            DummyImage.check_config(self._dummyimage_right_config_wo_width)

    def test__check_config_wrong_type(self) -> None:
        wrong_types = [None, True, "", [], (), {}, self]  # type: ignore
        for wrong_type in wrong_types:
            # arrange
            config_in = self._dummyimage_right_config_wo_width
            config_in["width"] = wrong_type  # type: ignore
            # assert
            with self.assertRaises(TypeError, msg=repr(config_in)):
                DummyImage.check_config(config_in)

    def test__check_config_wrong_value(self) -> None:
        wrong_values = [0, -1]
        for wrong_value in wrong_values:
            # arrange
            config_in = self._dummyimage_right_config_wo_width
            config_in["width"] = wrong_value
            # assert
            with self.assertRaises(ValueError, msg=repr(config_in)):
                DummyImage.check_config(config_in)


class DummyImageConfigHeightTest(unittest.TestCase):

    def setUp(self) -> None:
        self._dummyimage_right_config_wo_height = _DUMMYIMAGE_RIGHT_CONFIG.copy()
        del self._dummyimage_right_config_wo_height["height"]

    def tearDown(self) -> None:
        del self._dummyimage_right_config_wo_height

    def test__check_config_missing_value(self) -> None:
        # assert
        with self.assertRaises(KeyError):
            DummyImage.check_config(self._dummyimage_right_config_wo_height)

    def test__check_config_wrong_type(self) -> None:
        wrong_types = [None, True, "", [], (), {}, self]  # type: ignore
        for wrong_type in wrong_types:
            # arrange
            config_in = self._dummyimage_right_config_wo_height
            config_in["height"] = wrong_type  # type: ignore
            # assert
            with self.assertRaises(TypeError, msg=repr(config_in)):
                DummyImage.check_config(config_in)

    def test__check_config_wrong_value(self) -> None:
        wrong_values = [0, -1]
        for wrong_value in wrong_values:
            # arrange
            config_in = self._dummyimage_right_config_wo_height
            config_in["height"] = wrong_value
            # assert
            with self.assertRaises(ValueError, msg=repr(config_in)):
                DummyImage.check_config(config_in)


class DummyImageCrawlTest(unittest.TestCase):

    def test_crawl(self) -> None:
        # arrange
        crawler = DummyImage(**_DUMMYIMAGE_RIGHT_CONFIG)
        # act
        images_crawled = crawler.crawl()
        images_crawled_len = len(images_crawled)
        image_crawled = images_crawled.pop() if images_crawled_len else None
        # assert
        self.assertEqual(images_crawled_len, crawler._BUNCH, "crawler did not finish")
        if image_crawled:
            self.assertTrue(image_crawled.is_generic, 'this is not generic')


class DummyImageDescriptionTest(unittest.TestCase):

    def test_description_config(self) -> None:
        # act
        description = DummyImage.info()
        # assert
        assert isinstance(description.config, dict)
        for config_key in _DUMMYIMAGE_RIGHT_CONFIG.keys():
            self.assertIn(config_key, description.config)


class DummyImageLoaderTest(ImageCrawlerLoaderTest):

    @property
    def ic_name(self) -> str:
        return "DummyImage"

    @property
    def ic_class(self) -> Type[BaseImageCrawler]:
        return DummyImage

    def test_loader(self) -> None:
        self.check()
