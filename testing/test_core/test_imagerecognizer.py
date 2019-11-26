import unittest

from nichtparasoup.core.imagecrawler import ImageRecognizer


class BaseImageCrawlerPathIsImageTest(unittest.TestCase):

    def test_path_is_image(self) -> None:
        # arrange
        recognizer = ImageRecognizer()
        image_file_extensions = ('jpg', 'jpeg', 'gif', 'png', 'svg')
        # act & assert
        for image_file_extension in image_file_extensions:
            image_file_path = 'foo.' + image_file_extension
            self.assertTrue(recognizer.path_is_image(image_file_path), image_file_path)
            self.assertTrue(recognizer.path_is_image(image_file_path + '?foo'), image_file_path)
            self.assertTrue(recognizer.path_is_image(image_file_path + '#bar'), image_file_path)
            self.assertTrue(recognizer.path_is_image(image_file_path + '?foo#bar'), image_file_path)

    def test_path_is_not_image(self) -> None:
        # arrange
        recognizer = ImageRecognizer()
        not_image_file_extensions = ('', '/', '.html', '.js', '.css')
        # act & assert
        for not_image_file_extension in not_image_file_extensions:
            not_image_file_path = 'foo' + not_image_file_extension
            self.assertFalse(recognizer.path_is_image(not_image_file_path), not_image_file_path)
            self.assertFalse(recognizer.path_is_image(not_image_file_path + '?foo'), not_image_file_path)
            self.assertFalse(recognizer.path_is_image(not_image_file_path + '#bar'), not_image_file_path)
            self.assertFalse(recognizer.path_is_image(not_image_file_path + '?foo#bar'), not_image_file_path)
