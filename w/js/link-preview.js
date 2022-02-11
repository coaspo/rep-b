"use strict";

function enterLink(event) {
  const linkEl = event.target
  console.log('==1 enterLink ===' + event + ' el= ' + linkEl)
  let dialog = document.getElementById("123");
  if (dialog != null) {
    dialog.remove();
    dialog = null
  }
  if (linkEl.href.endsWith('jpg')) {
    return
  }
  linkEl.mouseIsOn = true;
  if (dialog === null) {
    dialog = document.createElement('DIALOG');
    const linkRect = linkEl.getBoundingClientRect()
    console.log(linkEl.href + '--============')
    dialog._href = linkEl.href
    console.log(linkRect.right + '---' + linkRect.bottom)
    dialog._left = linkEl.offsetLeft + 40
    dialog._top = linkEl.offsetTop + 13
    console.log(dialog._left + '- - -' + dialog._top)
    dialog.style.left = dialog._left + 'px'
    dialog.style.top = dialog._top + 'px'
    dialog._link = event.target
    dialog.onmouseleave = leaveDialog
    dialog.onclick = _browseUrl
    dialog.id = '123'
    dialog.setAttribute("open", "open");
    linkEl.parentNode.insertBefore(dialog, linkEl.nextSibling)
    console.log('      created dialog')
  }
  console.log(event.screenX + ' > ' + dialog._left + ' && ' + event.screenY + ' > ' + dialog._top);
  dialog.mouseIsOn = event.screenX > dialog._left && event.screenY > dialog._top;
  if (dialog.innerHTML == '') {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
      if (this.readyState == 4 && this.status == 200) {
        dialog = document.getElementById("123");
        //console.log('   status '+ this.status +'  Estate '+this.readyState);
        dialog.innerHTML = this.responseText + '<br>' + dialog._link;
      }
      else {
        console.log('   ERR?? ' + this.status + '  ERR?? ' + this.readyState);
      }
    };
    xhttp.open("GET", linkEl, true);
    xhttp.setRequestHeader('Access-Control-Allow-Origin', '*');
    xhttp.withCredentials = false;
    //console.log('  send request')
    xhttp.send()
  }
}

function _browseUrl() { // not used
  const dialog = document.getElementById("123");
  window.open(dialog._href, "_top")
}

function leaveLink(event) { // not used
  const linkEl = event.target
  linkEl.mouseIsOn = false;
  console.log('==2 leaveLink === ' + linkEl)
  const dialog = document.getElementById("123");
  //console.log('  dialog '+ dialog);
  if (dialog !== null) {
    dialog.mouseIsOn = event.clientX > dialog._left &&
      event.clientY > dialog._top;
    // console.log(dialog.mouseIsOn)
    if (!dialog.mouseIsOn) {
      dialog.remove();
      //console.log('   removed dialog')
    }
  }
}

function enterDialog() {   // not used
  const dialog = document.getElementById("123");
  // console.log('---1 enterDialog --- '+dialog)
  if (dialog !== null) {
    dialog._mouseIsOn = true;
  }
}

function leaveDialog() {
  const dialog = document.getElementById("123");
  //console.log('---2 leaveDialog --- '+dialog)
  if (dialog !== null) {
    //console.log(dialog._link.mouseIsOn)
    dialog.remove();
    //console.log('  removed dialog')
  }
}

