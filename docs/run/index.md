# run _nichtparasoup_

Via commandline, run `python -m nichtparasoup.cli`
or just simply run `nichtparasoup`.

The switch `--help` will display help.

`nichtparasoup` uses the following sub-commands
* `server`       - manage a server 
* `imagecrawler` - manage installed imagecrawlers


## run server  

`nichtparasoup server run`
simply runs a server.

option: `--config <file>`.  
use an own config for the server. If omitted, the default is used. to write your own config, see the sections below.

when you start _nichtparasoup_
1. system will fill up cache by startup
1. system starts up the web-server
1. point your browser to the configured localhost:5000/ or whatever is configured in the config
1. start page will request single images randomly by /get and show it
1. when system's cache is empty, it will be refilled by the crawler automatically
1. you will (hopefully) get new results.

keep in mind:  
every time you restart _nichtparasoup_, the cache forgets about its previous shown images.  
There is no persistence.



## server config related functions 

_nichtparasoup_ uses YAML config files.
for more details about config see the [config](../config/index.md) documentation.

for an eay handling this sub-command comes into play.

`nichtparasoup server config` 

the following subcommands are available:
* `check`          - validate and probe a YAML config file
* `dump-defaults`  - dump YAML config into a file


### check a config

check if a file is a valid config.
will prompt prompt errors and warnings, if any.

`nichtparasoup serer config --check <file>`


### dump a config

for a quick start writing your own config, this command will dump the current default config into a file.
you may edit this config to your needs and then - after having it checked - run nichtparasoup using it.

`nichtparasoup serer config dump-defaults <file>`


## get info for installed imagecrawlers 

this sub-command gives information about several things...

`nichtparasoup imagecrawler`

the following subcommands are available:
* `list` - list installed image crawlers
* `desc` - describe an installed image crawler and its config


### list ImageCrawlers

list installed ImageCrawlers

`nichtparasoup imagecrawler list`


### describe ImageCrawler

get info about an installed ImageCrawler, how to configure it and so on.

`nichtparasoup imagecrawler desc <image-crawler>`



