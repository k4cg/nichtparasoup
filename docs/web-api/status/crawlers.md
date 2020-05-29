# web-api: crawlers status

call via `/status/crawlers`.

example response:

```json
{
  "140647222227296": {
    "name": "Reddit",
    "weight": 3,
    "type": "nichtparasoup.imagecrawlers.reddit:Reddit",
    "config": {
      "subreddit": "EarthPorn"
    },
    "images": {
      "len": 47,
      "size": 2272
    }
  },
  "140647222227912": {
    "name": "Picsum",
    "weight": 1,
    "type": "nichtparasoup.imagecrawlers.picsum:Picsum",
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


## key: `<id>`

- a crawlers id 


## `name`

- the ImageCrawler's name, just like in the config
- type: string or null


## `weight`

- the probability an random image is used thom this crawler
- type: integer or float

## `type`

- the ImageCrawler's type representation
- format: "path.to.namespace:ClassName"
- type: string

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

- how many bytes takes the image list?
- type: integer
