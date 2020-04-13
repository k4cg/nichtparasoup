__all__ = ['create_parser', 'run_command']

from argparse import ArgumentParser
from sys import exit as sys_exit
from typing import Optional, Type

from nichtparasoup._internals import _LINEBREAK, _message, _message_exception, _type_module_name_str
from nichtparasoup.commands._internal import _imagecrawler_completer
from nichtparasoup.imagecrawler import BaseImageCrawler, get_imagecrawlers


def create_parser(parser: Optional[ArgumentParser] = None) -> ArgumentParser:
    parser = parser or ArgumentParser()
    parser.description = 'Describe an imagecrawler.'
    parser.add_argument(
        '--debug',
        help='debug',
        action='store_true', dest='debug',
    )
    crawler_name = parser.add_argument(
        help='crawler name',
        metavar='<crawler_name>',
        action='store', dest='crawler_name', type=str,
    )
    crawler_name.completer = _imagecrawler_completer  # type: ignore
    return parser


def run_command(crawler_name: str, *, debug: bool) -> int:  # pragma: no cover
    imagecrawler_class = get_imagecrawlers().get_class(crawler_name)
    if imagecrawler_class:
        _print_imagecrawler_info(imagecrawler_class, debug=debug)
        return 0
    _message_exception(ValueError('unknown ImageCrawler {!r}'.format(crawler_name)))
    return 1


def _print_imagecrawler_info(imagecrawler_class: Type[BaseImageCrawler], *, debug: bool) -> None:
    bull = ' * '
    imagecrawler_info = imagecrawler_class.info()
    _message(imagecrawler_info.description)
    _message('')
    if imagecrawler_info.long_description:
        _message(imagecrawler_info.long_description)
        _message('')
    if imagecrawler_info.config:
        _message('CONFIG')
        mlen = max(len(k) for k in imagecrawler_info.config.keys())
        _message(_LINEBREAK.join(
            bull + '{key:{mlen}}: {desc}'.format(mlen=mlen, key=key, desc=desc)
            for key, desc
            in imagecrawler_info.config.items()
        ))
        _message('')
    if debug:
        _message(_LINEBREAK.join([
            'DEBUG INFO',
            bull + 'Icon : {}'.format(imagecrawler_info.icon_url),
            bull + 'Class: {}'.format(_type_module_name_str(imagecrawler_class)),
        ]))
        _message('')


if __name__ == '__main__':
    options = create_parser().parse_args()
    sys_exit(run_command(**options.__dict__))
