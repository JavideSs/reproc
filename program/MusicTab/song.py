from data.data_types import *

from PIL import Image
from tinytag import TinyTag

import os
import platform
import struct
from io import BytesIO

#==================================================

class Song():
    NONE_SONG = ""
    NONE_ID = -1

    next_id = 0

    def __init__(self, song_path:str):
        if song_path == Song.NONE_SONG:
            self.id = Song.NONE_ID
            return

        self.id = Song.next_id
        Song.next_id += 1

        self.path = song_path
        self.time = round(TinyTag.get(self.path).duration)
        self.date = os.path.getmtime(self.path)

        self.visible = True

    #__________________________________________________

    def __eq__(self, other_song):
        if self.id == other_song.id == Song.NONE_ID:
            return True
        if self.id == Song.NONE_ID or other_song.id == Song.NONE_ID:
            return False
        return self.path == other_song.path

    #___

    def getPath(self):
        return self.__path

    def setPath(self, path:str):
        self.__path = path
        name = os.path.splitext(os.path.basename(path))[0]
        #Keep special characters
        #https://stackoverflow.com/questions/44965129/ucs-2-not-able-to-encode
        self.__name = "".join(c if c <= "\uffff"
            else "".join(chr(x) for x in struct.unpack(">2H", c.encode("utf-16be")))
            for c in name)

    path = property(fget=getPath, fset=setPath)


    @property
    def name(self):
        return self.__name


    @property
    def extension(self):
        return os.path.splitext(self.path)[-1]


    @staticmethod
    def supported_format(song_str:str):
        if platform.system() == "Windows":
            supported_formats = (".mp3", ".ogg")
        elif platform.system() == "Linux":
            supported_formats = ".ogg"
        else:
            supported_formats = ".ogg"

        return song_str.endswith(supported_formats)

    #___

    #Represents time in string format
    @staticmethod
    def formatTime(s_total:int):
        m, s = divmod(s_total, 60)
        h, m = divmod(m, 60)

        if h: return "{:1d}:{:02d}:{:02d}".format(int(h), int(m), int(s))
        else: return "{:2d}:{:02d}".format(int(m), int(s))


    def getFormattedTime(self):
        return self.formatTime(self.time)


    def getFrequency(self) -> int:
        return TinyTag.get(self.path).samplerate


    def getArt(self, scale:Tuple[int,int]) -> PILImage:
        art_data = TinyTag.get(self.path, image=True).get_image()
        art_data_pil = Image.open(BytesIO(art_data))
        art_data_pil.thumbnail(scale, Image.ANTIALIAS)
        return art_data_pil