
// helper functions for re-use ...
window.helperFuncs = {

    noop: function () { }, // no operation

    addEvent: function (obj, event, fn, capture) {
        "use strict";
        if (!obj) { return; }
        if (obj.attachEvent) {
            obj.attachEvent("on" + event, fn);
        }
        else if (obj.addEventListener) {
            obj.addEventListener(event, fn, capture);
        }
    },

    fireEvent: function (obj, event) {
        "use strict";
        if (!obj) { return; }
        if (obj.dispatchEvent) {
            obj.dispatchEvent(new Event(event));
        }
        else {
            obj.fireEvent("on" + event);
        }
    },

    storageFactory: function () {
        try {
            var ls = window.localStorage;
            var lst = "test";
            ls.setItem(lst, lst);
            if (lst != ls.getItem(lst)) { throw "ls.getItem"; }
            ls.removeItem(lst);
            return ls;
        }
        catch (e) {
            return {
                // temp storage to emulate local storage in dev mode
                // only needed functions are implemented
                __store: {},
                setItem: function (k, v) { this.__store[k] = v; },
                getItem: function (k) { return this.__store[k]; },
                removeItem: function (k) { delete (this.__store[k]); }
            };
        }
    },

    className: {
        add: function (elem, className) {
            elem.className += " " + className;
        },
        remove: function (elem, className) {
            elem.className = elem.className.replace(new RegExp("\\s*\\b" + className + "\\b", "g"), "");
        }
    },

    fullscreen: {
        isSupported: (
            document.fullscreenEnabled ||
            document.msFullScreenEnabled ||
            document.mozFullScreenEnabled ||
            document.webkitFullscreenEnabled
        ),
        getFullScreenElement: function () {
            if (!this.isSupported) {
                return undefined;
            }
            return (
                document.fullscreenElement ||
                document.msFullscreenElement ||
                document.mozFullScreenElement ||
                document.webkitFullscreenElement
            );
        },
        enter: function (elem) {
            if (!this.isSupported) {
                return false;
            }
            if (elem.requestFullscreen) {
                elem.requestFullscreen();
                return true;
            } else if (elem.msRequestFullscreen) {
                elem.msRequestFullscreen();
                return true;
            } else if (elem.mozRequestFullScreen) {
                elem.mozRequestFullScreen();
                return true;
            } else if (elem.webkitRequestFullscreen) {
                elem.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
                return true;
            }
            return false;
        },
        exit: function () {
            if (!this.isSupported) {
                return false;
            }
            if (!this.getFullScreenElement) {
                return false;
            }
            if (document.exitFullscreen) {
                document.exitFullscreen();
                return true;
            } else if (document.msExitFullscreen) {
                document.msExitFullscreen();
                return true;
            } else if (document.mozCancelFullScreen) {
                document.mozCancelFullScreen();
                return true;
            } else if (document.webkitExitFullscreen) {
                document.webkitExitFullscreen();
                return true;
            }
            return false;
        },
        toggle: function (elem) {
            if (elem === this.getFullScreenElement()) {
                return this.exit() ? false : undefined;
            } else {
                return this.enter(elem) ? true : undefined;
            }
        },
        onChange: function (callback) {
            var hf = window.helperFuncs;
            hf.addEvent(document, "fullscreenchange", callback);
            hf.addEvent(document, "mozfullscreenchange", callback);
            hf.addEvent(document, "webkitfullscreenchange", callback);
            hf.addEvent(document, "msfullscreenchange", callback);
        }
    }

};
