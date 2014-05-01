# nichtparasoup

nichtparasoup is a project inspired by [github.com/exi/soupcache](https://github.com/exi/soupcache).
at [k4cg](http://k4cg.org) we use this very often. but the project has some issues, so we cannot host it onsite.

the idea behind nichtparasoup is to keep it as simple as possible by just requiring 2 python libraries. you should be able to simply
download and install `werkzeug` and `bs4` and point your browser to the configured port of your machine.

<img src="https://github.com/k4cg/nichtparasoup/raw/master/screenshot.png">

# setup

```bash
git clone https://github.com/k4cg/nichtparasoup
cd nichtparasoup
sudo pip install -r requirements.txt
```

configure the (hopefully self explaining) config options at the top of `nichtparasoup.py`

```python
### configuration
nps_port = 5000
nps_bindip = "0.0.0.0"
soupiobase = "http://soup.io/"
soupiourl = "http://soup.io/everyone?type=image"
min_cache_imgs = 50
min_cache_imgs_before_refill = 10
logfile = "nichtparasoup.log"
user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
cacheFill_sleep = 1.0 # seconds
```

after that you can just run

```bash
./nichtparasoup.py &
```

# internals

## behavior

when you start nichtparasoup

* on startup the cache will be filled (with 50 image urls by default)
* the web server will be started
* point your browser to the configured host:port
* startpage will request single images randomly by `/get` and show them
* when cache is empty, it will be refilled by the crawler automatically
* you will (hopefully) get new results

keep in mind: every time you restart the python script, the cache forgets about its previous
shown images. so is not persistent.

## parsing soup.io

what a typical soup.io image div looks like

    <div class="imagecontainer" style="width:480px; height:611px">
      <img alt="4441 ea4b 480" height="611" src="http://asset-e.soup.io/asset/7115/4441_ea4b_480.jpeg" width="480" />
    </div>

the "more" loading link (or "endless scrolling" mechanism) looks like

    <div id="more_loading" class="endlessnotice">
      <strong>Just a second, loading <a href="/everyone?since=418774878">more posts</a>...</strong>
    </div>

## caveats

basically nichtparasoup.py works like

* request imgage url via `/get`
* when cache is empty cache_fill() gets called and will refill the cache

when the cache refilling happens, the get-request needs some more time (like 3-4 seconds) what can cause
some delay on the image wall. the solution would be to implement the refilling mechanism to be in a separate thread.
but i am not familiar with threadsafe programming at the moment.

.oO(maybe at some point soup.io does not deliver enough content, so we might extent to using other imageboards too)

# testing and check for correctness

A typical use case is that the cache runs for ~4 hours. By a frequence of 1 image per every 2 seconds
means that we need 1800 images per hour, results in 7200 images per thursday evening.

* detect duplicates in "added images" - done
* detect duplicates in "delivered images" - done
* detect duplicates in "urls parsing" - done
* how many sites have to be parsed for filling the max_cache_imgs cache.


# todo

* implement time counter, how long does it takes to fill the cache
* implement clientside javascript for swapping the image in by using `/get`
* implement slider for adjusting image sequence
