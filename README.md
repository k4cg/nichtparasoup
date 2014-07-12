# nichtparasoup

nichtparasoup is a hackerspaces home entertainment system. It randomly displays images/gifs from [soup.io](http://soup.io), [pr0gramm](http://pr0gramm.com) and [reddit](http://reddit.com).

at our hackerspace [k4cg](http://k4cg.org) we used [soupcache](https://github.com/exi/soupcache) very often but the project has some issues, so we cannot host ist onsite and decided to write our own.

the idea behind nichtparasoup is to keep it as simple as possible by just requiring 2 python libraries. you should just be able to download, install `werkzeug` and `bs4` and point your browser to the configured port of your machine

<img src="https://github.com/k4cg/nichtparasoup/raw/master/screenshot.png">

# setup

```bash
git clone https://github.com/k4cg/nichtparasoup
cd nichtparasoup
sudo pip install -r requirements.txt
```

configure the (hopefully self explaining) config options at the top of `nichtparasoup.py`

```python
## configuration
nps_port = 5000
nps_bindip = "0.0.0.0"
min_cache_imgs = 50
min_cache_imgs_before_refill = 20
user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
logfile = "nichtparasoup.log"
logverbosity = "DEBUG"
```

after that you can just run

```bash
./nichtparasoup.py &
```

# internals

## behavior

when you start nichtparasoup

* fill up cache by startup (50 imageurls cached by default)
* starts up the webserver
* point your browser to the configured host:port
* startpage will request single image randomly by `/get` and show them
* when cache is empty, it will be refilled by the crawler automatically
* you will (hopefully) get new results.

keep in mind: everytime you restart the python script, the cache forgets about its previous
shown images. So is not persistent.

## cache_fill in threads

once you start up nichtparasoup the crawler will initially fill the cache up to `$min_cache_imgs`. this happens in a separate thread in the background. when your configured `$min_cache_imgs_before_refill` get hit, the crawler starts choosing a new random image provider (see at the top) and refills your cache. the crawler thread wakes up every `1.337` seconds and checks the status of the current imgmap. 

