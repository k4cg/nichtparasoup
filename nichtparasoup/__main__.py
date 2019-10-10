if __name__ == "__main__":
    from nichtparasoup.core import NPCore
    from nichtparasoup.imagecrawler import get_class as get_imagecrawler_class
    from nichtparasoup.webserver import WebServer

    # TODO: write this foo based on some proper settings
    config = dict(
        host='127.0.0.1',
        port=5000,
        imagecrawlers=[
            dict(type="Dummy", weight=0.5, config=dict(image_uri='/images/dummy.png')),
            dict(type="Picsum", weight=1, config=dict(width=800, height=600)),
        ]
    )

    np_core = NPCore()

    for imagecrawler_config in config['imagecrawlers']:  # type: ignore
        imagecrawler_class = get_imagecrawler_class(imagecrawler_config["type"])
        if not imagecrawler_class:
            raise Exception("unknown crawler type: {}".format(imagecrawler_config["type"]))
        imagecrawler_obj = imagecrawler_class(**imagecrawler_config["config"])  # type: ignore
        np_core.add_imagecrawler(imagecrawler_obj, imagecrawler_config['weight'])

    webserver = WebServer(np_core)

    # TODO: cleanup unused foo

    webserver.run(
        config['host'], config['port'],  # type: ignore
        use_debugger=False
    )
