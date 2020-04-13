from argparse import ArgumentTypeError
from typing import Any, Set

from argcomplete import FilesCompleter  # type: ignore

from nichtparasoup.imagecrawler import get_imagecrawlers


def _arg_int_ge_zero(string: str) -> int:
    value = int(string)
    if value < 0:
        raise ArgumentTypeError('{!r} is not a positive integer'.format(string))
    return value


def _arg_float_ge_zero(string: str) -> float:
    value = float(string)
    if value < 0.0:
        raise ArgumentTypeError('{!r} is not a positive float'.format(string))
    return value


_yaml_file_completer = FilesCompleter(allowednames=('yaml', 'yml'), directories=True)


def _imagecrawler_completer(*_: Any, **__: Any) -> Set[str]:  # pragma: no cover
    """ImageCrawler completer.
    see https://kislyuk.github.io/argcomplete/#specifying-completers
    """
    return set(get_imagecrawlers().names())
