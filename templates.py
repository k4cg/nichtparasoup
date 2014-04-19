root = """
<!DOCTYPE HTML>
<html>
<head>
	<title>nichtparasoup</title>
	<script type="application/javascript">
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

	pub.continue = function ()
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

			if ( this.status === 200 ) //
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
	</script>
	<style type="text/css">
html {
	direction: ltr;
	overflow: scroll;
	overflow-x: hidden;
}
html, body {
	color: #ccc;
	background-color: black;
	margin: 0ex 0em;
	padding: 0ex 0em;
}

#header {
	z-index: 99999;
	display: block;
	position: fixed;
	top: 0ex;
	left: 0em;
	right: 0em;
	height: 4ex;
	margin: 0ex 0em 0.5ex;
	padding: 0ex 1em;
	line-height: 4ex;
	border-bottom: 0.5ex solid #111;
	background-color: #111;
	background-color: rgba(23, 23, 23, 0.9);

	text-align: center;

}

#toggle {
	margin: 0ex 5em;
	cursor: pointer;
	display: inline-block;
	width: 5em;
}
#toggle:hover { text-decoration: underline; }

#wall {
	margin-top: 5ex;
	display: block;
}
#wallbreaker {
	clear: both;
	display: none;
}

#wall img {
	margin: 1ex 1ex;
	padding: 0ex 0em;
	border: 1px solid #999;
	display: inline;
	display: inline-block;
	float: left;
}

#wall img.hidden {
	display: none;
}

#wall img.scaleIn {
	animation: scaleIn linear 0.5s;
	-webkit-animation: scaleIn linear 0.5s;
	-moz-animation: scaleIn linear 0.5s;
	-o-animation: scaleIn linear 0.5s;
	-ms-animation: scaleIn linear 0.5s;

	transform-origin: top left;
	-webkit-transform-origin: top left;
	-moz-transform-origin: top left;
	-o-transform-origin: top left;
	-ms-transform-origin: top left;
}
@keyframes scaleIn {
	from { transform: scale(0); }
	to   { transform: scale(1); }
}
@-webkit-keyframes scaleIn {
	from { -webkit-transform: scale(0); }
	to   { -webkit-transform: scale(1); }
}
@-moz-keyframes scaleIn {
	from { -moz-transform: scale(0); }
	to   { -moz-transform: scale(1); }
}
@-o-keyframes scaleIn {
	from { -o-transform: scale(0); }
	to   { -o-transform: scale(1); }
}
@-ms-keyframes scaleIn {
	from { -ms-transform: scale(0); }
	to   { -ms-transform: scale(1); }
}


	</style>
</head>
<body onload="document.getElementById('interval').onchange(); iw.init('wall');">
	<div id="header">
		update
		interval: 1<input type="range" min="1" max="9" step="1" value="5" onchange="iw.setInterval(this.value)" id="interval" />9
		<a onclick="this.innerHTML = ( iw.toggle() ? 'halt' : 'continue' );" id="toggle" >halt</a>
	</div>
	<div id="wall">
		<span id="wallbreaker"></span>
	</div>
	<noscript>!!! enable JavaScript !!!</noscript>
</body>
</html>
"""
