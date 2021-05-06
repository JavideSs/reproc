from mutagen.mp3 import MP3
from pygame.mixer import init, music
from threading import Thread, Timer
from random import choice
from operator import attrgetter
import os

from config import *

class Song():
    def __init__(self, name, id, path, secons, time, date):
        self.name = name
        self.id = id
        self.path = path
        self.secons = secons
        self.time = time
        self.date = date

#______________________________________________________________________________________________________
#______________________________________________________________________________________________________

class Main():
    def __init__(self):
        self.songs_all = []

        if os.path.exists(folder_music):
            self.initNameSongs()
        else:
            os.mkdir(folder_music)

        self.songs_playlist = self.songs_all.copy()
        self.songs_previous = []

        self.state_random = False
        self.state_bucle = False

        init(48000)

#______________________________________________________________________________________________________

    def formatoTime(self, s_total):
        m, s = divmod(s_total,60)
        h, m = divmod(m,60)

        if not h:
            return "{:2d}:{:02d}".format(int(m),int(s))
        else:
            return "{1d}:{:2d}:{:02d}".format(int(h),int(m),int(s))


    def initNameSongs(self):
        with os.scandir(folder_music) as it:
            id = 0
            for file in it:
                if file.is_file() and file.name.endswith(".mp3"):
                    path = folder_music+"/"+file.name
                    s_total = MP3(path).info.length

                    song = Song(file.name[:-4], id, path, s_total, self.formatoTime(s_total), os.stat(path).st_ctime)
                    self.songs_all.append(song)
                    id += 1

    #______________________________________________________

    def filterNameSongs(self, song_name):
        self.songs_playlist.clear()
        for song in self.songs_all:
            if song_name.lower() in song.name.lower():
                self.songs_playlist.append(song)


    def getNameSongs(self):
        return self.songs_playlist

    #______________________________________________________

    def playById(self, song_id):
        for song in self.songs_playlist:
            if song_id == song.id:
                music.load(song.path)
                music.play()
                if (not any(self.songs_previous)) or (song.name!=self.songs_previous[-1].name):
                    self.songs_previous.append(song)
                return song


    def playNext(self, id_next):
        if self.state_bucle and any(self.songs_previous):
            song = self.playById(self.songs_previous[-1].id)

        elif self.state_random:
            song = self.playById(choice(self.songs_playlist).id)

        else:
            if id_next != "":
                song = self.playById(int(id_next))
            else:
                song = self.playById(self.songs_playlist[0].id)

        return song


    def playPrevious(self):
        if any(self.songs_previous):
            if len(self.songs_previous) > 1:
                del self.songs_previous[-1]
            song = self.playById(self.songs_previous[-1].id)
            return song
        else:
            return False


    def pause(self):
        music.pause()


    def resume(self):
        music.unpause()


    def isSongLoad(self):
        return music.get_busy()

    #______________________________________________________

    def setVolumen(self, volumen):
        music.set_volume(volumen)

    #______________________________________________________

    def setTime(self, time):
        music.rewind()
        music.set_pos(time)

    #______________________________________________________

    def orderByName(self, state):
        if state:
            self.songs_all.sort(key=attrgetter("name"), reverse=True)
            self.songs_playlist.sort(key=attrgetter("name"), reverse=True)
        else:
            self.songs_all.sort(key=attrgetter("name"), reverse=False)
            self.songs_playlist.sort(key=attrgetter("name"), reverse=False)


    def orderByDate(self, state):
        if state:
            self.songs_all.sort(key=attrgetter("date"), reverse=True)
            self.songs_playlist.sort(key=attrgetter("date"), reverse=True)
        else:
            self.songs_all.sort(key=attrgetter("date"), reverse=False)
            self.songs_playlist.sort(key=attrgetter("date"), reverse=False)


    def orderByTime(self, state):
        if state:
            self.songs_all.sort(key=attrgetter("time"), reverse=True)
            self.songs_playlist.sort(key=attrgetter("time"), reverse=True)
        else:
            self.songs_all.sort(key=attrgetter("time"), reverse=False)
            self.songs_playlist.sort(key=attrgetter("time"), reverse=False)
