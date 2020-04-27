__all__ = ['main', 'cli']

from click import Command

from .._internals import _message, _message_exception
from ..imagecrawler import get_imagecrawlers


def main() -> None:  # pragma: no cover
    imagecrawlers = get_imagecrawlers()  # may trigger debug output
    if len(imagecrawlers) > 0:
        _message(sorted(imagecrawlers.names()))
    else:
        _message_exception(Warning('no ImageCrawler found.'))


cli = Command(
    name='imagecrawler-list',
    help='List available imagecrawlers.',
    callback=main,
    params=[
    ]
)

if __name__ == '__main__':
    cli.main()
