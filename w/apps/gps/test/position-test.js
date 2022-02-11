"use strict";
window.DEBUG = true

function unitTestsMain() {
  console.log('-- unitTestsMain() started');
  document.getElementById("results").innerHTML = ''
  window.testFailed = false
  try {
        x_y_z_t_test()
        ds_dt_test()
        mSecKphMph_test()
        metersFeetMiles_test()
        northSouth_test()
        polarAngle_test()
    showPosition_test()
    console.log('-- unitTestsMain() done');
  } catch (err) {
    const msg = document.getElementById("results").innerHTML + '\n  ' + err
    document.getElementById("results").innerHTML = msg
    console.error('ERR unitTestsMain() ' + err)
    console.error(err.stack)
    window.testFailed = true
  }
  if (window.testFailed) {
    document.body.style.background = '#ff6666';
  } else {
    document.body.style.background = '#ccffcc';
  }
}

unitTestsMain();


function clearResults() {
  document.getElementById("results").innerHTML = ''
  document.body.style.background = 'white';
}


function unitTest() {
  showPosition_test()
}



function x_y_z_t_test() {
  pt = {
    xyzt: [], lat0: 42.4, lng0: 71, alt0: 55, t0: 1617684042111,
    lat: 42.5, lng: 71, alt: 65, t: 1617684047111
  }
  let [x, y, z, t] = x_y_z_t(pt)
  checkValue('1 x_y()  x .1° dlat ', 0, x);
  checkValue('1        y ', 11119, y);
  checkValue('1        z ', 10, z);
  checkValue('1        t ', 5, t);

  pt = {
    xyzt: [], lat0: 42, lng0: 71, alt0: 55, t0: 1617684047000,
    lat: 42, lng: 71.1, alt: 0, lng: 71.1, alt: 0, t: 1617684057000,
  }
  let [x1, y1, z1, t1] = x_y_z_t(pt)
  checkValue('2 x_y()  x .1° dlng ', 8263, x1);
  checkValue('2        y ', 0, y1);
  checkValue('2        z ', -55, z1);
  checkValue('2        t ', 10, t1);

  pt = {
    xyzt: [], lat0: 42, lng0: 71, alt0: 55,
    lat: 42.1, lng: 71.1, alt: 55
  }
  let [x2, y2, z2, t2] = x_y_z_t(pt)
  let d = Math.sqrt(x2 * x2 + y2 * y2).toFixed(0)
  checkValue('3 x_y()  d .1° diagnal ', 13850, d);
}


function ds_dt_test() {
  pt = { xyzt: [[0, 0, 0, 0], [0, 9, 0, 1]] }
  let actual = ds_dt(pt)
  checkValue('4 ds_dt()  straight ', 9, actual);

  pt = { xyzt: [[0, 0, 0, 1], [0, 30, 40, 3]] }
  actual = ds_dt(pt)
  checkValue('4          diagnol ', 25, actual);
}


function mSecKphMph_test() {
  let expected = '9 m/s, 32 kph, 20 mph'
  let actual = mSecKphMph(9)
  checkValue('5 mSecKphMph()  20 mph ', expected, actual);
}


function metersFeetMiles_test() {
  let expected = '10,000 m, 32,808 ft, 6.2 miles'
  let actual = metersFeetMiles(10000)
  checkValue('6 metersFeetMiles()  10 km ', expected, actual);
}


function northSouth_test() {
  checkValue('7 northSouth()  N ', 'N', northSouth(349));
  checkValue('7               NW ', 'NW', northSouth(337));
  checkValue('7               SE ', 'SE', northSouth(113));
}


