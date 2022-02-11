"use strict";

function searchContentsMain(baseUrl, filePathsFilePath, labelsFilePath, searchFileUrls, searchLabels) {
  try {
    const inputText = document.getElementById('inputText').value.toLowerCase().trim();
    if (window.DEBUG) console.log('*searchContentsMain() inputText= ' + inputText);
    if (window.DEBUG) console.log('*searchContentsMain() labelsFilePath= ' + labelsFilePath);
    if (inputText.length == 0) {
      document.getElementById("search-results").innerHTML = ''
      return;
    }

    if (window.DEBUG) console.log('*searchContentsMain() window.inputText= ' + inputText);
    document.getElementById("search-results").innerHTML = 'Wait... searching web pages'

    const result = searchContents(inputText, searchFileUrls, searchLabels);
    if (window.DEBUG) console.log('*searchContentsMain() search.html= ' + result.html);
    if (window.DEBUG) console.log('*searchContentsMain() search.hitUrl= ' + result.hitUrl);
    document.getElementById("search-results").innerHTML = result.html;
    if (result.hitUrl != '') {
      window.open(result.hitUrl, "_self");
    }
  } catch (err) {
    console.log('ERR searchContentsMain() ' + err)
    console.log(err.stack)
    document.getElementById("search-results").innerHTML = err
  }
}

function searchContents(inputText, searchFileUrls, searchLabels) {
  if (window.DEBUG) console.log('*searchFiles() inputText = ' + inputText)
  const problemsHtml = scanFileContents(inputText, 'problem', searchFileUrls)
  const urlResult = searchUrls(inputText, searchFileUrls)
  const indexResult = searchFileIndex(inputText, searchFileUrls, searchLabels)
  var result = {};
  result.html = urlResult.html + '\n\n' + indexResult.html + '\n\n' + problemsHtml
  result.html = result.html.replace('\n\n\n\n', '\n\n').trim()
  if (result.html.length === 0) {
    result.html = 'Did not find: "' + inputText + '"';
  } else if ((problemsHtml.length + urlResult.numOfUrls + indexResult.urlCount) == 1) {
    result.hitUrl = urlResult.url + indexResult.url // one of the 'results' urls is blank
  }
  return result;
}

