
(function (pub, win)
{	"use strict";

	// define vars and shortcuts up here to get the compressor shorten them
	var vars , func , conf
	  , doc = win.document , math = win.Math ; // shortcuts

	conf = {
		imgMaxWidthPerc  : 0.8 , // disable scaling: set to 0
		imgMaxHeightPerc : 0.8   // disable scaling: set to 0
	};

	vars = {
		styleE : null ,
		baseId : ''
	};

	func = {
		createStyle  : function ()
		{
			var styleE , base;

			if ( ! base )
			{
				base = doc.getElementsByTagName('head')[0];
			}
			if ( ! base )
			{
				base = doc.getElementsByTagName('body')[0];
			}
			if ( ! base )
			{
				base = doc.getElementsByTagName('html')[0];
			}
			if ( ! base )
			{
				base = doc.lastChild;
			}

			styleE = doc.createElement('style');
			styleE.setAttribute('type','text/css');
			styleE = base.appendChild(styleE);

			return styleE;
		} ,

		getAdjustmentStr : function ()
		{
			var style
			  , maxWidth , maxHeight
			  , baseId = vars.baseId
			  , imgStyleStr = '' , imgStyle = {};

			if ( ! baseId ) { return ''; }

			maxWidth  = math.floor(win.innerWidth  * conf.imgMaxWidthPerc);
			maxHeight = math.floor(win.innerHeight * conf.imgMaxHeightPerc);
			if ( maxWidth > 0 )
			{
				imgStyle["max-width"]  = maxWidth +'px';
				imgStyle["width"] = "auto";
			}
			if ( maxHeight > 0 )
			{
				imgStyle["max-height"] = maxHeight +'px';
				imgStyle["height"] = "auto";
			}

			for ( var s in imgStyle )
			{
				imgStyleStr += s +':'+ imgStyle[s] +';'
			}

			style = '#'+ baseId +' img {'+ imgStyleStr +'}';

			return style;
		},

		adjustImgSize : function ()
		{
			var styleE = vars.styleE;
			if ( ! styleE ) { return false; }

			styleE.innerHTML = styleE.innerText = styleE.cssText = func.getAdjustmentStr();

			return true;
		} ,

		addEvent : function (obj, event, fn)
		{
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


	pub.init = function (baseId)
	{
		vars.styleE = func.createStyle();
		vars.baseId = baseId;
		func.adjustImgSize();
		func.addEvent(win, 'resize', func.adjustImgSize);
	};


})(iwl={}, this);
