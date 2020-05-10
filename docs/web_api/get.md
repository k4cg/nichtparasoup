# web-api: get

will pop a random image from the ImageServer.

call via `/get`.

example response:

```json
{
  "uri": "https://i.redd.it/wybru584upx31.jpg",
  "is_generic": false,
  "source": "https://www.reddit.com/r/EarthPorn/comments/du0tmw/straight_out_of_a_fairytale_watkins_glen_new_york/",
  "more": {},
  "crawler": {
    "id": 140647222227296, 
    "type": "nichtparasoup.imagecrawlers.reddit:Reddit"
  }
}
```


## `uri`

- thr URI of an image
- type: string


## `is_generic`

- whether the image URI is generic or not
- type: boolean


## `source`

- the image's source
- type: null or string


## `more`

- additional relevant information the crawler found 
- type: object


## `crawler`

- information about the ImageCrawler that found this image
- type: object 


### `id`

- the ImageCrawler's id - see also [crawlers status](status_crawlers.md)
- type: integer


### `type`

- the ImageCrawler's type for easy access in the frontend
- type: string
