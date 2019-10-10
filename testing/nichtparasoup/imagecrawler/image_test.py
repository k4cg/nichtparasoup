import unittest

from nichtparasoup.imagecrawler import Image


class ImageTest(unittest.TestCase):

    def test_uri_is_hash(self) -> None:
        # arrange
        image1 = Image("testA")
        image2 = Image("testA")
        image3 = Image("testB")

        # act
        image1_hash = hash(image1)
        image2_hash = hash(image2)
        image3_hash = hash(image3)

        # assert
        self.assertEqual(image1_hash, image2_hash, "hashes expected to be equal")
        self.assertNotEqual(image1_hash, image3_hash, "hashes expected not to be equal")
