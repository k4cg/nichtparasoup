#!/usr/bin/env python2

### libraries
import os
import random
import logging
import urllib2
import urlparse
import templates as tmpl
from bs4 import BeautifulSoup
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.utils import redirect
from werkzeug.serving import run_simple

### configuration
nps_port = 5000
nps_bindip = "0.0.0.0"
soupiobase = "http://soup.io/"
soupiourl = "http://soup.io/everyone"
max_cache_imgs = 50
logfile = "nichtparasoup.log"
user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'

### init values
headers = { 'User-Agent' : user_agent }
imgmap = {} # will be filled by cache_fill
blacklist = [] # will be filled by cache_get
lasturl = "" # will be used to remind the last page
logger = logging.getLogger('nichtparasoup')
hdlr = logging.FileHandler(logfile)
hdlr.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)


### cache functions
#fill up the cache with ids and images
def cache_fill():

    # set counters for log
    sc = 0 # site count
    c = 0  # image count

    # initialzie url values
    global lasturl
    url = soupiourl

    # jump to last parsed site in history per cache_fill run
    while (len(imgmap) < max_cache_imgs):

        # choose last found "more_url" if its not the first run
        if (lasturl != "" and sc != 0 ):
            url = lasturl

        # make request
        req = urllib2.Request(url, None, headers)
        logger.debug("parsing %s" % url)
        response = urllib2.urlopen(req)

        # throw everything in beautifulsoup and get images
        page = BeautifulSoup(response.read())
        containers = page.find_all("div", { "class" : "imagecontainer" })

        # get more content ("scroll down")
        # to know what page to parse next
        url = page.find("div", { "id" : "more_loading" }).find("a")["href"]
        url = urlparse.urljoin(soupiobase, url)

        # update new last url when we're not on first run
        if (sc != 0):
            lasturl = url

        # increase site count for log
        sc = sc + 1

        # for every found imagecontainer
        # add img-alt and img-src to map if not blacklisted
        # and if max_cache is not reached yet
        for con in containers:
            if (len(imgmap) < max_cache_imgs):
                if not any(con.find('img')['alt'] in s for s in blacklist):
                    imgmap.update({con.find('img')['alt']: con.find('img')['src'] } )
                    logger.debug("added: %s - status: %d" % (con.find('img')['src'], len(imgmap)))
                    c = c + 1 # increase image counter for log

    logger.info("added %d new images to cache by parsing %d pages" % (c, sc) )

# return a img url
def cache_get():

    # if the cache is not empty, return an object
    # and add id to blacklist. otherwise start refilling the cache
    if imgmap:
        a = random.choice(imgmap.keys())
        url = imgmap.pop(a)
        blacklist.append(a) # add it to the blacklist to detect duplicates
        logger.debug("delivered: %s - remaining: %d" % (url, len(imgmap)))
        return url
    else:
        cache_fill()
        msg = "refilling cache - remaining: %d - already seen: %d" % (len(imgmap),len(blacklist))
        logger.warning(msg)
        return msg

# print status of cache
def cache_status():
    msg = "images cached: %d - already seen: %d" % (len(imgmap), len(blacklist))
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
        except HTTPException, e:
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
# on startup, fill the cache and get up the webserver
def main():
    cache_fill()
    run_simple(nps_bindip, nps_port, nichtparasoup(), use_debugger=False, use_reloader=True)

if __name__ == "__main__":
    main()
