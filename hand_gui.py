import eel
import base64
import cv2 as cv
import time
import datetime

def start_gui(output_frame, cnt_gui):
    if(cnt_gui == 0):   #初回時のみにeel.init、eel.start起動、以降起動しない（cnt_guiが1と固定になるため）
        eel.init('GUI')
        eel.start(
        'index.html',
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
    if(output_frame is not None):
        # UI側へ転送(画像) #####################################################
        _, imencode_image = cv.imencode('.jpg', output_frame)
        base64_image = base64.b64encode(imencode_image)
        eel.set_base64image("data:image/jpg;base64," +
                                    base64_image.decode("ascii"))

    return cnt_gui

#    key = cv.waitKey(1)
#    if key == 27:  # ESC
#        break
