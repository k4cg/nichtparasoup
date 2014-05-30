#!/usr/bin/env python

### libraries
import os
import re
import random
import json
import logging
import time
import sys
try:
    import urllib.request as urllib2 #py3
except:
    import urllib2 #py2
try:
    import urllib.parse as urlparse # py3
except:
    import urlparse #py2
import templates as tmpl
import threading
from bs4 import BeautifulSoup
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.utils import redirect
from werkzeug.serving import run_simple

## configuration
nps_port = 5000
nps_bindip = "0.0.0.0"
min_cache_imgs = 50
min_cache_imgs_before_refill = 20
user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
logfile = "nichtparasoup.log"
logverbosity = "DEBUG"
soupiobase = "http://soup.io/"
soupiourl = "http://soup.io/everyone?type=image"
imgururl = "https://imgur.com/random"
pr0grammurl = "http://pr0gramm.com/static/"
redditurl = "http://www.reddit.com/r/images"

### init values
headers = { 'User-Agent' : user_agent }
imgmap = []  # will be filled by cache_fill
blacklist = []  # will be filled by cache_get

logger = logging.getLogger('nichtparasoup')
hdlr = logging.FileHandler(logfile)
hdlr.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)


lasturl_soupio = ""  # will be used to remind the last page
redditurl_next = ""  # will be used to remind the next page

### cache functions
# soup.io image provider
def soupio():

    # initialize URI values
    global lasturl_soupio
    url = soupiourl

    # choose last found "more_url" if its not the first run
    if (lasturl_soupio != ""):
        url = lasturl_soupio

    # make request
    req = urllib2.Request(url, None, headers)
    logger.debug("parsing %s" % url)
    try: 
        response = urllib2.urlopen(req,timeout=2)
    except urllib2.URLError as e:
        pass

    # throw everything in BeautifulSoup and get images
    page = BeautifulSoup(response.read())
    containers = page.find_all("div", { "class" : "imagecontainer" })

    # get more content ("scroll down")
    # to know what page to parse next
    url = page.find("div", { "id" : "more_loading" }).find("a")["href"]
    url = urlparse.urljoin(soupiobase, url)

    # update new last URI when we're not on first run
    lasturl_soupio = url

    # for every found imageContainer
    # add img-src to map if not blacklisted
    # ignore min_cache_imgs at this point - always parse whole page
    for con in containers:
        image = con.find('img')['src']
        if not any(image in s for s in blacklist):
            imgmap.append(image)
            blacklist.append(image) # add it to the blacklist to detect duplicates
            logger.debug("added: %s - status: %d" % (image, len(imgmap)))
    return imgmap

# imgur.com image provider
def imgur():
    global imgururl

    for c in range(1,5):
        # make request
        req = urllib2.Request(imgururl, None, headers)
        try:
            response = urllib2.urlopen(req,timeout=2)
        except urllib2.URLError as e:
            pass

        image = BeautifulSoup(response.read()).find("div", { "id" : "image" }).find("img")["src"]

        if not any(image in s for s in blacklist):
          imgmap.append(image)
          blacklist.append(image) # add it to the blacklist to detect duplicates
          logger.debug("added: %s - status: %d" % (image, len(imgmap)))
    return imgmap

def reddit():
    global redditurl_next, redditurl

    if (redditurl_next == ""):
        redditurl_next = redditurl +'.json'

    req = urllib2.Request(redditurl_next, None, headers)
    try:
        response = urllib2.urlopen(req, timeout=2)
        charset = response.info().get_param('charset', 'utf8')
        data = json.loads(response.read().decode(charset))

        redditurl_next = urlparse.urljoin(redditurl_next, "?after="+ data['data']['after'])

        for child in data['data']['children']:
            image = child['data']['url']
            if not any(image in s for s in blacklist):
                imgmap.append(image)
                blacklist.append(image)  # add it to the blacklist to detect duplicates
                logger.debug("added: %s - status: %d" % (image, len(imgmap)))

    except urllib2.URLError as e:
        logger.debug("Url %s broken" % req)
        pass

    return imgmap

# pr0gramm.com image provider
def pr0gramm():
    global pr0grammurl

    req = urllib2.Request(pr0grammurl, None, headers)
    try: 
        response = urllib2.urlopen(req,timeout=2)
    except urllib2.URLError as e:
        pass

    filter = re.compile('^/static/[\d]+')
    pages = BeautifulSoup(response.read()).findAll("a", href=filter)

    for p in pages:
        x =  "http://pr0gramm.com%s" % urllib2.quote(p["href"])
        req = urllib2.Request(x, None, headers)
        response = urllib2.urlopen(req)
        try:
            image = BeautifulSoup(response.read()).find("img")["src"]
            image = "http://pr0gramm.com%s" % (image)
            if not any(image in s for s in blacklist):
                imgmap.append(image)
                blacklist.append(image) # add it to the blacklist to detect duplicates
                logger.debug("added: %s - status: %d" % (image, len(imgmap)))
        except (NameError, TypeError):
            pass

    return imgmap

# wrapper function for cache filling
def cache_fill_loop():

    global imgmap
    sources = [ soupio, imgur, pr0gramm, reddit ]
    while True :

        # fill cache up to min_cache_imgs
        logger.debug(len(imgmap))
        if ( len(imgmap) < min_cache_imgs_before_refill ) :

            logger.debug("in mincache condition")
            while (len(imgmap) < min_cache_imgs):
                imgmap = random.choice(sources)()

        # sleep for non-invasive threading ;)
        time.sleep(1.337)


# return a img url from map
def cache_get():
    url = ""

    # if the cache is not empty, return an object
    # and add id to blacklist.
    if imgmap:
        url = random.choice(imgmap)
        imgmap.remove(url)
        logger.debug("delivered: %s - remaining: %d" % (url, len(imgmap)))

    return url


# print status of cache
def cache_status():
    msg = "images cached: %d (%d bytes) - already seen: %d (%d bytes)" % (len(imgmap),
            sys.getsizeof(imgmap), len(blacklist), sys.getsizeof(blacklist))
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

    try :
        # start the cache filler tread
        cache_fill_thread = threading.Thread(target=cache_fill_loop)
        cache_fill_thread.daemon = True
        cache_fill_thread.start()
    except (KeyboardInterrupt, SystemExit) :
        # end the cache filler thread properly
        min_cache_imgs = -1 # stop cache_fill-inner_loop

    # give the cache_fill some time in advance
    time.sleep(1.337)

    # start webserver after a bit of delay
    run_simple(nps_bindip, nps_port, nichtparasoup(), use_debugger=False)


if __name__ == "__main__":
    main()
