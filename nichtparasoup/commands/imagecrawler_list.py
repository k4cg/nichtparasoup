__all__ = ['main']

from logging import DEBUG as L_DEBUG, ERROR as L_ERROR

from click import command, option

from nichtparasoup._internals import _log, _logging_init, _message, _message_exception
from nichtparasoup.imagecrawler import get_imagecrawlers


@command(name='imagecrawler-list')
@option('--debug', is_flag=True, help='enable debug output.')
def main(*, debug: bool = False) -> None:  # pragma: no cover
    """List available imagecrawlers.
    """
    _logging_init(L_DEBUG if debug else L_ERROR)
    imagecrawlers = get_imagecrawlers()  # may trigger debug output
    _log('debug', '- List of loaded ImageCrawlers -')
    if len(imagecrawlers) > 0:
        _message(sorted(imagecrawlers.names()))
    else:
        _message_exception(Warning('no ImageCrawler found.'))


if __name__ == '__main__':
    main()
