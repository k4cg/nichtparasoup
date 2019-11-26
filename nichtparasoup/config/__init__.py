__all__ = ["get_config", "get_defaults", "dump_defaults", "get_imagecrawler", "parse_yaml_file"]

from os.path import dirname, join as path_join
from typing import Any, Dict, Optional

from nichtparasoup.core.imagecrawler import BaseImageCrawler

_schema_file = path_join(dirname(__file__), "schema.yaml")
_schema = None  # type: Optional[Any]

_defaults_file = path_join(dirname(__file__), "defaults.yaml")
_defaults = None  # type: Optional[Dict[str, Any]]


def get_imagecrawler(config_crawler: Dict[str, Any]) -> BaseImageCrawler:
    from nichtparasoup.imagecrawler import get_class as get_crawler_class
    imagecrawler_class = get_crawler_class(config_crawler['type'])
    if not imagecrawler_class:
        raise ValueError('unknown crawler type {!r}'.format(config_crawler['type']))
    try:
        imagecrawler_obj = imagecrawler_class(**config_crawler['config'])
    except Exception as e:
        raise Exception('failed setup of {type!r} with config {config!r}'.format(
            type=config_crawler['type'], config=config_crawler['config'])) from e
    return imagecrawler_obj


def parse_yaml_file(file_path: str) -> Dict[str, Any]:
    import yamale  # type: ignore
    global _schema
    if not _schema:
        _schema = yamale.make_schema(_schema_file, parser='ruamel')
    _data = yamale.make_data(file_path, parser='ruamel')
    config = yamale.validate(_schema, _data, strict=True)[0][0]  # type: Dict[str, Any]
    config.setdefault('logging', dict())
    config['logging'].setdefault('level', 'INFO')
    for config_crawler in config['crawlers']:
        config_crawler.setdefault("weight", 1)
        config_crawler.setdefault('config', dict())
    return config


def dump_defaults(file_path: str) -> None:
    from shutil import copyfile
    copyfile(_defaults_file, file_path)


def get_defaults() -> Dict[str, Any]:
    global _defaults
    if not _defaults:
        _defaults = parse_yaml_file(_defaults_file)
    from copy import deepcopy
    return deepcopy(_defaults)


def get_config(config_file: Optional[str] = None) -> Dict[str, Any]:
    if not config_file:
        return get_defaults()
    try:
        return parse_yaml_file(config_file)
    except Exception as e:
        raise ValueError('invalid config file {!r}'.format(config_file)) from e
