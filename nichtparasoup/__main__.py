
if __name__ == "__main__":
    from nichtparasoup.core import NPCore
    from nichtparasoup.imagecrawler import get_class as get_imagecrawler_class
    from nichtparasoup.webserver import WebServer
    from nichtparasoup.config import get_defaults, parse_yaml_file
    from nichtparasoup.config.argparse import parser as argparser

    def exit(status, message=None, file=None):
        from sys import exit, stderr
        if message:
            if not file:
                file = stderr
            file.write(message)
        exit(status)


    config = get_defaults()

    args = argparser.parse_args()
    config_file = args.config_file
    if config_file:
        try:
            config = parse_yaml_file(config_file)
        except ValueError as e:
            exit(1, 'ERROR: invalid config file {}.\r\n'
                    'use the builtin linter to have the file checked\r\n'.format(config_file))
    del config_file
    del args

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
    except PermissionError as e:
        exit(2, 'ERROR: cannot start {} on port {}\r\n'.format(
            type(webserver).__name__, config['webserver']['port']))
