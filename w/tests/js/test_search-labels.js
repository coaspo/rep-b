"use strict";
function testSearchLabelsMain(baseUrl) {
   getUrlLabelTest(baseUrl);
   searchUrlsTest(baseUrl);
   searchFileIndexTest(baseUrl);
}

function getUrlLabelTest(baseUrl) {
   const name = getUrlLabel(baseUrl + '/tests/search-files/recipe.html');
   validate('0 search-labels.js:getUrlLabel()', 'tests/search-files/recipe.html', name)
}


function searchUrlsTest(baseUrl) {
   const searchFileUrls = [baseUrl + "/tests/search-files/recipe.html",
   baseUrl + "/tests/search-files/links.html"]

   const result = searchUrls('recipe', searchFileUrls)
   console.log(result)
   const expected = '<a href="' + baseUrl + '/tests/search-files/recipe.html">tests/search-files/<id style=\'color:red\'>recipe</id>.html</a>';
   validate('1 search-labels.js:searchUrls(),links html', expected, result.html)

   const expected1 = baseUrl + '/tests/search-files/recipe.html';
   validate('1 search-labels.js:searchUrls(),links 1 url', expected1, result.url)
   validate('1 search-labels.js:searchUrls(),links numOfUrls', 1, result.numOfUrls)

   const result2 = searchUrls('tests', searchFileUrls)
   console.log(result)
   const expected2 = '<a href="' + baseUrl + '/tests/search-files/recipe.html"><id style=\'color:red\'>tests</id>/search-files/recipe.html</a>\n\
<a href="'+ baseUrl + '/tests/search-files/links.html"><id style=\'color:red\'>tests</id>/search-files/links.html</a>';
   validate('2 search-labels.js:searchUrls(),links html 2', expected2, result2.html)
   validate('2 search-labels.js:searchUrls(),links url 2', 'NA', result2.url)
   validate('2 search-labels.js:searchUrls(),links numOfUrls 2', 2, result2.numOfUrls)

   const result3 = searchUrls('xxxx', searchFileUrls)
   validate('3 search-labels.js:searchUrls(),links html 0', '', result3.html)
}


function searchFileIndexTest(baseUrl) {
   const labels = [['smart search site', 0, '//www.wolfram.com/'],
   ['free books site', 1, 'https://www.freebookcentre.net'],
   ['coursera- free course site', 1, 'https://www.coursera.org/']];
   const searchFileUrls = [baseUrl + '/tests/search-files/etc.html',
   baseUrl + '/tests/search-files/misc.html'];
   const result = searchFileIndex('xxxx', searchFileUrls, labels)
   validate('4 search-labels.js:searchFileIndex(),no find', '', result.html)

   const result2 = searchFileIndex('smart', searchFileUrls, labels)
   const expected2 = '<a href="' + baseUrl + '/tests/search-files/etc.html">tests/search-files/etc.html</a>: \
<a href="//www.wolfram.com/"><id style=\'color:red\'>smart</id> search site</a>'
   validate('5 search-labels.js:searchFileIndex(), html ', expected2, result2.html)
   validate('5 search-labels.js:searchFileIndex(), url ', '//www.wolfram.com/', result2.url)
   validate('5 search-labels.js:searchFileIndex(), numOfUrls ', 1, result2.urlCount)

   const result3 = searchFileIndex('free', searchFileUrls, labels)
   const expected3 = '<a href="' + baseUrl + '/tests/search-files/misc.html">tests/search-files/misc.html</a>: \
<a href="https://www.freebookcentre.net"><id style=\'color:red\'>free</id> books site</a> \
<a href="https://www.coursera.org/">coursera- <id style=\'color:red\'>free</id> course site</a>'
   validate('6 search-labels.js:searchFileIndex(), html 2 ', expected3, result3.html)
   validate('6 search-labels.js:searchFileIndex(), url 2 ', 'NA', result3.url)
   validate('6 search-labels.js:searchFileIndex(), numOfUrls 2 ', 2, result3.urlCount)

   const result4 = searchFileIndex('site', searchFileUrls, labels)
   const expected4 = '<a href="' + baseUrl + '/tests/search-files/etc.html">tests/search-files/etc.html</a>: <a href="//www.wolfram.com/">smart search <id style=\'color:red\'>site</id></a>\n\
\n\
<a href="'+ baseUrl + '/tests/search-files/misc.html">tests/search-files/misc.html</a>: <a href="https://www.freebookcentre.net">free books <id style=\'color:red\'>site</id></a> <a href="https://www.coursera.org/">coursera- free course <id style=\'color:red\'>site</id></a>'
   validate('7 search-labels.js:searchFileIndex(), html 2 ', expected4, result4.html)
   validate('7 search-labels.js:searchFileIndex(), url 2 ', 'NA', result4.url)
   validate('7 search-labels.js:searchFileIndex(), numOfUrls 2 ', 3, result4.urlCount)
}

