import cv2
import numpy as np
from random import randint
import autopy

def drawInferences(values, names=['', '', '', '']):
    nb_classes              = 4
    left_margin             = 150
    margin                  = 50
    thickness               = 40

    font                    = cv2.FONT_HERSHEY_SIMPLEX
    fontScale               = 1
    fontColor               = (255,255,255)
    lineType                = 2

    blank = np.zeros((450,650,3), np.uint8)


    #プロンプト色変換場所
    #25行目
    for i in range(nb_classes):
        if(values[i] > 0.7):
            cv2.rectangle(blank, (left_margin, margin + int(margin*i)), (left_margin + int(values[i]*200), margin + thickness + int(margin*i)), (0,255,0), -1)
            #if(values[2] > 0.7):
                #autopy.mouse.click(autopy.mouse.Button.RIGHT)
        else:
            cv2.rectangle(blank, (left_margin, margin + int(margin*i)), (left_margin + int(values[i]*200), margin + thickness + int(margin*i)), (255,255,255), -1)
        cv2.putText(blank, names[i], (0, margin + int(margin*i) + int(thickness/2)), font, fontScale, fontColor, lineType)
        cv2.putText(blank, str(values[i]), (left_margin + 200, margin + int(margin*i) + int(thickness/2)), font, fontScale, fontColor, lineType)

    cv2.imshow("Inferences", blank)

def test():
    values = [0.2, 0.3, 0.2,0.2]
    names = ['Garbage','Palm','Rock','Ok']
    while(True):
        for i in range(len(values)):
            values[i] = randint(0, 100)/100
        drawInferences(values, names)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test()
