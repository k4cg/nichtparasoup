# nichtparasoup

nichtparasoup is a hackerspaces home entertainment system. It randomly
displays images/gifs from [soup.io](http://soup.io),
[pr0gramm](http://pr0gramm.com), [4chan](http://4chan.org),
[9gag](http://9gag.com) and [reddit](http://reddit.com).

at our hackerspace [k4cg](http://k4cg.org) we used
[soupcache](https://github.com/exi/soupcache) very often but the project
has some issues, so we cannot host ist onsite and decided to write our own.

the idea behind nichtparasoup is to keep it as simple as possible by just
requiring 3 python libraries. you should just be able to download, install
`werkzeug`, `configparser` and `bs4` and point your browser to the
configured port of your machine

<img src="https://github.com/k4cg/nichtparasoup/raw/master/screenshot.png">

# setup

```bash
git clone https://github.com/k4cg/nichtparasoup
cd nichtparasoup
sudo pip install -r requirements.txt
```

after that you can just run

```bash
./nichtparasoup.py &
```

# configuration

configuration takes place in `config.ini`. edit the defaults file to your needs. sections are:

### general

specify port, bindaddress and useragent that nichtparasoup uses for visiting the sites on crawler

```
Port: 5000
IP: 0.0.0.0
Useragent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25
```

### cache

`Images` indicates how many images will be loaded on each crawler run
`Images_min_limit` configures at how many images the crawler starts again collecting new images from the sites.

```
Images: 150
Images_min_limit: 20
```

### logging

logging section is mostly selfexplaining

```
Log_name: nichtparasoup
File: nichtparasoup.log
Verbosity: debug
```

### sites

Configuration of your source work like this.

```
; set to false or remove a Crawler, to disable it
SoupIO: everyone
Pr0gramm: static ,new, top
Reddit: nsfw,gifs,pics,nsfw_gifs,aww,aww_gifs,reactiongifs,wtf,FoodPorn,cats,ImGoingToHellForThis,EarthPorn,facepalm,fffffffuuuuuuuuuuuu,oddlysatisfying
NineGag: geeky,wtf,girl,hot,trending
Instagram: cats,animals,pornhub,nerdy_gaming_art,nature,wtf
Fourchan: b,sci
```
For example Reddit: wtf,gifs will end up in `http://reddit.com/r/wtf` and `http://reddit.com/r/gifs` end up
being in the crawler. For 9gag you can add any site that hits the scheme `http://9gag.com/<topic>`.


# contribution

basically, check the repo out and initialize the template bundler

As the template bundler is a seperate repo you have to execute the following command if you want to use it (to create your own templates)

```bash
git submodule update --init --recursive
```

# internals

## commands

You can interact with nichtparasoup in an "api" way very easy.
For example `curl localhost:5000/<command>`. You can insert every command here listed
below.

* `/get` - gets a image url from the list and prints out the url
* `/imagelist` - prints out every image url in the cache
* `/blacklist` - prints out every image url that is blacklisted (e.g. "already seen")
* `/status` - prints amount of images in cache and blacklist and size im memory of these two lists
* `/flush` - will delete everything in cache but not in blacklist
* `/reset` - deletes everything in cache and blacklist

## behavior

when you start nichtparasoup

* fill up cache by startup (150 imageurls cached by default)
* starts up the webserver
* point your browser to the configured `localhost:5000/`
* startpage will request single image randomly by `/get` and show them
* when cache is empty, it will be refilled by the crawler automatically
* you will (hopefully) get new results.

keep in mind: everytime you restart nichtparasoup, the cache forgets about its previous
shown images. So is not persistent.

## cache_fill in threads

once you start up nichtparasoup the crawler will initially fill the cache up
`Images`. this happens in a separate thread in the background. when your
configured `Images_min_limit` get hit, the crawler starts choosing
a new random image provider (see at the top) and refills your cache. the crawler
thread wakes up every `1.337` seconds and checks the status of the current imgmap.

