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
                if(l>=50):
                    print("50over!!")
                    print(poseName)
                    #識別が50を超えたポーズで指定の動作
                    #if poseName=="Palm":
                        #pointerMove()
                        #autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)
                    if str(poseName)=="Dang":
                        print("Click_Right!!!!")
                        autopy.mouse.toggle(autopy.mouse.Button.LEFT,True)
                        #pose_Click_Right()

                    poseCount[i]=0

            # return poseCount
            #todo(switch文で)
        else:
            i+=1
    return poseCount



def pose_Click_left():#OKの時発火
    print("Click_left!!!!")
    #autopy.mouse.click(autopy.mouse.Button.LEFT)

def pose_Click_Right():#グーの時発火
    print("Click_Right!!!!")
    autopy.mouse.toggle(autopy.mouse.Button.LEFT,True)
    #autopy.mouse.click(autopy.mouse.Button.RIGHT)

def pose_Drug_Drop():#空白の処理
    print("Drug_Drop!!!!")

def pointerMove(x,y):#パーの時発火
        print("pointerMove!!!!")
        autopy.mouse.move(x,y)
        autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)
