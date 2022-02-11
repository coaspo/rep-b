"use strict";
// Default search button
document.getElementById('inputText').addEventListener('keypress', function (e) {
  const key = e.which || e.keyCode;
  if (key === 13) { // 13 is enter
    browse('https://duckduckgo.com/?q=zzzz  site:org');
  }
});

// Weather - current 12 hours, and next 12, 12 hours
let w = new Worker("js/weather.js");
w.onmessage = function (event) {
  if (event.data == undefined) {
    event.data = 'unable to get weather; see '
  }
  document.getElementById("weather").innerHTML = event.data;
  w.terminate();
  w = undefined;
};


// Contents button
function scanContents() {
  window.DEBUG = true;
  const baseUrl = getBaseUrl()
  const filePathsFilePath = '/search_file_paths.txt'
  const labelsFilePath = '/search_labels.txt'
  const searchFileUrls = getFileUrls(baseUrl, filePathsFilePath)
  const searchLabels = getSearchLabels(baseUrl, labelsFilePath)
  if (window.DEBUG) console.log('*scanContents() baseUrl= ' + baseUrl +
    '\n scanContents() searchFileUrls= ' + searchFileUrls +
    '\n scanContents() searchLabels= ' + searchLabels);
  searchContentsMain(baseUrl, filePathsFilePath, labelsFilePath, searchFileUrls, searchLabels);
}

// Switch tab
function opencontName(evt, tabName) {
  sessionStorage.setItem("tabName_index", 't'+tabName);
  var tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (let i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";"tabName_index"
  }
  tablinks = document.getElementsByClassName("tablink");
  for (let i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
  if (tabName == 'Food') {
    // Display a random set of recipes;  see cook.js
    document.getElementById("recipes").innerHTML = getRecipes(3)
  }
  var inputText = document.getElementById('inputText');
  var inputText2 = document.getElementById('inputText2');
  if (tabName == 'Projects' && inputText2.value == '') {
    // use Main input in Projects tab
    inputText2.value = inputText.value
  } else if (tabName == 'Main'  && inputText.value == '') {
    // use Projects input in Main tab
    inputText.value = inputText2.value
  }
}

if (document.URL.startsWith('file')) {
  //document.body.style.background = "lightyellow" // indicates server not running
}

// Curron postion; for weather.js and position link
var latitude = 'lat=42.3587' // Boston
var longitude = 'lon=-71.0567'
if (navigator.geolocation) {
  navigator.geolocation.getCurrentPosition(localPosition);
}

function localPosition(position) {
  latitude = 'lat=' + position.coords.latitude
  longitude = 'lon=' + position.coords.longitude
}

// Main search button
function browse(url, name = "_self") {
  if (window.DEBUG) console.log('browse, url=' + url)
  var text = document.getElementById('inputText').value;
  browseUrl(url, name, text)
}

// Projects search button
function browse2(url, name = "_self") {
  if (window.DEBUG) console.log('browse2, url==' + url)
  var text = document.getElementById('inputText2').value;
  browseUrl(url, name, text)
}

function browseUrl(url, name = "_self", txt) {
  var text = txt.replace(/  /g, " ")
  if (url.includes('homedepot')) {
    text = text.replace(/ /g, "%2520")
  } else if (url.includes('weather')) {
    text = latitude + '&' + longitude
  } else if (url.includes('/maps/')) {
    text = latitude + ',' + longitude
  }
  url = url.replace('zzzz', text)
  console.info('*browse() url= ' + url)
  const win = window.open(url, name);
  win.focus();
}

// Dispaly test web pages in the Apps tab
function showTestLinks(e) {
  if (window.event) { // IE
    var keynum = e.keyCode;
  } else if (e.which) { // Netscape/Firefox/Opera
    var keynum = e.which;
  }
  const c = String.fromCharCode(keynum);
  if (c == 'T') {
    const test = document.querySelector('.test');
    test.style.fontSize = document.body.style.fontSize
  }
}

