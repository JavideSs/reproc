from tkinter import ttk
from tkinter import PhotoImage
from ttkthemes import ThemedTk

import sys

from program.tab1Music import TabMusic
from program._config import *


print(author)
w = ThemedTk()
w.set_theme("arc")

w.title('Reproc')
w.geometry("416x480")
w.resizable(False,False)
w.eval('tk::PlaceWindow . center')

t1 = TabMusic(w)

if sys.platform == "win32":
    from program.extraSysTray import ModeTray
    ModeTray(w, t1)

def checkInLoop():
    t1.updateTimeSong()
    w.after(100, checkInLoop)
w.after(1000, checkInLoop)

w.mainloop()
