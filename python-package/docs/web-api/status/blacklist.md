# web-api: blacklist status

Information about the blacklist.

Each crawled non-generic image is added into the blacklist right away to sircumvent duplications.
this means the blacklist is constantly growing.  
When the web-api's [`/reset`](../reset.md) is triggered successfully, the blacklist gets flushed.

Call via `/status/blacklist`.

HTTP Status Code: 200.

Example response:

```json
{
  "len": 50,
  "size": 2272
}
```


## `len`

- how many images are currently in the blacklist?
- type: integer


## `size`

- how many bytes is the blacklist large?
- type: integer
