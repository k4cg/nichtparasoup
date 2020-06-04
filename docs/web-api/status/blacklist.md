# web-api: blacklist status

information about the blacklist.

each crawled non-generic image is added into the blacklist right away to sircumvent duplications.
this means the blacklist is constantly growing.  
when the web-api's `/reset` is triggered successfully, the blacklist gets flushed.

call via `/status/blacklist`.

example response:

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
