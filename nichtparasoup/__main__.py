from nichtparasoup._internals import _exit
from nichtparasoup.config import get_defaults, parse_yaml_file
from nichtparasoup.config.argparse import parser as argparser
from nichtparasoup.core import NPCore
from nichtparasoup.core.server import Server as ImageServer
from nichtparasoup.imagecrawler import get_class as get_imagecrawler_class
from nichtparasoup.webserver import WebServer

config = None
args = argparser.parse_args()
config_file = args.config_file
if config_file:
    from os.path import join as path_join, realpath, curdir
    config_file = realpath(path_join(curdir, config_file))
    print('Info: using config file: {}'.format(config_file))
    try:
        config = parse_yaml_file(config_file)
    except ValueError:
        _exit(status=2,
              message=['Error: invalid config file',
                       'Solution: use the built-in validator'])
    except Exception as e:
        _exit(status=2, exception=e)
if not config:
    config = get_defaults()

imageserver = ImageServer(NPCore(), **config['imageserver'])

for crawler_config in config['crawlers']:
    imagecrawler_class = get_imagecrawler_class(crawler_config["type"])
    if imagecrawler_class:
        imagecrawler_obj = imagecrawler_class(**crawler_config["config"])
        imageserver.core.add_imagecrawler(imagecrawler_obj, crawler_config['weight'])

webserver = WebServer(imageserver, **config['webserver'])

webserver.run(use_debugger=False)
