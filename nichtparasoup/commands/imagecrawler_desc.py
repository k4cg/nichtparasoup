__all__ = ['main', 'cli']

from typing import Type

from click import Argument, BadParameter, Choice, Command, Option

from nichtparasoup._internals import _LINEBREAK, _message, _type_module_name_str
from nichtparasoup.imagecrawler import BaseImageCrawler, get_imagecrawlers


def main(name: str, *, debug: bool = False) -> None:  # pragma: no cover
    imagecrawler_class = get_imagecrawlers().get_class(name)
    if not imagecrawler_class:
        raise BadParameter(name, param_hint='name')
    _print_imagecrawler_info(imagecrawler_class, debug=debug)


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


cli = Command(
    name='imagecrawler-desc',
    help='Describe an imagecrawler and its configuration.',
    callback=main,
    params=[
        Argument(
            param_decls=['name'],
            metavar='NAME',
            type=Choice(tuple(get_imagecrawlers().names())),
        ),
        Option(
            param_decls=['--debug'],
            help='Enable debug output.',
            is_flag=True,
        ),
    ],
)

if __name__ == '__main__':
    cli.main()  # pylint: disable=no-value-for-parameter
