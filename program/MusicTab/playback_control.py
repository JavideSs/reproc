from tkinter import Scale as TkScale, PhotoImage, font, DoubleVar, StringVar
from tkinter.ttk import Frame, Label, Separator, Scale
from ui.customtk import TkCanvasGif, TkButtonImgHoverImg, TkButtonImgHoverNone

from ui import images as b64img
from ui.images.utilities import *

from .song import Song

from data import config
from data.data_types import *

#==================================================

class PlaybackControl(Frame):
    def __init__(self, w, *args, **kwargs):

        self.playback = w.playback


        super().__init__(w, *args, **kwargs)


        self.artwork = Artwork(self)
        self.artwork.grid(row=0, column=0, rowspan=2, padx=8, pady=8)

        self.timeline = Timeline(self)
        self.timeline.grid(row=1, column=1, columnspan=9, pady=(5,10))

        self.btn_random = TkButtonImgHoverNone(self,
            command=self.playback.toggleRandom,
            imgs=(PhotoImage(data=b64img.btn_random_off),
                PhotoImage(data=b64img.btn_random_on)),
            bg=config.colors["BG"],
            change_img_on_click=True)
        self.btn_random.grid(row=0, column=1, pady=(8,0))

        if config.general["random"]:
            self.playback.toggleRandom()
            self.btn_random.set_img(1)

        self.btn_loop = TkButtonImgHoverNone(self,
            command=self.playback.toggleLoop,
            imgs=(PhotoImage(data=b64img.btn_loop_off),
                PhotoImage(data=b64img.btn_loop_on)),
            bg=config.colors["BG"],
            change_img_on_click=True)
        self.btn_loop.grid(row=0, column=2, pady=(8,0))

        if config.general["loop"]:
            self.playback.toggleLoop()
            self.btn_loop.set_img(1)

        self.separator1 = Separator(self, orient="vertical")
        self.separator1.grid(row=0, column=3, sticky="ns", padx=(10,10), pady=(13,5))

        self.btn_play_previous = TkButtonImgHoverImg(self,
            command=w.fprevious,
            imgs=(b64img.btn_playizq,),
            bg=config.colors["BG"])
        self.btn_play_previous.grid(row=0, column=4, pady=(8,0))

        self.btn_playpause = TkButtonImgHoverImg(self,
            command=w.fplaypause,
            imgs=(b64img.btn_play,
                b64img.btn_playing),
            bg=config.colors["BG"])
        self.btn_playpause.grid(row=0, column=5, padx=(2,2), pady=(8,0))

        self.btn_play_next = TkButtonImgHoverImg(self,
            command=w.fnext,
            imgs=(b64img.btn_playder,),
            bg=config.colors["BG"])
        self.btn_play_next.grid(row=0, column=6, pady=(8,0))

        self.separator2 = Separator(self, orient="vertical")
        self.separator2.grid(row=0, column=7, sticky="ns", padx=(10,5), pady=(13,5))

        self.btn_volume = TkButtonImgHoverImg(self,
            command=self._setVolumeDirect,
            imgs=(b64img.btn_volume_on,
                b64img.btn_volume_off),
            bg=config.colors["BG"],
            change_img_on_click=True)
        self.btn_volume.grid(row=0, column=8, sticky="e", pady=(8,0))

        self.scale_volume = TkScale(self,
            command=self._setVolume,
            orient="horizontal",
            width=10, length=50,
            from_=0, to=100,
            showvalue=False,
            highlightbackground=config.colors["BG"],
            troughcolor=config.colors["WIDGET_BG1"],
            activebackground=config.colors["WIDGET_BG2"])
        self.scale_volume.grid(row=0, column=9, pady=(8,0))

        self.scale_volume.set(config.general["volume"]*100)


        #self.__volume_previous" != 0 when mute, represents the volume before mute, == 0 when unmute
        self.__volume_previous = 0

    #__________________________________________________

    def setPlay(self):
        self.btn_playpause.set_img(1)
        self.artwork.playGif()


    def setPause(self):
        self.btn_playpause.set_img(0)
        self.artwork.stopGif()

    #___

    #Set volume with btn, triggers "self._setVolume()"
    def _setVolumeDirect(self):
        #Mute to unmute
        if self.__volume_previous:
            self.scale_volume.set(self.__volume_previous)
            self.__volume_previous = 0
        #Unmute to mute
        else:
            self.__volume_previous = self.scale_volume.get()
            self.scale_volume.set(0)


    #Set volume with scale
    def _setVolume(self, state_scale_volume):
        volume = float(state_scale_volume)/100
        self.playback.setVolume(volume)

        #Mute to unmute
        if self.__volume_previous and volume:
            self.btn_volume.set_img(0)
            self.__volume_previous = 0
        #Unmute to mute
        elif not self.__volume_previous and not volume:
            self.btn_volume.set_img(1)
            self.__volume_previous = 100


