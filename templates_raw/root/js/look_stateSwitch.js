; /* remember for development: lines that include the string "@stripOnBuild" will be stripped on build ;-) */

(function (ss, win)
{ "use strict";

	var addEvent = win.helperFuncs.addEvent;

	var classPrefix = 'state_';

	/* there is currently a bug in the builder that does not handle escaped chars right ... */
	var classRE = new RegExp("\\\\s*\\\\b" + classPrefix +"[01]\\\\b\\\\s*"); // so i have to escape it doubled ..
	var classRE = new RegExp("\\s*\\b" + classPrefix +"[01]\\b\\s*"); // this would be the correct string // @stripOnBuild


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