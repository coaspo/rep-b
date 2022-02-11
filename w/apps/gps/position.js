
var pt = { xyzt: [] }


function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(showPosition);
  } else {
    document.getElementById("info").innerHTML = "Geolocation is not supported by this browser.";
  }
}


function showPosition(position) {
  try {
    const coord = position.coords
    const alt = formatNum(coord.altitude, 0)
    pt.lat = coord.latitude
    pt.lng = coord.longitude
    pt.alt = alt
    pt.t = new Date().getTime()
    display("lat,lng", pt.lat, "&deg;, ", pt.lng, "&deg;")
    display("alti", alt, " m")
    let accuracy = coord.accuracy.toFixed(0)
    display("accu", accuracy, ' m, ', formatNum(coord.altitudeAccuracy, 0), ' m')

    display("speed", mSecKphMph(coord.speed))
    let heading = formatNum(coord.heading, 0)
    display("head", heading, "&deg; ", northSouth(heading))

    if (pt.xyzt.length == 0) {
      pt.xyzt.push([0, 0, 0, 0])
      pt.lat0 = pt.lat
      pt.lng0 = pt.lng
      pt.alt0 = pt.alt
      pt.xPrev = 0
      pt.yPrev = 0
      pt.t0 = pt.t
      display("lat,lng", pt.lat, "&deg;, ", pt.lng, "&deg; 🔵 ", pt.xyzt.length)
      return
    }

    var [x, y, z, t] = x_y_z_t(pt)
    if (coord.altitudeAccuracy != null) {
      accuracy = Math.min(accuracy, coord.altitudeAccuracy)
    }
    const ds = Math.sqrt(Math.pow(x - pt.xPrev, 2) + Math.pow(y - pt.yPrev, 2))
    const msg = '[m,sec] x.y,z,t xPrev,yPrev ' + x + ',' + y + ',' + z + ',' + t + ' ' +
      pt.xPrev + ',' + pt.yPrev + '   n ds ' + pt.xyzt.length + ' ' + ds.toFixed(1)
    display("info", msg)
    console.info(msg)
    const threshold = Math.max(3, accuracy / 3)
    if (ds < threshold) {
      display("head-dx/dy", '')
      display("speed-ds/dt", '')
      return
    }
    display("lat,lng", pt.lat, "&deg;, ", pt.lng, "&deg; 🔵", pt.xyzt.length)
    // Derived parameters
    pt.xyzt.push([x, y, z, t])

    display("x", metersFeetMiles(x))
    display("y", metersFeetMiles(y))
    heading = polarAngle(pt)
    display("head-dx/dy", heading, "&deg; ", northSouth(heading))
    display("speed-ds/dt",function showPosition(position) mSecKphMph(ds_dt(pt)))
    display("sum(ds)", metersFeetMiles(sum_ds(pt)))
    display("R", metersFeetMiles(radius(pt).toFixed(1)))
    pt.xPrev = x
    pt.yPrev = y
  } catch (err) {
    console.error('ERR postion.js ' + err)
    console.error(err.stack)
    const msg = document.getElementById("info").innerHTML + '\n' + err
    document.getElementById("indo").innerHTML = msg
  }
}


function display() {
  const element = document.getElementById(arguments[0]);
  text = ''
  for (j = 1; j < arguments.length; j++) {
    text += arguments[j]
  }
  element.innerHTML = text
}


function isDistaceValid(x, y, xPrev, yPrev, accuracy) {
  const ds = Math.sqrt(Math.pow(x - xPrev, 2) + Math.pow(y - yPrev, 2))
  return ds >= accuracy / 2
}


function x_y_z_t(pt) {
  const R = 10007540 * 2 / Math.PI
  let y = (R * (pt.lat - pt.lat0) * Math.PI / 180)
  let x = (R * (pt.lng - pt.lng0) * Math.PI / 180 * Math.cos((pt.lat + pt.lat0) / 2 * Math.PI / 180))
  x = Math.round(x)
  y = Math.round(y)
  const z = pt.alt0 == '-' || pt.alt == '-' ?
    '-' : Math.round(pt.alt - pt.alt0)
  const t = Math.round((pt.t - pt.t0) / 1000)
  return [x, y, z, t]
}


