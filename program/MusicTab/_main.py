import tkinter as tk
from tkinter import ttk

from .playback import Playback
from .playback_control import PlaybackControl
from .playlist import Playlist
from .playlist_control import PlaylistControl

from data import config
from data.data_types import *

#==================================================

class MusicTab(tk.Frame):
    def __init__(self, w, *args, **kwargs):
        self.w = w

        super().__init__(w, *args, **kwargs)


        self.fdirectplay = lambda: self._play(self._directPlay)
        self.fplaypause = lambda: self._play(self.playback.playpause)
        self.fprevious = lambda: self._play(self.playback.playPrevious)
        self.fnext = lambda: self._play(self.playback.playNext)


        self.playlist = Playlist(self)
        self.playlist.grid(row=1, column=0, sticky="nsew")

        self.playback = Playback(self.playlist)
        self.playlist.setPlayback(self.playback)

        self.playlist_scroll = ttk.Scrollbar(self, command=self.playlist.yview)
        self.playlist_scroll.grid(row=1, column=1, sticky="nsw")
        self.playlist.configure(yscrollcommand=self.playlist_scroll.set)

        self.playback_control = PlaybackControl(self)
        self.playback_control.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.playlist_control = PlaylistControl(self)
        self.playlist_control.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.playlist_control.playlist_handler_set.setPlaylist(config.general["playlist"])


        self.playback_control.timeline.scale_time.bind("<ButtonRelease-1>", self._setTime)

        self.playlist.bind("<Return>", lambda _event: self.fdirectplay())
        self.playlist.bind("<Double-ButtonRelease-1>", lambda _event: self.fdirectplay())
        #Direct play when click on an itemTV play image
        self.playlist.bind("<ButtonRelease-1>", lambda event: self.fdirectplay() if event.x < Playlist.ROW_HEIGHT else None)

        not_in_entry = lambda event: not str(event.widget).endswith("entry")
        self.playback_control.bind_all("<space>", lambda event: self.fplaypause() if not_in_entry(event) else None)
        self.playback_control.bind_all("<Control-Right>", lambda event: self.fnext() if not_in_entry(event) else None)
        self.playback_control.bind_all("<Control-Left>", lambda event: self.fprevious() if not_in_entry(event) else None)
        self.playback_control.bind_all("<Right>", lambda event: self._moveTime(5) if not_in_entry(event) else None)
        self.playback_control.bind_all("<Left>", lambda event: self._moveTime(-5) if not_in_entry(event) else None)


        #Do not use "if self.playlist.isSongPlaying(): ..." because the song may have finished between seconds
        self.__is_song_playing_in_setp = False


        #Update song every second
        w.after(100, self._updateTimeLoop)

    #__________________________________________________

    def _updateTimeLoop(self):
        if self.__is_song_playing_in_setp:
            song_playing = self.playback.song_playing
            time_new = round(self.playback_control.timeline.getTime()) + 1

            if time_new < song_playing.time:
                self.playback_control.timeline.setTime(time_new)
            else:
                self.fnext()

        self.w.after(1000, self._updateTimeLoop)

    #___

    def _update(self, song_previous_id:int, is_song_new:int, song_playing_id:int):
        song_playing = self.playback.song_playing

        if self.playback.isSongPlaying():
            self.playlist.setPlay(song_playing_id)
        elif self.playback.isSongLoad():
            self.playlist.setPause(song_playing_id)

        if is_song_new:
            if self.playlist.exists(song_previous_id):
                #If not rewind
                if self.playback.song_playing.id != song_previous_id:
                    self.playlist.setUnload(song_previous_id)

            if self.playlist.exists(song_playing.id):
                self.playlist.setFocus(song_playing.id)

            self.playback_control.timeline.setNewSong(song_playing)
            self.playback_control.artwork.setArtWork(song_playing)
            self.w.extraevents.newSong(song_playing)

        if self.playback.isSongPlaying():
            self.__is_song_playing_in_setp = True
            self.playback_control.setPlay()
            self.w.extraevents.playSong()

        else:
            self.__is_song_playing_in_setp = False
            self.playback_control.setPause()
            self.w.extraevents.stopSong()


    #Play the selected itemTV
    def _directPlay(self):
        #fun: When an itemTV that does not exist is clicked and there is no song played
        if not self.playlist.selection():
            return False

        #If song is playing, play/pause itemTV
        if int(self.playlist.selection()[0]) == self.playback.song_playing.id:
            self.playback.playpause()
            return False

        #If new song, play the selected itemTV
        self.playback.playById(int(self.playlist.selection()[0]))
        return True


    def _play(self, func_play:Callable):
        song_previous_id = self.playback.song_playing.id

        is_song_new = func_play()   #rewind is considered as new

        song_playing_id = self.playback.song_playing.id

        self._update(song_previous_id, is_song_new, song_playing_id)


    def _setTime(self, _event):
        if self.playback.isSongLoad():
            time_new = self.playback_control.timeline.getTime()
            self.playback.setTime(time_new)
            self.playback_control.timeline.setTime(round(time_new))


    def _moveTime(self, time:int):
        if self.playback.isSongLoad():
            song_playing = self.playback.song_playing
            time_new = max(round(self.playback_control.timeline.getTime()) + time, 0)

            if time_new < song_playing.time:
                self.playback.setTime(time_new)
                self.playback_control.timeline.setTime(time_new)
            else:
                self.fnext()

            return "break"  #fun: Avoid focuses on the previous itemTV clicked directly