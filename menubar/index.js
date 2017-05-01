const {app, BrowserWindow} = require('electron')
const path = require('path')
const url = require('url')

let win
const Menubar = require('menubar');
const menubar = Menubar({width: 1000, height: 800});
console.log(path.join(__dirname + '/index.html'))

menubar.on('ready', function ready () {
  console.log('app is ready')
})
