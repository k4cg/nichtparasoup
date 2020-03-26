__all__ = ['__version__']

from os.path import dirname, join

try:
    with open(join(dirname(__file__), 'VERSION')) as version_file:
        __version__ = version_file.read().strip() or 'UNKNOWN.falsy'
except BaseException:  # pragma: no cover
    __version__ = 'UNKNOWN.read'
