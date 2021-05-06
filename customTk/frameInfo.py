from tkinter import Entry
from tkinter.ttk import Frame, Separator, Label

#==================================================

class TkFrameInfo(Frame):
    def __init__(self, w, text:str, lbl_width:int, info_width:int, info_bg:str, *args, **kwargs):
        super().__init__(w, *args, **kwargs)

        self.lbl = Label(self,
            width=lbl_width,
            text=text)
        self.lbl.grid(row=0, column=0)

        self.info = Entry(self,
            width=info_width,
            readonlybackground=info_bg,
            borderwidth=0,
            justify="left",
            state="readonly")
        self.info.grid(row=0, column=1)

        self.sep = Separator(self, orient="horizontal")
        self.sep.grid(row=1, column=0, columnspan=2, sticky="new")


    def insert(self, text):
        self.info["state"] = "normal"
        self.info.delete(0, "end")
        self.info.insert(0, text)
        self.info["state"] = "readonly"