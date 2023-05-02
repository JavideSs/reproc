from data.data_types import *

from .MusicTab.song import Song

import os
import platform

#==================================================

class ExtraEvents():
    def __init__(self, w): pass
    def release(self): pass
    def newSong(self, song:Song): pass
    def playSong(self): pass
    def stopSong(self): pass


class Windows7ExtraEvents(ExtraEvents):
    def __init__(self, w):
        from ui.win_features import ThumbBar

        self.thumbbar = ThumbBar(w,
            img_path=os.path.join("ui","images","file","thumbbar","thumbbar.bmp"),
            btns=(
                ("Previous", w.tab_music.fprevious),
                ("Play", w.tab_music.fplaypause),
                ("Pause", w.tab_music.fplaypause),
                ("Next", w.tab_music.fnext)),
            btnsset=(0,1,3))

    def newSong(self, song):
        pass

    def playSong(self):
        self.thumbbar.set(1, 2)

    def stopSong(self):
        self.thumbbar.set(1, 1)

    def release(self):
        self.thumbbar.release()


class LinuxExtraEvents(ExtraEvents):
    def __init__(self, w):
        pass

    def newSong(self, song):
        pass

    def playSong(self):
        pass

    def stopSong(self):
        pass

    def release(self):
        pass

#==================================================

def createExtraEvents(w):
    if platform.system() == "Windows":
        if int(platform.version().split(".")[0]) > 7:
            return Windows7ExtraEvents(w)

    elif platform.system() == "Linux":
        return LinuxExtraEvents(w)

    return ExtraEvents(w)