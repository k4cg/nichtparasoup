
// remember: every line that contains a @stripOnBuild will be stripped on build ;-)

(function(np, imageTargetID, window, undefined)
{ "use strict";
	var log = function () {};
	log = function () { window.console.log.apply(window.console, arguments); }; // in case we forget to strip a log // @stripOnBuild
	log('feel started'); // @stripOnBuild




	/*
	 * put everything public/protected in a single-use object called 'np'
	 * every thing else is private ...
	 */

	{ // some helper variables and shortcuts
		var document = window.document
		  , localStorage = window.localStorage
		  ;
	}

	{ // some helper functions
		var bitset = { // BitSet helper functions
			  "gen": function (bit)
				{
					var r =  1 << bit;
					log('BS gen', bit ,'->', r); // @stripOnBuild
					return r;
				}
			, "check": function (int, bit)
				{
					var tar = this.gen(bit)
					  , r = ( (int & tar) == tar );
					log('BS check', int, bit, ' against:', tar, '->', r); // @stripOnBuild
					return r;
				}
			, "set": function (int, bit)
				{
					var r = int | this.gen(bit);
					log('BS set', int, bit, '->', r);
					return r;
				}
			, "unset": function (int, bit)
				{
					var r = this.check(int, bit) ? int ^ this.gen(bit) : int;
					log('BS unset', int, bit, '->', r);
					return r;
				}
			};
	}

	np.constants = { // a bunch of constants
		stateBS : { // bitset positions for states
			manual : 0 ,
			boss : 1 ,
			presented : 2 ,
			scroll : 3
		}
	};

	np._imageTarget = undefined;

	np._images = [];

	np._state = 0;

	np._fetchRequest = new XMLHttpRequest();


	np._options = {
		  interval : 0
		, nsfw : false
		};



	np._fetchRequest.onreadystatechange = function ()
	{

	};

	np._fetch = function ()
	{
		var r_rs = this._fetchReq.readyState;
		if ( r_rs == 4 || r_rs == 0 )
		{
			this._fetchReq.open("GET", this.source, false);
			this._fetchReq.send(null);
		}
	};

	np._pushImage = function (uri)
	{
		if ( this._imageTarget )
		{
			log('addded image');     // @stripOnBuild
			var image = document.createElement('article');
			this._images.push(image);
			this._imageTarget.appendChild(image);
		}
		else                                                                        // @stripOnBuild
		{                                                                           // @stripOnBuild
			log('! image not added', 'no target', this._imageTarget);      // @stripOnBuild
		}                                                                           // @stripOnBuild
	};

	np._popImage = function ()
	{
		var image = this._images.shift();
		if ( image && image.parentNode )
		{
			image.parentNode.removeChild(image);
		}
		log('popped an image ... if there was one ... '); // @stripOnBuild
	};

	np._optionsStorage = {
		  target : "np_store"
		, save : ( localStorage == undefined
			? function () {
					log('no support', ' options save');     // @stripOnBuild
				}
			: function ()
				{
					log('options saved');
					localStorage.setItem(this.target, np._options);
				}
			)
		, load : ( localStorage == undefined
			? function ()
				{
					log('no support', ' options load');     // @stripOnBuild
				}
			: function ()
				{
					var lo = localStorage.getItem(this.target);
					if ( lo )
					{
						log('options loaded'); // @stripOnBuild
						np._options = lo;
					}
					else                                        // @stripOnBuild
					{                                           // @stripOnBuild
						log('options load failed');     // @stripOnBuild
					}                                           // @stripOnBuild
				}
			)
		};

	np.setInterval = function (interval)
	{
		log('set interval', interval); // @stripOnBuild
		this._options.interval = interval;
		this._optionsStorage.save();
	};

	np.setState = function (which, status)
	{
		this._state = bitset[ status ? "set" : "unset" ](this._state, which);
		log("setState", which, status, '->', this._state); // @stripOnBuild
		return this;
	};

	window.addEventListener('load', function ()
	{ // init
		log('init started'); // @stripOnBuild

		np._imageTarget = document.getElementById(imageTargetID);
		log('imageTarget:', np._imageTarget); // @stripOnBuild

		np._optionsStorage.load();

		window.addEventListener('scroll', function ()
		{
			log('scroll detected', 'offset:',window.pageYOffset); // @stripOnBuild
			np.setState(np.constants.stateBS.scroll, window.pageXOffset != 0 );
		});

		// document. // scroll to top
		document.addEventListener('visibilitychange', function ()
		{
			log('visibilitychange detected', 'hidden:', document.hidden); // @stripOnBuild
			np.setState(np.constants.stateBS.presented, document.hidden);
		});

		log('init ended'); // @stripOnBuild
	});







	log('feel done'); // @stripOnBuild
})(window.nichtparasoup={}, 'wall', window);