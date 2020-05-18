__all__ = ['main', 'cli']

from click import ClickException, Command, echo

from ..imagecrawlers import get_imagecrawlers
from ._internals import _cli_option_debug


def main() -> None:  # pragma: no cover
    imagecrawlers = get_imagecrawlers()  # may trigger debug output
    if len(imagecrawlers) == 0:
        raise ClickException('No ImageCrawler found.')
    for imagecrawler in sorted(imagecrawlers.names()):
        echo(imagecrawler)


cli = Command(
    name='imagecrawler-list',
    help='List available imagecrawlers.',
    callback=main,
    params=[
        _cli_option_debug,
    ]
)

if __name__ == '__main__':
    cli.main()
