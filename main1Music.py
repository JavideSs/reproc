from mutagen.mp3 import MP3
from pygame import mixer

from random import choice
from operator import attrgetter
import struct
import os

from _config import folder_music


class Song():
    def __init__(self, id, name, path, secons, time, date):
        self.id = id
        self.name = name
        self.path = path
        self.secons = secons
        self.time = time
        self.date = date

#______________________________________________________________________________________________________
#______________________________________________________________________________________________________

class Main():
    def __init__(self):
        self._songs_all = []

        if os.path.exists(folder_music):
            self.initNameSongs()
        else:
            os.mkdir(folder_music)

        self._songs_playlist = self._songs_all.copy()
        self._songs_previous = []

        self.state_random = False
        self.state_bucle = False

        mixer.init(48000) #Frecuencia mp3 con 320kbps

#______________________________________________________________________________________________________

    @staticmethod
    def formatoTime(s_total):
        m, s = divmod(s_total,60)
        h, m = divmod(m,60)

        if not h:
            return "{:2d}:{:02d}".format(int(m),int(s))
        else:
            return "{:1d}:{:02d}:{:02d}".format(int(h),int(m),int(s))


    def initNameSongs(self):
        with os.scandir(folder_music) as it:
            id = 0
            for file in it:
                if file.is_file() and file.name.endswith(".mp3"):
                    name_playable = ''.join(c if c <= '\uffff' else ''.join(chr(x) for x in struct.unpack('>2H', c.encode('utf-16be'))) for c in file.name[:-4])
                    path = folder_music+"/"+file.name
                    s_total = round(MP3(path).info.length)

                    song = Song(id, name_playable, path, s_total, Main.formatoTime(s_total), os.stat(path).st_ctime)
                    self._songs_all.append(song)
                    id += 1

    #______________________________________________________

    def filterNameSongs(self, song_name):
        self._songs_playlist.clear()
        for song in self._songs_all:
            if song_name.lower() in song.name.lower():
                self._songs_playlist.append(song)


    def getNameSongs(self):
        return self._songs_playlist

    #______________________________________________________

    def playById(self, song_id):
        for song in self._songs_playlist:
            if song_id == song.id:
                mixer.music.load(song.path)
                mixer.music.play()
                #Evitamos list index out of range y si la anterior no es la misma cancion...
                if (not any(self._songs_previous)) or (song.name!=self._songs_previous[-1].name):
                    self._songs_previous.append(song)
                return song


    def playNext(self, id_next):
        if self.state_bucle and any(self._songs_previous):
            song = self.playById(self._songs_previous[-1].id)

        elif self.state_random:
            song = self.playById(choice(self._songs_playlist).id)

        else:
            if id_next != "":
                song = self.playById(int(id_next))
            else:
                song = self.playById(self._songs_playlist[0].id)

        return song


    def playPrevious(self):
        if any(self._songs_previous):
            if len(self._songs_previous) > 1:
                del self._songs_previous[-1]
            song = self.playById(self._songs_previous[-1].id)
            return song
        else:
            return False


    def pause(self):
        mixer.music.pause()


    def resume(self):
        mixer.music.unpause()


    def isSongLoad(self):
        return mixer.music.get_busy()

    #______________________________________________________

    def setVolumen(self, volumen):
        mixer.music.set_volume(volumen)

    #______________________________________________________

    def setTime(self, time):
        mixer.music.rewind()
        mixer.music.set_pos(time)

    #______________________________________________________

    def orderBy(self, state, atributo):
        self._songs_all.sort(key=attrgetter(atributo), reverse=state)
        self._songs_playlist.sort(key=attrgetter(atributo), reverse=state)
