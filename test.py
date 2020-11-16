import autopy
import math
import time
import random
import sys
width, height = autopy.screen.size()
# autopy.mouse.pos()

clickCount=0
print(clickCount)

# print(width)
# print("\n")
# print(height)
# #マウスの位置取得
# print(autopy.mouse.location())
# #マウス移動
# autopy.mouse.move(10, 520)
# autopy.mouse.toggle(autopy.mouse.Button.LEFT,True)
# autopy.mouse.move(14, 524)
# # autopy.mouse.smooth_move(0, 900)
#
# #クリック
# #autopy.mouse.click(autopy.mouse.Button.RIGHT)
#
# #ドラッグアンドドロップ
# #押し続ける
# #autopy.mouse.toggle(autopy.mouse.Button.LEFT,True)
# #ディレイ０．０３２が限界
# time.sleep(0.032)
# autopy.mouse.move(800,800)
#
# #autopy.mouse.smooth_move(900,10,1)
# #離す
# autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)
# # time.sleep(0.5)
# # autopy.mouse.toggle(None,True)
# # autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)
#
#
#
#
#
# # TWO_PI = math.pi * 2.0
# #
# #
# # def sine_mouse_wave():
# #     """
# #     Moves the mouse in a sine wave from the left edge of
# #     the screen to the right.
# #     """
# #     width, height = autopy.screen.size()
# #     height /= 2
# #     height -= 10  # Stay in the screen bounds.
# #
# #     for x in range(int(width)):
# #         y = int(height * math.sin((TWO_PI * x) / width) + height)
# #         autopy.mouse.move(x, y)
# #         time.sleep(random.uniform(0.001, 0.003))
# #
# #
# # sine_mouse_wave()
