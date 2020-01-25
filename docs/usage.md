# usage 

Via commandline, run `python3 -m nichtparasoup`
or just simply `nichtparasoup`.

The switch `-h`/`--help` will display help.

`nichtparasoup` uses the following sub-commands
* `run` - run a server 
* `config` - config related functions
* `info` - get info for several topics


## run server  

`nichtparasoup run`
simply runs a server.

optional parameter: `-c`/`--use-config` `<file>`.
use a won config for the server. If omitted, the default is used. to write your own config, see the sections below.

when you start _nichtparasoup_
1. system will fill up cache by startup
1. system starts up the web-server
1. point your browser to the configured localhost:5000/ or whatever is configured in the config
1. start page will request single images randomly by /get and show it
1. when system's cache is empty, it will be refilled by the crawler automatically
1. you will (hopefully) get new results.

keep in mind: every time you restart _nichtparasoup_, the cache forgets about its previous shown images. So is not persistent.



## config related functions 

_nichtparasoup_ uses YAML config files.
for more details about config see the [config](config.md) documentation.

for an eay handling this sub-command comes into play.

`nichtparasoup config` 

the following switches are available:
* `--check` - validate and probe a YAML config file
* `--dump`  - dump YAML config into a file


### check a config

check if a file is a valid config.
will prompt prompt errors and warnings, if any.

`nichtparasoup config --check <file>`


### dump a config

for a quick start writing your own config, this command will dump the current default config into a file.
you may edit this config to your needs and then - after having it checked - run nichtparasoup using it.

`nichtparasoup config --dump <file>`


## get info for several topics  

this sub-command gives information about several things...

`nichtparasoup info`

the following switches are available:
* `--imagecrawler-list` - list available image crawler types
* `--imagecrawler-desc` - describe an image crawler type and its config
* `--version`           - show installed version number


### list available ImageCrawlers

list available ImageCrawlers

`nichtparasoup info --imagecrawler-list`


### describe ImageCrawler

get info about an ImageCrawler, how to configure it and so on.

`nichtparasoup info --imagecrawler-desc`


### version

display installed version and exit.

`nichtparasoup info --version`
