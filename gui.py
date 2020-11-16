import cv2
import numpy as np
from random import randint
import autopy
clickCount=0
def drawInferences(values, names=['', '', '', '', '']):
    nb_classes              = 5
    left_margin             = 150
    margin                  = 50
    thickness               = 40

    font                    = cv2.FONT_HERSHEY_SIMPLEX
    fontScale               = 1
    fontColor               = (255,255,255)
    lineType                = 2

    blank = np.zeros((450,650,3), np.uint8)

    #プロンプト色変換場所
    #25行目
    #サイン指定かつ70%以上で検出した場合 "黄緑" 色にゲージが変更、指定したマウス処理を実行
    for i in range(nb_classes):
        if(values[i] > 0.7):
            cv2.rectangle(blank, (left_margin, margin + int(margin*i)), (left_margin + int(values[i]*200), margin + thickness + int(margin*i)), (0,255,0), -1)

            if(values[4] > 0.7):#パーの制度が7割以上識別で１カウントする。→50カウントで右クリックイベントが発火
                global clickCount
                clickCount+=1
                if(clickCount<=50):
                    autopy.mouse.click(autopy.mouse.Button.RIGHT)
                    clickCount=0
        else:
            cv2.rectangle(blank, (left_margin, margin + int(margin*i)), (left_margin + int(values[i]*200), margin + thickness + int(margin*i)), (255,255,255), -1)
        cv2.putText(blank, names[i], (0, margin + int(margin*i) + int(thickness/2)), font, fontScale, fontColor, lineType)
        cv2.putText(blank, str(values[i]), (left_margin + 200, margin + int(margin*i) + int(thickness/2)), font, fontScale, fontColor, lineType)

    cv2.imshow("Inferences", blank)
