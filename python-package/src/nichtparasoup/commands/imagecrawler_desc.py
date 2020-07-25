__all__ = ['main', 'cli']

from typing import Optional, Type

from click import Argument, BadParameter, Command, echo

from .._internals import _log
from ..core.imagecrawler import BaseImageCrawler
from ..imagecrawlers import get_imagecrawlers
from ._internals import _cli_option_debug


def main(name: str) -> None:  # pragma: no cover
    imagecrawler_class = get_imagecrawlers().get_class(name)
    if not imagecrawler_class:
        raise BadParameter(f'Unknown imagecrawler {name!r}\n\tSee "imagecrawler list" command for possible values',
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
        mlen = max(map(len, imagecrawler_info.config.keys()))
        echo('\n'.join(
            f'{bull} {key:{mlen}}: {desc}'
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
    try:
        prog_name: Optional[str] = __spec__.name  # type: ignore[name-defined]
    except NameError:
        prog_name = None
    cli.main(prog_name=prog_name)
