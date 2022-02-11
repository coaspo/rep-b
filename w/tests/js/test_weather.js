"use strict";
function testWeatherMain(baseUrl) {
   testTideIndex()
   testGetTidesLink()
   testGetWaterTemperatureLink()
   testReadNoaaWebSite()
}

function testTideIndex() {
   const predictions = [
      { t: "2020-09-15 18:45", v: "4.632" },
      { t: "2020-09-15 22:15", v: "10.853" },
      { t: "2020-09-15 22:30", v: "10.831" },
      { t: "2020-09-16 04:45", v: "-0.404" },
      { t: "2020-09-16 05:00", v: "-0.330" }]
   highTideIndex = getHighTideIndex(0, predictions)
   validate('1 weather.js:getHighTideIndex()   ', 1, highTideIndex);
   lowTideIndex = getLowTideIndex(highTideIndex + 1, predictions)
   validate('2 weather.js:getLowTideIndex()   ', 3, lowTideIndex);
}

function testGetTidesLink() {
   let predictions = [
      { t: "2020-09-15 18:45", v: "4.632" },
      { t: "2020-09-15 22:15", v: "10.853" },
      { t: "2020-09-15 22:30", v: "10.831" },
      { t: "2020-09-16 04:45", v: "-0.404" },
      { t: "2020-09-16 05:00", v: "-0.330" }]
   let link = getTidesLink(predictions)
   let expected = '<a href="https://tidesandcurrents.noaa.gov/stationhome.html?id=8443970" title="High tide: 10.853 ft, @ 2020-09-15 22:15;\n  Low tide: -0.404 ft, @ 2020-09-16 04:45">22:15 ⬆️</br>&nbsp; 4:45 L</a>'
   validate('3 weather.js:getTidesLink()   ', expected, link);
   predictions = [
      { t: "2020-09-15 18:45", v: "-0.599" },
      { t: "2020-09-15 22:15", v: "-0.643" },
      { t: "2020-09-15 22:30", v: "-0.565" },
      { t: "2020-09-16 04:45", v: "0.10" },
      { t: "2020-09-16 05:00", v: "0.05" }]
   link = getTidesLink(predictions)
   expected = '<a href="https://tidesandcurrents.noaa.gov/stationhome.html?id=8443970" title="Low tide: -0.643 ft, @ 2020-09-15 22:15;\n  High tide: 0.10 ft, @ 2020-09-16 04:45">22:15 ⬇️</br>&nbsp; 4:45 H</a>'
   validate('4 weather.js:getTidesLink()   ', expected, link);
}


function testGetWaterTemperatureLink() {
   const data = [
      { t: "2020-09-15 19:00", v: "60.2", f: "0,0,0" },
      { t: "2020-09-15 19:00", v: "65.2", f: "0,0,0" },
      { t: "2020-09-15 19:00", v: "68.2", f: "0,0,0" }]

   const link = getWaterTemperatureLink(data)
   const expected = '<a href="https://tidesandcurrents.noaa.gov/stationhome.html?id=8443970" title="Last 24 hr. min/max/ave\nwater temp: 60/68/65°">65°</a>'
   validate('10 weather.js:getWaterTemperatureLink()   ', expected, link);
}


function testReadNoaaWebSite() {
   // ref:  https://api.tidesandcurrents.noaa.gov/api/prod/
   try {
      const js = readText('https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date=20200915 18:56&end_date=20200915 19:56&station=8443970&product=predictions&interval=15&datum=mllw&units=english&time_zone=lst_ldt&application=web_services&format=json')
      const w = JSON.parse(js)
      validate('5 weather.js:readText()/tide   ', '5', w.predictions.length);
   } catch (err) {
      validate('5 weather.js:readText()/tide   ', '', err);
   }
   try {
      const js = readText('https://api.tidesandcurrents.noaa.gov/api/prod/datagetter?begin_date=20200915 18:56&end_date=20200915 20:56&station=8443970&product=water_temperature&interval=h&units=english&time_zone=lst_ldt&application=web_services&format=json')
      const w = JSON.parse(js)
      console.log(w)
      validate('6 weather.js:readText()/water-temp   ', '2', w.data.length);
   } catch (err) {
      validate('6 weather.js:readText()/water-temp   ', '', err);
   }
}



