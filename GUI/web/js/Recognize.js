      function clickBtn1(){
      const hidden_box = document.getElementById("hidden_box");

      if(hidden_box.style.display=="block"){
        hidden_box.style.display ="none";
      }else{
       hidden_box.style.display ="block";
      }
    }

    function sysclose(){
      eel.py_sysclose();
      window.close();
    }

    eel.expose(windowclose)
    function windowclose(){
      window.close();
    }
    
    /*
    function window.onbeforeunload(){
      eel.py_sysclose();
    }
    */
    eel.expose(set_elapsedtime);
    function set_elapsedtime(elapsedtime) {
        document.getElementById("elapsedtime").innerHTML = "elapsedtime:" + elapsedtime + "s";
    }

    eel.expose(set_base64image);
    function set_base64image(base64image) {
        document.getElementById("python_video").src = base64image;
    }

    eel.expose(set_posegauge);
    function set_posegauge(cnt_pose, name_pose){
      document.getElementById("getPose").innerHTML = name_pose + "取得";

      /*７割越えのポーズのゲージのみを取得したい場合はこれ*/
      var target = document.getElementById("poseGuage");

      target.innerHTML = cnt_pose + '回，' + name_pose + '<meter max= "100" min= "0" low= "20" high= "80" optimum= "90" value= ' + cnt_pose +'></meter>';

      /*全ポーズのゲージを取得したい場合はこれ
      var target0 = document.getElementById("poseGuage0");
      var target1 = document.getElementById("poseGuage1");
      var target2 = document.getElementById("poseGuage2");
      var target3 = document.getElementById("poseGuage3");
      var target4 = document.getElementById("poseGuage4");

      target0.innerHTML = cnt_pose[0] + '回，Dang<meter max= "100" min= "0" low= "20" high= "80" optimum= "90" value= ' + cnt_pose[0] +'></meter>';
      target1.innerHTML = cnt_pose[1] + '回，Garbage<meter max= "100" min= "0" low= "20" high= "80" optimum= "90" value= ' + cnt_pose[1] +'></meter>';
      target2.innerHTML = cnt_pose[2] + '回，Palm<meter max= "100" min= "0" low= "20" high= "80" optimum= "90" value= ' + cnt_pose[2] +'></meter>';
      target3.innerHTML = cnt_pose[3] + '回，Peace<meter max= "100" min= "0" low= "20" high= "80" optimum= "90" value= ' + cnt_pose[3] +'></meter>';
      target4.innerHTML = cnt_pose[4] + '回，Rock<meter max= "100" min= "0" low= "20" high= "80" optimum= "90" value= ' + cnt_pose[4] +'></meter>';
      */
    }

    /*ここから試作用、不要になったら削除*/
        /*eel.expose(test_clickBtn1);*/
        function test_clickBtn1(){
          /*起動(テスト用ボタン)押下時*/
          eel.start_flg();
          window.close();
        }

        /*eel.expose(test_clickBtn2);*/
        function test_clickBtn2(){
          /*終了(テスト用ボタン)押下時*/
          eel.end_flg();
          window.close();
        }

    /*ここまで試作用、不要になったら削除*/
