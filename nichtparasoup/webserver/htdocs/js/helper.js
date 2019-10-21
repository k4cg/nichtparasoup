; /* remember for development: lines that include the string "@stripOnBuild" will be stripped on build ;-) */


// helper functions for re-use ...

window.helperFuncs = {
  log : function () {} , // in case we forget to strip a log

  addEvent : function (obj, event, fn, capture)
  { "use strict";
    if ( ! obj ) { return; }

    if ( obj.attachEvent )
    {
      obj.attachEvent("on"+event, fn);
    }
    else if( obj.addEventListener )
    {
      obj.addEventListener(event, fn, capture);
    }
  } ,

  fireEvent : function (obj, event)
  { "use strict";
    if ( ! obj ) { return; }

    if ( obj.dispatchEvent )
    {
      obj.dispatchEvent(new Event(event));
    }
    else
    {
      obj.fireEvent("on" + event);
    }
  },

  storageFactory : function ()
  {
    try
    {
      var ls = window.localStorage;
      var lst = "test";
      ls.setItem(lst, lst);
      if (lst != ls.getItem(lst)) { throw "ls.getItem"; }
      ls.removeItem(lst);
      return ls;
    }
    catch (e)
    {
      return { // temp storage to emulate local storage in dev mode
        // only needed functions are implemented
          _store : {}
        , setItem    : function (k,v) { this._store[k]=v; }
        , getItem    : function (k) { return this._store[k]; }
      };
    }
  }

};

/* @stripOnBuild */ window.helperFuncs.log = function () {
/* @stripOnBuild */   window.console.log.apply(window.console, arguments);
/* @stripOnBuild */   var dbg = document.getElementById("dbg");
/* @stripOnBuild */   if ( dbg )
/* @stripOnBuild */   {
/* @stripOnBuild */     dbg.insertBefore(document.createTextNode(
/* @stripOnBuild */       (new Date()).toUTCString()
/* @stripOnBuild */       +" - "+
/* @stripOnBuild */       Array.prototype.join.call(arguments, " | ") +"\n"), dbg.firstChild);
/* @stripOnBuild */   }
/* @stripOnBuild */ };
