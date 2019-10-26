if __name__ == "__main__":
    from nichtparasoup.core import NPCore
    from nichtparasoup.imagecrawler import get_class as get_imagecrawler_class
    from nichtparasoup.webserver import WebServer
    from nichtparasoup.config import get_defaults, parse_yaml_file
    from nichtparasoup.config.argparse import parser as argparser

    config = get_defaults()

    args = argparser.parse_args()
    if args.config_file:
        config_from_file = parse_yaml_file(args.config_file)
        if config_from_file:
            config = config_from_file
    del args

    np_core = NPCore()

    for crawler_config in config['crawlers']:
        imagecrawler_class = get_imagecrawler_class(crawler_config["type"])
        if imagecrawler_class:
            imagecrawler_obj = imagecrawler_class(**crawler_config["config"])
            np_core.add_imagecrawler(imagecrawler_obj, crawler_config['weight'])

    webserver = WebServer(np_core, crawler_upkeep=config['server']['crawler_upkeep'])

    webserver.run(
        config['webserver']['host'], config['webserver']['port'],
        use_debugger=False
    )
