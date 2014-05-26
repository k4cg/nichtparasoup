
root = """
<!DOCTYPE html><html><head><title>nichtparasoup</title><script type="application/javascript">
(function(e,h,g){var a,f,d,c;
a={interval:1000,intervalMinSec:1,imgsMax:100,source:"./get",cssCNhidden:"hidden",cssCNscalein:"scaleIn"};
e.setInterval=function(i){a.interval=1000*Math.max(i,a.intervalMinSec)};f={halt:false,target:null,imgs:[],req:false};
e.halt=function(){f.halt=true;c.abort();return false};e["continue"]=function(){f.halt=false;d.fetch();return true};
e.toggle=function(){return e[f.halt?"continue":"halt"]()};d={imgOnload:function(){this.className=a.cssCNscalein
},add:function(k){if(!k){return}var i,o,m=f.target,n=f.imgs,l=a.imgsMax;var j=document.createElement("img");
j.className=a.cssCNhidden;j.onload=d.imgOnload;j.src=k;if(m.firstChild){i=m.insertBefore(j,m.firstChild)
}else{i=m.appendChild(j)}n.unshift(i);while(n.length>l){o=n.pop();o.parentNode.removeChild(o)
}},fetch:function b(){if(f.req){return false}f.req=true;c.open("GET",a.source,false);c.send(null)}};
c=new XMLHttpRequest();c.onreadystatechange=function(){if(this.readyState===4){f.req=false;var i=(this.status===200);
if(i){d.add(this.responseText)}if(!f.halt){h.setTimeout(d.fetch,a.interval)}}};
e.init=function(i){f.target=document.getElementById(i);d.fetch()}})(iw={},this);</script><style type="text/css">
html{direction:ltr;overflow:scroll;overflow-x:hidden}
html,body{color:#ccc;background-color:black;margin:0;padding:0;height:100%}
#header{z-index:99999;display:block;position:fixed;top:-42px;left:0;right:0;height:7ex;line-height:4ex;background-color:#111;background-color:rgba(23,23,23,0.9);text-align:center;border-bottom:1px solid #111;transition:all 0.6s ease-in-out 0s}
#header:hover{top:0;border-bottom:1px solid #808080}
input[type="range"]{position:relative;top:5px}
#toggle{margin:0 5em;cursor:pointer;display:inline-block;width:5em}#toggle:hover{text-decoration:underline}
#wall{margin-top:2ex;display:block;height:100%}#wallbreaker{clear:both;display:none}
#wall img{margin:1ex 1ex;padding:0;border:1px solid #999;display:inline;display:inline-block;float:left;max-height:80%}
#wall img.hidden{display:none}
#wall img.scaleIn{animation:scaleIn linear .5s;-webkit-animation:scaleIn linear .5s;-moz-animation:scaleIn linear .5s;-o-animation:scaleIn linear .5s;-ms-animation:scaleIn linear .5s;transform-origin:top left;-webkit-transform-origin:top left;-moz-transform-origin:top left;-o-transform-origin:top left;-ms-transform-origin:top left}
@keyframes scaleIn{from{transform:scale(0)}to{transform:scale(1)}}
@-webkit-keyframes scaleIn{from{-webkit-transform:scale(0)}to{-webkit-transform:scale(1)}}
@-moz-keyframes scaleIn{from{-moz-transform:scale(0)}to{-moz-transform:scale(1)}}
@-o-keyframes scaleIn{from{-o-transform:scale(0)}to{-o-transform:scale(1)}}
@-ms-keyframes scaleIn{from{-ms-transform:scale(0)}to{-ms-transform:scale(1)}}</style></head>
<body onload="document.getElementById('interval').onchange(); iw.init('wall');"><div id="header">update interval: 1
<input id="interval" max="9" min="1" onchange="iw.setInterval(this.value)" step="1" type="range" value="5"/>9
<a id="toggle" onclick="this.innerHTML = ( iw.toggle() ? 'halt' : 'continue' );">halt</a><br/>&#9776;</div><div id="wall">
<span id="wallbreaker"></span></div><noscript>!!! enable JavaScript !!!</noscript></body></html>
"""
