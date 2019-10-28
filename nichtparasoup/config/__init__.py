__all__ = ["parse_yaml_file", "get_defaults", "dump_defaults", "get_imagecrawler"]

from os.path import dirname, join as path_join, realpath
from typing import Any, Dict, Optional

from nichtparasoup.core.imagecrawler import BaseImageCrawler

_schema_file = realpath(path_join(dirname(__file__), "schema.yaml"))
_schema = None  # type: Optional[Any]

_defaults_file = realpath(path_join(dirname(__file__), "defaults.yaml"))
_defaults = None  # type: Optional[Dict[str, Any]]


def get_imagecrawler(config_crawler: Dict[str, Any]) -> BaseImageCrawler:
    from nichtparasoup.imagecrawler import get_class as get_crawler_class
    imagecrawler_class = get_crawler_class(config_crawler['type'])
    if not imagecrawler_class:
        raise ValueError('unknown crawler type {type!r}'.format(type=config_crawler['type']))
    try:
        imagecrawler_obj = imagecrawler_class(**config_crawler['config'])
    except Exception as e:
        raise Exception('{error!r}\r\n\twith config {config!r}'.format(error=e, config=config_crawler['config']))
    return imagecrawler_obj


def parse_yaml_file(file_path: str) -> Dict[str, Any]:
    import yamale  # type: ignore
    global _schema
    if not _schema:
        _schema = yamale.make_schema(_schema_file, parser='ruamel')
    data = yamale.make_data(file_path, parser='ruamel')
    config_valid = yamale.validate(_schema, data, strict=True)
    config = config_valid[0][0]  # type: Dict[str, Any]
    for config_crawler in config['crawlers']:
        config_crawler.setdefault("weight", None)
        if config_crawler.get('config') is None:
            config_crawler["config"] = dict()
    return config


def get_defaults() -> Dict[str, Any]:
    global _defaults
    if not _defaults:
        _defaults = parse_yaml_file(_defaults_file)
    from copy import deepcopy
    return deepcopy(_defaults)


def dump_defaults(file_path: str) -> None:
    from shutil import copyfile
    copyfile(_defaults_file, file_path)
