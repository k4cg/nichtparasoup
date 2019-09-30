#!/usr/bin/env python

### import libraries
from crawler.giphy import Giphy
from crawler.fourchan import Fourchan
from crawler.instagram import Instagram
from crawler.ninegag import NineGag
from crawler.pr0gramm import Pr0gramm
from crawler.soupio import SoupIO
from crawler.reddit import Reddit
from os import path
import math
import random
import logging
import logging.handlers
import time
import threading
import argparse
import json

try:
    from configparser import RawConfigParser  # py3
except ImportError:
    from ConfigParser import RawConfigParser  # py2

try:
    from urllib.parse import quote_plus as url_quote_plus  # py3
except ImportError:
    from urllib import quote_plus as url_quote_plus        # py2

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
                        required=True,
                        help='a file path to the config ini',
                        dest="config_file")
args = arg_parser.parse_args()

# configuration
# init config parser
config = RawConfigParser()

# read defaults
config.read(path.join(_file_path, 'config.defaults.ini'))
try:
    config.read_file(args.config_file)  # py3
except AttributeError:
    config.readfp(args.config_file)     # py2
args.config_file.close()

# get actual config items
nps_port = config.getint("General", "Port")
nps_bindip = config.get("General", "IP")

min_cache_imgs_before_refill = config.getint("Cache", "Images_min_limit")
user_agent = config.get("General", "Useragent")

# crawler logging config
logverbosity = config.get("Logging", "Verbosity")
logger = logging.getLogger("nichtparasoup")

if config.get("Logging", "Destination").lower() == 'syslog':
    hdlr = logging.handlers.SysLogHandler()
else:
    hdlr = logging.FileHandler(config.get("Logging", "File"))
    hdlr.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s %(message)s'))

logger.addHandler(hdlr)
logger.setLevel(logverbosity.upper())

# werkzeug logging config
log = logging.getLogger('werkzeug')
log.setLevel(logging.CRITICAL)

try:
    urlpath = config.get("General", "Urlpath")
except:
    urlpath = ''

factor_separator = "*"
call_flush_timeout = 10  # value in seconds
call_flush_last = time.time() - call_flush_timeout

call_reset_timeout = 10  # value in seconds
call_reset_last = time.time() - call_reset_timeout

Crawler.request_headers({'User-Agent': user_agent})
Crawler.set_logger(logger)

# config the  crawlers


def get_crawlers(configuration, section):
    """
    parse the config section for crawlers
    * does recognize (by name) known and implemented crawlers only
    * a robust config reading and more freedom for users

    :param configuration: RawConfigParser
    :param section: string
    :return: crawler, factors
    """
    crawlers = {}
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
            if crawler_class == SoupIO:
                crawler_config = "everyone"

        crawler_sites_and_factors = [site_stripped for site_stripped in [site.strip() for site in crawler_config.split(",")]  # trim sites
                                     if site_stripped]  # filter stripped list for valid values

        if not crawler_sites_and_factors:
            continue  # skip crawler if no valid sites configured

        crawler_sites = []
        factors[crawler_class_name] = {}

        # Separate Site and Factor
        for factorPair in crawler_sites_and_factors:
            if factor_separator not in factorPair:
                # No Factor configured
                crawler_sites.append(url_quote_plus(factorPair))
                continue

            factorPair_parts = [factorPairPart.strip(
            ) for factorPairPart in factorPair.split(factor_separator)]

            if not factorPair_parts or not len(factorPair_parts) == 2:
                continue

            site = url_quote_plus(factorPair_parts[0])
            factor = float(factorPair_parts[1])

            crawler_sites.append(site)

            if site not in factors[crawler_class_name] and 0 < factor <= 10:
                factors[crawler_class_name][site] = factor

        logger.info("found configured Crawler: %s = %s Factors: %s" % (
            crawler_class_name, repr(crawler_sites), repr(factors[crawler_class_name])))

        if crawler_class == Reddit:
            crawler_uris = {site: "https://www.reddit.com/r/%s" %
                            site for site in crawler_sites}
        elif crawler_class == NineGag:
            crawler_uris = {site: "https://9gag.com/%s" %
                            site for site in crawler_sites}
        elif crawler_class == Pr0gramm:
            crawler_uris = {crawler_sites[0]                            : "https://pr0gramm.com/api/items/get"}
        elif crawler_class == SoupIO:
            crawler_uris = {site: ("http://www.soup.io/%s" if site in ["everyone"]  # public site
                                   else "http://%s.soup.io") % site  # user site
                            for site in crawler_sites}
        elif crawler_class == Instagram:
            crawler_uris = {site: "https://instagram.com/%s" %
                            site for site in crawler_sites}
        elif crawler_class == Fourchan:
            crawler_uris = {site: "https://boards.4chan.org/%s/" %
                            site for site in crawler_sites}
        elif crawler_class == Giphy:
            crawler_uris = {
                site: "https://api.giphy.com/v1/gifs/search?q=%s" % site for site in crawler_sites}

        if crawler_class_name not in crawlers:
            crawlers[crawler_class_name] = {}

        crawlers[crawler_class_name] = {site: crawler_class(
            crawler_uris[site], site) for site in crawler_uris}

    return crawlers, factors


