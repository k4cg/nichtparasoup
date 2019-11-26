# web-api: server status

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


## `version`

- version of the server
- type: string


## `uptime`

- server uptime in seconds
- type: integer


## `reset`

- type: object


### `count`

- who often was the server reset during it's life time
- type: integer


### `since`

- how may seconds ago was the last reset
- type: integer


## `images`

- type: object


### `served`

- how many images were served via web-api's `/get`
- type: integer


### `crawled`

- how many images were crawled during the servers life time?
- type: integer
