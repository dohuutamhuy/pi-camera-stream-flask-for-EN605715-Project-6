function getData() {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open( "GET", '/gps_feed', false ); // false for synchronous request
  xmlHttp.send();
  document.getElementById('gps').innerHTML = xmlHttp.responseText;
  setTimeout(getData, 1000);
}

function getImg() {
  var canvas = document.getElementById("img_canvas");
  var ctx = canvas.getContext("2d");
  var img = new Image;
  img.src = "video_feed"
  ctx.drawImage(img, 10, 10);
  setTimeout(getImg, 100);
};


getData();
getImg();