function ds_dt(pt) {
  i = pt.xyzt.length - 1
  const p = pt.xyzt[i--]
  const p1 = pt.xyzt[i]
  var [x, y, z, t] = [p[0], p[1], p[2], p[3]]
  var [x1, y1, z1, t1] = [p1[0], p1[1], p1[2], p1[3]]
  const ds = Math.sqrt(Math.pow(x - x1, 2) + Math.pow(y - y1, 2) + Math.pow(z - z1, 2))
  const speed = ds / (t - t1)
  return formatNum(speed, 1)
}


function formatNum(num, decimalDigits) {
  if (num == null) {
    return '-'
  }
  return Number(num.toFixed(decimalDigits))
}


function sum_ds(pt) {
  let sum = 0
  for (let i = 0; i < pt.xyzt.length - 1; i++) {
    const p = pt.xyzt[i]
    const p1 = pt.xyzt[i + 1]
    var [x, y, z, t] = [p[0], p[1], p[2], p[3]]
    var [x1, y1, z1, t1] = [p1[0], p1[1], p1[2], p1[3]]
    if (z == '-' || z1 == '-') {
      z = z1 = 0
    }
    const ds = Math.sqrt(Math.pow(x - x1, 2) + Math.pow(y - y1, 2) + Math.pow(z - z1, 2))
    sum += ds
  }
  sum = formatNum(sum, 0)
  return sum
}


function radius(pt) {
  // from https://www.movable-type.co.uk/scripts/latlong.html
  const R = 10007540 * 2 / Math.PI  // meters; 6371e3;
  const φ1 = pt.lat0 * Math.PI / 180; // φ, λ in radians
  const φ2 = pt.lat * Math.PI / 180;
  const Δφ = (pt.lat - pt.lat0) * Math.PI / 180;
  const Δλ = (pt.lng - pt.lng0) * Math.PI / 180;
  const a = Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
    Math.cos(φ1) * Math.cos(φ2) *
    Math.sin(Δλ / 2) * Math.sin(Δλ / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  let d = R * c;
  d = formatNum(d, 0)
  return d
}


function metersFeetMiles(distance) {
  let feet = distance * 3.2808
  feet = formatNum(feet, 0)
  let miles = feet / 5280
  miles = formatNum(miles, 1)
  return distance.toLocaleString() + " m, " +
    feet.toLocaleString() + " ft, " +
    miles + " miles"
}


function mSecKphMph(speed) {
  if (speed == null) {
    return '-'
  }
  let kph = speed * 60 * 60 / 1000
  kph = formatNum(kph, 0)
  let mph = kph / 1.61
  mph = formatNum(mph, 0)
  return formatNum(speed, 1) + " m/s, " + kph + " kph, " + mph + " mph"
}


function northSouth(heading) {
  if (heading == '-' || heading < 0) {
    return '-'
  }
  let i = Math.floor((heading + 22.5) / 45)
  if (i > 7) {
    i = 0
  }
  var c = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
  return c[i]
}


function polarAngle(pt) {
  i = pt.xyzt.length - 1
  const p = pt.xyzt[i--]
  const p1 = pt.xyzt[i]
  var [x, y] = [p[0], p[1]]
  var [x1, y1] = [p1[0], p1[1]]
  let dx = (x - x1).toFixed(3)
  const dy = (y - y1).toFixed(3)
  if (dx == 0.0 && dy == 0.0) {
    return -9999 // error
  }
  if (dx == 0.0) {
    dx = 0.001 // =1 mm
  }
  let θ = Math.atan(dy / dx) * 180 / Math.PI
  θ = dx > 0.0 ? 90 - θ : 270 - θ
  return Math.round(θ)
}


function save() {
  let link = document.getElementById("link")
  if (link == null) {
    link = document.createElement("a");
    link.id = 'link';
    document.body.appendChild(link);
  }
  let text = ''
  for (i in pt.xyzt) {
    if (i > 0) {
      text += '\n'
    }
    p = pt.xyzt[i]
    text += p[0] + ',' + p[1] + ',' + p[2] + ',' + p[3]
  }
  var myBlob = new Blob([text], { type: 'text/plain' });
  blobUrl = URL.createObjectURL(myBlob);
  link.href = blobUrl;
  const now = new Date();
  const time = now.getHours() + '-' + now.getMinutes()
  link.download = "gps-" + time + ".txt";
  link.innerHTML = "Download file, last updated: " + time.replace('-', ':');
}


function getAddress() {
  const url = 'https://gps-coordinates.org/?lat=' + pt.lat + '&lng=' + pt.lng
  window.open(url)
}
