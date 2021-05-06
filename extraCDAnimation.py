from tkinter.ttk import Label
from PIL import Image, ImageTk

from _config import color_reproc


class CDgif(Label):
    def __init__(self, w, filename):

        img = Image.open(filename)
        gif =  []

        try:
            while True:
                gif.append(img.copy())
                img.seek(len(gif))
        except EOFError:
            pass

        self.delay = img.info['duration']

        self.frames = [ImageTk.PhotoImage(gif[0])]
        Label.__init__(self, w, image=self.frames, background=color_reproc, padd=5)

        lut = [1] * 256
        lut[img.info["transparency"]] = 0

        temp = gif[0]
        for image in gif[1:]:
            mask = image.point(lut, "1")
            temp.paste(image, None, mask)
            frame = temp.convert('RGBA')
            self.frames.append(ImageTk.PhotoImage(frame))

        self.idx = 0

    def play(self):
        self.config(image=self.frames[self.idx])
        self.idx += 1
        if self.idx == len(self.frames):
            self.idx = 0
        self.cancel = self.after(self.delay, self.play)
