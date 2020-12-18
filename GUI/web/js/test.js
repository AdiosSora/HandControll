function clickBtn1(){
  eel.open_endpage();
}

function end_ok(){
  eel.py_sysclose();
  window.close();
}

function end_no(){
  window.close();
}

eel.expose(sys_close);
function sys_close() {
    window.close();
}

eel.expose(windowclose)
function windowclose(){
  window.close();
}

eel.expose(set_posegauge);
function set_posegauge(cnt_pose, name_pose){

  /*７割越えのポーズのゲージのみを取得したい場合はこれ*/
  var target = document.getElementById("poseGuage");

  target.innerHTML = cnt_pose + '回，' + name_pose + '<meter max= "100" min= "0" low= "20" high= "80" optimum= "90" value= ' + cnt_pose +'></meter>';

}
