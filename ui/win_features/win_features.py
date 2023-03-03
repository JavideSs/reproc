from ctypes import windll

from data.config import SYSTEM, SYSTEM_ARCH

#==================================================

if SYSTEM == "Windows":
    if SYSTEM_ARCH == "64bit":
        from .ThumbBar import ThumbBar_x64 as ThumbBar
    else:
        from .ThumbBar import ThumbBar_x86 as ThumbBar

    class WinFeatures():
        def __init__(self, w):
            self.w = w
            self.hWnd = windll.user32.GetParent(w.winfo_id())

        def createThumbBar(self, fprevious, fplaypause, fnext):
            self.w.after(10, lambda: ThumbBar.create(self.hWnd, fprevious, fplaypause, fplaypause, fnext))

        def updateThumbBar(self, is_song_playing:bool):
            ThumbBar.update(is_song_playing)

        def releaseThumbBar(self):
            ThumbBar.release()

else:
    class WinFeatures():
        def __init__(self, *v): pass
        def createThumbBar(self, *v): pass
        def updateThumbBar(self, *v): pass
        def releaseThumbBar(self, *v): pass
