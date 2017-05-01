// const listItem = document.createElement('li');
// const listContent = document.createElement('p');
// listItem.setAttribute('class', "list-group-item");
// listItem.setAttribute('data-url', urlbar.value);
// listContent.textContent = urlbar.value;
// listItem.appendChild(listContent);
// favList.appendChild(listItem);
// listItem.addEventListener('click', () => {
//   const url = listItem.getAttribute('data-url');
//   webview.setAttribute('src', url);
// });
//
const exec = require('child_process').exec;
exec('ls -la ./', (err, stdout, stderr) => {
if (err) { console.log(err); }
  console.log(stdout);
});
setInterval(function() { console.log("hoge"); }, 10000);
