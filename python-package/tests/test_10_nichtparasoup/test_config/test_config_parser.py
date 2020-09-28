from pathlib import Path
from typing import Any

import pytest

from nichtparasoup.config import ConfigFilePath, parse_yaml_file

_TESTDATA = Path(__file__).parent / 'testdata_configs'
_TESTDATA_POSITIVE = _TESTDATA / 'positive'
_TESTDATA_NEGATIVE = _TESTDATA / 'negative'


def type_repr(a: Any) -> str:
    return repr(type(a))


class TestConfigParserCall:

    @pytest.mark.parametrize(
        'file',
        [
            _TESTDATA_POSITIVE / 'minimal.yaml',
            str(_TESTDATA_POSITIVE / 'minimal.yaml'),
        ],
        ids=type_repr
    )
    def test_positive(self, file: ConfigFilePath) -> None:
        # act
        parse_yaml_file(file)

    @pytest.mark.parametrize(
        'file',
        [
            _TESTDATA_NEGATIVE / 'does_not_exists.yaml',
            str(_TESTDATA_NEGATIVE / 'does_not_exists.yaml'),
        ],
        ids=type_repr
    )
    def test_does_not_exist(self, file: ConfigFilePath) -> None:
        # act & assert
        with pytest.raises(FileNotFoundError):
            parse_yaml_file(file)


class TestConfigParserDefaults:

    def test_set_optional_loglevel(self) -> None:
        # arrange
        file = _TESTDATA_POSITIVE / 'logging_level_missing.yaml'
        # act
        config = parse_yaml_file(file)
        # assert
        assert config['logging']['level'] == 'INFO'

    def test_set_optional_weight(self) -> None:
        # arrange
        file = _TESTDATA_POSITIVE / 'crawler_weight_missing.yaml'
        # act
        config = parse_yaml_file(file)
        # assert
        assert len(config["crawlers"]) == 1
        assert config["crawlers"][0]["weight"] == 1.0

    def test_set_optional_exhausted(self) -> None:
        # arrange
        file = _TESTDATA_POSITIVE / 'crawler_exhausted_missing.yaml'
        # act
        config = parse_yaml_file(file)
        # assert
        assert len(config["crawlers"]) == 1
        assert config["crawlers"][0]["restart_at_front_when_exhausted"] is False

    def test_set_optional_config(self) -> None:
        # arrange
        file = _TESTDATA_POSITIVE / 'crawler_config_missing.yaml'
        # act
        config = parse_yaml_file(file)
        # assert
        assert len(config["crawlers"]) == 1
        assert config["crawlers"][0]["config"] == dict()
