__all__ = ["get_config", "get_defaults", "dump_defaults", "get_imagecrawler", "parse_yaml_file",
           "ImageCrawlerSetupError",
           "DEFAULTS_FILE", "SCHEMA_FILE",
           "Config"]

from os.path import dirname, join, realpath
from shutil import copyfile
from typing import Any, Dict, Optional

from yamale import make_data, make_schema, validate as yamale_validate  # type: ignore

from ..core.imagecrawler import BaseImageCrawler
from ..imagecrawler import get_imagecrawlers

DEFAULTS_FILE = join(dirname(realpath(__file__)), "defaults.yaml")
SCHEMA_FILE = join(dirname(realpath(__file__)), "schema.yaml")


Config = Dict[str, Any]


class ImageCrawlerSetupError(Exception):

    def __init__(self, ic_name: str, ic_class: type, ic_config: Dict[Any, Any]) -> None:  # pragma: no cover
        super().__init__()
        self._name = ic_name
        self._class = ic_class
        self._config = ic_config

    def __str__(self) -> str:  # pragma: no cover
        return 'Failed setup crawler {!r} of type {!r} with config {!r}'.format(self._name, self._class, self._config)


def get_imagecrawler(config_crawler: Dict[str, Any]) -> BaseImageCrawler:
    imagecrawler_name = config_crawler['name']
    imagecrawler_class = get_imagecrawlers().get_class(imagecrawler_name)
    if not imagecrawler_class:
        raise ValueError('Unknown crawler name {!r}'.format(imagecrawler_name))
    imagecrawler_config = config_crawler['config']
    try:
        return imagecrawler_class(**imagecrawler_config)
    except Exception as e:
        raise ImageCrawlerSetupError(imagecrawler_name, imagecrawler_class, imagecrawler_config) from e


def parse_yaml_file(file_path: str) -> Config:
    _data = make_data(file_path, parser='ruamel')
    _schema = make_schema(SCHEMA_FILE, parser='ruamel')
    yamale_validate(_schema, _data, strict=True)
    config = _data[0][0]  # type: Config
    config.setdefault('logging', dict())
    config['logging'].setdefault('level', 'INFO')
    for config_crawler in config['crawlers']:
        config_crawler.setdefault("weight", 1)
        config_crawler.setdefault('config', dict())
    return config


def dump_defaults(file_path: str) -> None:  # pragma: no cover
    copyfile(DEFAULTS_FILE, file_path)


def get_defaults() -> Config:  # pragma: no cover
    return parse_yaml_file(DEFAULTS_FILE)


def get_config(config_file: Optional[str] = None) -> Config:
    if not config_file:
        return get_defaults()
    try:
        return parse_yaml_file(config_file)
    except BaseException as ex:
        raise ValueError('invalid config file {!r}: {}'.format(config_file, ex)) from ex
