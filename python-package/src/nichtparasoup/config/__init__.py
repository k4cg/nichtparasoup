__all__ = ["get_config", "get_defaults", "dump_defaults", "get_imagecrawler", "parse_yaml_file",
           "ImageCrawlerSetupError",
           "DEFAULTS_FILE", "SCHEMA_FILE",
           "Config", "ConfigFilePath"]

from os import PathLike
from pathlib import Path
from shutil import copyfile
from typing import Any, Dict, Optional, Union

from yamale import make_data, make_schema, validate as yamale_validate  # type: ignore

from ..core.imagecrawler import BaseImageCrawler
from ..imagecrawlers import get_imagecrawlers

Config = Dict[str, Any]

ConfigFilePath = Union[str, PathLike]

DEFAULTS_FILE: ConfigFilePath = str((Path(__file__).parent / 'defaults.yaml').resolve(strict=True))
SCHEMA_FILE: str = str((Path(__file__).parent / 'schema.yaml').resolve(strict=True))

_YAML_PARSER = 'ruamel'


class ImageCrawlerSetupError(Exception):

    def __init__(self,
                 ic_name: str, ic_class: type, ic_config: Dict[Any, Any],
                 message: Optional[str] = None) -> None:
        super().__init__()
        self._name = ic_name
        self._class = ic_class
        self._config = ic_config
        self._message = message

    def __str__(self) -> str:  # pragma: no cover
        string = f'Failed setup crawler {self._name!r} of type {self._class!r} with config {self._config!r}.'
        if self._message:
            string += f'\n\t{self._message}'
        return string


def get_imagecrawler(config_crawler: Dict[str, Any]) -> BaseImageCrawler:
    imagecrawler_name = config_crawler['name']
    imagecrawler_class = get_imagecrawlers().get_class(imagecrawler_name)
    if not imagecrawler_class:
        raise ValueError(f'Unknown crawler name {imagecrawler_name!r}')
    imagecrawler_config = config_crawler['config']
    try:
        imagecrawler = imagecrawler_class(**imagecrawler_config)
    except Exception as ex:
        raise ImageCrawlerSetupError(imagecrawler_name, imagecrawler_class, imagecrawler_config, str(ex)) from ex
    else:
        imagecrawler._np_name = imagecrawler_name
        return imagecrawler


def parse_yaml_file(file_path: ConfigFilePath) -> Config:
    _data = make_data(Path(file_path).resolve(strict=True), parser=_YAML_PARSER)
    _schema = make_schema(SCHEMA_FILE, parser=_YAML_PARSER)
    yamale_validate(_schema, _data, strict=True)
    config: Config = _data[0][0]
    config.setdefault('logging', {})
    config['logging'].setdefault('level', 'INFO')
    for config_crawler in config['crawlers']:
        config_crawler.setdefault("weight", 1.0)
        config_crawler.setdefault('restart_at_front_when_exhausted', False)
        config_crawler.setdefault('config', {})
    return config


def dump_defaults(file_path: ConfigFilePath) -> None:  # pragma: no cover
    copyfile(DEFAULTS_FILE, str(file_path))


def get_defaults() -> Config:  # pragma: no cover
    return parse_yaml_file(DEFAULTS_FILE)


def get_config(config_file: Optional[ConfigFilePath] = None) -> Config:
    if not config_file:
        return get_defaults()
    try:
        return parse_yaml_file(config_file)
    except BaseException as ex:
        raise ValueError(f'invalid config file {config_file!r}: {ex}') from ex
