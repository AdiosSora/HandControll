import autopy

def checkPose(x, y,Namelist,poseName,poseCount):#識別が7割超えたポーズがどれかを判定し、それぞれのイベントを発火する。
    # global i
    # if not poseCount:
    #     for tmp in Namelist:
    #         poseCount.append(0)
    i=0
    dropswitch=0
    if poseName=="Palm":
        pointerMove(x,y)
    for tmp in Namelist:
        if(str(Namelist[i])==str(poseName)and poseName!="Garbage"):
            poseCount[i]+=1
            print(poseCount)

            #識別が50を超えたか識別。
            for l in poseCount:
                if(l<=50 and poseName=="Dang"):
                    dropswitch==1
                    pose_Drag()

                elif(l<=10 and poseName=="Dang"):
                    pose_Click_left()

                elif(dropswitch==1 and l<=10 and poseName=="Palm"):
                    pose_Drop()

                    #識別が50を超えたポーズで指定の動作

                        #pointerMove()
                        #autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)
                    if str(poseName)=="Dang":
                        pose_Click_Right()

                    poseCount[i]=0

            # return poseCount
            #todo(switch文で)
        else:
            i+=1
    return poseCount



def pose_Click_left():#OKの時発火
    print("[AutoPy]Click_left")
    autopy.mouse.click(autopy.mouse.Button.LEFT)

def pose_doubleClick_left():#OKの時発火
    print("Click_left!!!!")
    autopy.mouse.click(autopy.mouse.Button.LEFT)
    autopy.mouse.click(autopy.mouse.Button.LEFT)

def pose_Drag():#グーの時発火
    print("Drag!!!!")
    autopy.mouse.toggle(autopy.mouse.Button.LEFT,True)

def pose_Drop():#空白の処理
    print("Drop!!!!")
    autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)

def pointerMove(x,y):#パーの時発火
    print("pointerMove!!!!")
    try:
        autopy.mouse.move(x,y)
        autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)
    except:
        print("outof")
