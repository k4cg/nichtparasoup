# web-api: crawlers status

call via `/status/crawlers`.

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


## `<id>`

- a crawlers id 


## `type`

- the ImageCrawler's type
- type: string


## `weight`

- the probability an random image is used thom this crawler
- type: integer or float

## `config

- the ImageCrawler's current config
- type: object

## `images`

- information about the images currently held by this crawler since last crawl run.
- type: object


### `len`

- amount of images
- type: integer


### `size`

- mow many bytes takes the image list?
- type: integer
