from typing import Any

import pytest

from nichtparasoup_imagecrawler_dummyimage import DummyImage

_DUMMYIMAGE_RIGHT_CONFIG = {'width': 800, 'height': 600}


class TestDummyImageConfigCorrect:

    def test__check_config_right_value(self) -> None:
        # arrange
        config_in = _DUMMYIMAGE_RIGHT_CONFIG.copy()
        # act
        config_out = DummyImage.check_config(config_in)
        # assert
        assert config_out == config_in


class TestDummyImageConfigWidth:

    def test__check_config_missing_value(self) -> None:
        # arrange
        config_in = _DUMMYIMAGE_RIGHT_CONFIG.copy()
        del config_in['width']
        # act & assert
        with pytest.raises(KeyError):
            DummyImage.check_config(config_in)

    @pytest.mark.parametrize(
        'wrong_type',
        [None, True, '', [], (), {}, object()],
        ids=type
    )
    def test__check_config_wrong_type(self, wrong_type: Any) -> None:
        # arrange
        config_in = _DUMMYIMAGE_RIGHT_CONFIG.copy()
        config_in['width'] = wrong_type
        # assert
        with pytest.raises(TypeError):
            DummyImage.check_config(config_in)

    @pytest.mark.parametrize(
        'wrong_value',
        [0, -1],
        ids=['zero', 'negative']
    )
    def test__check_config_wrong_value(self, wrong_value: int) -> None:
        # arrange
        config_in = _DUMMYIMAGE_RIGHT_CONFIG.copy()
        config_in['width'] = wrong_value
        # assert
        with pytest.raises(ValueError):
            DummyImage.check_config(config_in)


class TestDummyImageConfigHeight:

    def test__check_config_missing_value(self) -> None:
        # arrange
        config_in = _DUMMYIMAGE_RIGHT_CONFIG.copy()
        del config_in['height']
        # act & assert
        with pytest.raises(KeyError):
            DummyImage.check_config(config_in)

    @pytest.mark.parametrize(
        'wrong_type',
        [None, True, '', [], (), {}, object()],
        ids=type
    )
    def test__check_config_wrong_type(self, wrong_type: Any) -> None:
        # arrange
        config_in = _DUMMYIMAGE_RIGHT_CONFIG.copy()
        config_in['height'] = wrong_type
        # assert
        with pytest.raises(TypeError):
            DummyImage.check_config(config_in)

    @pytest.mark.parametrize(
        'wrong_value',
        [0, -1],
        ids=['zero', 'negative']
    )
    def test__check_config_wrong_value(self, wrong_value: int) -> None:
        # arrange
        config_in = _DUMMYIMAGE_RIGHT_CONFIG.copy()
        config_in['height'] = wrong_value
        # assert
        with pytest.raises(ValueError):
            DummyImage.check_config(config_in)


class TestDummyImageCrawl:

    def test_crawl(self) -> None:
        # arrange
        crawler = DummyImage(**_DUMMYIMAGE_RIGHT_CONFIG)
        # act
        images_crawled = crawler._crawl()
        # assert
        assert len(images_crawled) == crawler._BUNCH, 'crawler did not finish'
        for image_crawled in images_crawled:
            assert image_crawled.is_generic is True, 'this is not generic'


class TestDummyImageDescription:

    def test_description_config(self) -> None:
        # act
        description = DummyImage.info()
        # assert
        assert isinstance(description.config, dict)
        assert _DUMMYIMAGE_RIGHT_CONFIG.keys() == description.config.keys()
