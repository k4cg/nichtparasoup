# usage 

Via commandline, run `python3 -m nichtparasoup`
or just simply `nichtparasoup`.

The switch `-h`/`--help` will display help.

`nichtparasoup` uses the followinf sub-commands
* `run` - run a server 
* `config` - config related functions
* `info` - get info for several topics


## run server  

`nichtparasoup run`
simply runs a server.

optional parameter: `-c`/`--use-config` `<file>`.
use a won config for the server. If omitted, the default is used.

to write your own config, see the sections below.


## config related functions 

`nichtparasoup config` 


### check a config

`nichtparasoup config --check <file>`


### getting stated

`nichtparasoup config --dump <file>`


## get info for several topics  

`nichtparasoup info`


### list available ImageCrawlers

`nichtparasoup info --imagecrawler-list`


### describe ImageCrawler

`nichtparasoup info --imagecrawler-desc`


### version

`nichtparasoup info --version`
