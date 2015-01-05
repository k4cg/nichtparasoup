; /* remember for development: lines that include the string "@stripOnBuild" will be stripped on build ;-) */


// helper functions for re-use ...

window.helperFuncs = {
	log : function () {} , // in case we forget to strip a log

	addEvent : function (obj, event, fn, capture)
		{ "use strict";
			if ( obj.attachEvent )
			{
				obj.attachEvent('on'+event, fn);
			}
			else if( obj.addEventListener )
			{
				obj.addEventListener(event, fn, capture);
			}
		} ,

	fireEvent : function (obj, event)
	{
		if ( obj.dispatchEvent )
		{
			obj.dispatchEvent(new Event(event));
		}
		else
		{
			obj.fireEvent('on' + event);
		}
	}
};

/* @stripOnBuild */ window.helperFuncs.log = function () {
/* @stripOnBuild */ 	window.console.log.apply(window.console, arguments);
/* @stripOnBuild */ 	var dbg = document.getElementById("dbg");
/* @stripOnBuild */ 	if ( dbg )
/* @stripOnBuild */ 	{
/* @stripOnBuild */ 		dbg.insertBefore(document.createTextNode(
/* @stripOnBuild */ 			(new Date()).toUTCString()
/* @stripOnBuild */ 			+" - "+
/* @stripOnBuild */ 			Array.prototype.join.call(arguments, ' | ') +"\n"), dbg.firstChild);
/* @stripOnBuild */ 	}
/* @stripOnBuild */ };
