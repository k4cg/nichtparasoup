#!/usr/bin/env python

### import libraries
from os import path
import random
import logging
import time
import threading
import argparse

try:
    from configparser import RawConfigParser  # py 3
except ImportError:
    from ConfigParser import RawConfigParser  # py 2

try:
    from urllib.parse import quote_plus as url_quote_plus  # py3
except ImportError:
    from urllib import quote_plus as url_quote_plus  # py2

from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.serving import run_simple

## import templates
import templates as tmpl

## import crawler
from crawler import Crawler

_file_path = path.dirname(path.realpath(__file__))

# argument parser
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-c', '--config-file', metavar='<file>',
                        type=argparse.FileType('r'),
                        default=open(path.join(_file_path, 'config.ini'), 'r'),
                        help='a file path to the config ini',
                        dest="config_file")
args = arg_parser.parse_args()

## configuration
config = RawConfigParser()
config.read(path.join(_file_path, 'config.defaults.ini'))
try:
    config.read_file(args.config_file)  # py3
except AttributeError:
    config.readfp(args.config_file)  # py2
args.config_file.close()

nps_port = config.getint("General", "Port")
nps_bindip = config.get("General", "IP")
min_cache_imgs = config.getint("Cache", "Images")
min_cache_imgs_before_refill = config.getint("Cache", "Images_min_limit")
user_agent = config.get("General", "Useragent")
logverbosity = config.get("Logging", "Verbosity")
logger = logging.getLogger(config.get("Logging", "Log_name"))
hdlr = logging.FileHandler(config.get("Logging", "File"))
hdlr.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(hdlr)
logger.setLevel(logverbosity.upper())

factor_separator = "-"
call_flush_timeout = 10  # value in seconds
call_flush_last = time.time() - call_flush_timeout

call_reset_timeout = 10  # value in seconds
call_reset_last = time.time() - call_reset_timeout

Crawler.request_headers({'User-Agent': user_agent})
Crawler.set_logger(logger)

### config the  crawlers
from crawler.reddit import Reddit
from crawler.soupio import SoupIO
from crawler.pr0gramm import Pr0gramm
from crawler.ninegag import NineGag
from crawler.instagram import Instagram
from crawler.fourchan import Fourchan
from crawler.giphy import Giphy


def get_crawlers(configuration, section):
    """
    parse the config section for crawlers
    * does recognize (by name) known and implemented crawlers only
    * a robust config reading and more freedom for users

    :param configuration: RawConfigParser
    :param section: string
    :return: list
    """
    crawlers = []
    factors = {}

    for crawler_class in Crawler.__subclasses__():
        crawler_class_name = crawler_class.__name__
        if not configuration.has_option(section, crawler_class_name):
            continue  # skip crawler if not configured

        crawler_config = configuration.get(section, crawler_class_name)
        if not crawler_config or crawler_config.lower() == "false":
            continue  # skip crawler if not configured or disabled

        crawler_uris = {}

        # mimic old behaviours for bool values
        if crawler_config.lower() == "true":
            if crawler_class == Pr0gramm:
                crawler_config = "static"
            elif crawler_class == SoupIO:
                crawler_config = "everyone"

        crawler_sites_and_factors = [url_quote_plus(site_stripped) for site_stripped in
                                     [site.strip() for site in crawler_config.split(",")]  # trim sites
                                     if site_stripped]  # filter stripped list for valid values

        if not crawler_sites_and_factors:
            continue  # skip crawler if no valid sites configured

        crawler_sites = []
        factors[crawler_class_name] = {}

        # Separate Site and Factor
        for factorPair in crawler_sites_and_factors:
            if factor_separator not in factorPair:
                # No Factor configured
                crawler_sites.append(factorPair)
                continue

            factorPair_parts = [factorPairPart.strip() for factorPairPart in factorPair.split(factor_separator)]

            if not factorPair_parts or not len(factorPair_parts) == 2:
                continue

            site = factorPair_parts[0]
            factor = float(factorPair_parts[1])

            crawler_sites.append(site)

            if site not in factors[crawler_class_name] and 0 < factor <= 10:
                factors[crawler_class_name][site] = factor

        logger.info("found configured Crawler: %s = %s Factors: %s" % (
            crawler_class_name, repr(crawler_sites), repr(factors[crawler_class_name])))

        if crawler_class == Reddit:
            crawler_uris = {site: "http://www.reddit.com/r/%s" % site for site in crawler_sites}
        elif crawler_class == NineGag:
            crawler_uris = {site: "http://9gag.com/%s" % site for site in crawler_sites}
        elif crawler_class == Pr0gramm:
            crawler_uris = {site: "http://pr0gramm.com/static/%s" % site for site in crawler_sites}
        elif crawler_class == SoupIO:
            crawler_uris = {site: ("http://www.soup.io/%s" if site in ["everyone"]  # public site
                                   else "http://%s.soup.io") % site  # user site
                            for site in crawler_sites}
        elif crawler_class == Instagram:
            crawler_uris = {site: "http://instagram.com/%s" % site for site in crawler_sites}
        elif crawler_class == Fourchan:
            crawler_uris = {site: "http://boards.4chan.org/%s/" % site for site in crawler_sites}
        elif crawler_class == Giphy:
            crawler_uris = {site: "http://api.giphy.com/v1/gifs/search?q=%s" % site for site in crawler_sites}

        crawlers += [crawler_class(crawler_uris[site], site) for site in crawler_uris]

    return crawlers, factors


