from nichtparasoup._internals import _exit
from nichtparasoup.cli.argparse import parser as argparser
from nichtparasoup.config import get_defaults, get_imagecrawler, parse_yaml_file
from nichtparasoup.core import NPCore
from nichtparasoup.core.server import Server as ImageServer
from nichtparasoup.webserver import WebServer

config = None

args = argparser.parse_args()
config_file = args.config_file
if config_file:
    from os.path import join as path_join, realpath, curdir
    config_file = realpath(path_join(curdir, config_file))
    try:
        config = parse_yaml_file(config_file)
    except Exception:
        _exit(status=3, exception=ValueError(
            'invalid config file {!r}\r\n\tSolution: use the built-in validator'.format(config_file)))
del args
del config_file

if not config:
    config = get_defaults()

imageserver = ImageServer(NPCore(), **config['imageserver'])
for crawler_config in config['crawlers']:
    imagecrawler = get_imagecrawler(crawler_config)
    if not imageserver.core.has_imagecrawler(imagecrawler):
        imageserver.core.add_imagecrawler(imagecrawler, crawler_config['weight'])
    del imagecrawler
webserver = WebServer(imageserver, **config['webserver'])

del imageserver
del config

# everything is clean and tidy.

webserver.run()
