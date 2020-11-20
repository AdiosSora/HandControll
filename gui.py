import cv2
import numpy as np
from random import randint
import autopy
import PoseAction
clickCount=0
clearCount=0
def drawInferences(values, names=['', '', '', '', '']):
    global clearCount
    global clickCount
    nb_classes              = 5
    left_margin             = 150
    margin                  = 50
    thickness               = 40

    font                    = cv2.FONT_HERSHEY_SIMPLEX
    fontScale               = 1
    fontColor               = (255,255,255)
    lineType                = 2

    blank = np.zeros((450,600,3), np.uint8)

    #いずれかのハンドポーズが70%以上で識別識別した場合　”黄緑色に”　色を変える
    #nb_classesの要素数ループを繰り返す
    for i in range(nb_classes):
        if(values[i] > 0.7):
            cv2.rectangle(blank, (left_margin, margin + int(margin*i)), (left_margin + int(values[i]*200), margin + thickness + int(margin*i)), (0,255,0), -1)
            print(names[i])
            test=PoseAction.checkPose(names,names[i])#testに7割越え識別したポーズの名称が代入される。
            # PoseAction.PoseIgnition(test)
            #if(values[1] > 0.7):
                #autopy.mouse.click(autopy.mouse.Button.RIGHT)
        else:
            cv2.rectangle(blank, (left_margin, margin + int(margin*i)), (left_margin + int(values[i]*200), margin + thickness + int(margin*i)), (255,255,255), -1)
        cv2.putText(blank, names[i], (0, margin + int(margin*i) + int(thickness/2)), font, fontScale, fontColor, lineType)
        cv2.putText(blank, str(values[i]), (left_margin + 200, margin + int(margin*i) + int(thickness/2)), font, fontScale, fontColor, lineType)

    cv2.imshow("Inferences", blank)

            if(values[3]>0.7):#パーの精度が7割以上で１カウント。→５０回でclick動作等のカウントを０clear
                global clearCount
                clearCount+=1
                # print("パー::")
                # print(clearCount)
                if(clearCount>=40):
                    clearCount=0
                    clickCount=0


            if(values[4] > 0.7):#グーの制度が7割以上識別で１カウントする。→50カウントで右クリックイベントが発火
                clickCount+=1
                # print("グー::")
                # print(clickCount)
                if(clickCount>=40):
                    autopy.mouse.click(autopy.mouse.Button.LEFT)
                    clickCount=0

    while(True):


        #valueの要素数を取得し、０から取得した要素数までループ
        for i in range(len(values)):

            #0.0～1.0までの数をランダムでvalue[i]に代入する
            values[i] = randint(0,100)/100

        #drawInferences:描画する
        drawInferences(values, names)

        #qを押下するとプログラム終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    #全ての画面を閉じる
    cv2.destroyAllWindows()

#コマンドラインでgui.pyを実行したときのみの処理
if __name__ == "__main__":
    test()
