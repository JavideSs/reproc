from tkinter import ttk
from tkinter import PhotoImage
from ttkthemes import ThemedTk

from program.tab1Music import TabMusic
from program.extraSysTray import ModeTray
from program._config import *


print(author)
w = ThemedTk()
w.set_theme("arc")

w.title('Reproc')
w.geometry("416x480")
w.resizable(False,False)
w.eval('tk::PlaceWindow . center')
w.iconbitmap(folder_img+r"\icon.ico")

t1 = TabMusic(w)
ModeTray(w, t1)

def checkInLoop():
    t1.updateTimeSong()
    w.after(100, checkInLoop)
w.after(1000, checkInLoop)

w.mainloop()