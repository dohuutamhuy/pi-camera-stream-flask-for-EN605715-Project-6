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
  setTimeout(getImg, 65);
};

function getIMU() {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open( "GET", '/imu_feed', false ); // false for synchronous request
  xmlHttp.send();
  latest_msg = xmlHttp.responseText;
  if (!latest_msg.includes("Failed")) {
    document.getElementById("imu").innerHTML = "Latest Data:  " + latest_msg;
  var item = document.createElement("li");
  item.innerHTML = latest_msg;
  document.getElementById("all_imu").appendChild(item);
  $("#all_imu").animate({
    scrollTop: $("#all_imu").prop("scrollHeight"),
  }, 300);
  }
  setTimeout(getIMU, 350);
}

// Old get IMU
// function getIMU() {
//   var xhr = new XMLHttpRequest();
//   xhr.open('GET', "/imu_feed");
//   xhr.send();
//   var position = 0;
//   function handleNewData() {
//       var messages = xhr.responseText.split("\r");
//       if (messages.length > 500) {
//         setTimeout(getIMU, 1);
//         return;
//       }
//       latest_msg = messages[messages.length-1];
//       if (latest_msg == "") {
//         latest_msg = messages[messages.length-2];        
//       }
//       document.getElementById("imu").innerHTML = "Latest Data:  " + latest_msg;
//       messages.slice(position, -1).forEach(function(value){
//         var item = document.createElement("li");
//         item.innerHTML = value;
//         document.getElementById("all_imu").appendChild(item);
//       })
//       position = messages.length - 1;
//       $("#all_imu").animate({
//         scrollTop: $("#all_imu").prop("scrollHeight"),
//       }, 300);
//       setTimeout(handleNewData, 300);
//   }  
//   handleNewData();
// }

getIMU();
getData();
getImg();
