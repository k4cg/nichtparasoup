(function (win) {
	"use strict";

	var onload_old = win.onload;

	win.onload = function ()
	{
		if ( onload_old ) { onload_old.call(this); }


		var win = this , doc = win.document
		  , wId = 'wall';


		iw.init(wId);
		iwl.init(wId);

		document.getElementById('interval').onchange();
	};

})(this);