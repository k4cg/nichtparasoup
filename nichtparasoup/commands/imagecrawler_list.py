__all__ = ['main', 'cli']

from click import ClickException, Command, echo

from ..imagecrawler import get_imagecrawlers


def main() -> None:  # pragma: no cover
    imagecrawlers = get_imagecrawlers()  # may trigger debug output
    for imagecrawler in sorted(imagecrawlers.names()):
        echo(imagecrawler)
    else:
        raise ClickException('No ImageCrawler found.')


cli = Command(
    name='imagecrawler-list',
    help='List available imagecrawlers.',
    callback=main,
    params=[
    ]
)

if __name__ == '__main__':
    cli.main()