(sources, factors) = get_crawlers(config, "Sites")
if not sources:
    raise Exception("no sources configured")


# wrapper function for cache filling
def cache_fill_loop():
    global sources
    while True:  # fill cache up to min_cache_imgs
        if Crawler.info()["images"] < min_cache_imgs_before_refill:
            while Crawler.info()["images"] < min_cache_imgs:
                random.choice(sources).crawl()

        # sleep for non-invasive threading ;)
        time.sleep(1.337)


# return a img url from map
def cache_get():
    return Crawler.get_image()


# print status of cache
def cache_status():
    info = Crawler.info()
    msg = "images cached: %d (%d bytes) - already crawled: %d (%d bytes)" % \
          (info["images"], info["images_size"], info["blacklist"], info["blacklist_size"])
    logger.info(msg)
    return msg


# print imagelist
def show_imagelist():
    return "\n".join(Crawler.show_imagelist())


# print blacklist
def show_blacklist():
    return "\n".join(Crawler.show_blacklist())


# flush blacklist
def flush():
    global call_flush_last
    time_since_last_call = time.time() - call_flush_last
    if time_since_last_call >= call_flush_timeout:
        Crawler.flush()
        call_flush_last = time.time()
        time_since_last_call = 0
    return "%i000" % (call_flush_timeout - time_since_last_call)


# reset the crawler
def reset():
    global call_reset_last
    time_since_last_call = time.time() - call_reset_last
    if time_since_last_call >= call_reset_timeout:
        Crawler.reset()
        call_reset_last = time.time()
        time_since_last_call = 0
    return "%i000" % (call_reset_timeout - time_since_last_call)


### werkzeug webserver
# class with mapping to cache_* functions above
class NichtParasoup(object):
    # init webserver with routing
    def __init__(self):
        self.url_map = Map([
            Rule('/', endpoint='root'),
            Rule('/status', endpoint='cache_status'),
            Rule('/get', endpoint='cache_get'),
            Rule('/imagelist', endpoint='show_imagelist'),
            Rule('/blacklist', endpoint='show_blacklist'),
            Rule('/flush', endpoint='flush'),
            Rule('/reset', endpoint='reset'),
        ])

    # proxy call to the wsgi_app
    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    # calculate the request and use the defined map to route
    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, 'on_' + endpoint)(request, **values)
        except HTTPException as e:
            return e

    # the wsgi app itself
    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    # start page with js and scroll
    def on_root(self, request):
        return Response(tmpl.root, mimetype='text/html')

    # map function for print the status
    def on_cache_status(self, request):
        return Response(cache_status())

    # map function for getting an image url
    def on_cache_get(self, request):
        return Response(cache_get())

    # map function for showing blacklist
    def on_show_blacklist(self, request):
        return Response(show_blacklist())

    # map function for showing imagelist
    def on_show_imagelist(self, request):
        return Response(show_imagelist())

    # map function for flushing (deleting everything in cache)
    def on_flush(self, request):
        return Response(flush())

    # map function for resetting (deleting everythign in cache and blacklist)
    def on_reset(self, request):
        return Response(reset())


### runtime
# main function how to run
# on start-up, fill the cache and get up the webserver
if __name__ == "__main__":
    try:
        # start the cache filler tread
        cache_fill_thread = threading.Thread(target=cache_fill_loop)
        cache_fill_thread.daemon = True
        cache_fill_thread.start()
    except (KeyboardInterrupt, SystemExit):
        # end the cache filler thread properly
        min_cache_imgs = -1  # stop cache_fill-inner_loop

    # give the cache_fill some time in advance
    time.sleep(1.337)

    # start webserver after a bit of delay
    run_simple(nps_bindip, nps_port, NichtParasoup(), use_debugger=False)
