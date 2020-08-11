
(function (ss, win) {
    "use strict";

    var addEvent = win.helperFuncs.addEvent;

    var classPrefix = " state_";
    var classRE = new RegExp(classPrefix + "[01]", "g");

    var setClass = function (domElem, state) {
        domElem.className = domElem.className.replace(classRE, "") + classPrefix + (state ? 1 : 0);
    };

    ss.init = function (domElem) {
        addEvent(domElem, "change", function () {
            setClass(this.parentNode, this.checked);
        });
        setClass(domElem.parentNode, domElem.checked);
    };

})(window.stateSwitch = {}, window);
