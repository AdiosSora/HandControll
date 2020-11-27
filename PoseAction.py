import autopy

def checkPose(x, y,Namelist,poseName,poseCount):#識別が7割超えたポーズがどれかを判定し、それぞれのイベントを発火する。
    # global i
    # if not poseCount:
    #     for tmp in Namelist:
    #         poseCount.append(0)
    i=0
    if poseName=="Palm":
            pointerMove(x,y)
            print("out ob bound　ポインター")
    return poseCount
    for tmp in Namelist:
        if(str(Namelist[i])==str(poseName)and poseName!="Garbage"):
            poseCount[i]+=1
            print(poseCount)

            #識別が50を超えたか識別。
            for l in poseCount:
                if(l<=50 and poseName=="Dang"):
                    #if(poseCount[3]==0)
                        #poseCount[3]+=1
                    if(poseCount[3]==1):
                        pointerMove(x,y)

                    poseCount[3]=1
                    pose_Drag(l)

                #elif(l<=10 and poseName=="Dang"):
                    #and poseCount[3]==0
                    #pose_Click_left(l)

                elif(poseName=="Palm" and poseCount[3]==1):
                    pose_Drop(l)
                    poseCount[3]=0
                    #if str(poseName)=="Dang":
                        #print("Click_Right!!!!")
                        #autopy.mouse.toggle(autopy.mouse.Button.LEFT,True)
                        #pose_Click_Right()
                    #識別が50を超えたポーズで指定の動作

                        #pointerMove()
                        #autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)
                    if str(poseName)=="Dang":
                        pose_Click_Right()

                elif (poseName=="Palm"):
                    pointerMove(x,y)
                poseCount[i]=0

            # return poseCount
            #todo(switch文で)
        else:
            i+=1
    return poseCount



def pose_Click_left(l):
    print("Click_left!!!!")
    autopy.mouse.click(autopy.mouse.Button.LEFT)

def pose_doubleClick_left():
    print("Click_left!!!!")
    autopy.mouse.click(autopy.mouse.Button.LEFT)
    autopy.mouse.click(autopy.mouse.Button.LEFT)

def pose_Drag(l):
    print("Drag!!!!")
    autopy.mouse.toggle(autopy.mouse.Button.LEFT,True)
    l=0

def pose_Drop(l):
    print("Drop!!!!")
    autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)
    l=0

def pointerMove(x,y):
    print("pointerMove!!!!")
    try:
        autopy.mouse.move(x,y)
        autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)
    except:
        print("outof")
