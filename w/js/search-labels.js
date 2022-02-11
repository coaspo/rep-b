"use strict";
function searchFileIndex(inputText, searchFileUrls, searchLabels) {
  const result = {};
  result.html = '';
  result.url = '';
  result.urlCount = 0;
  let prevFileIndex = -1
  for (var i in searchLabels) {
    const fields = searchLabels[i]
    let label = fields[0]
    if (label.indexOf(inputText) < 0) {
      continue;
    }
    const fileIndex = fields[1]
    if (prevFileIndex != fileIndex) {
      prevFileIndex = fileIndex
      if (result.html.length > 0) {
        result.html += '\n\n'
      }
      result.html += _getLink(searchFileUrls[fileIndex]) + ':'
    }
    label = highLight(label, inputText)
    if (fields.length == 3) {
      result.urlCount++;
      const url = fields[2]
      result.html += ' <a href="' + url + '">' + label + '</a>'
      result.url = url
    } else {
      result.html += ' ' + label
    }
  }
  if (result.urlCount > 1 && result.html.length > 0) {
    result.url = 'NA'
  }
  if (window.DEBUG) console.log('*searchIndexedLabels() result.html=' + result.html)
  return result
}


function searchUrls(text, searchFileUrls) {
  if (window.DEBUG) console.log('*searchUrls() text=' + text + ' searchFileUrls=' + searchFileUrls)
  const result = {};
  result.html = '';
  result.url = '';
  result.numOfUrls = 0;
  for (var i in searchFileUrls) {
    const url = searchFileUrls[i]
    let label = getUrlLabel(url).toLowerCase()
    if (label.indexOf(text) > -1) {
      if (result.html.length > 0) {
        result.html += '\n'
      }
      result.numOfUrls++;
      label = highLight(label, text)
      result.html += '<a href="' + url + '">' + label + '</a>'
      result.url = url
    }
  }
  if (result.numOfUrls > 1 && result.html.length > 0) {
    result.url = 'NA'
  }
  if (window.DEBUG) console.log('*searchUrls() result.html=' + result.html)
  return result
}



function _getLink(url) {
  const label = getUrlLabel(url)
  const link = '<a href="' + url + '">' + label + '</a>'
  return link;
}

