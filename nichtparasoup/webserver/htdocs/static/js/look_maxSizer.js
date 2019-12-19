
(function (pub, win) {
    "use strict";

    // define vars and shortcuts up here to get the compressor shorten them
    var vars, func, conf,
        doc = win.document, math = win.Math; // shortcuts

    conf = {
        imgMaxWidthPerc: 0.9, // disable scaling: set to 0
        imgMaxHeightPerc: 0.9   // disable scaling: set to 0
    };

    vars = {
        styleE: null,
        cssSelector: ""
    };

    func = {
        createStyle: function () {
            var styleE, base;

            if (!base) {
                base = doc.getElementsByTagName("head")[0];
            }
            if (!base) {
                base = doc.getElementsByTagName("body")[0];
            }
            if (!base) {
                base = doc.getElementsByTagName("html")[0];
            }
            if (!base) {
                base = doc.lastChild;
            }

            styleE = doc.createElement("style");
            styleE.setAttribute("type", "text/css");
            styleE = base.appendChild(styleE);

            return styleE;
        },

        getAdjustmentStr: function () {
            var maxWidth, maxHeight,
                cssSelector = vars.cssSelector,
                cssString = "", style = {};

            if (!cssSelector) { return ""; }

            maxWidth = math.floor(win.innerWidth * conf.imgMaxWidthPerc);
            maxHeight = math.floor(win.innerHeight * conf.imgMaxHeightPerc);


            if (maxWidth > 0) {
                style["max-width"] = maxWidth + "px";
                style["width"] = "auto";
            }
            if (maxHeight > 0) {
                style["max-height"] = maxHeight + "px";
                style["height"] = "auto";
            }

            for (var s in style) {
                cssString += s + ":" + style[s] + ";";
            }

            style = cssSelector + " {" + cssString + "}";

            return style;
        },

        adjustSize: function () {
            var styleE = vars.styleE;
            if (!styleE) { return false; }

            styleE.innerHTML = styleE.innerText = styleE.cssText = func.getAdjustmentStr();

            return true;
        },

        addEvent: window.helperFuncs.addEvent
    };

    pub.init = function (cssSelector) {
        vars.styleE = func.createStyle();
        vars.cssSelector = cssSelector;
        func.adjustSize();
        func.addEvent(win, "resize", func.adjustSize);
    };

})(window.maxSizer = {}, window);
