__all__ = ["__version__"]

try:
    from nichtparasoup.__version__ import __version__
except ImportError:
    __version__ = 'development'
