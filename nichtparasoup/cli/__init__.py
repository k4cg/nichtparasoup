__all__ = ['main']

from os.path import dirname
from sys import version_info

from click import group, version_option

import nichtparasoup
# from nichtparasoup.cli.completion import main as completion # @FIXME removed until fixed -- see module itself
from nichtparasoup.commands.imagecrawler_desc import main as imagecrawler_desc
from nichtparasoup.commands.imagecrawler_list import main as imagecrawler_list
from nichtparasoup.commands.server_config_check import main as server_config_check
from nichtparasoup.commands.server_config_dump_defaults import main as server_config_dump_defaults
from nichtparasoup.commands.server_run import main as server_run

VERSION_STRING = '%(version)s from {location} (python {py_version})'.format(
    location=dirname(nichtparasoup.__file__),
    py_version='{}.{}'.format(version_info.major, version_info.minor)
)


@group(name='nichtparasoup')
@version_option(version=nichtparasoup.__version__, message=VERSION_STRING)
def main() -> None:  # pragma: no cover
    """Nichtparasoup
    """


# @FIXME removed until fixed -- see module itself
# main.add_command(completion, name='completion')


@main.group(name='server')
def server() -> None:  # pragma: no cover
    """Manage server.
    """


server.add_command(server_run, name='run')


@server.group(name='config')
def server_config() -> None:  # pragma: no cover
    """Manage server configs.
    """


server_config.add_command(server_config_check, name='check')
server_config.add_command(server_config_dump_defaults, name='dump-defaults')


@main.group(name='imagecrawler')
def imagecrawler() -> None:  # pragma: no cover
    """Manage imagecrawlers.
    """


imagecrawler.add_command(imagecrawler_list, name='list')
imagecrawler.add_command(imagecrawler_desc, name='desc')
