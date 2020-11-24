import autopy

def checkPose(Namelist,poseName,poseCount):#識別が7割超えたポーズがどれかを判定し、それぞれのイベントを発火する。
    # global i
    # if not poseCount:
    #     for tmp in Namelist:
    #         poseCount.append(0)
    action=["","","",""]
    i=0
    for tmp in Namelist:
        if(str(Namelist[i])==str(poseName)and poseName!="Garbage"):
            poseCount[i]+=1
            print(poseCount)

            #識別が50を超えたか識別。
            for l in poseCount:
                if(l>=50):
                    print("50over!!")

                    #識別が50を超えたポーズで指定の動作
                    if poseName=="Ok":
                        pose_Click_left()
                    elif poseName=="Palm":
                        pointerMove()
                    elif poseName=="Rock":
                        pose_Click_Right()

                    poseCount[i]=0

            # return poseCount
            #todo(switch文で)
        else:
            i+=1
    return poseCount



def pose_Click_left():#OKの時発火
    print("Click_left!!!!")

def pose_Click_Right():#グーの時発火
    print("Click_Right!!!!")
    autopy.mouse.click(autopy.mouse.Button.RIGHT)

def pose_Drug_Drop():#空白の処理
    print("Drug_Drop!!!!")

def pointerMove():#パーの時発火
    print("pointerMove!!!!")
