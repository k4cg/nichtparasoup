__all__ = ["get_config", "get_defaults", "dump_defaults", "get_imagecrawler", "parse_yaml_file",
           "ImageCrawlerSetupError"]

from os.path import dirname, join as path_join, realpath
from typing import Any, Dict, Optional

from nichtparasoup.core.imagecrawler import BaseImageCrawler

_SCHEMA_FILE = realpath(path_join(dirname(__file__), "schema.yaml"))
_schema = None  # type: Optional[Any]

_DEFAULTS_FILE = realpath(path_join(dirname(__file__), "defaults.yaml"))
_defaults = None  # type: Optional[Dict[str, Any]]


class ImageCrawlerSetupError(Exception):

    def __init__(self, ic_name: str, ic_class: type, ic_config: Dict[Any, Any]) -> None:  # pragma: no cover
        self._name = ic_name
        self._class = ic_class
        self._config = ic_config

    def __str__(self) -> str:  # pragma: no cover
        return 'Failed setup crawler {!r} of type {!r} with config {!r}'.format(self._name, self._class, self._config)


def get_imagecrawler(config_crawler: Dict[str, Any]) -> BaseImageCrawler:
    from nichtparasoup.imagecrawler import get_imagecrawlers
    imagecrawler_name = config_crawler['name']
    imagecrawler_class = get_imagecrawlers().get_class(imagecrawler_name)
    if not imagecrawler_class:
        raise ValueError('unknown crawler name {!r}'.format(imagecrawler_name))
    imagecrawler_config = config_crawler['config']
    try:
        return imagecrawler_class(**imagecrawler_config)
    except Exception as e:
        raise ImageCrawlerSetupError(imagecrawler_name, imagecrawler_class, imagecrawler_config) from e


def parse_yaml_file(file_path: str) -> Dict[str, Any]:
    import yamale  # type: ignore
    global _schema
    if not _schema:
        _schema = yamale.make_schema(_SCHEMA_FILE, parser='ruamel')
    _data = yamale.make_data(file_path, parser='ruamel')
    yamale.validate(_schema, _data, strict=True)
    config = _data[0][0]  # type: Dict[str, Any]
    config.setdefault('logging', dict())
    config['logging'].setdefault('level', 'INFO')
    for config_crawler in config['crawlers']:
        config_crawler.setdefault("weight", 1)
        config_crawler.setdefault('config', dict())
    return config


def dump_defaults(file_path: str) -> None:
    from shutil import copyfile
    copyfile(_DEFAULTS_FILE, file_path)


def get_defaults() -> Dict[str, Any]:
    global _defaults
    if not _defaults:
        _defaults = parse_yaml_file(_DEFAULTS_FILE)
    from copy import deepcopy
    return deepcopy(_defaults)


def get_config(config_file: Optional[str] = None) -> Dict[str, Any]:
    if not config_file:
        return get_defaults()
    try:
        return parse_yaml_file(config_file)
    except Exception as e:
        raise ValueError('invalid config file {!r}'.format(config_file)) from e
