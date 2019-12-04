import unittest

from nichtparasoup.core.image import Image, ImageCollection


class ImageTest(unittest.TestCase):

    def test_uri_is_hash(self) -> None:
        # arrange
        uri = 'test'
        image = Image(uri, 'test')
        # assert
        self.assertEqual(hash(uri), hash(image))

    def test_uri_makes_equal(self) -> None:
        # arrange
        uri = 'test'
        image1 = Image(uri, 'test1')
        image2 = Image(uri, 'test2')
        # assert
        self.assertEqual(image1, image2)

    def test_unequal_other_types(self) -> None:
        # arrange
        image = Image("testA", 'test')
        other_types = [None, True, 23, 4.2, "", [], (), {}, self]  # type: ignore
        # assert
        for other_type in other_types:
            self.assertNotEqual(image, other_type)

    def test_equal(self) -> None:
        # arrange
        image1 = Image("testA", 'testA')
        image2 = Image("testA", 'testA')
        image3 = Image("testB", 'testB', is_generic=True)
        image4 = Image("testB", 'testB', is_generic=True)
        # assert
        self.assertEqual(image1, image1)
        self.assertEqual(image1, image2)
        self.assertEqual(image3, image3)
        self.assertNotEqual(image3, image4)

    def test_remove_nongeneric_from_container(self) -> None:
        # arrange
        image1 = Image("testA", 'testA', is_generic=True)
        image2 = Image("testA", 'testA', is_generic=True)
        images = ImageCollection()
        images.add(image1)
        # act
        images.discard(image2)
        # assert
        self.assertEqual(1, len(images))
        self.assertIn(image1, images)
