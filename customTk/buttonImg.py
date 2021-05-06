from tkinter import Button

from data.images.utilities import b64ToTk, b64ToPIL, PILToTk, brightensColorImg

from abc import ABC, abstractmethod

#Classes to add style to a button
#Receives a tuple of images that it contemplates
#They can be set automatically on each click, or manually
#==================================================

class TkButtonImg(ABC, Button):
    def __init__(self, w, command, imgs:tuple, bg:str, change_img_on_click:bool=False, *args, **kwargs):
        self.imgs = imgs
        self.img_tag_now = 0

        super().__init__(w,
            command=command if not change_img_on_click else lambda: self._on_click(command),
            image=self.imgs[self.img_tag_now],
            background=bg,
            activebackground=bg,
            highlightbackground=bg,
            borderwidth=0,
            *args, **kwargs)


    def _on_click(self, command):
        command()
        if self.img_tag_now == len(self.imgs)-1:    self.img_tag_now = 0
        else:                                       self.img_tag_now = self.img_tag_now + 1


    #Set image manually
    def set_img(self, tag:int):
        self.img_tag_now = tag
        self["image"] = self.imgs[self.img_tag_now]


#==================================================


class TkButtonImgHover(TkButtonImg):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bind("<Enter>", self._on_hover_enter)
        self.bind("<Leave>", self._on_hover_leave)


    @abstractmethod
    def _on_hover_enter(self, _event): pass

    @abstractmethod
    def _on_hover_leave(self, _event): pass


#==================================================


class TkButtonImgHoverNone(TkButtonImg):
    def __init__(self, w, *args, **kwargs):
        super().__init__(w, *args, **kwargs)


    def _on_click(self, command):
        super()._on_click(command)
        self["image"] = self.imgs[self.img_tag_now]


#==================================================


class TkButtonImgHoverImg(TkButtonImgHover):
    def __init__(self, w, imgs:tuple, *args, **kwargs):
        self.is_hover = False

        func_brightens = lambda img: PILToTk(brightensColorImg(b64ToPIL(img), 1.5))
        self.imgs_brightens = tuple(map(func_brightens, imgs))

        super().__init__(w, imgs=tuple(map(b64ToTk, imgs)), *args, **kwargs)


    def set_img(self, tag:int):
        if self.is_hover:
            self.img_tag_now = tag
            self["image"] = self.imgs_brightens[self.img_tag_now]
        else:
            super().set_img(tag)


    def _on_click(self, command):
        super()._on_click(command)
        self["image"] = self.imgs_brightens[self.img_tag_now]


    def _on_hover_enter(self, _event):
        self.is_hover = True
        self["image"] = self.imgs_brightens[self.img_tag_now]

    def _on_hover_leave(self, _event):
        self.is_hover = False
        self["image"] = self.imgs[self.img_tag_now]


#==================================================


class TkButtonImgHoverBg(TkButtonImgHover):
    def __init__(self, w, imgs:tuple, bg:str, bg_on_hover:str, *args, **kwargs):
        self.bg = bg
        self.bg_hover = bg_on_hover

        super().__init__(w, imgs=imgs, bg=bg, *args, **kwargs)
        self["activebackground"] = self.bg_hover
        self["highlightbackground"] = self.bg_hover


    def _on_click(self, command):
        super()._on_click(command)
        self["image"] = self.imgs[self.img_tag_now]


    def _on_hover_enter(self, _event):
        self["bg"] = self.bg_hover

    def _on_hover_leave(self, _event):
        self["bg"] = self.bg