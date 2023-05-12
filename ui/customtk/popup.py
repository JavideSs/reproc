from tkinter import Widget, Toplevel, Frame, Label
from .buttonText import TkButtonTextHoverBg

from data.data_types import *

#==================================================

class TkPopup(Toplevel):
    def __init__(self, w, geometry:Tuple[int,int], title:str, bg_bar:str, bg:str, *args, **kwargs):

        tk_main_w = Widget.nametowidget(w, ".")
        super().__init__(tk_main_w, *args, **kwargs)

        coord_x = tk_main_w.winfo_x() + tk_main_w.winfo_width()//2 - geometry[0]//2
        coord_y = tk_main_w.winfo_y() + tk_main_w.winfo_height()//2 - geometry[1]//2
        self.geometry(f"{geometry[0]}x{geometry[1]}+{coord_x}+{coord_y}")

        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.grab_set()

        self.titlebar = Frame(self, bg=bg_bar)
        self.titlebar.pack(side="top", fill="x", expand=True)

        self.lbl_title = Label(self.titlebar,
            text=title,
            bg=bg_bar,
            justify="center")
        self.lbl_title.pack(side="left", fill="x", expand=True)

        self.btn_exit = TkButtonTextHoverBg(self.titlebar,
            command=self.destroy,
            text="⨯",
            bg=bg_bar,
            bg_on_hover="red",
            font="bold")
        self.btn_exit.pack(side="right")

        self.titlebar.bind('<Button-1>', self.getCoord)
        self.lbl_title.bind('<Button-1>', self.getCoord)

        self.w = Frame(self, bg=bg)
        self.w.pack(side="bottom", fill="both", expand=True)


    #https://stackoverflow.com/questions/23836000/can-i-change-the-title-bar-in-tkinter/48738216#48738216
    def getCoord(self, event:Event):
        coord_x_titlebar = self.winfo_x() - event.x_root
        coord_y_titlebar = self.winfo_y() - event.y_root

        def moveW(event):
            self.geometry(f"+{event.x_root + coord_x_titlebar}+{event.y_root + coord_y_titlebar}")

        self.titlebar.bind('<B1-Motion>', moveW)
        self.lbl_title.bind('<B1-Motion>', moveW)