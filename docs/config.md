# config

_nichtparasoup_ uses configs in [YAML](https://yaml.org/) file format.
Supported are YAML v1.0 to v1.2.

for a quick start run `nichtparasoup config --dump`.  
to have your config checked, run `nichtparasoup cinfig --check`.

this document explains all the options and what it you need to know to write your own config.

here is a simple example config:

```yaml
webserver:
  hostname: "0.0.0.0"
  port: 5000

imageserver:
  crawler_upkeep: 30

crawlers:
  - type: "Reddit"
    weight: 3
    config:
      subreddit: 'EarthPorn'
  - type: "Picsum"
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

- hostname the web server recognizes
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
  or read the [docs](imagecrawlers)
- type: list

### `type` 

- name of the crawler
- for a list of available types see the commandline help: `nichtparasoup info --imagecrawler-list`  
- type: string

### `weight`

- probability to be chosen randomly
- type: integer or float
- constraint: > 0
- optional
- default: 1

### `config`

- the crawler's own config
- for description of a crawler and how to configure, see commandline help `nichtparasoup info --imagecrawler-desc`  
  or read the [docs](imagecrawlers)
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
