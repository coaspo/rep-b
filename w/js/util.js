"use strict";
function saveScrollPosition(pageName) { // variable argument in arguments array
  let y = window.scrollY;
  sessionStorage.setItem("scrollPosition_" + pageName, y.toString());
}

function restoreScrollPosition(pageName) { // variable argument in arguments array
  if (pageName == 'index') {
    let tabName = sessionStorage.getItem("tabName_index");
    document.getElementById(tabName).click();
  }
  let y = Number(sessionStorage.getItem("scrollPosition_" + pageName));
  window.scrollTo(0, y);
}

function getBaseUrl() {
    const url = String(document.URL);
    const i_base = url.indexOf('/w/') + 2;
    const baseUrl = url.substr(0, i_base);
    if (window.DEBUG) console.log('*_getBaseUrl() baseUrl= ' + baseUrl)
    return baseUrl
}

function getFileUrls(baseUrl, filePathsFilePath) {
    const url = baseUrl + filePathsFilePath
    if (window.DEBUG) console.log('*getFileUrls() url= ' + url);
    const html = readText(url);

    const lines = html.trim().split('\n');
    var fileUrls = [];

    for (let i = 0; i < lines.length; i++) {
        fileUrls[i] = baseUrl + '/' + lines[i];
    }
    if (window.DEBUG) console.log('*getFileUrls() paths=\n' +
        String(fileUrls).replace(/,/g, '\n'));
    return fileUrls;
}

function getSearchLabels(baseUrl, labelsFilePath) {
    const url = baseUrl + labelsFilePath
    if (window.DEBUG) console.log('*_getSearchLabels() url= ' + url);
    const labelText = readText(url);

    const lines = labelText.trim().split('\n');
    var labels = [];

    for (let i = 0; i < lines.length; i++) {
        var fields = lines[i].split('$$')
        labels[i] = fields;
    }
    if (window.DEBUG) console.log('*_getSearchLabels() labels=\n' + String(labels));
    return labels;
}


function readText(url) {
    if (window.DEBUG) console.log('*readText() url= ' + url);
    var req = new XMLHttpRequest();
    req.open('GET', url, false); // `false` makes the request synchronous
    try {
        req.send(null);
    } catch (err) {
        throw err + ' on reading: ' + url;
    }
    var text
    if (req.status === 200) {
        text = req.responseText.trim();
    } else {
        text = req.status + ' on reading: ' + url;
        console.log('*readTexinitGlobalst() ERR text= ' + text)
        throw text
    }
    if (window.DEBUG) console.log('*readText() text= ' + text)
    return text
}

function getUrlLabel(url) {
    const i1 = url.lastIndexOf('/w/') + 3;
    const label = url.substring(i1);
    return label;
}


