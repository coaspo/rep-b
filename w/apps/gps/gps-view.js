function display() {
  const element = document.getElementById(arguments[0]);
  text = ''
  for (j = 1; j < arguments.length; j++) {
    text += arguments[j]
  }
  if (element == null) {
    alert('Cannot find id: ' + arguments[0] +
      '\n fill-n text: ' + text)
    return
  }
  element.innerHTML = text
}
