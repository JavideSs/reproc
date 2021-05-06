import os
from mutagen.mp3 import MP3
from pygame.mixer import init, music
from threading import Thread, Timer

from config import *

class Song():
    def __init__(self, name, path, secons, time, fecha, rate):
        self.name = name
        self.path = path
        self.secons = secons
        self.time = time
        self.fecha = fecha
        self.rate = rate


class Main():
    def __init__(self):
        self.songs_all = []
        try:
            self.initNameSongs()
        except:
            os.mkdir(folder_music)
        self.songs_playlist = self.songs_all.copy()
        self.volumen = 100
        self.id_next = 0

#______________________________________________________________________________________________________

    def initNameSongs(self):
        with os.scandir(folder_music) as it:
            for file in it:
                if file.is_file() and file.name.endswith(".mp3") and file.name not in self.songs_all:
                    path = folder_music+"/"+file.name
                    metadata = MP3(path)
                    rate = metadata.info.sample_rate
                    s_total = metadata.info.length
                    m, s = divmod(s_total,60)
                    h, m = divmod(m,60)
                    song = Song(file.name[:-4], path, s_total, [int(h),int(m),int(s)], os.stat(path).st_ctime, rate)
                    self.songs_all.append(song)


    def filterNameSongs(self, song_name):
        self.songs_playlist.clear()
        for song in self.songs_all:
            if song_name.lower() in song.name.lower():
                self.songs_playlist.append(song)


    def getNameSongs(self):
        return self.songs_playlist

    #______________________________________________________

    def playByName(self, song_name):
        for id, song in enumerate(self.songs_playlist):
            if song_name == song.name:
                init(song.rate)
                music.load(song.path)
                music.play()
                music.set_volume(self.volumen)
                self.id_next = id + 1
                return song


    def playByOrder(self):
        song = self.playByName(self.songs_playlist[self.id_next].name)
        return song


    def pauseSong(self):
        music.pause()


    def resumeSong(self):
        music.unpause()


    def playNext():
        pass


    def playPrevious():
        pass


    def playRandom():
        pass


    def playBucle():
        pass


    def setVolumen(self, volumen):
        self.volumen = volumen
        try:
            music.set_volume(volumen)
        except:
            pass


    def setTime(self, time):
        music.rewind()
        music.set_pos(time)


    def getTime():
        pass


    def orderByDate():
        pass


    def orderByName():
        pass


    def orderByTime():
        pass
