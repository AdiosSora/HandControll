$(document).ready(function(){
  var select = document.getElementById("selecter");
  var cnt = 0;
  navigator.mediaDevices.enumerateDevices()
  .then(function(devices) {
    devices.forEach(function(device) {
      if(device.kind == "videoinput"){
        var Id = device.deviceId;
        var Label;
        if(device.label.indexOf('(') != -1){
           Label = device.label.slice(0,device.label.indexOf('('));
           Label = document.createTextNode(String(cnt) + " : " + Label);
        }else{
           Label = document.createTextNode(String(cnt) + " : " + device.label);
        }
          console.log(device.label);
          $('#selector').append($('<option>').html(Label).val(Id));
          cnt += 1;

      }
    });
     // エラー発生時
  }).catch(function(err) {
    console.error('カメラの接続に失敗しました', err);
});
});


//カメラプレビュー
  var constraints = { audio: false, video: {
      width: 1920,
      height: 1080,
  }}

  navigator.mediaDevices.getUserMedia(constraints)
    .then(function(stream) {
      var video = document.querySelector('video');
      video.srcObject = stream;
      video.onloadedmetadata = function(e) {
        video.play();
      };
    })
    .catch(function(err) {
      console.log(err.name + ": " + err.message);
    });

//セレクトしたカメラに切り替え
$(function($) {
    $('#selector').change(function() {
        constraints.video.deviceId = $('#selector option:selected').val();
        video.srcObject.getTracks().forEach(track => track.stop())
        navigator.mediaDevices.getUserMedia(constraints)
          .then(function(stream) {
            const video = document.querySelector('video');
            video.srcObject = stream;
            video.onloadedmetadata = function(e) {
              video.play();
            };
          })
          .catch(function(err) {
            console.log(err.name + ": " + err.message);
          });
    });

});

//フレームレスウィンドウを作成する
const BrowerWindow = require('electron').BrowserWindow
var win = new BrowerWindow({width:800, height:600, frame:false , transparent:true, frame:false})

// // 確認ボタンを押したときにカメラが使用できるか確認
// $(function($){
//   $('#check').click(function(){
//     if(video.srcObject.active == false){
//       window.alert('カメラの接続を確認してください');
//     }else{
//       console.log("seikou");
//       // window.location.href = 'complete.html';
//     }
//   });
// });

// eel.expose(js_function);
// function js_function(){
//   return $('#selector option:selected').text().slice(0,1);
// }
