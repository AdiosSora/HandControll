import eel
import base64
import cv2 as cv
import time
import datetime

flg_sys = 0#終了ボタンを押されたかのフラグ

@eel.expose
def py_sysclose():
    global flg_sys
    flg_sys = 1

def start_gui(output_frame, cnt_gui, cnt_pose, name_pose):
    try:#Recognize.htmlが × をクリックして終了した場合をキャッチ
        if(cnt_gui == 0):   #初回時のみにeel.init、eel.start起動、以降起動しない（cnt_guiが1と固定になるため）
            eel.init('GUI/web/html')
            eel.start(
            'Recognize.html',
    #        mode='chrome',
    #        cmdline_args=['--start-fullscreen'],
            block=False)
            cnt_gui = 1

    #    while True:
            #start_time = time.time()

        eel.sleep(0.01) #コメントアウトするとindex.htmlにつながらないっぽい

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
        return cnt_gui, flg_sys

    except:#Recognize.htmlが × をクリックして終了した場合の例外処理
        #print("強制終了！！！！")
        eel.init('GUI/web/html')
        eel.start(
        'html/Recognize.html',
#        mode='chrome',
#        cmdline_args=['--start-fullscreen'],
        block=False)
        #print("再起動！！！！")
        return cnt_gui, flg_sys

def cam_source():
    eel.init('GUI/web/html')
    eel.start('Check.html',block=False)
    num = eel.js_function()()
    print(num)
    return int(num)
