"use strict";
function testSearchMain(baseUrl, searchFileUrls, searchLabels) {
   const filePathsFilePath = '/tests/search_file_paths__t.txt'
   const labelsFilePath = '/tests/search_labels__t.txt'
   if (window.DEBUG) console.log('*testSearchMain() baseUrl= ' + baseUrl +
      '\n *testSearchMain() searchFileUrls= ' + searchFileUrls +
      '\n *testSearchMain() searchLabels= ' + searchLabels);
   searchContentsMainTest1(baseUrl, filePathsFilePath, labelsFilePath, searchFileUrls, searchLabels);
   searchContentsMainTest2(baseUrl, filePathsFilePath, labelsFilePath, searchFileUrls, searchLabels);
   searchContentsMainTest(baseUrl, filePathsFilePath, labelsFilePath, searchFileUrls, searchLabels);
}

function searchContentsMainTest1(baseUrl, filePathsFilePath, labelsFilePath, searchFileUrls, searchLabels) {
   document.getElementById('inputText').value = '  '
   searchContentsMain(baseUrl, filePathsFilePath, labelsFilePath, searchFileUrls, searchLabels)
   let actual = document.getElementById("search-results").innerHTML
   validate('1.1 search.js:searchContentsMain1()  innerHTML ', '', actual);
}

function searchContentsMainTest2(baseUrl, filePathsFilePath, labelsFilePath, searchFileUrls, searchLabels) {
   document.getElementById('inputText').value = 'xyz'
   searchContentsMain(baseUrl, filePathsFilePath, labelsFilePath, searchFileUrls, searchLabels)
   let expected = 'Did not find: "xyz"'
   let actual = document.getElementById("search-results").innerHTML
   validate('1.2 search.js:searchContentsMain2()  innerHTML ', expected, actual);
}

function searchContentsMainTest(baseUrl, filePathsFilePath, labelsFilePath, searchFileUrls, searchLabels) {
   document.getElementById('inputText').value = 'egg'
   searchContentsMain(baseUrl, filePathsFilePath, labelsFilePath, searchFileUrls, searchLabels);
   let expected = '<a href="' + baseUrl + `/tests/search-files/food/egg_.txt">tests/search-files/food/<id style="color:red">egg</id>_.txt</a>
<a href="` + baseUrl + `/tests/search-files/food/eggs_.txt">tests/search-files/food/<id style="color:red">egg</id>s_.txt</a>`
   let actual = document.getElementById("search-results").innerHTML
   validate('1 search.js:searchContentsMain()  innerHTML ', expected, actual);
}



