# web-api: `/status` 

get several information about the server

call via `/status` or `/status/<what>`.


## server

call via `/status/server`.

example response:

```json
{
  "version": "2.0.0",
  "uptime": 689,
  "reset": {
    "count": 0,
    "since": 689
  },
  "images": {
    "served": 3,
    "crawled": 50
  }
}
```


### `version`

- version of the server
- type: string


### `uptime`

- server uptime in seconds
- type: integer


### `reset`

- type: object


#### `count`

- who often was the server reset during it's life time
- type: integer


#### `since`

- how may seconds ago was the last reset
- type: integer


### `images`

- type: object


#### `served`

- how many images were served via web-api's `/get`
- type: integer


#### `crawled`

- how many images were crawled during the servers life time?
- type: integer


## crawlers

call via `/status/server`.

example response:

```json
{
  "140647222227296": {
    "type": "Reddit",
    "weight": 3,
    "config": {
      "subreddit": "EarthPorn"
    },
    "images": {
      "len": 47,
      "size": 2272
    }
  },
  "140647222227912": {
    "type": "Picsum",
    "weight": 1,
    "config": {
      "width": 300,
      "height": 600
    },
    "images": {
      "len": 30,
      "size": 1248
    }
  }
}
```


### `<id>`

- a crawlers id 


### `type`

- the ImageCrawler's type
- type: string


### `weight`

- the probability an random image is used thom this crawler
- type: integer or float

### `config

- the ImageCrawler's current config
- type: object

### `images`

- information about the images currently held by this crawler since last crawl run.
- type: object


#### `len`

- amount of images
- type: integer


#### `size`

- mow many bytes takes the image list?
- type: integer

## blacklist

information about the blacklist.

each crawled non-generic image is added into the blacklist right away to sircumvent duplications.
this means the blacklist is constantly growing.  
when the web-api's `/reset` is triggered successfully, the blacklist gets flushed.

call via `/status/server`.

example response:

```json
{
  "len": 50,
  "size": 2272
}
```


### `len`

- how many images are currently in the blacklist?
- type: integer


### `size`

- how many bythes is the blacklist large?
- type: integer
