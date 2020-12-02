import autopy
import tkinter as tk

def checkPose(x, y,Namelist,poseName,poseCount):#識別が7割超えたポーズがどれかを判定し、それぞれのイベントを発火する。
    print(poseCount)


    if(poseName=="Palm"):#7割り超えポーズがパーであった場合は瞬時にマウス移動を実行し、処理を終了する
        pointerMove(x,y)
        return poseCount


    i=0
    for tmp in Namelist:#
        if(Namelist[i]!=poseName and poseName!="Garbage"):
            i+=1
        else:
            if(poseName!="Garbage" and poseName!="Palm"):
                poseCount[i]+=1
                if(poseCount[i]>=40):
                        if(str(Namelist[i])=="Dang"):
                            print("ドラッグアンドdrop")
                            poseCount[i]=0

                        if(str(Namelist[i])=="Peace"):
                            print("クリック")
                            poseCount[i]=0

                        if(str(Namelist[i])=="Rock"):
                            print("右クリック")
                            poseCount[i]=0
            break
    return poseCount





def pose_Click_left():
    print("Click_left!!!!")
    #autopy.mouse.click(autopy.mouse.Button.LEFT)

def pose_doubleClick_left():
    print("Click_left!!!!")
    #autopy.mouse.click(autopy.mouse.Button.LEFT)
    #autopy.mouse.click(autopy.mouse.Button.LEFT)

def pose_Drag():
    print("Drag!!!!")
    #autopy.mouse.toggle(autopy.mouse.Button.LEFT,True)
    #l=0

def pose_Drop():
    print("Drop!!!!")
    #autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)
    #l=0

def pointerMove(x,y):
    print("pointerMove!!!!")
    try:
        autopy.mouse.move(x,y)
        #autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)
    except:
        print("outof")
