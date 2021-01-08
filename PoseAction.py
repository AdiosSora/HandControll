import autopy
import tkinter as tk
import time


def checkPose(x, y,Namelist,poseName,poseCount,moveCount):#識別が7割超えたポーズがどれかを判定し、それぞれのイベントを発火する。
    i=0
    # print(poseCount)


    #7割り超えポーズがパーであった場合は瞬時にマウス移動を実行し、処理を終了する
        # autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)

        # poseCount=[0,0,0,0,0,0]#ドラッグ動作をさせるポーズの名前番地のカウントを０clear。ドラックのカウントclearで必要。
        # return poseCount
    if(poseName=="Palm"):
        autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)

    if(poseName=="Dang"):
        pointerMoveDang(x,y,moveCount)

    for tmp in Namelist:#
        if(Namelist[i]!=poseName and poseName!="Garbage"):#ゴミのインデントをスキップする
            i+=1
        else:
            if(poseName!="Garbage"):
                poseCount[i]+=1
                if(poseCount[i]>=5):#条件の右の数だけポーズ識別で各動作を開始
                        if(str(Namelist[i])=="Dang"):#グーの動作
                            print("グー")
                            poseCount=pose_Drag(poseCount,i)
                        if(str(Namelist[i])=="Seri"):#チョキの動作
                            poseCount=[0,0,0,0,0,0]
                            pose_Click_left()
                        if(str(Namelist[i])=="Rock"):#wishの動作
                            poseCount=pose_Click_right(poseCount,i)
                        if(str(Namelist[i])=="Three"):
                            poseCount=[0,0,0,0,0,0]
                            pose_doubleClick_left()
                        if(str(Namelist[i])=="Palm"):
                            poseCount=[0,0,0,0,0,0]
                            moveCount[2]=0
            break
    return poseCount,moveCount



def pose_Click_left():
    print("Click_left!!!!")
    autopy.mouse.click(autopy.mouse.Button.LEFT)

def pose_doubleClick_left():
    print("Click_left!!!!")
    autopy.mouse.click(autopy.mouse.Button.LEFT)
    autopy.mouse.click(autopy.mouse.Button.LEFT)

def pose_Click_right(poseCount,i):
    if(poseCount[i]==5):
        print("Click_right!!!!")
        autopy.mouse.click(autopy.mouse.Button.RIGHT)
    else:
        poseCount[i]=5
    return poseCount

def pose_Drag(poseCount,i):
    print("ドラッグ")
    if(poseCount[i]==5):#ドラッグのポーズを連続で識別した場合、連打する判定が生まれていたためこのifが必要。
        print("ドラッグアンドdrop")
        autopy.mouse.toggle(autopy.mouse.Button.LEFT,True)
    else:
        poseCount[i]=5
    return poseCount

def pose_Drop():
    print("Drop!!!!")
    #autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)
    #l=0
#ポインターの移動
def pointerMove(x,y,moveCount):
    history_x,history_y = autopy.mouse.location()

    #前回座標との差を算出
    abs_x = history_x-x
    abs_y = history_y-y
    #差が一定値大きかった場合のみ座標の移動を行う
    if(abs(abs_x)>70 or abs(abs_y)>70):
        #値が超えても1回目の移動は無視する
        moveCount[1]+=1
        if(moveCount[1]>1):
            i = 1
            moveCount[1]=0
            #中点の算出および移動
            for i in range(25):
                try:
                    autopy.mouse.move(history_x-(abs_x//25)*i,history_y-(abs_y//25)*i)
                except Exception as e:
                    print(e)
                time.sleep(0.00001)
    else:
        #差が一定値未満だった場合の処理（細かい操作のため）
        #再マッピングを行うためのカウント
        moveCount[0]+=1
        #カウントが５０を超えたら再マッピングを行う
        if(moveCount[0]>50):
                try:
                    for i in range(5):
                        autopy.mouse.move(history_x-(abs_x//5)*i,history_y-(abs_y//5)*i)
                        time.sleep(0.00001)
                except Exception as e:
                    print(e)
                moveCount[0] = 0


    return moveCount

def pointerMoveDang(x,y,moveCount):
    history_x,history_y = autopy.mouse.location()


    try:
        #前回座標との差を算出
        abs_x = history_x-x
        abs_y = history_y-y

        #差が一定値大きかった場合のみ座標の移動を行う
        if(abs(abs_x)>75 or abs(abs_y)>75):
            moveCount[2]+=1
            if(moveCount[2]>12):
                i = 1
                for i in range(20):
                        autopy.mouse.move(history_x-(abs_x//20)*i,history_y-(abs_y//20)*i)
                        time.sleep(0.00001)

        else:
            #差が一定値未満だった場合の処理（細かい操作のため）
            #再マッピングを行うためのカウント
            moveCount[3]+=1
            if(moveCount[3]>50):
                    try:
                        for i in range(20):
                            autopy.mouse.move(history_x-(abs_x//20)*i,history_y-(abs_y//20)*i)
                            time.sleep(0.00001)
                    except Exception as e:
                        print(e)
                    moveCount[3] = 0

    except Exception as e:
        print(e)




        # if(abs(abs_x)>20 and abs(abs_y)<30):
        #     print('xmove')
        #     k = 1
        #     for k in range(5):
        #         autopy.mouse.move(history_x-(abs_x//5)*k,history_y)
        #         time.sleep(0.0001)
        #
        # if(abs(abs_x)<30 and abs(abs_y)>20):
        #     print('ymove')
        #     j = 1
        #     for j in range(5):
        #         autopy.mouse.move(history_x,history_y-(abs_y//5)*j)
        #         time.sleep(0.0001)
