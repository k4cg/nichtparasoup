
// remember for development: lines that include the string "@striponbuild" will be stripped on build ;-)



(function (pub, win, udef)
{	"use strict";
	var conf, vars, func, req;

	conf = { // config
		interval : 1000 ,
		intervalMinSec : 1 ,

		imgsMax : 100 ,

		source : "./get" ,
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
			var imgsMax = conf.imgsMax
			  , imgs = vars.imgs
			  , target = vars.target
		      , container = func.buildImgContainer(this) , containerE , containerR;

			if ( target.firstChild ) {
				containerE = target.insertBefore(container, target.firstChild);
			}
			else {
				containerE = target.appendChild(container);
			}

			imgs.unshift(containerE);

			while ( imgs.length > imgsMax )
			{
				containerR = imgs.pop();
				containerR.parentNode.removeChild(containerR);
			}
		} ,

		add : function (url) {
			if ( ! url ) { return; }

			var img = document.createElement('img');
			img.onload = func.imgOnload;
			img.src = url;
		} ,

		fetch : function ()
		{
			if ( vars.req ) { return false; }
			vars.req = true;

			try
			{
				req.open("GET", conf.source, false);
				req.send(null);
			}
			catch (e)
			{
				// @todo error handling
			}
		} ,

		parseUri : function (uri)
			{ // source: https://gist.github.com/jlong/2428561
			var parser = document.createElement('a');
			parser.href = uri;

			return {
				  protocol : parser.protocol // => "http:"
				, hostname : parser.hostname // => "example.com"
				, port     : parser.port     // => "3000"
				, pathname : parser.pathname // => "/pathname/"
				, search   : parser.search   // => "?search=test"
				, hash     : parser.hash     // => "#hash"
				, host     : parser.host     // => "example.com:3000"
				};
		} ,

		buildImgContainer : function (img)
		{
			var src = img.src.split('#', 2)
			  , uri = src[0]
			  , crawler = (""+ src[1]).toLowerCase() ;

			/* structure looks like :
				<div class="img">
					<img src="{uri}" />
					<span class="src {crawler}">
						<a href="{uri}">{uri}</a>
					</span>
				</div>
			*/

			var container = document.createElement('div');
			container.className = "img";
			container.appendChild(img);

			var info = container.appendChild(document.createElement('span'));
			info.className = "src "+ crawler;

			var a = info.appendChild(document.createElement('a'));
			a.href = uri;
			a.innerHTML = uri;
			// a.target = "_blank";

			return container;
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



	// for testing : add the add-function to public
	pub.test_add = function (url) { func.add(url) };   // @striponbuild

})(iw={}, this);
