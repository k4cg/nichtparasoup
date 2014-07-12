#!/usr/bin/env python

### import libraries
import random
import logging
import time
import threading

from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.serving import run_simple


## import templates
import templates as tmpl


## import crawler
from crawler import Crawler


## configuration
nps_port = 5000
nps_bindip = "0.0.0.0"
min_cache_imgs = 150
min_cache_imgs_before_refill = 20
user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'

logfile = "nichtparasoup.log"
logverbosity = "DEBUG"

### init values
logger = logging.getLogger('nichtparasoup')
hdlr = logging.FileHandler(logfile)
hdlr.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

Crawler.headers({'User-Agent': user_agent})
Crawler.set_logger(logger)

### config the  crawlers
from crawler.reddit import Reddit
from crawler.soupio import Soupio
from crawler.pr0gramm import Pr0gramm
from crawler.imgur import Imgur

sources = [Reddit("http://www.reddit.com/r/gifs"),
           Reddit("http://www.reddit.com/r/pics"),
           Reddit("http://www.reddit.com/r/nsfw"),
           Reddit("http://www.reddit.com/r/nsfw_gifs"),
           Reddit("http://www.reddit.com/r/aww"),
           Reddit("http://www.reddit.com/r/aww_gifs"),
           Reddit("http://www.reddit.com/r/reactiongifs"),
           Reddit("http://www.reddit.com/r/wtf"),
           Reddit("http://www.reddit.com/r/FoodPorn"),
           Reddit("http://www.reddit.com/r/cats"),
           Reddit("http://www.reddit.com/r/StarWars"),
           Soupio("http://soup.io/everyone"),
           Pr0gramm("http://pr0gramm.com/static/")]


# wrapper function for cache filling
def cache_fill_loop():
    global sources
    sources = [source for source in sources if isinstance(source, Crawler)]

    while True:  # fill cache up to min_cache_imgs
        if Crawler.info()["images"] < min_cache_imgs_before_refill :
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
    msg = "images cached: %d (%d bytes) - already crawled: %d (%d bytes)" %\
          (info["images"], info["images_size"], info["blacklist"], info["blacklist_size"])
    logger.info(msg)
    return msg


### werkzeug webserver
# class with mapping to cache_* functions above
class nichtparasoup(object):

    # init webserver with routing
    def __init__(self):
        self.url_map = Map([
            Rule('/', endpoint='root'),
            Rule('/status', endpoint='cache_status'),
            Rule('/get', endpoint='cache_get'),
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


### runtime
# main function how to run
# on start-up, fill the cache and get up the webserver
def main():
    try:
        # start the cache filler tread
        cache_fill_thread = threading.Thread(target=cache_fill_loop)
        cache_fill_thread.daemon = True
        cache_fill_thread.start()
    except (KeyboardInterrupt, SystemExit):
        # end the cache filler thread properly
        global min_cache_imgs
        min_cache_imgs = -1 # stop cache_fill-inner_loop

    # give the cache_fill some time in advance
    time.sleep(1.337)

    # start webserver after a bit of delay
    run_simple(nps_bindip, nps_port, nichtparasoup(), use_debugger=False)


if __name__ == "__main__":
    main()
