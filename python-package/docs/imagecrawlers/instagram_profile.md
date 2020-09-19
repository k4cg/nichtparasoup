# ImageCrawler: InstagramProfile

## Purpose

A Crawler for profile pages of [https://www.instagram.com](https://www.instagram.com).

## Config

The config needs either a `user_name` or a `profile_id`.  
Using `profile_id`  is always the best bet, but it might be harder to fet this info.
So using `user_name` and hope the crawler can fetch the `profile_id` itself might be a first step.

### `user_name`

- the UserName on Instagram
- type: string
- example: "justinbieber"

### `profile_id`

- the ProfileId on Instagram
- type: integer
- example: 6860189

To get this information visit `https://www.instagram.com/<user_name>/?__a=1` and fetch `graphql.user.id`.
