# config

_nichtparasoup_ uses configs in [YAML](https://yaml.org/) file format.
Supported are YAML v1.0 to v1.2.

for a quick start run `nichtparasoup config --dump`.  
to have your config checked, run `nichtparasoup config --check`.

this document explains all the options and what it you need to know to write your own config.

here is a complete example config:

```yaml
webserver:
  hostname: "0.0.0.0"
  port: 5000
  proxy:
    x_for: 0
    x_proto: 0
    x_host: 0
    x_port: 0
    x_prefix: 0

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


## `proxy`

- reverse proxy config - if you don't know what this is, you probably don't need it :-)
- type: map
- optional
- default: null (=disable reverse proxy)


### purpose

> When an application is running behind a proxy server, WSGI may see the request as coming from that server rather than
> the real client. Proxies set various headers to track where the request actually came from.  
> \[The `proxy` settings\] should be configured with the number of proxies that are chained in front of it. Not all proxies set all the
> headers. Since incoming headers can be faked, you must set how many proxies are setting each header so the middleware 
> knows what to trust.

source: [Werkzeug X-Forwarded-For Proxy Fix](https://werkzeug.palletsprojects.com/en/0.16.x/middleware/proxy_fix/)

To disable reverse proxy, just do not configure it - or set all keys to `0`.

### configurable keys

- keys available:
   * `x_for`    – Number of values to trust for X-Forwarded-For.
   * `x_proto`  – Number of values to trust for X-Forwarded-Proto.
   * `x_host`   – Number of values to trust for X-Forwarded-Host.
   * `x_port`   – Number of values to trust for X-Forwarded-Port.
   * `x_prefix` – Number of values to trust for X-Forwarded-Prefix.
- types: integer 
- constraint: >= 0


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
