from .CThumbBar import ThumbBar
from ctypes import windll

class Win7Features():
    def __init__(self, w):
        self.w = w
        self.hWnd = windll.user32.GetParent(w.winfo_id())

    def createThumbBar(self, fprevious, fplaypause, fnext):
        self.w.after(10, lambda: ThumbBar.create(self.hWnd, fprevious, fplaypause, fplaypause, fnext))

    def updateThumbBar(self, state):
        ThumbBar.update(state)

    def releaseThumbBar(self):
        ThumbBar.release()