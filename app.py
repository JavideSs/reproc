from tkinter import ttk
from tkinter import PhotoImage
from ttkthemes import ThemedTk

from tab1Music import TabMusic
from tab2Download import TabDownload
from extraSysTray import ModeTray
from _iconbase64 import img_tab_music, img_tab_download, img_tab_settings
from _config import *


print(author)
w = ThemedTk()
w.set_theme("arc")  #equilux -> dark

w.title('Reproc')
w.geometry("418x500")
w.resizable(False,False)
w.eval('tk::PlaceWindow . center')
w.configure(background=color_reproc)

style = ttk.Style()
style.map("TNotebook.Tab",foreground=[("selected","#914ecc"),("active","#cca9eb")])
style.configure("TNotebook.Tab",font=("calibri",8))
#Eliminar rectangulo seleccionador
style.layout("TNotebook.Tab",[("Plain.Notebook.tab",{"children":[('Treeitem.image',{"side":"left","sticky":"we"}),("Treeitem.text",{"side":"left","sticky":"we"})]})])

tabs = ttk.Notebook(w); tabs.pack(expand=True, fill='both', padx=(tabs_padd,tabs_padd))
img_tab1 = PhotoImage(data=img_tab_music)
tab1 = ttk.Frame(); tabs.add(tab1, text="  Music Player ", image=img_tab1, pad=(-tabs_padd,0,-tabs_padd,0))
img_tab2 = PhotoImage(data=img_tab_download)
tab2 = ttk.Frame(); tabs.add(tab2, text="  Download      ", image=img_tab2, pad=(-tabs_padd,0,-tabs_padd,0))
img_tab3 = PhotoImage(data=img_tab_settings)
tab3 = ttk.Frame(); tabs.add(tab3, text="  Settings         ", image=img_tab3, pad=(-tabs_padd,0,-tabs_padd,0))

t1 = TabMusic(w, tab1)
t2 = TabDownload(w, tab2)
ModeTray(w, t1)

def checkInLoop():
    t1.updateTimeSong()
    w.after(100, checkInLoop)
w.after(1000, checkInLoop)

w.mainloop()
