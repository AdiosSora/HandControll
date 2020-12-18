import autopy
import tkinter as tk
import time


def checkPose(x, y,Namelist,poseName,poseCount):#識別が7割超えたポーズがどれかを判定し、それぞれのイベントを発火する。
    i=0
    print(poseCount)


    #7割り超えポーズがパーであった場合は瞬時にマウス移動を実行し、処理を終了する
        # autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)

        # poseCount=[0,0,0,0,0,0]#ドラッグ動作をさせるポーズの名前番地のカウントを０clear。ドラックのカウントclearで必要。
        # return poseCount

    if(poseName=="Dang"):
        pointerMoveDang(x,y)

    for tmp in Namelist:#
        if(Namelist[i]!=poseName and poseName!="Garbage"):#ゴミのインデントをスキップする
            i+=1
        else:
            if(poseName!="Garbage"):
                poseCount[i]+=1
                if(poseCount[i]>=12):#条件の右の数だけポーズ識別で各動作を開始
                        if(str(Namelist[i])=="Dang"):#グーの動作
                            print("グー")
                            poseCount=pose_Drag(poseCount,i)
                        if(str(Namelist[i])=="Seri"):#チョキの動作
                            poseCount=[0,0,0,0,0,0]
                            pose_Click_left()
                        if(str(Namelist[i])=="Rock"):#wishの動作
                            poseCount=[0,0,0,0,0,0]
                            pose_Click_right()
                        if(str(Namelist[i])=="Three"):
                            poseCount=[0,0,0,0,0,0]
                        if(str(Namelist[i])=="Palm"):
                            poseCount=[0,0,0,0,0,0]
                            autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)
            break
    return poseCount



def pose_Click_left():
    print("Click_left!!!!")
    autopy.mouse.click(autopy.mouse.Button.LEFT)

def pose_doubleClick_left():
    print("Click_left!!!!")
    autopy.mouse.click(autopy.mouse.Button.LEFT)
    autopy.mouse.click(autopy.mouse.Button.LEFT)

def pose_Click_right():
    print("Click_right!!!!")
    autopy.mouse.click(autopy.mouse.Button.RIGHT)

def pose_Drag(poseCount,i):
    print("ドラッグ")
    if(poseCount[i]==12):#ドラッグのポーズを連続で識別した場合、連打する判定が生まれていたためこのifが必要。
        print("ドラッグアンドdrop")
        autopy.mouse.toggle(autopy.mouse.Button.LEFT,True)
    else:
        poseCount[i]=12
    return poseCount

def pose_Drop():
    print("Drop!!!!")
    #autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)
    #l=0

def pointerMove(x,y):
    history_x,history_y = autopy.mouse.location()
    try:
        abs_x = history_x-x
        abs_y = history_y-y
        if(abs(abs_x)>20 or abs(abs_y)>20):
            i = 1
            for i in range(20):
                autopy.mouse.move(history_x-(abs_x//20)*i,history_y-(abs_y//20)*i)
                time.sleep(0.0001)
                # autopy.mouse.move(x,y)
            # autopy.mouse.move(x,y)
        #autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)

    except Exception as e:
        print(e)

def pointerMoveDang(x,y):
    history_x,history_y = autopy.mouse.location()
    try:

        abs_x = history_x-x
        abs_y = history_y-y

        if(abs(abs_x)>30 or abs(abs_y)>30):

            i = 1
            for i in range(20):
                autopy.mouse.move(history_x-(abs_x//20)*i,history_y-(abs_y//20)*i)
                time.sleep(0.0001)

    except Exception as e:
        print(e)

#テスト　のち削除
def pointerMove2(x,y):
    history_x,history_y = autopy.mouse.location()
    try:

        abs_x = history_x-x
        abs_y = history_y-y

        if(abs(abs_x)>50 or abs(abs_y)>50):

            i = 1
            for i in range(30):
                autopy.mouse.move(history_x-(abs_x//30)*i,history_y-(abs_y//30)*i)
                time.sleep(0.00001)


        if(abs(abs_x)>20 and abs(abs_y)<30):
            print('xmove')
            k = 1
            for k in range(5):
                autopy.mouse.move(history_x-(abs_x//5)*k,history_y)
                time.sleep(0.0001)

        if(abs(abs_x)<30 and abs(abs_y)>20):
            print('ymove')
            j = 1
            for j in range(5):
                autopy.mouse.move(history_x,history_y-(abs_y//5)*j)
                time.sleep(0.0001)
    except Exception as e:
        print(e)
