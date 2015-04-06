# ROOT LAYOUT dev env 

~ this is a local runnable UI builder environment that needs no web server and no internet connection (just `file://`).
Ideal for development on long train rides ;-)

~ since this development may require XHttpRequests (= AJAX) you want to use a web browser that supports such requests via `file://` - like FireFox - or start a local web server via
`python -m SimpleHTTPServer <port>`.





## how to develop

The file `root.html` is the main UI file for _nichtparasoup_. 
It may include any known HTML, JS and CSS you need.


The UI file(s) will be bundled. For details see the `build.sh`. 
Therefore some specialties are needed to know: 

* the HTML tag `striponbuild` will be removed on build and may be used for debug/develop purposes
* each line of CSS or JS that contains the string `@striponbuild` is stripped on build, so this may be used for development purposes also

attention: 
the `normalize.css` is symlinked. symlinks may not work properly on windows systems.  





## how to test 

The ready made UI will normally do a AJAX request to `./get` which should return the URI of an image.
For testing purposes and local dev, a file `test/get_local` was prepared which will respond a locally stored image. Since this Image will have the same Size every time, there is also a file `test/get_remote` which used to respond a random (resolution/content) image. I guess you know how to handle them.
