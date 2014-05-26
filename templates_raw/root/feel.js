
// remember for development: lines that include the string "@striponbuild" will be stripped on build ;-)



(function (pub, win, udef)
{	"use strict";
	var conf, vars, func, req;

	conf = { // config
		interval : 1000 ,
		intervalMinSec : 1 ,

		imgsMax : 100 ,

		source : "./get" ,

		cssCNhidden : 'hidden' ,
		cssCNscalein : 'scaleIn'
	};


	pub.setInterval = function ( sec )
	{
		conf.interval = 1000* Math.max(sec, conf.intervalMinSec);
	};


	vars = { // private variables
		halt : false ,
		target : null ,
		imgs : [] ,
		req : false
	};

	pub.halt = function ()
	{
		vars.halt = true;
		req.abort();
		return false;
	};

	pub['continue'] = function ()
	{
		vars.halt = false;
		func.fetch();
		return true;
	};

	pub.toggle = function ()
	{
		return pub[ vars.halt ? 'continue' : 'halt' ]();
	};




	func = { // private functions
		imgOnload : function () {
			this.className = conf.cssCNscalein;
		} ,

		add : function (url) {
			if ( ! url ) { return; }

			var imgE, imgR
			  , target = vars.target, imgs = vars.imgs, imgsMax = conf.imgsMax;

			var img = document.createElement('img');
			img.className = conf.cssCNhidden;
			img.onload = func.imgOnload;
			img.src = url;


			if (target.firstChild) {
				imgE = target.insertBefore(img, target.firstChild);
			}
			else {
				imgE = target.appendChild(img);
			}

			imgs.unshift(imgE);

			while ( imgs.length > imgsMax )
			{
				imgR = imgs.pop();
				imgR.parentNode.removeChild(imgR);
			}
		} ,

		fetch : function fetch ()
		{
			if ( vars.req ) { return false; }
			vars.req = true;

			req.open("GET", conf.source, false);
			req.send(null);
		}
	};


	req = new XMLHttpRequest();
	req.onreadystatechange = function()
	{
		if( this.readyState === 4 )
		{
			vars.req = false;

			var ok = ( this.status === 200 );
			ok |= !this.status; // @striponbuild - offline mode will have no status - so this is only avalable in dev mode

			if ( ok )
			{
				func.add(this.responseText);
			}

			if ( ! vars.halt )
			{
				win.setTimeout(func.fetch, conf.interval);
			}
		}
	};

	pub.init = function (targetId)
	{
		vars.target = document.getElementById(targetId);
		func.fetch();
	};

})(iw={}, this);
