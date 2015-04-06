; /* remember for development: lines that include the string "@stripOnBuild" will be stripped on build ;-) */

(function(np, window, undefined)
{ "use strict";

	var log = window.helperFuncs.log;
	log('feel started'); // @stripOnBuild



	var addEvent = window.helperFuncs.addEvent
	  , fireEvent = window.helperFuncs.fireEvent
	  ;


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
			//		log('BS gen', bit ,'->', r); // @stripOnBuild
					return r;
				}
			, "check": function (int, bit)
				{
					var tar = this.gen(bit)
					  , r = ( (int & tar) == tar );
			//		log('BS check', int, bit, ' against:', tar, '->', r); // @stripOnBuild
					return r;
				}
			, "set": function (int, bit)
				{
					var r = int | this.gen(bit);
			//		log('BS set', int, bit, '->', r);
					return r;
				}
			, "unset": function (int, bit)
				{
					var r = this.check(int, bit) ? int ^ this.gen(bit) : int;
			//		log('BS unset', int, bit, '->', r);
					return r;
				}
			};
	}

	np.constants = { // a bunch of public constants
		stateBS : { // BitSet positions for states
			init : 0 , // init play blocker
			manual : 1 , // manual play/pause
			boss : 2 , // boss mode - not implemented yet
			presented : 3 , // tab is presented
			active : 4 ,  // window is presented
			scroll : 5 , // window is scrolled away from top
			gallery : 6 // image is clicked for gallery-view
		}
	};

	np.__bossMode_className = ' boss';
	np.__bossMode_className_RE = new RegExp(np.__bossMode_className, 'g');

	np._imageTarget = undefined;

	np._imageFadeInTime = 1000;

	np._images = [];
	np._imagesMax = 50;

	np._state = bitset.set(0, np.constants.stateBS.init);

	np._fetchRequest = new XMLHttpRequest();
	np._serverResetRequest = new XMLHttpRequest();
	np._serverFlushRequest = new XMLHttpRequest();


	np._options = {
		  interval : 10
		, playInBackground : false
		, nsfw : false // not implemented yet
		};

	np.__timeout = 0;

	addEvent(np._fetchRequest, "readystatechange", function ()
	{
		var req = this;
		log("XHR onreadystatechange", req.readyState); // @stripOnBuild
		if ( req.readyState == 4 && req.status == 200 )
		{
			var imageURI = req.responseText;
			if ( imageURI )
			{
				var src = imageURI.split('#', 2)
				  , uri = src[0]
				  , crawler = (""+ src[1]).toLowerCase();
				np._pushImage(uri, crawler, function (added)
				{
					if ( added && ! np.__timeout )
					{
						np.__timeout = window.setTimeout(function ()
						{
							np.__timeout = 0;
							np._fetch();
						}, np._options.interval * 1000);
					}
				});
			}
		}
	});


	np.__controllableRequestReadystatechange = function ()
	{
		var req = this;
		log("XHR onreadystatechange", req.readyState); // @stripOnBuild
		if ( req.readyState == 4 && req.status == 200 )
		{
			var controlElement = req.controlElement;
			if ( controlElement )
			{
				var sleep = parseFloat(req.responseText);
				if (isNaN(sleep)) {
					sleep = 500; // half a second should be enough as a default ... 
				}
				window.setTimeout(function ()
				{
					controlElement.disabled = false;
					controlElement.setAttribute('disabled', null);
					controlElement.removeAttribute('disabled');
				}, sleep);
			}
		}
	};

	addEvent(np._serverResetRequest, "readystatechange", np.__controllableRequestReadystatechange);
	addEvent(np._serverFlushRequest, "readystatechange", np.__controllableRequestReadystatechange);


	np._fetch = function ()
	{
		var req = this._fetchRequest;
		var r_rs = req.readyState;
		if ( r_rs == 4 || r_rs == 0 )
		{
			log("triggered fetch"); // @stripOnBuild
			req.open("GET", './get', true);
			req.send();
		}
	};

	np._mkImage = function (uri, crawler, onReady)
	{
		log('mkImage', uri, crawler); // @stripOnBuild
		var imageDoc = document.createElement('img');
		addEvent(imageDoc, "load", function ()
		{
			log('loaded', this.src); // @stripOnBuild
			/* structure looks like :
				<article>
					<stripOnBuild>{DEBUG_MSG}</stripOnBuild>
					<img src="{uri}" />
					<section class="src {crawler}">
						<a href="{uri}">{uri}</a>
					</section>
				</article>
			*/
			var imageLink = document.createElement('a');
			imageLink.setAttribute('class', 'fancybox');
			imageLink.setAttribute('href', uri);
			imageLink.setAttribute('rel', 'group');
			imageLink.appendChild(imageDoc);
			$("a.fancybox").fancybox();
			var imageBox = document.createElement('article');
			imageBox.appendChild(imageLink);
			var srcSpan = imageBox.appendChild(document.createElement('section'));
			srcSpan.className = 'src '+ crawler;

			var srcA = srcSpan.appendChild(document.createElement('a'));
			srcA.href = srcA.innerHTML = srcA.innerText = this.src;

			if ( typeof onReady == "function" )
			{
				onReady(imageBox);
			}
		});
		imageDoc.src = uri;
	};

	np._pushImage = function (uri, crawler, onReady)
	{
		if ( this._imageTarget )
		{
			log('add image', uri);     // @stripOnBuild
			this._mkImage(uri, crawler, function (image)
				{
					var add = ( np._state == 0 );
					if ( add )
					{
						np._images.push(image);
						np._imageTarget.insertBefore(image, np._imageTarget.firstChild);
						log('added image', image);     // @stripOnBuild
						if ( np._images.length > np._imagesMax )
						{
							np._popImage();
						}
					}
					else                                                        // @stripOnBuild
					{                                                           // @stripOnBuild
						log('image not loaded, since _state != 0', np._state);  // @stripOnBuild
					}                                                           // @stripOnBuild

					if ( typeof onReady == "function" )
					{
						window.setTimeout(function () {
							onReady(add);
						}, np._imageFadeInTime);
					}
				});
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
		, save : function ()
			{
				log('options saved');
				localStorage.setItem(this.target, JSON.stringify(np._options));
			}
		, load : function ()
			{
				var lo = localStorage.getItem(this.target);
				if ( lo )
				{
					try
					{
						lo = JSON.parse(lo);
						log('options loaded'); // @stripOnBuild
						np._options = lo;
					}
					catch ( ex )
					{
						log('ERROR:', ex); // @stripOnBuild
					}
				}
				else                                // @stripOnBuild
				{                                   // @stripOnBuild
					log('options load failed');     // @stripOnBuild
				}                                   // @stripOnBuild
			}
		};

	np.serverReset = function (controlElement)
	{
		var req = this._serverResetRequest;
		var r_rs = req.readyState;
		if ( r_rs == 4 || r_rs == 0 )
		{
			log("triggered serverReset"); // @stripOnBuild
			req.controlElement = controlElement;
			controlElement.disabled = true;
			controlElement.setAttribute('disabled', 'disabled');
			req.open("GET", './reset', true);
			req.send();
		}
	};

	np.serverFlush = function (controlElement)
	{
		var req = this._serverFlushRequest;
		var r_rs = req.readyState;
		if ( r_rs == 4 || r_rs == 0 )
		{
			log("triggered serverFlush"); // @stripOnBuild
			req.controlElement = controlElement;
			controlElement.disabled = true;
			controlElement.setAttribute('disabled', 'disabled');
			req.open("GET", './flush', true);
			req.send();
		}
	};

	np.setInterval = function (interval)
	{
		log('set interval', interval); // @stripOnBuild
		this._options.interval = interval;
		this._optionsStorage.save();
	};

	np.getInterval = function ()
	{
		return this._options.interval;
	};

	np.setState = function (which, status)
	{
		var oldState0 = ( this._state == 0 );
		this._state = bitset[ status ? "set" : "unset" ](this._state, which);
		log("setState", which, status, '->', this._state); // @stripOnBuild
		var state0 = ( this._state == 0 );

		// not sure it this is the right place for this ... but i had to put it somewhere ...
		if ( which == this.constants.stateBS.boss )
		{
			var rootElem = document.documentElement;
			if ( status )
			{
				rootElem.className += this.__bossMode_className;
				try
				{
					window.blur();
				}
				catch ( ex )
				{
					// nothing to do ... .
				}
			}
			else
			{
				rootElem.className = rootElem.className.replace(this.__bossMode_className_RE, '');
			}
		}

		if ( state0 != oldState0 )
		{ // state changed
			if (this._state == 0)
			{
				log('! continue'); // @stripOnBuild
				this._fetch();
			}
			else
			{
				log("! halt"); // @stripOnBuild
				this._fetchRequest.abort();
			}
		}
	};

	np.getState = function (which)
	{
		return bitset.check(this._state, which);
	};

	np.__inited = false;
	np.init = function (imageTargetID, imageFadeInTime)
	{
		if ( this.__inited )
		{
			log('init ran already'); // @stripOnBuild
			return false;
		}

		this.__inited = true;
		log('init started'); // @stripOnBuild

		this._imageTarget = document.getElementById(imageTargetID);
		this._imageTarget.appendChild(document.createTextNode('')); // to prevent issues with insertBefore()
		log('imageTarget:', this._imageTarget); // @stripOnBuild

		this._imageFadeInTime = imageFadeInTime;
		log('imageFadeInTime', this._imageFadeInTime); // @stripOnBuild

		this._optionsStorage.load();


		addEvent(window, 'scroll', function ()
		{
			log('scroll detected', 'offset:', this.pageYOffset); // @stripOnBuild
			np.setState(np.constants.stateBS.scroll, this.pageYOffset > 0 );
		});
		this.setState(this.constants.stateBS.scroll, window.pageYOffset > 0 );


		var c_background = document.getElementById('c_background');
		c_background.checked = this._options.playInBackground;
		fireEvent(c_background, 'change');
		addEvent(c_background, 'change', function ()
		{
			np._options.playInBackground = this.checked;
			np._optionsStorage.save();
			log('playInBackground', np._options.playInBackground);  // @stripOnBuild
		});


		/* blur and focus event is broken some time - can not reproduce :-( */
		addEvent(window, 'blur', function ()
		{
			log('!# window blur'); // @stripOnBuild
			if ( ! np._options.playInBackground )
			{
				np.setState(np.constants.stateBS.active, true);
			}
		});
		addEvent(window, 'focus', function ()
		{
			log('!# window active'); // @stripOnBuild
			np.setState(np.constants.stateBS.active, false);
		});

		if ( document.hidden != undefined )
		{
			// document. // scroll to top
			addEvent(document, 'visibilitychange', function ()
			{
				log('-- visibility change detected', 'hidden:', this.hidden); // @stripOnBuild
				np.setState(np.constants.stateBS.presented, this.hidden);
			});
			this.setState(this.constants.stateBS.presented, document.hidden);
		}

		var c_speed = document.getElementById('c_speed');
		c_speed.value = this.getInterval();
		addEvent(c_speed, 'change', function ()
		{
			np.setInterval(this.value);
		});

		var c_state = document.getElementById('c_state');
		c_state.checked = ! this.getState(this.constants.stateBS.manual);
		addEvent(c_state, 'change', function ()
		{
			np.setState(np.constants.stateBS.manual, !this.checked);
		});


		var sc_reset = document.getElementById('sc_reset');
		addEvent(sc_reset, 'click', function ()
		{
			var controlElement = this;
			if ( ! controlElement.disabled )
			{
				np.serverReset(controlElement);
			}
		});

		var sc_flush = document.getElementById('sc_flush');
		addEvent(sc_flush, 'click', function ()
		{
			var controlElement = this;
			if ( ! controlElement.disabled )
			{
				np.serverFlush(controlElement);
			}
		});

		this.setState(this.constants.stateBS.init, false);
		log('init ended'); // @stripOnBuild
	};



	log('feel done'); // @stripOnBuild
})(window.nichtparasoup={}, window);
