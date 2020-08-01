# config

_nichtparasoup_ uses configs in [YAML](https://yaml.org/) file format.
Supported is YAML v1.0 to v1.2.

for a quick start run `nichtparasoup config --dump`.  
to have your config checked, run `nichtparasoup config --check`.

this document explains all the options and all you need to know to write your own config.

here is a complete example config:

```yaml
webserver:
  hostname: "0.0.0.0"
  port: 5000

imageserver:
  crawler_upkeep: 30

crawlers:
  - name: "Reddit"
    weight: 3
    restart_at_front_when_exhausted: True
    config:
      subreddit: 'EarthPorn'
  - name: "Picsum"
    config:
      width: 300
      height: 600

logging:
  level: 'INFO'
```

## `webserver` 

- WebServer config
- type: map

### `hostname` 

- hostname the web server recognizes. can also be a unix socket
- type: string

### `port` 

- port the webserver uns on
- type: integer
- constraint: 1 <= port <= 65535

## `imageserver`

- ImageServer config
- type: map

### `crawler_upkeep`

- number of images the server must keep at all time
- type: integer
- constraint: >= 10

## `crawlers`

- list of ImageCrawlers to use.
- ATTENTION: crawlers are treated like a unique list. the combination of type and config makes them unique
- for a list of available types see the commandline help `nichtparasoup info --imagecrawler-list`
- for description of a crawler and how to configure, see commandline help `nichtparasoup info --imagecrawler-desc`
  or read the [docs](../imagecrawlers/index.md)
- type: list

### `name` 

- name of the crawler
- for a list of available types see the commandline help: `nichtparasoup info --imagecrawler-list`  
- type: string

### `weight`

- probability to be chosen randomly
- type: integer or float
- constraint: > 0
- optional
- default: 1.0

### `restart_at_front_when_exhausted`

- force the crawler to start at front, when the end of the source was reached.
- type: bool
- optional
- default: False

### `config`

- the crawler's own config
- for description of a crawler and how to configure, see commandline help `nichtparasoup info --imagecrawler-desc`  
  or read the [docs](../imagecrawlers/index.md)
- type: map
- optional

## `logging`

- logging settings
- type: map
- optional

### `level`

- log level settings
- type: enum('CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG')
- optional
- default: 'INFO'
