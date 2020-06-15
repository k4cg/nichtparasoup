import pytest

from nichtparasoup.core.imagecrawler import ImageRecognizer


class TestBaseImageCrawlerPathIsImage:

    _IMAGE_EXT = ['jpg', 'jpeg', 'gif', 'png', 'svg']

    @pytest.mark.parametrize('image_file_extension', _IMAGE_EXT)
    def test_path_is_image(self, image_file_extension: str) -> None:
        # arrange
        recognizer = ImageRecognizer()
        image_file_path = f'foo.{image_file_extension}'
        # act & assert
        assert True is recognizer.path_is_image(image_file_path)
        assert True is recognizer.path_is_image(f'{image_file_path}?foo')
        assert True is recognizer.path_is_image(f'{image_file_path}?foo={image_file_path}')
        assert True is recognizer.path_is_image(f'{image_file_path}#bar')
        assert True is recognizer.path_is_image(f'{image_file_path}#file_{image_file_path}')
        assert True is recognizer.path_is_image(f'{image_file_path}?foo#bar')
        assert True is recognizer.path_is_image(f'{image_file_path}?foo={image_file_path}#bar')
        assert True is recognizer.path_is_image(f'{image_file_path}?foo#file_{image_file_path}')
        assert True is recognizer.path_is_image(f'{image_file_path}?foo={image_file_path}#file_{image_file_path}')

    @pytest.mark.parametrize('image_file_extension', _IMAGE_EXT)
    def test_path_is_not_false_positive_image(self, image_file_extension: str) -> None:
        # arrange
        recognizer = ImageRecognizer()
        image_file_path = f'foo.{image_file_extension}'
        # act & assert
        assert False is recognizer.path_is_image(f'_{image_file_extension}')
        assert False is recognizer.path_is_image(f'_{image_file_extension}?foo')
        assert False is recognizer.path_is_image(f'_?foo={image_file_path}')
        assert False is recognizer.path_is_image(f'_{image_file_extension}#bar')
        assert False is recognizer.path_is_image(f'_#file_{image_file_path}')
        assert False is recognizer.path_is_image(f'_{image_file_extension}?foo#bar')
        assert False is recognizer.path_is_image(f'_?foo={image_file_path}#bar')
        assert False is recognizer.path_is_image(f'_?foo#file_{image_file_path}')
        assert False is recognizer.path_is_image(f'_?foo={image_file_path}#file_{image_file_path}')

    @pytest.mark.parametrize('not_image_file_extension', ['', '/', '.', '..', '.html', '.js', '.css'])
    def test_path_is_not_image(self, not_image_file_extension: str) -> None:
        # arrange
        recognizer = ImageRecognizer()
        not_image_file_path = f'foo{not_image_file_extension}'
        # act & assert
        assert False is recognizer.path_is_image(not_image_file_path)
        assert False is recognizer.path_is_image(f'{not_image_file_path}?foo')
        assert False is recognizer.path_is_image(f'{not_image_file_path}#bar')
        assert False is recognizer.path_is_image(f'{not_image_file_path}?foo#bar')
