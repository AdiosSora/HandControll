import eel
import base64
import cv2 as cv
import time
import datetime


def start_gui(output_q, cropped_output_q):
    #eel.init("GUI")
    #eel.start('index.html', block=False)
    flg = 0
    i = 0
    while i<100:
        if(flg == 0):
            eel.init("GUI")
            eel.start('index.html', block=False)
            flg = 1
        if(output_q is None):
            break
        eel.sleep(0.01)
        output_frame = output_q.get()
            #cropped_output = cropped_output_q.get()


            #if (cropped_output is not None):
                    #切り取った画像をBGR形式からRGB形式へ変更する。
            #    _, imencode_image = cv.imencode('.jpg', cropped_output)
            #    base64_image = base64.b64encode(imencode_image)
            #    eel.set_base64image("data:image/jpg;base64," + base64_image.decode("ascii"))

                # print("frame ",  index, num_frames, elapsed_time, fps)
            #print("cropped_output!!!!!!!!!")


        if (output_frame is not None):

            _, imencode_image = cv.imencode('.jpg', output_frame)
            base64_image2 = base64.b64encode(imencode_image)
            eel.set_base64image2("data:image/jpg;base64," + base64_image2.decode("ascii"))

    print("hand_gui.py終了！！！")
    #print("cnt_gui=",cnt_gui)
    #return cnt_gui+1
