from tkinter import PhotoImage, font, DoubleVar, StringVar, Scale as TkScale
from tkinter.ttk import Frame, Separator, Label, Scale
from customTk import TkButtonImgHoverNone, TkButtonImgHoverImg, TkCanvasGif

from data import config, images as b64img
from data.images.utilities import b64ToPIL, PILToTk
from .song import Song

from data.data_types import *

#==================================================

class SongControl(Frame):
    def __init__(self, w, *args, **kwargs):

        self.playlist = w.playlist

        super().__init__(w, *args, **kwargs)

        #___

        self.artwork = Artwork(self)
        self.artwork.grid(row=0, column=0, rowspan=2, padx=8, pady=8)

        #___

        self.timeline = Timeline(self)
        self.timeline.grid(row=1, column=1, columnspan=9, pady=(5,10))

        #___

        self.btn_random = TkButtonImgHoverNone(self,
            command=self.playlist.toggleRandom,
            imgs=(PhotoImage(data=b64img.btn_random_off),
                PhotoImage(data=b64img.btn_random_on)),
            bg=config.colors["BG"],
            change_img_on_click=True)
        self.btn_random.grid(row=0, column=1, pady=(8,0))

        if config.general["random"]:
            self.playlist.toggleRandom()
            self.btn_random.set_img(1)

        #___

        self.btn_loop = TkButtonImgHoverNone(self,
            command=self.playlist.toggleLoop,
            imgs=(PhotoImage(data=b64img.btn_loop_off),
                PhotoImage(data=b64img.btn_loop_on)),
            bg=config.colors["BG"],
            change_img_on_click=True)
        self.btn_loop.grid(row=0, column=2, pady=(8,0))

        if config.general["loop"]:
            self.playlist.toggleLoop()
            self.btn_loop.set_img(1)

        #___

        self.separator1 = Separator(self, orient="vertical")
        self.separator1.grid(row=0, column=3, sticky="ns", padx=(10,10), pady=(13,5))

        #___

        self.btn_play_previous = TkButtonImgHoverImg(self,
            command=w.fprevious,
            imgs=(b64img.btn_playizq,),
            bg=config.colors["BG"])
        self.btn_play_previous.grid(row=0, column=4, pady=(8,0))

        #___

        self.btn_playpause = TkButtonImgHoverImg(self,
            command=w.fplaypause,
            imgs=(b64img.btn_play,
                b64img.btn_playing),
            bg=config.colors["BG"])
        self.btn_playpause.grid(row=0, column=5, padx=(2,2), pady=(8,0))

        #___

        self.btn_play_next = TkButtonImgHoverImg(self,
            command=w.fnext,
            imgs=(b64img.btn_playder,),
            bg=config.colors["BG"])
        self.btn_play_next.grid(row=0, column=6, pady=(8,0))

        #___

        self.separator2 = Separator(self, orient="vertical")
        self.separator2.grid(row=0, column=7, sticky="ns", padx=(10,5), pady=(13,5))

        #___

        self.btn_volume = TkButtonImgHoverImg(self,
            command=self._setVolumeDirect,
            imgs=(b64img.btn_volume_on,
                b64img.btn_volume_off),
            bg=config.colors["BG"],
            change_img_on_click=True)
        self.btn_volume.grid(row=0, column=8, sticky="e", pady=(8,0))

        #___

        self.scale_volume = TkScale(self,
            command=self._setVolume,
            orient="horizontal",
            width=10, length=50,
            from_=0, to_=100,
            showvalue=False,
            highlightbackground=config.colors["BG"],
            troughcolor=config.colors["BG_WIDGET_GREY"],
            activebackground=config.colors["BG_WIDGET_BLUE"])
        self.scale_volume.grid(row=0, column=9, pady=(8,0))

        self.scale_volume.set(config.general["volume"]*100)

        #___

        '''
        "self.__volume_previous" != 0 when mute, represents the volume before mute, == 0 when unmute
        '''
        self.__volume_previous = 0

    #__________________________________________________

    #Set volume with btn
    def _setVolumeDirect(self):
        #Unmute to mute
        if self.__volume_previous:
            self.scale_volume.set(self.__volume_previous)
            self.__volume_previous = 0
        #Mute to unmute
        else:
            self.__volume_previous = self.scale_volume.get()
            self.scale_volume.set(0)


    #Set volume with scale
    def _setVolume(self, state_scale_volume:int):
        volume = int(state_scale_volume)/100
        self.playlist.setVolume(volume)

        #Mute to unmute
        if self.__volume_previous and volume:
            self.btn_volume.set_img(0)
            self.__volume_previous = 0
        #Unmute to mute
        if not self.__volume_previous and not volume:
            self.btn_volume.set_img(1)
            self.__volume_previous = 100


