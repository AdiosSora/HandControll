import autopy
import tkinter as tk



def checkPose(x, y,Namelist,poseName,poseCount):#識別が7割超えたポーズがどれかを判定し、それぞれのイベントを発火する。
    i=0
    print(poseCount)


    if(poseName=="Palm"):#7割り超えポーズがパーであった場合は瞬時にマウス移動を実行し、処理を終了する
        autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)
        pointerMove(x,y)
        poseCount=[0,0,0,0,0,0]#ドラッグ動作をさせるポーズの名前番地のカウントを０clear。ドラックのカウントclearで必要。
        return poseCount

    if(poseName=="Rock"):
        pointerMove(x,y)

    for tmp in Namelist:#
        if(Namelist[i]!=poseName and poseName!="Garbage"):#ゴミのインデントをスキップする
            i+=1
        else:
            if(poseName!="Garbage" and poseName!="Palm"):
                poseCount[i]+=1
                if(poseCount[i]>=15):#条件の右の数だけポーズ識別で各動作を開始
                        if(str(Namelist[i])=="Dang"):#グーの動作
                            print("グー")
                        if(str(Namelist[i])=="Peace"):#チョキの動作
                            poseCount[i]=0

                        if(str(Namelist[i])=="Rock"):#wishの動作
                            poseCount=pose_Drag(poseCount,i)
            break
    return poseCount



def pose_Click_left():
    print("Click_left!!!!")
    #autopy.mouse.click(autopy.mouse.Button.LEFT)

def pose_doubleClick_left():
    print("Click_left!!!!")
    #autopy.mouse.click(autopy.mouse.Button.LEFT)
    #autopy.mouse.click(autopy.mouse.Button.LEFT)

def pose_Drag(poseCount,i):
    print("ドラッグ")
    if(poseCount[i]==15):#ドラッグのポーズを連続で識別した場合、連打する判定が生まれていたためこのifが必要。
        print("ドラッグアンドdrop")
        autopy.mouse.toggle(autopy.mouse.Button.LEFT,True)
    else:
        poseCount[i]=15
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
        if(abs(abs_x)>15 or abs(abs_y)>15):
            autopy.mouse.move(history_x-abs_x//4,history_y-abs_y//4)
            autopy.mouse.move(history_x-abs_x//2,history_y-abs_y//2)
            autopy.mouse.move(history_x-(abs_x//4)*3,history_y-(abs_y//4)*3)
            autopy.mouse.move(x,y)
        #autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)

    except:
        print("outof")
