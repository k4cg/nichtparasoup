; /* remember for development: lines that include the string "@stripOnBuild" will be stripped on build ;-) */

(function (ss, win)
{ "use strict";

	var addEvent = win.helperFuncs.addEvent;

	var classPrefix = 'state_';
	var classRE = new RegExp("\\s*\\b" + classPrefix +"[01]\\b\\s*");

	var setClass = function (domElem, state)
	{
		domElem.className = classPrefix + (state ? 1 : 0 ) + " " + domElem.className.replace(classRE, "");
	};

	ss.init = function (domElem)
	{
		addEvent(domElem, "change", function ()
		{
			setClass(this.parentNode, this.checked);
		});
		setClass(domElem.parentNode, domElem.checked);
	};

})(window.stateSwitch={}, window);