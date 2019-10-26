__all__ = ["parse_yaml_file"]

from os.path import dirname, join as path_join
from typing import Any, Dict, List, Optional

_schema_file = path_join(dirname(__file__), "schema.yaml")
_schema = None  # type: Optional[Dict[str, Any]]

_defaults_file = path_join(dirname(__file__), "defaults.yaml")
_defaults = None  # type: Optional[Dict[str, Any]]


def parse_yaml_file(file_path: str) -> Optional[Dict[str, Any]]:
    import yamale  # type: ignore
    from nichtparasoup.imagecrawler import get_class as get_crawler
    global _schema
    if not _schema:
        _schema = yamale.make_schema(_schema_file, parser='ruamel')
    data = yamale.make_data(file_path, parser='ruamel')
    config_valid = yamale.validate(_schema, data, strict=True)
    if not config_valid:
        return None
    config = config_valid[0][0]  # type: Dict[str, Any]
    crawlers = config['crawlers']  # type: List[Dict[Any, Any]]
    for crawler in crawlers:
        crawler.setdefault("weight", 1)
        imagecrawler = get_crawler(crawler['type'])
        if not imagecrawler:
            raise ValueError('unknown crawler type: {}'.format(crawler['type']))
        imagecrawler.check_config(crawler['config'])
    return config


def get_defaults() -> Dict[str, Any]:
    from copy import deepcopy
    global _defaults
    if not _defaults:
        _defaults = parse_yaml_file(_defaults_file)
    return deepcopy(_defaults) if _defaults else dict()


def dump_defaults(file_path: str) -> None:
    from shutil import copyfile
    copyfile(_defaults_file, file_path)
