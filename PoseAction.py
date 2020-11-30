import autopy
import tkinter as tk

def checkPose(x, y,Namelist,poseName,poseCount):#識別が7割超えたポーズがどれかを判定し、それぞれのイベントを発火する。
    # global i
    # if not poseCount:
    #     for tmp in Namelist:
    #         poseCount.append(0)
    i=0
    #if poseName=="Palm":
            #pointerMove(x,y)
            #print("out ob bound　ポインター")
    #return poseCount
    for tmp in Namelist:
        if(str(Namelist[i])==str(poseName)and poseName!="Garbage"):
            #poseCount[i]+=1
            print(poseCount)

            #識別が50を超えたか識別。
            for l in poseCount:
                if(poseName=="Dang"):
                    if(l > 500 and poseCount[4] == 1):
                        if(poseCount[3]==1):
                            pointerMove(x,y)
                            poseCount[0]+=1
                        else:
                            pose_Drag(l)
                            poseCount[3]=1
                            poseCount[0]+=1
                    else:
                        poseCount[0]+=1
                    poseCount[4]=1
                elif(poseName=="Palm"):
                    if(poseCount[0] <= 500 and poseCount[4] == 1):
                        pose_Click_left(l)
                        poseCount[0]=0
                    elif(poseCount[3]==1):
                        pose_Drop(l)
                        poseCount[3]=0
                        poseCount[0]=0
                    else:
                        pointerMove(x,y)
                        poseCount[0]=0
                    poseCount[4]=0
                #poseCount[i]=0

            # return poseCount
            #todo(switch文で)
        else:
            i+=1
    return poseCount



def pose_Click_left(l):
    print("Click_left!!!!")
    #autopy.mouse.click(autopy.mouse.Button.LEFT)

def pose_doubleClick_left():
    print("Click_left!!!!")
    #autopy.mouse.click(autopy.mouse.Button.LEFT)
    #autopy.mouse.click(autopy.mouse.Button.LEFT)

def pose_Drag(l):
    print("Drag!!!!")
    #autopy.mouse.toggle(autopy.mouse.Button.LEFT,True)
    #l=0

def pose_Drop(l):
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
