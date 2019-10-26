from typing import NoReturn, Optional, TextIO

from nichtparasoup.config import get_defaults, parse_yaml_file
from nichtparasoup.config.argparse import parser as argparser
from nichtparasoup.core import NPCore
from nichtparasoup.imagecrawler import get_class as get_imagecrawler_class
from nichtparasoup.webserver import WebServer


def exit(status: int = 0, message: Optional[str] = None, file: Optional[TextIO] = None) -> NoReturn:
    import sys
    if message:
        if not file:
            file = sys.stderr
        file.write(message)
    sys.exit(status)


config = None

args = argparser.parse_args()
config_file = args.config_file
if config_file:
    try:
        config_from_file = parse_yaml_file(config_file)
    except FileNotFoundError as e:
        exit(status=24, message='ERROR: No such file {}\r\n'.format(e.filename))
    except ValueError:
        exit(status=23,
             message='ERROR: invalid config file {}\r\n'
                     'use the builtin validator to have the file checked\r\n'.format(config_file))
del config_file
del args

if not config:
    config = get_defaults()

np_core = NPCore()

for crawler_config in config['crawlers']:
    imagecrawler_class = get_imagecrawler_class(crawler_config["type"])
    if imagecrawler_class:
        imagecrawler_obj = imagecrawler_class(**crawler_config["config"])
        np_core.add_imagecrawler(imagecrawler_obj, crawler_config['weight'])

webserver = WebServer(np_core, crawler_upkeep=config['server']['crawler_upkeep'])

try:
    webserver.run(
        config['webserver']['host'], config['webserver']['port'],
        use_debugger=False
    )
except PermissionError:
    exit(status=2,
         message='ERROR: cannot start {} on port {}\r\n'.format(
             type(webserver).__name__, config['webserver']['port']))