(sources, factors) = get_crawlers(config, "Sites")
if not sources:
    raise Exception("no sources configured")
if factors:
    Crawler.set_factors(factors)


# wrapper function for cache filling
def cache_fill_loop():
    global sources
    while True:  # fill cache up to min_cache_imgs per site

        info = Crawler.info()
        for crawler in sources:
            for site in sources[crawler]:
                key = crawler + "_" + site

                if key not in info["images_per_site"] or info["images_per_site"][key] < min_cache_imgs_before_refill:
                    try:
                        sources[crawler][site].crawl()
                        info = Crawler.info()
                    except Exception as e:
                        logger.error("Error in crawler %s - %s: %s" %
                                     (crawler, site, e))
                        break

        # sleep for non-invasive threading ;)
        time.sleep(1.337)


# return image data from map
def cache_get():
    return Crawler.get_image()

# get status of cache


def cache_status_dict():
    info = Crawler.info()
    return {
        "crawler": Crawler.info(),
        "factors": factors,
        "min_cache_imgs_before_refill": min_cache_imgs_before_refill,
    }

# print status of cache


def cache_status_text():
    status = cache_status_dict()
    info = status['crawler']

    bar_reps = 5
    bar_repr_refill = status['min_cache_imgs_before_refill'] / bar_reps

    msg = "images cached: %d (%d bytes) - already crawled: %d (%d bytes)" % \
          (info["images"], info["images_size"],
           info["blacklist"], info["blacklist_size"])
    logger.info(msg)

    for crawler in sources:
        for site in sources[crawler]:
            key = crawler + "_" + site
            if key in info["images_per_site"]:

                factor = 1
                if crawler in factors and site in factors[crawler]:
                    factor = factors[crawler][site]

                count = info["images_per_site"][key]

                bar = "|"
                for i in range(0, int(math.ceil(count / bar_reps))):
                    if i < bar_repr_refill:
                        bar += "#"
                    else:
                        bar += "*"

                sitestats = ("%15s - %-15s with factor %4.1f: %2d Images " +
                             bar) % (crawler, site, factor, count)
                logger.info(sitestats)
                msg += "\r\n" + sitestats
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


# werkzeug webserver
# class with mapping to cache_* functions above
class NichtParasoup(object):
    # init webserver with routing
    def __init__(self):
        self.url_map = Map([
            Rule(urlpath + '/', endpoint='root'),
            Rule(urlpath + '/status', endpoint='cache_status'),
            Rule(urlpath + '/get', endpoint='cache_get'),
            Rule(urlpath + '/imagelist', endpoint='show_imagelist'),
            Rule(urlpath + '/blacklist', endpoint='show_blacklist'),
            Rule(urlpath + '/flush', endpoint='flush'),
            Rule(urlpath + '/reset', endpoint='reset'),
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
        if request.values.get('t') == 'json':
            return Response(json.dumps(cache_status_dict()), mimetype='application/json')
        return Response(cache_status_text())

    # map function for getting an image url
    def on_cache_get(self, request):
        return Response(json.dumps(cache_get()), mimetype='application/json')

    # map function for showing blacklist
    def on_show_blacklist(self, request):
        return Response(show_blacklist())

    # map function for showing imagelist
    def on_show_imagelist(self, request):
        return Response(show_imagelist())

    # map function for flushing (deleting everything in cache)
    def on_flush(self, request):
        return Response(flush())

    # map function for resetting (deleting everything in cache and blacklist)
    def on_reset(self, request):
        return Response(reset())


# runtime
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
        min_cache_imgs_before_refill - 1

    # give the cache_fill some time in advance
    time.sleep(1.337)

    # start webserver after a bit of delay
    run_simple(nps_bindip, nps_port, NichtParasoup(), use_debugger=False)
