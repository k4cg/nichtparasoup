__all__ = ["get_class"]

import pkgutil
from importlib import import_module
from os.path import dirname
from types import ModuleType
from typing import Dict, Optional, Type

from nichtparasoup.core.imagecrawler import BaseImageCrawler

# TODO: write the whole thing testable


def _get_subclasses_from_module(module_name: str, baseclass: type) -> Dict[str, type]:
    subclasses = dict()
    module = import_module('.{}'.format(module_name), __name__)  # type: ModuleType
    if hasattr(module, '__all__'):
        index = module.__all__  # type: ignore
    else:
        index = [attrib for attrib in dir(module) if '_' != attrib[:1]]
    for imported_name in index:
        imported_var = getattr(module, imported_name)
        if issubclass(imported_var, baseclass):
            subclasses[imported_name] = imported_var
    return subclasses


def _get_subclasses_from_package(package_path: str, baseclass: type) -> Dict[str, type]:
    subclasses = dict()  # type: Dict[str, type]
    for (_, module_name, _) in pkgutil.iter_modules([package_path]):
        module_subclasses = _get_subclasses_from_module(module_name, baseclass)
        for (module_subclass_name, module_subclass) in module_subclasses.items():
            if subclasses.get(module_subclass_name):
                raise Exception('duplicate subclass defined: {}'.format(module_subclass_name))
            subclasses[module_subclass_name] = module_subclass
    return subclasses


_imagecrawlers_builtin = None   # type: Optional[Dict[str, type]]


def get_class(class_name: str) -> Optional[Type[BaseImageCrawler]]:
    global _imagecrawlers_builtin
    if not _imagecrawlers_builtin:
        _imagecrawlers_builtin = _get_subclasses_from_package(dirname(__file__), BaseImageCrawler)
    return _imagecrawlers_builtin.get(class_name)
