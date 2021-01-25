# web-api: reset

Try to trigger a reset on the ImageServer.  

This will flush the ImageServers blacklist and force all ImageCrawlers to start from the beginning.

HTTP Status Code: 202.

call via `/reset`.

example response:

```json
{
  "requested": false,
  "timeout": 3107
}
```

## `requested`

- whether the reset was requested or not. 
- type: boolean

## `timeout`

- amount of seconds to wait until the next reset can be done
- type: integer
