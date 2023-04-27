from tkinter import Button

from data.data_types import *

#==================================================

class TkButtonText(ABC, Button):
    def __init__(self, w, text:str, *args, **kwargs):
        super().__init__(w,
            text=text,
            borderwidth=0,
            *args, **kwargs)

        self.bind("<Enter>", self._on_hover_enter)
        self.bind("<Leave>", self._on_hover_leave)


    @abstractmethod
    def _on_hover_enter(self, _event): pass

    @abstractmethod
    def _on_hover_leave(self, _event): pass


#==================================================


class TkButtonTextHoverFg(TkButtonText):
    def __init__(self, w, text:str, fg:str, fg_on_hover:str, *args, **kwargs):
        self.fg = fg
        self.fg_hover = fg_on_hover

        super().__init__(w, text=text, fg=fg, *args, **kwargs)
        self["activeforeground"] = self.fg_hover


    def _on_hover_enter(self, _event):
        self["fg"] = self.fg_hover

    def _on_hover_leave(self, _event):
        self["fg"] = self.fg


#==================================================


class TkButtonTextHoverBg(TkButtonText):
    def __init__(self, w, text:str, bg:str, bg_on_hover:str, *args, **kwargs):
        self.bg = bg
        self.bg_hover = bg_on_hover

        super().__init__(w, text=text, bg=bg, *args, **kwargs)
        self["activebackground"] = self.bg_hover
        self["highlightbackground"] = self.bg_hover


    def _on_hover_enter(self, _event):
        self["bg"] = self.bg_hover

    def _on_hover_leave(self, _event):
        self["bg"] = self.bg