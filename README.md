# nichtparasoup

_nichtparasoup_ is a hackspaces entertainment system.
It randomly displays images from
[reddit](https://reddit.com).  
Other crawlers are currently removed, but will be back soon.


![logo](https://raw.githubusercontent.com/k4cg/nichtparasoup/master/images/logo.png)


---


At our hackspace [k4cg](https://k4cg.org) we use it since 2 years now.  
It turns out to be a very non-invasive way of entertaining a crowd of nerds 
without having the noise and interruptions of videos or other stuff.

Here is what it looks like in your browser
![screenshot](https://raw.githubusercontent.com/k4cg/nichtparasoup/master/images/screenshot.png)

and even better, on a beamer in your local hackspace!
![hackspace](https://raw.githubusercontent.com/k4cg/nichtparasoup/master/images/hackspace.jpg)


## How it works

Images are crawled from multiple public pre-configured sources.  
No image is actually downloaded, just the URL to images are gathered. Found images are kept in a list, also it is assured that the same URL is never gathered twice.

To display the crawled images, _nichtparasoup_ starts a webserver display a web UI.  
The web UI fetches a random image URL from the _nichtparasoup_ server one by one. In the web UI the images are downloaded from the original source.  
Also the original source is linked and marked by an icon. Just hover or click the icon in the bottom right of each image.

Everytime _nichtparasoup_ serves an image URL it also removes it from its list. This means an image URL is served only once - unless the server was resetted. (This might change in the future)


## Demo

Visit [nicht.parasoup.de/demo/](http://nicht.parasoup.de/demo/) to try it!


## Install, Usage, Config, etc 

see the [docs](https://github.com/k4cg/nichtparasoup/tree/master/docs)


## License

MIT - see the [`LICENSE`](https://github.com/k4cg/nichtparasoup/blob/master/LICENSE) file for details.


## Credits

* see the [`AUTHORS`](https://github.com/k4cg/nichtparasoup/blob/master/AUTHORS) file for a list of essential contributors
* parts of the logo are taken
   from [Smashicons](https://www.flaticon.com/authors/smashicons)
   on [www.flaticon.com](https://www.flaticon.com/)
   are licensed [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/)
