
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
    display("speed-ds/dt", mSecKphMph(ds_dt(pt)))
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


