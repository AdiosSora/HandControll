import eel
import base64
import cv2 as cv
import time
import datetime
import traceback
import autopy

flg_sys = 0 #終了ボタンを押されたかのフラグ
width,height = autopy.screen.size()

@eel.expose
def open_endpage():
    #終了画面の、 endpage.html を立ち上げる
    eel.start("html/endpage.html",
                mode='chrome',
                size=(500,500),  #サイズ指定（横, 縦）
                position=(width/2-250, height/2-250), #位置指定（left, top）
                block=False
                )
    eel.sleep(0.01)

@eel.expose
def py_sysclose():
    #正常終了する場合のフラグを立てる
    global flg_sys
    flg_sys = 1

def start_gui(output_frame, cnt_gui, cnt_pose, name_pose, flg_restart, flg_start, keep_flg):
    if(cnt_gui == 0):   #初回時のみにeel.init、eel.start起動、以降起動しない（cnt_guiが1と固定になるため）

        #ここから、簡易的な画面(手の画像なし)の test.html へ遷移
        global flg_sys
        flg_sys = 0
        eel.init("GUI/web")
        eel.start("html/test.html",
                    mode='chrome',
                    size=(250,100),  #サイズ指定（横, 縦）
                    position=(width,height), #位置指定（left, top）
                    block=False
                    )
        #ここまで test.html 、Recognize.html を使用しない場合はこの範囲をコメントアウト

        #ここから、手の画像付きの今までの画面の Recognize.html へ遷移
#        eel.init('GUI/web')
#        eel.start(
#        'html/Recognize.html',
#             mode='chrome',
#            cmdline_args=['--start-fullscreen'],
#        block=False)
        #ここまでRecognize.html 、test.html を使用しない場合はこの範囲をコメントアウト

        print("htmlスタート！！！")
        #cnt_gui = 1
    elif(cnt_gui == 2): #カメラが切断された際に Recognize.html を閉じる
        eel.windowclose()
        return cnt_gui, flg_sys, flg_restart, flg_start, keep_flg
        #while True:
            #start_time = time.time()
    try:    #Recognize.htmlが × をクリックして終了した場合をキャッチ
        eel.sleep(0.01) #コメントアウトするとindex.htmlにつながらないっぽい
        #flg_restart = 0
            # カメラキャプチャ #####################################################
            #ret, frame = cap.read()
            #if not ret:
                #continue
            #output_frame = output_q.get()
        #if(flg_sys == 1):
            #print("強制終了！！！！")
            #return cnt_gui, flg_sys

        #ここから、Recognize.html を使うときに使用
#        if(output_frame is not None):
            # UI側へ転送(画像) #####################################################
#            _, imencode_image = cv.imencode('.jpg', output_frame)
#            base64_image = base64.b64encode(imencode_image)
#            eel.set_base64image("data:image/jpg;base64," +
#                                        base64_image.decode("ascii"))
        #ここまで、Recognize.html を使うときに使用

        eel.set_posegauge(cnt_pose, name_pose)

        #ここから、test.html を使うときに使用
        if(flg_sys == 1):
            eel.sys_close()
        #ここまで、test.html を使うときに使用
        
        cnt_gui = 1
        return cnt_gui, flg_sys, flg_restart, flg_start, keep_flg

    except: # SystemExit as sys_e:
        traceback.print_exc()
        #print("強制終了！！！！")
        if(cnt_gui == 0 and flg_restart == 0):
            #初回起動時はここに飛ばし、cnt_gui の変更だけ実施
            #print("1")
            cnt_gui = 1
        #再起動した際にすでに eel が起動しているか判定
        elif(flg_restart == 1):
            #HandPose.py 実行中にカメラが切断された際はここに飛ばし、 flg_restart の変更だけ実施
            #print("2")
            flg_restart = 0
            #if(flg_start == 1):
                #開始時点でカメラが消失していた場合は、
                #こちらで eel を再起動し、× をクリックした際の動作を実行
                #flg_start = 0
                #eel.init('GUI/web/html')
                #eel.start(
                #'Recognize.html',
                #mode='chrome',
                #cmdline_args=['--start-fullscreen'],
                #block=False)
                #print("再起動！！！！")
        elif(cnt_gui == 1):
            if(keep_flg == 1):
                #Main.py で connect.html を立ち上げていた際はここに飛ばし、keep_flg の変更だけ行う
                keep_flg = 0
                #print("3")
            else:
                #Recognize.html で × をクリックして終了した場合の例外処理
                #print("4")

                #ここから、test.html を使うときに使用
                eel.init("GUI/web")
                #eel.start("開きたい上記のフォルダ下のファイル名",～
                eel.start("html/test.html",
                            mode='chrome',
                            size=(250,100),  #サイズ指定（横, 縦）
                            position=(width,height), #位置指定（left, top）
                            block=False
                            )
                #ここまで、test.html を使うときに使用

                #ここから、Recognize.html を使うときに使用
#                eel.init('GUI/web')
#                eel.start(
#                'html/Recognize.html',
#                mode='chrome',
#                cmdline_args=['--start-fullscreen'],
#                block=False)
                #ここまで、Recognize.html を使うときに使用

                print("再起動！！！！")
        return cnt_gui, flg_sys, flg_restart, flg_start, keep_flg

def cam_source():
    eel.init('GUI/web')
    eel.start('html/Check.html',block=False)
    num = eel.js_function()()
    print(num)
    return int(num)
