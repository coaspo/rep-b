"use strict";
// used in index.html
// let w = new Worker("js/weather.js");
// to get the weather
var i = 0;
var timeout

function timedCount() {
  let i = i + 1; // not used
  postMessage(i);
  setTimeout("timedCount()", timeout);
}


self.addEventListener('message', function (e) {
  const timeout = e.data.timeout
  timedCount()
}, false);
