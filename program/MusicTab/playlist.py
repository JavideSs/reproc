from tkinter import PhotoImage, Widget, messagebox, Frame, Menu, Entry
from tkinter.ttk import Treeview, Separator
from customTk import TkButtonImgHoverBg, validEntryText

from data import config, images as b64img
from data.images.utilities import TkSolid
from .song import Song

import os, shutil
from random import choice
from operator import attrgetter
from locale import setlocale, strxfrm, LC_ALL
from typing import List, Tuple

from pygame import mixer

#==================================================

COLUMN_TITLE_WIDTH = 345
COLUMN_DURATION_WIDTH = 40
ROW_HEIGHT = 25
N_ROWS = 14
IMGS_SIZE = (ROW_HEIGHT,ROW_HEIGHT)
NONE_ID = -1

class Playlist(Treeview):
    def __init__(self, w, *args, **kwargs):

        #selectmode="browse"    -> Cannot select multiple songs
        #show="tree"            -> Without headers
        super().__init__(w,
            show="tree",
            selectmode="browse",
            *args, **kwargs)

        self["columns"] = ("#duration")
        self.column("#0", width=COLUMN_TITLE_WIDTH)
        self.column("#duration", width=COLUMN_DURATION_WIDTH)

        #___

        self.imgs = {
            "play"      : PhotoImage(data=b64img.btn_TV_play),
            "playing"   : PhotoImage(data=b64img.btn_TV_playing),
            "none"      : TkSolid(size=IMGS_SIZE, color=config.colors["BG"])
        }

        #___

        #Fix: Scroll does not detect the change of itemTV, we must do it manually
        self.bind("<MouseWheel>", self._motionItem)
        #Stop hovering itemTV when stop hovering in TV
        self.bind("<Leave>", self._motionItemLeave)
        #Edit song when right click in itemTV
        self.bind("<Button-3>", lambda event: LabelEditSong(self, event))

        #___

        setlocale(LC_ALL, "")                   #Accepts special characters from all languages
        mixer.init(frequency=48000, channels=2) #MP3 frequency with 320kbps by default, stereo

        #___

        '''
        A song is loaded when no song has been heard yet, or self.playNext() cannot be done
        "self.isSongPlaying()" is false when song is paused, is false when not song is loaded
        "self.isSongLoad()" is true when song is paused, is false when not song is loaded
        "any(self.__songs_previous_id)" is true when song is paused, is true when not song is loaded but there has already been at least one song loaded
        '''

        '''
        (*)
        In pygame v1 "get_busy()" indicated "self.isSongLoad()", so self.__ is_playing had to be manually controlled
        In pygame v2 "get_busy()" indicated "self.isSongPlaying()", so self.__is_load had to be manually controlled
        '''

        self.__state_random = False
        self.__state_loop = False

        self.__is_load = False

        self.__song_playing_id = NONE_ID
        self.__song_hover_id = NONE_ID

        self.__songs_all: List[Song] = []
        self.__songs_previous_id: List[int] = []

    #__________________________________________________

    def _motionItemLeave(self, _event):
        #"self.__song_hover_id" may have no value when the TV is not completely full
        #"self.__song_playing_id" is not modified
        if self.__song_hover_id!=NONE_ID and self.__song_hover_id!=self.__song_playing_id:
            self.tag_configure(self.__song_hover_id,
                image=self.imgs["none"],
                background=config.colors["TV_BG"],
                foreground=config.colors["TV_FG"])
            self.__song_hover_id = NONE_ID


    def _motionItem(self, event):
        #Fix down scroll
        if event.delta == -120:
            #if its not the beginning
            if self.identify_row(ROW_HEIGHT*(N_ROWS +1)):
                event_y = event.y+ROW_HEIGHT
            else: return
        #Fix up scroll
        elif event.delta == 120:
            #If its not the end
            if self.identify_row(-ROW_HEIGHT):
                event_y = event.y-ROW_HEIGHT
            else: return
        #Not scroll
        else:
            event_y = event.y

        item_hover_id = int(self.identify_row(event_y))

        #If motion to another itemTV
        if item_hover_id != self.__song_hover_id:
            #Reset previous hover itemTV
            if self.__song_hover_id != NONE_ID:
                if self.__song_hover_id != self.__song_playing_id:
                    self.tag_configure(self.__song_hover_id,
                        image=self.imgs["none"],
                        background=config.colors["TV_BG"],
                        foreground=config.colors["TV_FG"])
                else:
                    self.tag_configure(self.__song_hover_id,
                        background=config.colors["TV_BG"])
            #Config new hover itemTV
            if item_hover_id != self.__song_playing_id:
                self.tag_configure(item_hover_id,
                    image=self.imgs["play"],
                    background=config.colors["TV_BG_HOVER"],
                    foreground=config.colors["TV_FG_HOVER"])

        self.__song_hover_id = item_hover_id

    #___

    def setPlaylist(self, playlist_path:str):
        with os.scandir(playlist_path) as it_folder:
            self.delPlaylist()

            for file in it_folder:
                if file.is_file and file.name.endswith(config.SUPPORTED_SONG_FORMATS):
                    song = Song(file.path)
                    self.__songs_all.append(song)
                    self.__insertSongTV(song)


    def delPlaylist(self):
        self.__songs_all.clear()
        self.__songs_previous_id.clear()
        self.delete(*self.get_children())

        if self.isSongLoad():
            mixer.music.unload()
            mixer.music.stop()
            self.__is_load = False
            self.__song_playing_id = NONE_ID

    #___

    #Insert song in TV
    def __insertSongTV(self, song:Song, pos="end"):
        self.insert(
            "", pos,
            text="   "+song.name,
            values=(song.getTimeFormat(),),
            iid=song.id, tag=song.id)

        #Magically the previous state if it was filtered is preserved
        if song.id != self.__song_playing_id:
            self.tag_configure(song.id,
                image=self.imgs["none"])

        self.tag_bind(song.id, "<Motion>", callback=self._motionItem)


    #Move song in TV
    def move(self, song:Song, pos_new:int):
        self.delete(song.id)
        self.__insertSongTV(song, pos_new)


    #Insert song in playlist/TV
    def __add__(self, song:Song):
        self.__songs_all.append(song)
        self.__insertSongTV(song)
        self.selection_set(song.id)
        self.see(song.id)


    #Remove song in playlist/TV
    def __sub__(self, song:Song):
        self.__songs_all.remove(song)
        if song.id in self.__songs_previous_id:
            self.__songs_previous_id.remove(song.id)
        self.delete(song.id)

    #___

    def isSongLoad(self) -> bool:
        return self.__is_load


    def isSongPlaying(self) -> bool:
        return mixer.music.get_busy()


    def getSongById(self, song_id:int) -> Song:
        for song in self.__songs_all:
            if song.id == song_id:
                return song
        return None


    def getSongPlayingId(self) -> int:
        return self.__song_playing_id


    def getSongPlaying(self) -> Song:
        return self.getSongById(self.getSongPlayingId())


    def getAllSongs(self) -> List[Song]:
        return self.__songs_all

    #___

    def playById(self, song_id:int):
        #Reset previous playing itemTV
        if len(self.__songs_previous_id) > 0:
            self.tag_configure(self.__song_playing_id,
                image=self.imgs["none"],
                foreground=config.colors["TV_FG"])

        song = self.getSongById(song_id)

        #pygame.mixer does not support different frequencies
        if mixer.get_init()[0] != song.getFrequency():
            mixer.quit()
            mixer.init(frequency=song.getFrequency(), channels=2)

        mixer.music.load(song.path)
        mixer.music.play()
        self.__is_load = True

        self.__song_playing_id = song_id
        self.tag_configure(self.__song_playing_id,
            image=self.imgs["playing"],
            foreground=config.colors["TV_FG_PLAYING"])

        #Push to "self.__songs_previous_id" if it is the first song or it is not the previous song
        if (not any(self.__songs_previous_id)) or (song_id!=self.__songs_previous_id[-1]):
            self.__songs_previous_id.append(song_id)


    #Play the selected itemTV
    def directPlay(self) -> bool:
        #If song is playing, play/pause itemTV
        if int(self.selection()[0]) == self.__song_playing_id:
            self.playpause()
            return False

        #If new song, play selected itemTV
        else:
            self.playById(int(self.selection()[0]))
            return True


    def playpause(self) -> bool:
        #Play to pause
        if self.isSongPlaying():
            mixer.music.pause()
            self.tag_configure(self.__song_playing_id,
                image=self.imgs["play"])
            return False

        else:
            #Pause to play
            if self.isSongLoad():
                mixer.music.unpause()
                self.tag_configure(self.__song_playing_id,
                    image=self.imgs["playing"])
                return False

            #First song to listen
            elif any(self.get_children()):
                self.playNext()
                return True

            else: return False


    def playNext(self) -> bool:
        #In bucle
        if self.__state_loop and any(self.__songs_previous_id):
            mixer.music.rewind()

        #In random and any in TV
        elif self.__state_random and any(self.get_children()):
            self.playById(choice([song for song in self.__songs_all if song.visible_inplaylist]).id)

        #Now and next is in TV
        elif self.isSongLoad() and self.getSongById(self.__song_playing_id).visible_inplaylist and self.next(self.__song_playing_id):
            self.playById(int(self.next(self.__song_playing_id)))

        #Any in TV
        elif any(self.get_children()):
            #Play first itemTV in view
            self.playById(int(self.identify_row(ROW_HEIGHT)))

        else:
            self.__is_load = False
            return False

        self.selection_set(self.__song_playing_id)
        self.see(self.__song_playing_id)
        return True


    def playPrevious(self) -> bool:
        if len(self.__songs_previous_id) > 0:
            #One is always left in the "self.__songs_previous_id", it loops with itself
            if len(self.__songs_previous_id) > 1:
                del self.__songs_previous_id[-1]

                if self.exists(self.__songs_previous_id[-1]):
                    self.playById(self.__songs_previous_id[-1])
                #Rewind if the previous itemTV does not exist
                else:
                    mixer.music.rewind()
            #Rewind if there is not previous itemTV
            else:
                mixer.music.rewind()

            if self.exists(self.__songs_previous_id[-1]):
                self.selection_set(self.__song_playing_id)
                self.see(self.__song_playing_id)

            return True
        else: return False

    #___

    def toggleRandom(self):
        self.__state_random = not self.__state_random


    def toggleLoop(self):
        self.__state_loop = not self.__state_loop

    #___

    @staticmethod
    def setVolume(volume:float):
        mixer.music.set_volume(volume)


    @staticmethod
    def setTime(time:float):
        #(!) "set_pos()" advances rarely
        mixer.music.rewind()
        mixer.music.set_pos(time)

    #___

    def getStates(self) -> Tuple[float, bool, bool]:
        return (mixer.music.get_volume(), self.__state_random, self.__state_loop)

    #___

    def filterName(self, song_name:str):
        #Restart TV depending on visibility
        self.delete(*self.get_children())
        for song in self.__songs_all:
            song.visible_inplaylist = song_name.lower() in song.name.lower()
            if song.visible_inplaylist: self.__insertSongTV(song)


    def sortBy(self, col:str, reverse:bool):
        if col == "title":  self.__songs_all.sort(reverse=reverse, key=lambda song: strxfrm(song.name))
        else:               self.__songs_all.sort(reverse=reverse, key=lambda song: attrgetter(col)(song))

        #Restart TV
        self.delete(*self.get_children())
        for song in self.__songs_all:
            if song.visible_inplaylist:
                self.__insertSongTV(song)


