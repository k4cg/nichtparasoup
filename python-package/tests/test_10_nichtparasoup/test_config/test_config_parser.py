from os.path import dirname, join as path_join, realpath

from nichtparasoup.config import parse_yaml_file


class TestConfigParserDefaults:
    _TESTDATA = realpath(dirname(__file__))
    _TESTDATA_POSITIVE = path_join(_TESTDATA, 'testdata_configs', 'positive')
    _TESTDATA_NEGATIVE = path_join(_TESTDATA, 'testdata_configs', 'negative')

    def test_set_optional_loglevel(self) -> None:
        # arrange
        file = path_join(self._TESTDATA_POSITIVE, 'logging_level_missing.yaml')
        # act
        config = parse_yaml_file(file)
        # assert
        assert config['logging']['level'] == 'INFO'

    def test_set_optional_weight(self) -> None:
        # arrange
        file = path_join(self._TESTDATA_POSITIVE, 'crawler_weight_missing.yaml')
        # act
        config = parse_yaml_file(file)
        # assert
        assert len(config["crawlers"]) == 1
        assert config["crawlers"][0]["weight"] == 1.0

    def test_set_optional_exhausted(self) -> None:
        # arrange
        file = path_join(self._TESTDATA_POSITIVE, 'crawler_exhausted_missing.yaml')
        # act
        config = parse_yaml_file(file)
        # assert
        assert len(config["crawlers"]) == 1
        assert config["crawlers"][0]["restart_at_front_when_exhausted"] is False

    def test_set_optional_config(self) -> None:
        # arrange
        file = path_join(self._TESTDATA_POSITIVE, 'crawler_config_missing.yaml')
        # act
        config = parse_yaml_file(file)
        # assert
        assert len(config["crawlers"]) == 1
        assert config["crawlers"][0]["config"] == dict()
