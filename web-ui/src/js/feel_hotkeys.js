(function (window) {
    "use strict";

    var addEvent = window.helperFuncs.addEvent,
        fireEvent = window.helperFuncs.fireEvent;

    var cancelBubble = function (event) {
        event.cancelBubble = true;
        if (event.stopPropagation) { event.stopPropagation(); }
        if (event.stopImmediatePropagation) { event.stopImmediatePropagation(); }
        if (event.preventDefault) { event.preventDefault(); }
    };

    var className_forceShow = ' forceShow',
        className_active = ' active';

    addEvent(window, 'load', function () {
        var document = this.document;

        var c_speedE = document.getElementById('c_speed'),
            min = parseInt(c_speedE.getAttribute('min')),
            max = parseInt(c_speedE.getAttribute('max'));

        var c_stateE = document.getElementById('c_state');

        var hotkeysE = document.getElementById('hotkeys'),
            controlsE = document.getElementById('controls');

        addEvent(window, 'keydown', function (event) {
            var np = this.nichtparasoup;
            if (!np) { return; }

            if (!event) { event = window.event; }

            var bubble = true;

            var keyCode = event.keyCode || event.which;
            var plusKey = false;
            switch (keyCode) {
                case 107: // plus : increase speed
                case 61: // = + : plus key on firefox
                case 187: // = +:  plus key on opera/safari/chrome (according to the internet http://www.javascripter.net/faq/keycodes.htm)
                case 171: // seems like this is plus on german keyboard?!
                    plusKey = true;
                case 109: // minus : decrease speed
                case 173: // = - : minus key on firefox
                case 189: // = - : minus key on opera/safari/chrome (according to the internet http://www.javascripter.net/faq/keycodes.htm)
                    c_speedE.blur(); // prevent possible double trigger loops ...
                    cancelBubble(event);
                    var speed = parseInt(c_speedE.value) + (plusKey ? -1 : +1);
                    if (speed < min) { speed = min; }
                    else if (speed > max) { speed = max; }
                    c_speedE.value = speed;
                    fireEvent(c_speedE, 'change');
                    break;
                case 32: // space
                    c_stateE.blur(); // prevent possible double trigger loops ...
                    cancelBubble(event);
                    c_stateE.checked = !c_stateE.checked; // no xor in JS ? boohoo
                    fireEvent(c_stateE, 'change');
                    break;
                case 27: // escape
                    cancelBubble(event);
                    var bossStateConst = np.constants.stateBS.boss;
                    np.setState(bossStateConst, !np.getState(bossStateConst));
                    break;
                case 74: // j
                    cancelBubble(event);
                    np._fetch();
                    np._setTimer();
                    break;
                default:
                    return;
            }

            var hotKeyIndicator = document.querySelector('.hk_' + keyCode);
            if (hotKeyIndicator) {
                hotkeysE.className += className_forceShow;
                controlsE.className += className_forceShow;
                hotKeyIndicator.className += className_active;
                window.setTimeout(function () {
                    hotkeysE.className = hotkeysE.className.replace(className_forceShow, '');
                    controlsE.className = controlsE.className.replace(className_forceShow, '');
                    hotKeyIndicator.className = hotKeyIndicator.className.replace(className_active, '')
                }, 1800);
            }

            return bubble;
        });
    });

})(window);