#==================================================


INIT_TIME = Song.timeFormat(0)
INIT_SONG = "._."
MAX_LEN_VISIBLE = 40

class Timeline(Frame):
    def __init__(self, w, *args, **kwargs):

        super().__init__(w, *args, **kwargs)

        #___

        self.state_txt_time1 = StringVar()
        self.state_txt_time1.set(INIT_TIME)

        self.txt_time1 = Label(self,
            textvariable=self.state_txt_time1,
            background=config.colors["BG"],
            font=font.nametofont("font_small_size"))
        self.txt_time1.grid(row=0, column=0, sticky="sw")

        #___

        self.state_txt_song = StringVar()
        self.state_txt_song.set(INIT_SONG)

        self.txt_song = Label(self,
            textvariable=self.state_txt_song,
            background=config.colors["BG"])
        self.txt_song.grid(row=0, column=1, pady=(0,2))

        #___

        self.state_txt_time2 = StringVar()
        self.state_txt_time2.set(INIT_TIME)

        self.txt_time1 = Label(self,
            textvariable=self.state_txt_time2,
            background=config.colors["BG"],
            font=font.nametofont("font_small_size"))
        self.txt_time1.grid(row=0, column=2, sticky="se")

        #___

        self.state_scale_time = DoubleVar()

        self.scale_time = Scale(self,
            orient="horizontal",
            length=300,
            from_=0, to_=100,
            value=0, variable=self.state_scale_time)
        self.scale_time.grid(row=1, column=0, columnspan=3)

        #___

        #Set time when direct click on the timeline
        self.scale_time.bind("<Button-1>", self._setTimeDirect)

        #___

        self.song_playing:Song = None

    #__________________________________________________

    def _setTimeDirect(self, event:Event):
        self.scale_time.event_generate("<Button-3>", x=event.x, y=event.y)
        return "break"  #Avoid recoil when holding

    #___

    def setNewSong(self, song:Song):
        self.song_playing = song
        self.state_scale_time.set(0)
        self.state_txt_time1.set(INIT_TIME)
        self.state_txt_time2.set(song.getTimeFormat())
        self.state_txt_song.set(song.name if len(song.name) < MAX_LEN_VISIBLE
            else song.name[:MAX_LEN_VISIBLE]+"...")   #Avoid long names

    #___

    '''
    Scale time to Song time
    scale.time -> 100 | x -> song.time | => x = scale.time*song.time/100
    '''
    def getTime(self, song:Song=None) -> int:
        song = self.song_playing if song is None else song
        return round((self.state_scale_time.get() * song.time) / 100)


    '''
    Song time to Scale time
    time -> song.time | x -> 100 | => x = time*100/song.time
    '''
    def setTime(self, time:int):
        self.state_scale_time.set((time * 100) / self.song_playing.time)
        self.state_txt_time1.set(Song.timeFormat(time))


#==================================================


ARTWORK_SIZE = (75,75)

class Artwork(TkCanvasGif):
    def __init__(self, w, *args, **kwargs):

        super().__init__(w,
            gif=b64ToPIL(b64img.gif_reproc),
            size=ARTWORK_SIZE,
            *args, **kwargs)

        #___

        self.artwork_default = PhotoImage(data=b64img.song_art_default)
        self.artwork_id = self.create_image(0,0, image=self.artwork_default, anchor="nw")
        self.setGif()

        self.__artwork:TkImage = None

    #__________________________________________________

    def setArtWork(self, song:Song):
        try:
            self.__artwork = PILToTk(song.getArt(ARTWORK_SIZE))
            self.itemconfig(self.artwork_id, image=self.__artwork)
        except:
            self.itemconfig(self.artwork_id, image=self.artwork_default)