#==================================================


class LabelEditSong(Frame):
    def __init__(self, playlist:Playlist, event, *args, **kwargs):

        self.playlist = playlist
        self.playlist_handler = playlist.master.playlist_control.playlist_handler_set

        song_id = int(playlist.identify_row(event.y))
        self.song = self.playlist.getSongById(song_id)

        coord = playlist.bbox(song_id)
        self.__coord_y = coord[1]

        colors = self.__colorItemTV()

        #highlightthickness=1 -> With outline
        super().__init__(self.playlist,
            width=coord[2]-ROW_HEIGHT, height=coord[3],
            background=colors[0],
            highlightthickness=1,
            *args, **kwargs)
        self.place(x=25, y=coord[1])

        #___

        self.entry_edit_song = Entry(self,
            width=45,
            background=colors[0],
            foreground=colors[1],
            borderwidth=0)
        self.entry_edit_song.grid(row=0, column=0, padx=(7,7))

        self.entry_edit_song.insert(0, self.song.name)
        self.entry_edit_song.icursor(5)
        self.entry_edit_song.focus()

        #___

        self.separator = Separator(self, orient="vertical")
        self.separator.grid(row=0, column=1, sticky="ns", pady=2)

        #___

        self.btn_rename = TkButtonImgHoverBg(self,
            command=self._rename,
            imgs=(PhotoImage(data=b64img.btn_TV_edit_rename),),
            bg=colors[0],
            bg_on_hover=config.colors["BTN_BG_HOVER"])
        self.btn_rename.grid(row=0, column=2)

        #___

        self.btn_move = TkButtonImgHoverBg(self,
            command=self._move,
            imgs=(PhotoImage(data=b64img.btn_TV_edit_move),),
            bg=colors[0],
            bg_on_hover=config.colors["BTN_BG_HOVER"])
        self.btn_move.grid(row=0, column=3, padx=2)

        #___

        self.btn_delete = TkButtonImgHoverBg(self,
            command=self._del,
            imgs=(PhotoImage(data=b64img.btn_TV_edit_delete),),
            bg=colors[0],
            bg_on_hover=config.colors["BTN_BG_HOVER"])
        self.btn_delete.grid(row=0, column=4)

        #___

        #Destroy when click in TV
        self.playlist.bind_all("<Button-1>", self._destroyLabel)
        #Destroy when scroll in TV
        self.playlist.bind("<MouseWheel>", self._destroyLabel)
        #Destroy when right click to open new label in TV
        self.playlist.bind("<Button-3>", self._destroyLabel)

    #______________________________________________________________________________________

    def _destroyLabel(self, event=None):
        #Do nothing if left click in LabelEditSong
        if event and str(event.widget).startswith(str(self)):
            return

        #New label if it is the right click
        if event and event.num==3:
            LabelEditSong(self.playlist, event)
        #Unbind all and bind right btn by default
        else:
            self.playlist.unbind("<Button-1>")
            self.playlist.bind("<MouseWheel>", self.playlist._motionItem)
            self.playlist.bind("<Button-3>", lambda event: LabelEditSong(self.playlist, event))
        self.destroy()

    #___

    def __isTheSongPlaying(self) -> bool:
        return self.playlist.getSongPlayingId() == self.song.id


    def __colorItemTV(self) -> Tuple[str, str]:
        #Is the focused itemTV
        if self.playlist.focus() and int(self.playlist.focus())==self.song.id:
            return (config.colors["TV_BG_SELECT"], config.colors["TV_FG_SELECT"])

        #Is not the focused itemTV but is playing
        elif self.__isTheSongPlaying():
            return (config.colors["TV_BG"], config.colors["TV_FG_PLAYING"])

        #Is just hovered
        else:
            return (config.colors["TV_BG_HOVER"], config.colors["TV_FG_HOVER"])

    #___

    def __checkImpediments(self, msg_error:str) -> bool:
        if self.__isTheSongPlaying():
            messagebox.showerror(msg_error, _("Action not allowed with a song that is playing"))

        elif not os.path.exists(config.playlist["path"]):
            messagebox.showwarning(msg_error, _("The folder does not to exist"))
            self.playlist_handler.delPlaylist(config.general["playlist"])

        elif not os.path.exists(self.song.path):
            messagebox.showerror(msg_error, _("The song does not to exist"))
            self.playlist - self.song

        else: return False
        return True

    #___

    def _rename(self):
        song_name_new = self.entry_edit_song.get()
        if validEntryText(song_name_new, text_original=self.song.name):

            if not self.__checkImpediments(_("Rename failed")):
                song_path_new = os.path.join(config.playlist["path"], song_name_new + self.song.extension)
                try:
                    os.rename(self.song.path, song_path_new)
                    #Refresh in TV
                    self.song.path = song_path_new
                    self.playlist.move(self.song, self.playlist.index(self.song.id))
                except:
                    messagebox.showerror(_("Rename failed"), _("Unknown action not allowed"))

        self._destroyLabel()


    def _move(self):
        tk_main_w = Widget.nametowidget(self, '.')
        coord_x = tk_main_w.winfo_x() + 250
        coord_y = tk_main_w.winfo_y() + self.__coord_y + 150

        self.menu = Menu(self,
            bg=config.colors["BG"],
            activebackground=config.colors["TV_BG_HOVER"],
            activeforeground=config.colors["FG"],
            tearoff=False)

        for playlist in config.user_config["Playlists"]:
            if playlist != config.general["playlist"]:
                #https://stackoverflow.com/questions/11723217/python-lambda-doesnt-remember-argument-in-for-loop
                func_get_set_playlist = lambda playlist=playlist: self.__move(playlist)
                self.menu.add_command(label=playlist, command=func_get_set_playlist)

        self.menu.tk_popup(coord_x, coord_y)


    def __move(self, playlist:str):
        if not self.__checkImpediments(_("Move failed")):
            playlist_path = config.user_config["Playlists"][playlist]["path"]

            if not os.path.exists(playlist_path):
                messagebox.showwarning(_("Move failed"), _("Destination folder does not exist"))
                self.playlist_handler.delPlaylist(playlist, in_tv=False)

            else:
                try:
                    shutil.copy2(src=self.song.path, dst=playlist_path)
                except:
                    messagebox.showerror(_("Move failed"), _("Unknown action not allowed"))

        self._destroyLabel()


    def _del(self):
        if not self.__checkImpediments(_("Delete failed")):
            try:
                os.remove(self.song.path)
                self.playlist - self.song
            except:
                messagebox.showerror(_("Delete failed"), _("Unknown action not allowed"))

        self._destroyLabel()