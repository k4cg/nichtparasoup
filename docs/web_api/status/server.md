# web-api: server status

call via `/status/server`.

example response:

```json
{
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


## `uptime`

- server uptime in seconds
- type: integer


## `reset`

- type: object


### `count`

- how often was the server reset during it's life time
- type: integer


### `since`

- how many seconds ago was the last reset
- type: integer


## `images`

- type: object


### `served`

- how many images were served via web-api's `/get`
- type: integer


### `crawled`

- how many images were crawled during the servers life time?
- type: integer
