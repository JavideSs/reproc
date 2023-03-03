from .song import Song

from data.data_types import *

from pygame import mixer

import random

#==================================================

class Playback():
    def __init__(self, playlist:TPlaylist):
        mixer.init(frequency=48000) #MP3 frequency with 320kbps by default, stereo

        self.playlist = playlist

        self.songs:List[Song] = []
        self.songs_previous_id:List[int] = []
        self.song_playing = Song(Song.NONE_SONG)

        self.__is_load = False

        self.state_random = False
        self.state_loop = False

    #__________________________________________________

    def isSongLoad(self) -> bool:
        return self.__is_load


    def isSongPlaying(self) -> bool:
        return mixer.music.get_busy()


    def getSongById(self, song_id:int):
        for song in self.songs:
            if song.id == song_id:
                return song
        return Song(Song.NONE_SONG)


    def getStates(self):
        return {
            "volume": mixer.music.get_volume(),
            "random": self.state_random,
            "loop": self.state_loop
        }

    #___

    def toggleRandom(self):
        self.state_random = not self.state_random


    def toggleLoop(self):
        self.state_loop = not self.state_loop


    def setVolume(self, volume:float):
        mixer.music.set_volume(volume)


    def setTime(self, time:float):
        #"set_pos()" advances rarely
        mixer.music.rewind()
        mixer.music.set_pos(time)

    #___

    def playById(self, song_id:int):
        song = self.getSongById(song_id)

        if mixer.get_init()[0] != song.getFrequency():
            mixer.quit()
            mixer.init(frequency=song.getFrequency())

        mixer.music.load(song.path)
        mixer.music.play()

        self.song_playing = song
        self.__is_load = True

        #Append to "self.songs_previous_id" if it is the first song or it is not the previous song
        if not len(self.songs_previous_id) or song_id!=self.songs_previous_id[-1]:
            self.songs_previous_id.append(song_id)


    def playpause(self):
        #Play to pause
        if self.isSongPlaying():
            mixer.music.pause()

        #Pause to play
        elif self.isSongLoad():
            mixer.music.unpause()

        #Play first song
        elif len(self.playlist.items()):
            self.playNext()
            return True

        return False


    def playNext(self):
        #In bucle
        if self.state_loop and len(self.songs_previous_id):
            mixer.music.rewind()

        #In random and any in playlist
        elif self.state_random and len(self.playlist.items()):
            self.playById(random.choice([song for song in self.songs if song.visible]).id)

        #Now and next is in playlist
        elif self.isSongLoad() and self.playlist.isListed(self.song_playing.id) and self.playlist.next(self.song_playing.id)!=Song.NONE_ID:
            self.playById(self.playlist.next(self.song_playing.id))

        #Any in playlist
        elif len(self.playlist.items()):
            #Play first itemTV in view
            self.playById(self.playlist.firstItemVisible())

        else:
            self.__is_load = False
            return False
        return True


    def playPrevious(self):
        if len(self.songs_previous_id):
            #One is always left in the "self.songs_previous_id", it loops with itself
            if len(self.songs_previous_id) > 1:
                del self.songs_previous_id[-1]

                if self.playlist.exists(self.songs_previous_id[-1]):
                    self.playById(self.songs_previous_id[-1])
                #Rewind if the previous song does not exist in playlist
                else:
                    mixer.music.rewind()
            #Rewind if there is not previous song
            else:
                mixer.music.rewind()

        else:
            self.__is_load = False
            return False
        return True