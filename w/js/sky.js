"use strict";
function degrees(rad) {
  return rad * 180 / Math.PI
}
class Earth {
  static LATIDUDE = 42.5 * Math.PI / 180
}
class Sun {
  constructor(date) {
    this.hourAngle = Sun.hourAngle(date);
    this.declination = Sun.declination(date);
    this.setSunsetSunrise(Earth.LATIDUDE, date)
  }
  static hourAngle(date) {
    const hours = date.getHours() + date.getMinutes() / 60.
    const angle = (hours - 44 / 60) / 24. * 360
    return angle
  }
  static declination(date) {
    const jan1Date = new Date((date.getFullYear(), 0, 1, 0, 0, 0, 0))
    const days = (date - jan1Date) / 1000 / 60 / 60 / 24
    // https://en.wikipedia.org/wiki/Position_of_the_Sun
    const declination = -Math.asin(0.39779 * Math.cos(0.98565 * Math.PI / 180. * (days + 10) +
      1.914 * Math.PI / 180. * Math.sin(0.98565 * Math.PI / 180. * (days - 2))))
    console.log('d=' + (declination * 180 / Math.PI))
    return declination
  }
  setSunsetSunrise(latitude, date) {
    const sin_a = Math.sin(-.83 * Math.PI / 180)
    const sin_f = Math.sin(latitude)
    const cos_f = Math.cos(latitude)
    const sin_d = Math.sin(this.declination)
    const cos_d = Math.cos(this.declination)
    const hourAngle = Math.acos((sin_a - sin_f * sin_d) / cos_f / cos_d) * 180 / Math.PI
    const midHour = date.getTimezoneOffset() === 240 ? 12.5 : 11.5 //  11.5 is for standard time
    this.sunriseHour = midHour - hourAngle / 15
    this.sunsetHour = midHour + hourAngle / 15
    const hours = date.getHours() + date.getMinutes() / 60
    this.isDown = hours < this.sunriseHour || hours > this.sunsetHour
    this.sunriseTime = Sun.hourMin(this.sunriseHour)
    this.sunsetTime = Sun.hourMin(this.sunsetHour)
    console.log(this.sunriseTime)
    console.log(this.sunsetTime)
  }
  static hourMin(decimalTime) {
    const hour = Math.trunc(decimalTime)
    const hh = hour < 13 ? hour : hour - 12
    const minute = Math.trunc((decimalTime - hour) * 60)
    const mm = minute < 10 ? '0' + minute : minute
    return hh + ':' + mm
  }
}
class NorthSky {
  static EQUATOR_RADIUS = 229 // for Betelgeuse  R*cos(7.25 deg)=227 pixels
  static updateNorthSkyCanvas(sun) {
    var ctx = NorthSky.getContext()

    ctx.beginPath();
    // clockwise polygon covers image
    var c = document.getElementById("backgrd");
    ctx.moveTo(0, 0);
    ctx.lineTo(c.width, 0);
    ctx.lineTo(c.width, c.height);
    ctx.lineTo(0, c.width);
    ctx.closePath();
    var southLat = 90 - Earth.LATIDUDE
    // hole to image is clockwise when sun is down
    ctx.ellipse(261, 332, 214, 180, 0, 0, 2 * Math.PI, sun.isDown);
    const backColor = sun.isDown ? 'black' : 'blue'
    ctx.fillStyle = backColor;
    ctx.globalAlpha = sun.isDown ? .2 : .1
    ctx.strokeStyle = "rgba(0.1,0.5,0.5,0)";
    ctx.lineWidth = 1;
    ctx.fill();
    ctx.globalAlpha = 1

    const y = 262 + NorthSky.EQUATOR_RADIUS * Math.sin(Earth.LATIDUDE)
    ctx.font = "20px Arial";
    ctx.fillText("Z", 262, y);
    ctx.fillText("N", 262, 172);
    ctx.fillText("S", 262, 502);
    ctx.fillText("E", 54, 350);
    ctx.fillText("W", 449, 350);
  }
  static update(date, sun) {
    NorthSky.clearCanvas()
    NorthSky.rotate(date)
    const sunRadiusMin = NorthSky.EQUATOR_RADIUS * Math.cos(Earth.LATIDUDE + sun.declination)
    const sunRadiusMax = NorthSky.EQUATOR_RADIUS * Math.cos(sun.declination + Math.PI / 4)
    const sunRadius = sunRadiusMin + Math.abs(.5 * NorthSky.EQUATOR_RADIUS * Math.cos(sun.hourAngle * Math.PI / 180. / 2))
    // .5 is arbitrary
    updateSunriseSunset(sun)
    NorthSky.drawDisc(sun.hourAngle, sunRadius)
    NorthSky.updateNorthSkyCanvas(sun)
  }
  static rotate(date) {
    const angle = NorthSky.daysAngle(date) + Sun.hourAngle(date)
    var stars_img = document.getElementById('stars')
    stars_img.style.transform = 'rotate(-' + angle + 'deg)'
    document.getElementById('date').innerHTML = NorthSky.dateAmPm(date)
  }
  static dateAmPm(date) {
    let ts = date.toString().substr(0, 16)
    let hours = date.getHours()
    let minutes = date.getMinutes()
    const ampm = hours >= 12 ? 'PM' : 'AM'
    hours = hours % 12
    hours = hours ? hours : 12 // the hour '0' should be '12'
    minutes = minutes < 10 ? '0' + minutes : minutes
    ts += ' ' + hours + ':' + minutes + ' ' + ampm
    return ts
  }
  static daysAngle(date) {
    const year = date.getFullYear()
    const spring_equinox_date = new Date(year, 2, 21, 0, 0, 0, 0)
    const days = (date - spring_equinox_date) / 1000 / 60 / 60 / 24.
    const angle = (days / 365.) * 360.
    console.log(angle + ':::::' + date)
    return angle
  }
  static clearCanvas() {
    var c = document.getElementById("backgrd");
    var ctx = c.getContext("2d")
    ctx.clearRect(0, 0, c.width, c.height)
  }
  static getContext() {
    var c = document.getElementById("backgrd");
    var ctx = c.getContext("2d")
    ctx.beginPath()
    return ctx
  }
  static drawDisc(angle, pixelRadius) {
    var ctx = NorthSky.getContext()

    const a = (180 + angle) * Math.PI / 180.
    const x = 262 + Math.round(pixelRadius * Math.sin(a))
    const y = 262 + Math.round(pixelRadius * Math.cos(a))
    ctx.fillStyle = 'red'
    ctx.strokeStyle = 'black';
    ctx.lineWidth = 10;
    ctx.arc(x, y, 5, 0, 2 * Math.PI, 1)
    ctx.fill()
    ctx.setLineDash([10, 5]);//dashes,spaces
    ctx.beginPath();
    ctx.lineWidth = 1;
    ctx.moveTo(262, 262);
    ctx.lineTo(x, y);
    ctx.strokeStyle = 'red';
    ctx.stroke();
  }
}
class SouthSky {
  static updateSouthSkyCanvas(date, sun) {
    var ctx = SouthSky.getContext()

    ctx.beginPath();
    // clockwise polygon covers image
    var c = document.getElementById("backgrd2");
    ctx.moveTo(0, 0);
    ctx.lineTo(c.width, 0);
    ctx.lineTo(c.width, c.height);
    ctx.lineTo(0, c.width);
    ctx.closePath();
    const dayHours = sun.sunsetHour - sun.sunriseHour
    const midHour = (sun.sunsetHour - sun.sunriseHour) / 2
    const jan1Date = new Date(date.getFullYear(), 0, 1, 0, 0, 0, 0)
    const days = (date - jan1Date) / 1000 / 60 / 60 / 24.
    const hour = date.getHours() + date.getMinutes() / 60.
    let x = (days / 365.25 - (hour - 2.5) / 24 - 82. / 360) * 1102 // 1102 is pixel width
    if (x > 1102)
      x = x - 1102
    else if (x < 0)
      x = x + 1102
    const a = (24 - dayHours) / 24 * 1102 / 2
    const y = (45 - degrees(Earth.LATIDUDE)) * 375 / 90
    // hole to image is clockwise when sun is down
    ctx.ellipse(552, y, a, 375, 0, 0, 2 * Math.PI, sun.isDown);
    ctx.closePath();

    var southLat = 90 - Earth.LATIDUDE
    const backColor = sun.isDown ? 'black' : 'blue'
    ctx.fillStyle = backColor;
    ctx.globalAlpha = sun.isDown ? .2 : .1
    ctx.strokeStyle = "rgba(0.1,0.5,0.5,0)";
    ctx.lineWidth = 1;
    ctx.fill();
    ctx.globalAlpha = 1
    const img = document.getElementById('stars2')
    const c2 = document.getElementById("starWindow");
    const ctx2 = c2.getContext("2d");
    ctx2.drawImage(img, x, 0, 1104, 525, 0, 0, 1104, 525);
  }
  static update(date, sun) {
    SouthSky.clearCanvas()
    const sunRadiusMin = NorthSky.EQUATOR_RADIUS * Math.cos(Earth.LATIDUDE + sun.declination)
    const sunRadiusMax = NorthSky.EQUATOR_RADIUS * Math.cos(sun.declination + Math.PI / 4)
    const sunRadius = sunRadiusMin + Math.abs(.5 * NorthSky.EQUATOR_RADIUS * Math.cos(sun.hourAngle * Math.PI / 180. / 2))
    // .5 is arbitrary
    updateSunriseSunset(sun)
    SouthSky.drawSun(sun.hourAngle, sunRadius)
    SouthSky.updateSouthSkyCanvas(date, sun)

  }
  static clearCanvas() {
    var c = document.getElementById("backgrd2");
    var ctx = c.getContext("2d")
    ctx.clearRect(0, 0, c.width, c.height)
  }
  static getContext() {
    var c = document.getElementById("backgrd2");
    var ctx = c.getContext("2d")
    ctx.beginPath()
    return ctx
  }
  static drawSun(angle, pixelRadius) {
    var ctx = SouthSky.getContext()

    let x = (angle / 360) * 1102 // 1102 is pixel width
    if (x > 1102)
      x = x - 1102
    else if (x < 0)
      x = x + 1102

    ctx.fillStyle = 'red'
    ctx.strokeStyle = 'black';
    ctx.lineWidth = 10;
    const y = 375 / 2 + degrees(Earth.LATIDUDE) * 375 / 90 / 2 * Math.cos(angle / 1102)
    ctx.arc(x, y, 5, 0, 2 * Math.PI, 1)
    ctx.fill()
    ctx.setLineDash([10, 5]);//dashes,spaces
    ctx.beginPath();
    ctx.lineWidth = 1;
    ctx.moveTo(x, 0);
    ctx.lineTo(x, y);
    ctx.strokeStyle = 'red';
    ctx.stroke();
  }
}

