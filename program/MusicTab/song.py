import os, struct
from io import BytesIO

from PIL import Image
from tinytag import TinyTag

from data.data_types import *

#==================================================

class Song():
    next_id = 0

    def __init__(self, song_path:str):
        self.id = Song.next_id
        Song.next_id += 1

        self.path = song_path
        self.time = round(TinyTag.get(self.path).duration)
        self.date = os.path.getmtime(self.path)
        self.visible_inplaylist = True

    #__________________________________________________

    def getPath(self) -> str:
        return self.__path

    def setPath(self, path:str):
        self.__path = path
        name = os.path.splitext(os.path.basename(self.path))[0]
        #Keep special characters
        #https://stackoverflow.com/questions/44965129/ucs-2-not-able-to-encode
        self.__name = ''.join(c if c <= '\uffff'
            else ''.join(chr(x) for x in struct.unpack('>2H', c.encode('utf-16be')))
            for c in name)

    path = property(fget=getPath, fset=setPath)


    @property
    def name(self) -> str:
        return self.__name


    @property
    def extension(self) -> str:
        return os.path.splitext(self.path)[-1]

    #___

    #Represents time in string format
    @staticmethod
    def timeFormat(s_total:int) -> str:
        m, s = divmod(s_total, 60)
        h, m = divmod(m, 60)

        if h: return "{:1d}:{:02d}:{:02d}".format(int(h), int(m), int(s))
        else: return "{:2d}:{:02d}".format(int(m), int(s))


    def getTimeFormat(self) -> str:
        return self.timeFormat(self.time)


    def getFrequency(self) -> int:
        return TinyTag.get(self.path).samplerate


    def getArt(self, scale:Tuple[int,int]) -> PILImage:
        art_data = TinyTag.get(self.path, image=True).get_image()

        #https://github.com/devsnd/tinytag/issues/100
        if art_data[:10] == b"o\x00v\x00e\x00r\x00\x00\x00":
            art_data = art_data[10:]

        art_data_pil = Image.open(BytesIO(art_data))
        art_data_pil.thumbnail(scale, Image.ANTIALIAS)
        return art_data_pil