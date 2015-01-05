; /* remember for development: lines that include the string "@stripOnBuild" will be stripped on build ;-) */


// helper functions for reuse ...

window.helperFuncs = {
	log : function () {} , // in case we forget to strip a log

	addEvent : function (obj, event, fn)
		{ "use strict";
			if ( obj.attachEvent )
			{
				obj.attachEvent('on'+event, fn);
			}
			else if( obj.addEventListener )
			{
				obj.addEventListener(event, fn, true);
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
