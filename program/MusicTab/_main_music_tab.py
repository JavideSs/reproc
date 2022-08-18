from tkinter import Frame
from tkinter.ttk import Scrollbar

from .playlist import Playlist, ROW_HEIGHT
from .playlist_control import PlaylistControl
from .song_control import SongControl

from data import config

#==================================================

class MusicTab(Frame):
    def __init__(self, w, *args, **kwargs):

        self.w = w

        super().__init__(w, *args, **kwargs)

        #___

        self.fdirectplay = lambda: self._play(self.playlist.directPlay)
        self.fprevious = lambda: self._play(self.playlist.playPrevious)
        self.fplaypause = lambda: self._play(self.playlist.playpause)
        self.fnext = lambda: self._play(self.playlist.playNext)

        #___

        self.playlist = Playlist(self, height=14)
        self.playlist.grid(row=1, column=0, sticky="nsew")

        self.playlist_scroll = Scrollbar(self, command=self.playlist.yview)
        self.playlist_scroll.grid(row=1, column=1, sticky="nsw")
        self.playlist.configure(yscroll=self.playlist_scroll.set)

        #___

        self.song_control = SongControl(self)
        self.song_control.grid(row=0, column=0, columnspan=2, sticky="ew")

        #___

        self.playlist_control = PlaylistControl(self)
        self.playlist_control.grid(row=2, column=0, columnspan=2, sticky="ew")

        #___

        #SetJson
        #Other sets have been updated when when its respective widget is initialized or when the playlist is set
        self.playlist_control.playlist_handler_set.setPlaylist(config.general["playlist"])

        #___

        #Direct play when pre click on an itemTV's play image
        self.playlist.bind("<ButtonRelease-1>", lambda event: self.fdirectplay() if event.x < ROW_HEIGHT else None)
        #Direct play when the return key is pressed on an itemTV
        self.playlist.bind("<Return>", lambda _event: self.fdirectplay())

        #Set time when pre click on the timeline
        self.song_control.timeline.scale_time.bind("<ButtonRelease-1>", self._setTime)

        #When these keys are pressed and there is no focus on an entry
        w.bind_all("<space>", lambda event: self.fplaypause() if not str(event.widget).endswith("entry") else None)
        w.bind_all("<Right>", lambda event: self._moveTime(5) if not str(event.widget).endswith("entry") else None)
        w.bind_all("<Left>", lambda event: self._moveTime(-5) if not str(event.widget).endswith("entry") else None)
        #Fix: Default bind of ttk.treeview focuses on the previous itemTV clicked directly
        self.playlist.bind("<Right>", lambda event: self._moveTime(5) if not str(event.widget).endswith("entry") else None)

        #Update song every second
        w.after(1000, self._updateTimeLoop)

    #__________________________________________________

    def saveJson(self):
        #Other saves are updated when their associated event is called
        states_to_save = self.playlist.getStates()
        config.general["volume"] = states_to_save[0]
        config.general["random"] = states_to_save[1]
        config.general["loop"] = states_to_save[2]

    #___

    '''
    Intermediary functions before the execution of the corresponding function play
    The corresponding widgets are updated
    '''

    def _play(self, func_play):
        is_song_new = func_play()

        if is_song_new:
            song_playing = self.playlist.getSongPlaying()
            self.song_control.artwork.setArtWork(song_playing)
            self.song_control.timeline.setNewSong(song_playing)

        if self.playlist.isSongPlaying():
            self.song_control.btn_playpause.set_img(1)
            self.song_control.artwork.playGif()
            #self.w.win7_features.updateThumbBar(1)

        elif self.playlist.isSongLoad():
            self.song_control.btn_playpause.set_img(0)
            self.song_control.artwork.stopGif()
            #self.w.win7_features.updateThumbBar(0)


    def _setTime(self, _event):
        if self.playlist.isSongLoad():
            time_new = self.song_control.timeline.getTime()
            Playlist.setTime(time_new)
            self.song_control.timeline.setTime(time_new)


    def _moveTime(self, time):
        if self.playlist.isSongLoad():
            song_playing = self.playlist.getSongPlaying()
            time_new = self.song_control.timeline.getTime(song_playing) + time
            time_new = time_new if time_new>0 else 0

            if time_new < song_playing.time:
                Playlist.setTime(time_new)
                self.song_control.timeline.setTime(time_new)
            else:
                self.fnext()

            return "break"  #Avoid focuses on the previous itemTV clicked directly
    #___

    def _updateTimeLoop(self):
        #Do not use "if self.playlist.isSongPlaying(): ..." because the song may have finished between seconds
        #"if self.song_control.artwork.isPlayingGif(): ..." is safer
        if self.song_control.artwork.isPlayingGif():
            song_playing = self.playlist.getSongPlaying()
            time_new = self.song_control.timeline.getTime(song_playing) + 1

            if song_playing is not None:
                if time_new < song_playing.time:
                    self.song_control.timeline.setTime(time_new)
                else:
                    self.fnext()

        self.w.after(1000, self._updateTimeLoop)