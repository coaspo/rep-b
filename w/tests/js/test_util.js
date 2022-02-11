function testUtilMain(baseUrl) {
    testReadText();
    getFileUrlsTest(baseUrl);
    readTextTest(baseUrl);
    getSearchLabelsTest(baseUrl);
}

function testReadText() {
    try {
        const js = readText('https://api.weather.gov/gridpoints/BOX/68,81/forecast')
        var w = JSON.parse(js)
        console.log(w.properties.periods[0]['detailedForecast'])
        validate('0 search.js:readText()   ', 'readforcast', 'readforcast');
    } catch (err) {
        validate('0 search.js:readText()   ', '', err);
    }
}

function getFileUrlsTest(baseUrl) {
    const searchFileUrls = getFileUrls(baseUrl, '/tests/search_file_paths__t.txt')
    const expected = [baseUrl + "/tests/search-files/category/words.html",
    baseUrl + "/tests/search-files/food/bread..txt",
    baseUrl + "/tests/search-files/food/dessert;.txt",
    baseUrl + "/tests/search-files/food/egg_.txt",
    baseUrl + "/tests/search-files/food/eggs_.txt",
    baseUrl + "/tests/search-files/food/theory,.txt",
    baseUrl + "/tests/search-files/links-2.html",
    baseUrl + "/tests/search-files/links.html",
    baseUrl + "/tests/search-files/problems-examples.html",
    baseUrl + "/tests/search-files/problems-solutions.html",
    baseUrl + "/tests/search-files/recipe.html"]
    validate('2 search.js:getFileUrls()', expected, searchFileUrls);
}


function readTextTest(baseUrl) {
    const text = readText(baseUrl + '/tests/search_labels__t.txt');
    const expected = 'wolfram$$1$$https://www.wolfram.com/\n\
worldometers$$1$$https://www.worldometers.info/\n\
week in virology$$1$$https://www.microbe.tv/twiv/archive/\n\
internet archive$$2$$https://archive.org\n\
free books$$2$$https://www.freebookcentre.net/\n\
coursera- free course$$2$$https://www.coursera.org/\n\
edx - mit, harvard$$2$$https://www.edx.org/\n\
pizza$$5\n\
serve done$$5'
    validate('3 search.js:readText()', expected, text)
    console.log('bbbbaseUrl=' + baseUrl)
}

function getSearchLabelsTest(baseUrl) {
    const searchLabels = getSearchLabels(baseUrl, '/tests/search_labels__t.txt')
    const expected = [["wolfram", "1", "https://www.wolfram.com/"],
    ["worldometers", "1", "https://www.worldometers.info/"],
    ["week in virology", "1", "https://www.microbe.tv/twiv/archive/"],
    ["internet archive", "2", "https://archive.org"],
    ["free books", "2", "https://www.freebookcentre.net/"],
    ["coursera- free course", "2", "https://www.coursera.org/"],
    ["edx - mit, harvard", "2", "https://www.edx.org/"],
    ["pizza", "5"],
    ["serve done", "5"]];
    validate('4 search.js:getSearchLabels()', expected, searchLabels);
}
