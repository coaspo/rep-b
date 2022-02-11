"use strict";

function checkValue(testName, expected, actual) {
  console.log('* testName=' + testName)
  const isPass = String(expected) == String(actual);
  console.log('* checkValue() expected=', expected)
  console.log('* checkValue() actual  =', actual)
  if (isPass) {
    var status = 'Pass: ' + testName;
  } else {
    window.testFailed = true;
    var status = '<id style=\'color:red\'>Failed; ' + testName + '</id>' +
      '\n--expected: ' + JSON.stringify(expected) +
      '\n----actual: ' + JSON.stringify(actual);
  }
  console.log('* checkValue() status=' + status);
  var msgs = document.getElementById("results").innerHTML;
  if (msgs.length > 0) {
    msgs += '\n';
  }
  msgs += status;
  document.getElementById("results").innerHTML = msgs
}
