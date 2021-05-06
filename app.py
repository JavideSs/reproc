from tkinter import PhotoImage
from tkinter.ttk import Notebook, Frame, Style
from ttkthemes import ThemedTk

from tabMusic import TabMusic
from config import *


print(author)
w = ThemedTk()
#equilux -> dark
w.set_theme("arc")

w.title('Reproc')
w.geometry("418x500")
w.resizable(False,False)
w.eval('tk::PlaceWindow . center')
w.configure(background=color_menu_up)

style = Style()
style.map("TNotebook.Tab",foreground=[("selected","#914ecc"),("active","#cca9eb")])
style.configure("TNotebook.Tab",font=("calibri",8))
style.layout("TNotebook.Tab",[("Plain.Notebook.tab",{"children":[('Treeitem.image',{"side":"left","sticky":"we"}),("Treeitem.text",{"side":"left","sticky":"we"})]})])

tabs = Notebook(w); tabs.pack(expand=True, fill='both', padx=(tabs_padd,tabs_padd))
img_tab1 = PhotoImage(file=folder_img+"/IconMusic.png")
tab1 = Frame(); tabs.add(tab1, text="  Music Player ", image=img_tab1, pad=(-tabs_padd,0,-tabs_padd,0))
img_tab2 = PhotoImage(file=folder_img+"/IconDownload.png")
tab2 = Frame(); tabs.add(tab2, text="  Download      ", image=img_tab2, pad=(-tabs_padd,0,-tabs_padd,0))
img_tab3 = PhotoImage(file=folder_img+"/IconSettings.png")
tab3 = Frame(); tabs.add(tab3, text="  Settings         ", image=img_tab3, pad=(-tabs_padd,0,-tabs_padd,0))

TabMusic(w, tab1)

w.mainloop()
