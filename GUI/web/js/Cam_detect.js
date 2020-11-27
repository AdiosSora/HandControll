function getVideoDevice(){
    const cameraDeviceIds = [/* { deviceId, label } */];
    navigator.mediaDevices.enumerateDevices().then(function(mediaDevices) {
      for (let len = mediaDevices.length, i = 0; i < len; i++) {
        const item = mediaDevices[i];
        // NOTE: カメラデバイスの場合、 kind プロパティには "videoinput" が入っている:
        if (item.kind === "videoinput") {
          const deviceId = item.deviceId;
          const label = item.label;
          // NOTE: ここでデバイスID（とラベル）を適当な変数に保存しておく
          cameraDeviceIds.push({ deviceId, label });

          var select = document.getElementById('device');

      	// option要素を削除（方法はいろいろありますが）
      	while (0 < select.childNodes.length) {
      		select.removeChild(select.childNodes[0]);
      	}

      	// option要素を生成
      	var option = document.createElement('option');
      	var text = document.createTextNode(cameraDeviceIds[0]);
      	option.appendChild(text);

      	// option要素を追加
      	select.appendChild(option);



        }
      }
    });
}