function polarAngle_test() {
  pt = { xyzt: [[0, 0, 0], [.5, .866, 0]] }
  let actual = polarAngle(pt)
  checkValue('5 polarAngle   p30 ', 30, actual);
  pt = { xyzt: [[0, 0, 0], [.5, -.866, 0]] }
  actual = polarAngle(pt)
  checkValue('5              p150 ', 150, actual);
  pt = { xyzt: [[0, 0, 0], [-.5, -.866, 0]] }
  actual = polarAngle(pt)
  checkValue('5              p210 ', 210, actual);
  pt = { xyzt: [[0, 0, 0], [-.5, .866, 0]] }
  actual = polarAngle(pt)
  checkValue('5              p330 ', 330, actual);

  pt = { xyzt: [[0, 0, 0], [0, 5, 0]] }
  actual = polarAngle(pt)
  checkValue('6 polarAng9le   p0 ', 0, actual);
  pt = { xyzt: [[0, 0, 0], [5, 0, 0]] }
  actual = polarAngle(pt)
  checkValue('6              p90 ', 90, actual);
  pt = { xyzt: [[0, 0, 0], [0, -5, 0]] }
  actual = polarAngle(pt)
  checkValue('6              p180 ', 180, actual);
  pt = { xyzt: [[0, 0, 0], [-5, 0, 0]] }
  actual = polarAngle(pt)
  checkValue('6              p270 ', 270, actual);
  pt = { xyzt: [[0, 0, 0], [-1, 111111, 0]] }
  actual = polarAngle(pt)
  checkValue('6              p360 ', 360, actual);

  pt = { xyzt: [[0, 0, 0], [0, 0, 0]] }
  actual = polarAngle(pt)
  checkValue('6              p9999', -9999, actual);
}


function showPosition_test() {
  let position = {
    coords: {
      latitude: 42.5, longitude: 71, altitude: 15,
      accuracy: 3.4, altitudeAccuracy: 5.65, speed: 11.34, heading: 122.12
    }
  }
  pt = { xyzt: [] }
  showPosition(position)
  checkInner('lat,lng', '42.5°, 71° 🔵 1');
  checkInner('alti', '15 m');
  checkInner('accu', '3 m, 6 m');
  checkInner('speed', '11.3 m/s, 41 kph, 25 mph');
  checkInner('head', '122° SE');
  const expected = {
    alt0: 15, lat0: 42.5, lng0: 71, t0: pt.t0,
    alt: 15, lat: 42, lng: 71, t: 0,
    xyzt: [0, 0, 0, 0]
  }
  checkValue('8 showPosition()   pt ', expected, pt);

  position = {
    coords: {
      latitude: 42.6, longitude: 71.1, altitude: 33,
      accuracy: 3.4, altitudeAccuracy: 5.65, speed: 44.44, heading: 277.0
    }
  }
  var currentTime = new Date().getTime();
  while (currentTime + 1000 >= new Date().getTime()) {
  }
  showPosition(position)
  checkInner('x', '8,192 m, 26,876 ft, 5.1 miles');
  checkInner('y', '11,119 m, 36,479 ft, 6.9 miles');
  checkInner('head-dx/dy', '36° NE');
  checkInner('speed-ds/dt', '13810.9 m/s, 49719 kph, 30881 mph');
  checkInner('sum(ds)', '13,811 m, 45,311 ft, 8.6 miles');
  checkInner('R', '13811.0 m, 45,311 ft, 8.6 miles');
  const expected2 = {
    alt: 33, alt0: 15, lat: 42.6, lat0: 42.5, lng: 71.1, lng0: 71,
    t0: pt.t0, t: 11,
    xyzt: [0, 0, 0, 1]
  }
}


function checkInner(id, expected) {
  let actual = document.getElementById(id).innerHTML
  checkValue('8 showPosition()  ' + id, expected, actual);
}




//   display("head", coord.heading)


//   display("x", metersFeetMiles(x))
//   display("y", metersFeetMiles(y))
//   display("head-dx/dy", '-')
//   display("speed-ds/dt", mSecKphMph(ds_dt(pt)))
//   display("sum(ds)", sum_ds(pt))
//   display("R", metersFeetMiles(radius(pt).toFixed(1)))
// }