; /* remember for development: lines that include the string "@stripOnBuild" will be stripped on build ;-) */


/* hot keys coming soon.

idea:
* right(39) := make interval slower
* left(37) := make interval faster
* space(32) := toggle play/pause
* escape(27) := toggle boss mode -> stop all loading, make all content invisible and show some productive instead ;-)


if a hot key is pressed, show a badge or something for notification ....
maybe its enough to just toggle the <header> or something?

hot keys need to be marked in the <footer> or somewhere noticeable ...

 */

(function (window)
{ "use strict";

	var addEvent = window.helperFuncs.addEvent
	  , fireEvent = window.helperFuncs.fireEvent;
	var log = window.helperFuncs.log;

	addEvent(window, 'load', function ()
	{
		var c_speed = document.getElementById('c_speed')
		  , min = parseInt(c_speed.getAttribute('min'))
		  , max = parseInt(c_speed.getAttribute('max'));

		var c_state = document.getElementById('c_state');

		addEvent(window, 'keydown', function (event)
		{
			var np = this.nichtparasoup;
			if ( ! np ) { return; }

			if ( ! event ) { event = window.event; }

			var bubble = true;

			var document = this.document;

			log('keyDown:', event.keyCode); // @stripOnBuild

			var kk = event.keyCode || event.which;
			switch ( kk )
			{
				case 39 : // right : increase speed
				case 37 : // left : decrease speed
					bubble = false;
					var speed = parseInt(c_speed.value) + ( kk == 39 ? +1 : -1 )  ;
					if ( speed < min ) { speed = min; }
					else if ( speed > max ) { speed = max; }
					c_speed.value = speed;
					fireEvent(c_speed, 'change');
					break;
				case 32 : // space
					c_state.blur(); // prevent possible duble trigger loops ...
					bubble = false;
					var manualStateConst = np.constants.stateBS.manual;
					c_state.checked = !c_state.checked; // no xor in JS ? boohoo
					fireEvent(c_state, 'change');
					break;
				case 27 : // escape
					bubble = false;
					var bossStateConst = np.constants.stateBS.boss;
					np.setState(bossStateConst, !np.getState(bossStateConst));
					break;
			}

			if ( ! bubble )
			{
				event.cancelBubble = true;
				if ( event.stopPropagation ) { event.stopPropagation(); }
				if ( event.stopImmediatePropagation ) { event.stopImmediatePropagation(); }
				if ( event.preventDefault ) { event.preventDefault(); }
			}

			return bubble;
		});
	});

})(window);