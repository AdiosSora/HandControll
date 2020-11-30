from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import win32api
import win32con
import pywintypes

image = PhotoImage(file='Poses/gage.png')
root=tkinter.Tk()
#root.master.wm_attributes("-topmost", True)
#root.master.wm_attributes("-disabled", True)
#root.master.wm_attributes("-transparentcolor", "white")
root.wm_attributes("-transparentcolor", "snow")
#root.attributes("-alpha",0.3)
ttk.Style().configure("TP.TFrame", background="snow")
f=ttk.Frame(master=root,style="TP.TFrame",width="400",height="300")
f.pack()

label=ttk.Label(master=root,image=image,foreground="red",background="snow")
label.place(x=150,y=150)
root.mainloop()
# #img = Image.open('Poses/gage.png')
# img = ImageTk.PhotoImage(img)
#
# label = tkinter.Canvas(width=400, height=300)
# label.place(x=100, y=50) # 左上の座標を指定
#
# #label = tkinter.Label(text='Powered by \nHogeHoge株式会社', font=('メイリオ','40'), fg='snow', bg='white')
# label.master.overrideredirect(True)
# window_width = 700
# window_height = 500
# label.master.geometry(str(window_width) + "x" + str(window_height) + "+400+300")
# label.master.lift()
# label.master.wm_attributes("-topmost", True)
# label.master.wm_attributes("-disabled", True)
# label.master.wm_attributes("-transparentcolor", "white")
#
# hWindow = pywintypes.HANDLE(int(label.master.frame(), 16))
# exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
# win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)
#
#
# def call_back_func():
#     print("call_back_funcの実行")
#     label.quit()
#     # label.destroy()
#     # =============================
#     # 色々と実験しましたが、結局 quit() すれば、mainloopを抜けることができることを発見しました。
#     # destroyではmainloopを抜けられないので、注意されたし。
#     # ==============================
#
#
# label.pack()
# # label.after(3000, call_back_func)
# # label.after(3000, lambda: label.quit())
# label.after(3000, lambda: [print("call_back_funcの実行"), label.quit()])
# label.mainloop()
#
# print("quitを実行すれば、mainloopを抜けることができた。\nめでたし、めでたし。")
# print("mainloopを抜けた後に、目的のアプリを表示させれば、自分の考えた通りの動作になります。")