#==================================================


class Timeline(Frame):
    INIT_TIME = Song.formatTime(0)
    INIT_NAME = "._."
    NAME_MAX_SIZE_VISIBLE = 230

    def __init__(self, w, *args, **kwargs):

        super().__init__(w, *args, **kwargs)


        self.state_txt_time1 = StringVar()
        self.state_txt_time1.set(Timeline.INIT_TIME)
        self.txt_time1 = Label(self,
            textvariable=self.state_txt_time1,
            background=config.colors["BG"],
            font=font.nametofont("font_small"))
        self.txt_time1.grid(row=0, column=0, sticky="sw")

        self.state_txt_song = StringVar()
        self.state_txt_song.set(Timeline.INIT_NAME)
        self.txt_song = Label(self,
            textvariable=self.state_txt_song,
            background=config.colors["BG"])
        self.txt_song.grid(row=0, column=1, pady=(0,2))

        self.state_txt_time2 = StringVar()
        self.state_txt_time2.set(Timeline.INIT_TIME)
        self.txt_time1 = Label(self,
            textvariable=self.state_txt_time2,
            background=config.colors["BG"],
            font=font.nametofont("font_small"))
        self.txt_time1.grid(row=0, column=2, sticky="se")

        self.state_scale_time = DoubleVar()
        self.scale_time = Scale(self,
            orient="horizontal",
            length=300,
            from_=0, to=100,
            value=0, variable=self.state_scale_time)
        self.scale_time.grid(row=1, column=0, columnspan=3)
        #Set time when direct click on the timeline
        self.scale_time.bind("<Button-1>", self._setTimeDirect)


        self.song_playing:Song = Song(Song.NONE_SONG)

    #__________________________________________________

    def _setTimeDirect(self, event:Event):
        self.scale_time.event_generate("<Button-3>", x=event.x, y=event.y)
        return "break"  #fun: Avoid recoil when holding

    #___

    def setNewSong(self, song:Song):
        #Avoid long names
        def limit_text_size(text:str, size:int):
            f = font.Font(font=font.nametofont("font"))
            cond = lambda text: f.measure(text)+f.measure("...") > size
            if cond(text):
                while cond(text):
                    text = text[:-1]
                text += "..."
            return text

        self.song_playing = song
        self.state_scale_time.set(0)
        self.state_txt_time1.set(Timeline.INIT_TIME)
        self.state_txt_time2.set(song.getFormattedTime())
        self.state_txt_song.set(limit_text_size(song.name, Timeline.NAME_MAX_SIZE_VISIBLE))

    #___

    def getTime(self) -> float:
        '''
        Scale time to Song time
        scale.time -> 100 | x -> song.time | => x = scale.time*song.time/100
        '''
        return (self.state_scale_time.get() * self.song_playing.time) / 100


    def setTime(self, time:int):
        '''
        Song time to Scale time
        time -> song.time | x -> 100 | => x = time*100/song.time
        '''
        self.state_scale_time.set((time * 100) / self.song_playing.time)
        self.state_txt_time1.set(Song.formatTime(time))


#==================================================


class Artwork(TkCanvasGif):
    SIZE = (75,75)

    def __init__(self, w, *args, **kwargs):

        super().__init__(w,
            gif=b64ToPIL(b64img.gif),
            size=Artwork.SIZE,
            *args, **kwargs)


        self.artwork_default = PhotoImage(data=b64img.song_art_default)
        self.artwork_id = self.create_image(0,0, image=self.artwork_default, anchor="nw")
        self.setGif()

        self.__artwork = PhotoImage()

    #__________________________________________________

    def setArtWork(self, song:Song):
        try:
            self.__artwork = PILToTk(song.getArt(Artwork.SIZE))
            self.itemconfig(self.artwork_id, image=self.__artwork)
        except:
            self.itemconfig(self.artwork_id, image=self.artwork_default)