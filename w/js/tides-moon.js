"use strict";

function getTS(date) {
  const time = date.toTimeString();
  const ts = date.toISOString().replace(/-/g, '').substr(0, 8) + ' ' + time.substr(0, 5);
  return ts
}

function getTides() {
  const today = new Date();
  const ts1 = getTS(today);
  const tomorrow = new Date(today.getTime() + 24 * 60 * 60 * 1000);
  const ts2 = getTS(tomorrow);
  const url = 'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date=' + ts1 +
    '&end_date=' + ts2 + '&station=8443970&product=predictions&interval=15&datum=mllw' +
    '&units=english&time_zone=lst_ldt&application=web_services&format=json';
  console.log(url)
  try {
    const js = readText(url)
    const w = JSON.parse(js)
    const predictions = w.predictions
    const link = getTidesLink(predictions)
    console.log(link)
    return link
  } catch (err) {
    console.log('ERR2 ' + err.message)
    console.log(err.stack)
    return ''
  }
}

function getTidesLink(predictions) {
  const isTideBecomingLow = Number(predictions[0].v) > Number(predictions[1].v);
  console.log(isTideBecomingLow)
  console.log(predictions)
  if (isTideBecomingLow) {
    const lowTideIndex = getLowTideIndex(0, predictions)
    const highTideIndex = getHighTideIndex(lowTideIndex + 1, predictions)
    console.log('low ' + lowTideIndex + ' high ' + highTideIndex)
    let lowTideTime = removeLeadingZero(predictions[lowTideIndex].t.substr(11));
    let highTideTime = removeLeadingZero(predictions[highTideIndex].t.substr(11));
    var nextTide = lowTideTime +
      ' ⬇️</br>' + highTideTime + ' H'
    var details = 'Low tide: ' + predictions[lowTideIndex].v + ' ft, @ ' + predictions[lowTideIndex].t +
      ';\n  High tide: ' + predictions[highTideIndex].v + ' ft, @ ' + predictions[highTideIndex].t
  } else {
    const highTideIndex = getHighTideIndex(0, predictions)
    const lowTideIndex = getLowTideIndex(highTideIndex + 1, predictions)
    console.log('high ' + highTideIndex + ' low ' + lowTideIndex)
    let lowTideTime = removeLeadingZero(predictions[lowTideIndex].t.substr(11));
    let highTideTime = removeLeadingZero(predictions[highTideIndex].t.substr(11));
    var nextTide = highTideTime +
      ' ⬆️</br>' + lowTideTime + ' L'
    var details = 'High tide: ' + predictions[highTideIndex].v + ' ft, @ ' + predictions[highTideIndex].t +
      ';\n  Low tide: ' + predictions[lowTideIndex].v + ' ft, @ ' + predictions[lowTideIndex].t
  }
  console.log(nextTide)
  const link = '<a href="https://tidesandcurrents.noaa.gov/stationhome.html?id=8443970" title="' +
    details + '">' + nextTide + '</a>'
  return link
}


function removeLeadingZero(time) {
  if (time.charAt(0) == '0') {
    time = '&nbsp; ' + time.substr(1);
  }
  return time;
}


function getLowTideIndex(iStart, ar) {
  let minHeight = Number(ar[iStart].v);
  for (var i = iStart + 1; i < ar.length; i++) {
    const waterHeight = Number(ar[i].v)
    if (waterHeight < minHeight)
      minHeight = waterHeight;
    else
      return i - 1;
  }
  return ar.length;
}

function getHighTideIndex(iStart, ar) {
  let maxHeight = Number(ar[iStart].v);
  console.log(maxHeight)
  for (var i = iStart + 1; i < ar.length; i++) {
    const waterHeight = Number(ar[i].v)
    console.log(i + ' ' + ar[i].v + ' ' + maxHeight + ' ' + (ar[i].v > maxHeight))
    if (waterHeight > maxHeight)
      maxHeight = waterHeight;
    else
      return i - 1;
  }
  return ar.length;
}

function getWaterTemperature() {
  const today = new Date();
  const ts2 = getTS(today);
  const yesterday = new Date(today.getTime() - 24 * 60 * 60 * 1000);
  const ts1 = getTS(yesterday);
  const url = 'https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date=' + ts1 +
    '&end_date=' + ts2 + '&station=8443970&product=water_temperature&interval=h' +
    '&units=english&time_zone=lst_ldt&application=web_services&format=json';

  console.log(url)
  try {
    const js = readText(url)
    const w = JSON.parse(js)
    const data = w.data
    if (typeof data == 'undefined')
      return ''
    const link = getWaterTemperatureLink(data)
    return link
  } catch (err) {
    console.log('ERR3 ' + err.message)
    console.log(err.stack)
    return ''
  }
}

function getWaterTemperatureLink(data) {
  let min = 100;
  let max = -100;
  let total = 0.0;
  let n = 0;
  for (var i = 0; i < data.length; i++) {
    const t = Number(data[i].v)
    if (t == 0)
      continue;
    n += 1
    total = total + t
    if (t < min)
      min = t;
    if (t > max)
      max = t;
  }
  const average = Math.round(total / n)
  const details = 'Last 24 hr. min/max/ave\nwater temp: ' + Math.round(min) +
    '/' + Math.round(max) + '/' + average
  const link = '<a href="https://tidesandcurrents.noaa.gov/stationhome.html?id=8443970" title="' +
    details + '°">' + average + '°</a>'
  return link
}


function getMoonPhase() {
  const new_moon_ms = new Date(2019, 4, 4, 18, 45, 0, 0).getTime();
  // May 4	6:45 pm;  selected arbitrarily from  https://www.timeanddate.com/moon/phases/usa/boston
  const synodic_month_ms = 29 * 24 * 60 * 60000 + 12 * 60 * 60000 + 44 * 60000 + 2802;
  //29 d 12 h 44 m 2.8016 s   https://en.wikipedia.org/wiki/Lunar_month
  const periods = ((new Date()).getTime() - new_moon_ms) / synodic_month_ms
  const fraction = periods - Math.trunc(periods)
  if (fraction <= .12) {
    emoji = '🌑'
  } else if (fraction <= .21) {
    emoji = '️🌒'
  } else if (fraction <= .31) {
    emoji = '🌓'
  } else if (fraction <= .38) {
    emoji = '🌔️'
  } else if (fraction <= .62) {
    emoji = '🌕️'
  } else if (fraction <= .69) {
    emoji = '🌖'
  } else if (fraction <= .79) {
    emoji = '️🌗'
  } else if (fraction <= .88) {
    emoji = '🌘'
  } else {
    emoji = '🌑'
  }
  const trend = fraction < .5 ? " ⬆️" : " ⬇️"
  full_moon_ms = Math.trunc(periods) * synodic_month_ms + synodic_month_ms / 2
  if (fraction > .5) {
    full_moon_ms += synodic_month_ms
  }
  next_full_moon_dt = '' + new Date(new_moon_ms + full_moon_ms)
  let html = '<a href="https://www.almanac.com/astronomy/moon/calendar/MA/Boston" title="full moon on ' +
    next_full_moon_dt.substr(0, 10) + '">';
  html += emoji + trend + '</a>'
  return html
}

try {
  const html = '<table><tr><td> &emsp; &emsp; </td><td>' + getTides() + '</br>' + getWaterTemperature() +
    '</td><td> &emsp; &emsp; </td><td>' + getMoonPhase() + '</td></tr></table>'
  self.postMessage(html);
} catch (err) {
  console.log(err.message)
  console.log(err.stack)
  self.postMessage('almanac ERR: ' + err.message)
}
