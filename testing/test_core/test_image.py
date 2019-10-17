import unittest

from nichtparasoup.core.image import Image, ImageCollection


class ImageTest(unittest.TestCase):

    def test_uri_is_hash(self) -> None:
        # arrange
        uri = 'test'
        image = Image(uri)
        # assert
        self.assertEqual(hash(uri), hash(image))

    def test_uri_makes_equal(self) -> None:
        # arrange
        uri = 'test'
        image1 = Image(uri)
        image2 = Image(uri)
        # assert
        self.assertEqual(image1, image2)

    def test_equal(self) -> None:
        # arrange
        image1 = Image("testA")
        image2 = Image("testA")
        image3 = Image("testB", is_generic=True)
        image4 = Image("testB", is_generic=True)
        # assert
        self.assertEqual(image1, image1)
        self.assertEqual(image1, image2)
        self.assertEqual(image3, image3)
        self.assertNotEqual(image3, image4)

    def test_remove_nongeneric_from_container(self) -> None:
        # arrange
        image1 = Image("testA", is_generic=True)
        image2 = Image("testA", is_generic=True)
        images = ImageCollection()
        images.add(image1)
        # act
        images.discard(image2)
        # assert
        self.assertEqual(1, len(images))
        self.assertIn(image1, images)
