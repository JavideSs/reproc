from tkinter import Canvas

from ui.images.utilities import *

from data.data_types import *

from PIL import ImageSequence

#==================================================


class TkCanvasGif(Canvas):
    #Class to add and control a transparent gif in tkinter
    #https://stackoverflow.com/questions/20370864/no-transparency-in-animated-gif-with-tkinter

    def __init__(self, w, gif:PILImage, size:tuple, bg:str=None, *args, **kwargs):

        super().__init__(w,
            width=size[0], height=size[1],
            background=bg,
            highlightthickness=0,
            *args, **kwargs)

        func = lambda frame: PILToTk(frame.convert(mode="RGBA" if not bg else "RGB"))
        self.frames = ImageSequence.all_frames(gif, func=func)

        self.__i_seq = 0
        self.__duration = gif.info["duration"]

        self.__cancel_id = None


    def setGif(self):
        self.canvas_gif = self.create_image(0,0, image=self.frames[0], anchor="nw")


    def isPlayingGif(self) -> bool:
        return self.__cancel_id is not None


    def __playGifLoop(self):
        self.itemconfig(self.canvas_gif, image=self.frames[self.__i_seq])

        self.__i_seq += 1
        if self.__i_seq == len(self.frames):
            self.__i_seq = 0

        self.__cancel_id = self.after(self.__duration, self.__playGifLoop)


    def playGif(self):
        if not self.__cancel_id:
            self.__playGifLoop()


    def stopGif(self):
        if self.__cancel_id is not None:
            self.after_cancel(self.__cancel_id)
            self.__cancel_id = None