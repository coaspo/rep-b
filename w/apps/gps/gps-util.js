function formatNum(num, decimalDigits) {
  if (num == null) {
    return '-'
  }
  return Number(num.toFixed(decimalDigits))
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

