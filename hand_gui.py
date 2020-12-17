import eel
import base64
import cv2 as cv
import time
import datetime
import traceback

flg_sys = 0#終了ボタンを押されたかのフラグ

@eel.expose
def py_sysclose():
    global flg_sys
    flg_sys = 1

def start_gui(output_frame, cnt_gui, cnt_pose, name_pose, flg_restart, flg_start):
    if(cnt_gui == 0):   #初回時のみにeel.init、eel.start起動、以降起動しない（cnt_guiが1と固定になるため）
        eel.init('GUI/web')
        eel.start(
        'html/Recognize.html',
             mode='chrome',
    #        cmdline_args=['--start-fullscreen'],
        block=False)
        print("htmlスタート！！！")
        cnt_gui = 1
    elif(cnt_gui == 2): #カメラが切断された際に Recognize.html を閉じる
        eel.windowclose()
        return cnt_gui, flg_sys, flg_restart, flg_start
    #    while True:
            #start_time = time.time()
    try:#Recognize.htmlが × をクリックして終了した場合をキャッチ
        eel.sleep(0.01) #コメントアウトするとindex.htmlにつながらないっぽい
        #flg_restart = 0
            # カメラキャプチャ #####################################################
            #ret, frame = cap.read()
            #if not ret:
                #continue
    #        output_frame = output_q.get()
    #    if(flg_sys == 1):
    #        print("強制終了！！！！")
    #        return cnt_gui, flg_sys

        if(output_frame is not None):
            # UI側へ転送(画像) #####################################################
            _, imencode_image = cv.imencode('.jpg', output_frame)
            base64_image = base64.b64encode(imencode_image)
            eel.set_base64image("data:image/jpg;base64," +
                                        base64_image.decode("ascii"))

        eel.set_posegauge(cnt_pose, name_pose)
        return cnt_gui, flg_sys, flg_restart, flg_start

    except:# SystemExit as sys_e:#Recognize.htmlが × をクリックして終了した場合の例外処理
        traceback.print_exc()
        #print("強制終了！！！！")
        #再起動した際にすでに eel が起動しているか判定
        if(flg_restart == 1):
            flg_restart = 0
            if(flg_start == 1):
                #開始時点でカメラが消失していた場合は、
                #こちらで eel を再起動し、× をクリックした際の動作を実行
                flg_start = 0
                eel.init('GUI/web/html')
                eel.start(
                'Recognize.html',
        #        mode='chrome',
        #        cmdline_args=['--start-fullscreen'],
                block=False)
                print("再起動！！！！")
        else:
            eel.init('GUI/web')
            eel.start(
            'html/Recognize.html',
    #        mode='chrome',
    #        cmdline_args=['--start-fullscreen'],
            block=False)
            print("再起動！！！！")
        return cnt_gui, flg_sys, flg_restart, flg_start

def cam_source():
    eel.init('GUI/web/html')
    eel.start('Check.html',block=False)
    num = eel.js_function()()
    print(num)
    return int(num)
