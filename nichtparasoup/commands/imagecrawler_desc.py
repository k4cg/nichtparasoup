__all__ = ['main', 'cli']

from typing import Type

from click import Argument, BadParameter, Command, echo

from .._internals import _log
from ..core.imagecrawler import BaseImageCrawler
from ..imagecrawlers import get_imagecrawlers
from ._internals import _cli_option_debug


def main(name: str) -> None:  # pragma: no cover
    imagecrawler_class = get_imagecrawlers().get_class(name)
    if not imagecrawler_class:
        raise BadParameter('Unknown imagecrawler {!r}\n\tSee "list" command for possible values'.format(name),
                           param_hint='name')
    _print_imagecrawler_info(imagecrawler_class)


def _print_imagecrawler_info(imagecrawler_class: Type[BaseImageCrawler]) -> None:   # pragma: no cover
    _log('debug', 'imagecrawler_class = %r', imagecrawler_class)
    bull = ' * '
    imagecrawler_info = imagecrawler_class.info()
    echo(imagecrawler_info.description)
    echo()
    if imagecrawler_info.long_description:
        echo(imagecrawler_info.long_description)
        echo()
    if imagecrawler_info.config:
        echo('CONFIG')
        mlen = max(len(k) for k in imagecrawler_info.config.keys())
        echo('\n'.join(
            bull + '{key:{mlen}}: {desc}'.format(mlen=mlen, key=key, desc=desc)
            for key, desc
            in imagecrawler_info.config.items()
        ))
        echo()


cli = Command(
    name='imagecrawler-desc',
    help='Describe an imagecrawler and its configuration.',
    callback=main,
    params=[
        _cli_option_debug,
        Argument(
            param_decls=['name'],
            type=str  # not a Choice, imagecrawler should be lazy-loaded
        )
    ],
)

if __name__ == '__main__':
    cli.main()
