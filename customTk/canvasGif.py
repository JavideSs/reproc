from tkinter import Canvas

from PIL import Image, ImageTk

from data.data_types import *

#==================================================

#Class to add and control a transparent gif in tkinter
#https://stackoverflow.com/questions/20370864/no-transparency-in-animated-gif-with-tkinter
class TkCanvasGif(Canvas):
    def __init__(self, w, gif:PILImage, size:Tuple[int,int], bg:str=None, *args, **kwargs):

        super().__init__(w,
            width=size[0], height=size[1],
            background=bg,
            highlightthickness=0,
            *args, **kwargs)

        mode = "RGBA" if not bg else "RGB"

        gif_seq = [gif.copy()]
        for _ in range(getattr(gif, "n_frames", 1)-1):
            gif.seek(len(gif_seq))
            gif_seq.append(gif.copy())

        self.gif_seq_tk = [ImageTk.PhotoImage(gif_seq[0].convert(mode))]

        lut = [1]*256
        lut[gif.info["transparency"]] = 0

        temp = gif_seq[0]
        for img in gif_seq[1:]:
            mask = img.point(lut, "1")
            temp.paste(img, None, mask)
            self.gif_seq_tk.append(ImageTk.PhotoImage(temp.convert(mode)))

        self.__i_seq = 0
        self.__duration = gif.info["duration"]

        self.__cancel_id = None


    def setGif(self):
        self.canvas_gif = self.create_image(0,0, image=self.gif_seq_tk[0], anchor="nw")


    def isPlayingGif(self) -> bool:
        return self.__cancel_id is not None


    def __playGifLoop(self):
        self.itemconfig(self.canvas_gif, image=self.gif_seq_tk[self.__i_seq])

        self.__i_seq += 1
        if self.__i_seq == len(self.gif_seq_tk):
            self.__i_seq = 0

        self.__cancel_id = self.after(self.__duration, self.__playGifLoop)


    def playGif(self):
        if not self.__cancel_id:
            self.__playGifLoop()


    def stopGif(self):
        if self.__cancel_id is not None:
            self.after_cancel(self.__cancel_id)
            self.__cancel_id = None