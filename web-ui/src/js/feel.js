
(function (np, window) {
    "use strict";

    var addEvent = window.helperFuncs.addEvent,
        fireEvent = window.helperFuncs.fireEvent;


    var fullscreen = window.helperFuncs.fullscreen;

    /*
     * put everything public/protected in a single-use object called "np"
     * every thing else is private ...
     */

    var document = window.document,
        rootElem = document.documentElement,
        localStorage = window.helperFuncs.storageFactory();

    var bitset = { // BitSet helper functions
        "gen": function (bit) {
            var r = 1 << bit;

            return r;
        },
        "check": function (int, bit) {
            var tar = this.gen(bit),
                r = ((int & tar) == tar);

            return r;
        },
        "set": function (int, bit) {
            var r = int | this.gen(bit);
            return r;
        },
        "unset": function (int, bit) {
            var r = this.check(int, bit) ? int ^ this.gen(bit) : int;
            return r;
        }
    };

    np.constants = { // a bunch of public constants
        stateBS: { // BitSet positions for states
            init: 0, // init play blocker
            manual: 1, // manual play/pause
            boss: 2, // boss mode - not implemented yet
            presented: 3, // tab is presented
            active: 4,  // window is presented
            scroll: 5, // window is scrolled away from top
            gallery: 6 // image is clicked for gallery-view
        }
    };

    np.__bossMode_className = "boss";
    np.__atTop_className = "atTop";
    np.__canFullScreen_className = "canFullScreen";

    np._imageTarget = undefined;

    np._imageFadeInTime = 1000;

    np._images = [];
    np._imagesMax = 50;

    np._state = bitset.set(0, np.constants.stateBS.init);

    np._fetchRequest = new XMLHttpRequest();
    np._serverResetRequest = new XMLHttpRequest();

    np._options = {
        interval: 10,
        playInBackground: false
    };

    np.__intervall = 0;

    np._setTimer = function () {
        if (np.__intervall) {
            window.clearInterval(np.__intervall);

        }
        if (this._state == 0) {
            np.__intervall = window.setInterval(function () {
                np._fetch();
            }, np._options.interval * 1000);

        }
    };

    addEvent(np._fetchRequest, "readystatechange", function () {
        var req = this,
            imageData;
        if (req.readyState == 4 && req.status == 200) {
            try {
                imageData = JSON.parse(req.responseText);
            }
            catch (e) {

            }
            if (imageData) {
                np._pushImage(imageData);
            }
        }
    });

    np.__controllableRequestReadystatechange = function () {
        var req = this;

        if (req.readyState == 4 && req.status == 200) {
            var controlElement = req.controlElement;
            if (controlElement) {
                var response = JSON.parse(req.responseText);
                var timeout = response.timeout * 1000;
                window.setTimeout(function () {
                    controlElement.disabled = false;
                    controlElement.setAttribute("disabled", null);
                    controlElement.removeAttribute("disabled");
                }, timeout);
            }
        }
    };

    addEvent(np._serverResetRequest, "readystatechange", np.__controllableRequestReadystatechange);

    np._fetch = function () {
        var req = this._fetchRequest;
        var r_rs = req.readyState;
        if (r_rs == 4 || r_rs == 0) {
            req.open("GET", "./get", true);
            req.send();
        }
    };

    np._mkImage = function (imageData, onReady) {
        if (!imageData.uri) { return; }

        imageData.genericMarker = "";
        if (imageData.is_generic) {
            // generic images need some extra to trick in-site caching
            imageData.genericMarker = (imageData.uri.indexOf("?") < 0 ? "?" : "&") + "is_generic=" + Math.random();
        }

        var imageDoc = document.createElement("img");
        addEvent(imageDoc, "load", function () {

            /* structure looks like :
              <figure>
                <img src="{uri}" />
                <figcaption data-crawler="{crawler}" data-source="{source}" data-is_generic="{is_generic}">
                  <a href="{uri}">{uri}</a>
                </figcaption>
              </figure>
            */

            var imageBox = document.createElement("figure");
            imageBox.appendChild(imageDoc);

            var srcBox = imageBox.appendChild(document.createElement("figcaption"));

            // not all browsers support dataset property - so use setAttribute function
            srcBox.setAttribute("data-crawler", imageData.crawler.type);
            srcBox.setAttribute("data-source", imageData.source);
            srcBox.setAttribute("data-is_generic", imageData.is_generic);

            var src = this.src;
            if (imageData.is_generic) {
                src = src.replace(imageData.genericMarker, '');
            }

            var srcA = srcBox.appendChild(document.createElement("a"));
            srcA.href = srcA.innerHTML = srcA.innerText = imageData.source || src;

            addEvent(imageDoc, 'click', function () {
                fullscreen.toggle(this);
            });

            if (typeof onReady == "function") {
                onReady(imageBox);
            }
        });
        imageDoc.src = imageData.uri + imageData.genericMarker;
    };

    np._pushImage = function (imageData) {
        if (this._imageTarget) {

            this._mkImage(imageData, function (image) {
                var add = (np._state == 0);
                if (add) {
                    np._images.push(image);
                    np._imageTarget.insertBefore(image, np._imageTarget.firstChild);
                    if (np._images.length > np._imagesMax) {
                        np._popImage();
                    }
                }
            });
        }
    };

    np._popImage = function () {
        var image = this._images.shift();
        if (image && image.parentNode) {
            image.parentNode.removeChild(image);
        }
    };

    np._optionsStorage = {
        target: "np_store",
        save: function () {
            localStorage.setItem(this.target, JSON.stringify(np._options));
        },
        load: function () {
            var lo = localStorage.getItem(this.target);
            if (lo) {
                try {
                    lo = JSON.parse(lo);
                    np._options = lo;
                }
                catch (ex) {
                    // pass
                }
            }
        }
    };

    np.serverReset = function (controlElement) {
        var req = this._serverResetRequest;
        var r_rs = req.readyState;
        if (r_rs == 4 || r_rs == 0) {
            req.controlElement = controlElement;
            controlElement.disabled = true;
            controlElement.setAttribute("disabled", "disabled");
            req.open("GET", "./reset", true);
            req.send();
        }
    };

    np.setInterval = function (interval) {
        this._options.interval = interval;
        this._optionsStorage.save();
        np._setTimer();
    };

    np.getInterval = function () {
        return this._options.interval;
    };

    np.setState = function (which, status) {
        var oldState0 = (this._state == 0);
        this._state = bitset[status ? "set" : "unset"](this._state, which);
        var state0 = (this._state == 0);

        // not sure it this is the right place for this ... but i had to put it somewhere ...
        switch (which) {
            case this.constants.stateBS.scroll:
                if (oldState0 === state0) {
                    // pass
                }
                else if (status) {
                    helperFuncs.className.remove(rootElem, this.__atTop_className);
                }
                else {
                    helperFuncs.className.add(rootElem, this.__atTop_className);
                }
                break;
            case this.constants.stateBS.boss:
                if (status) {
                    helperFuncs.className.add(rootElem, this.__bossMode_className);
                    try {
                        window.blur();
                    }
                    catch (ex) {
                        // pass
                    }
                }
                else {
                    helperFuncs.className.remove(rootElem, this.__bossMode_className);
                }
                break;
        }

        if (state0 != oldState0) {
            // state changed
            this._setTimer();
            if (this._state == 0) {
                this._fetch();
            }
            else {
                this._fetchRequest.abort();
            }
        }
    };

    np.getState = function (which) {
        return bitset.check(this._state, which);
    };

    np.__inited = false;
    np.init = function (imageTargetID, imageFadeInTime) {
        if (this.__inited) {
            return false;
        }

        this.__inited = true;

        this._imageTarget = document.getElementById(imageTargetID);
        this._imageTarget.appendChild(document.createTextNode("")); // to prevent issues with insertBefore()
        this._imageFadeInTime = imageFadeInTime;
        this._optionsStorage.load();

        if (fullscreen.isSupported) {
            helperFuncs.className.add(rootElem, this.__canFullScreen_className);
            fullscreen.onChange(function () {
                var inGallery = !!fullscreen.getFullScreenElement();
                np.setState(np.constants.stateBS.gallery, inGallery);
            });
        }

        addEvent(window, "scroll", function () {
            np.setState(np.constants.stateBS.scroll, this.pageYOffset > 0);
        });
        helperFuncs.className.add(rootElem, this.__atTop_className);
        window.scrollTo(0, 0);
        fireEvent(window, "scroll");

        var c_background = document.getElementById("c_background");
        c_background.checked = this._options.playInBackground;
        fireEvent(c_background, "change");
        addEvent(c_background, "change", function () {
            np._options.playInBackground = this.checked;
            np._optionsStorage.save();
        });

        /* blur and focus event is broken some time - can not reproduce :-( */
        addEvent(window, "blur", function () {
            if (!np._options.playInBackground) {
                np.setState(np.constants.stateBS.active, true);
            }
        });
        addEvent(window, "focus", function () {
            np.setState(np.constants.stateBS.active, false);
        });

        if (document.hidden != undefined) {
            // document. // scroll to top
            addEvent(document, "visibilitychange", function () {
                np.setState(np.constants.stateBS.presented, this.hidden);
            });
            this.setState(this.constants.stateBS.presented, document.hidden);
        }

        var c_speed = document.getElementById("c_speed");
        c_speed.value = this.getInterval();
        addEvent(c_speed, "change", function () {
            np.setInterval(this.value);
        });

        var c_state = document.getElementById("c_state");
        c_state.checked = !this.getState(this.constants.stateBS.manual);
        addEvent(c_state, "change", function () {
            np.setState(np.constants.stateBS.manual, !this.checked);
        });

        var sc_reset = document.getElementById("sc_reset");
        addEvent(sc_reset, "click", function () {
            var controlElement = this;
            if (!controlElement.disabled) {
                np.serverReset(controlElement);
            }
        });
        this.setState(this.constants.stateBS.init, false);
    };

})(window.nichtparasoup = {}, window);
