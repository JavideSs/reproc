import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from ui import customtk
from ui.utilities import *

from ui import sizes
from ui import images as b64img
from ui.images.utilities import *

from data import config
from data.data_types import *

from .song import Song

import os
import shutil
from operator import attrgetter
from locale import setlocale, strxfrm, LC_ALL

#==================================================

class Playlist(ttk.Treeview, TPlaylist):
    ROW_HEIGHT = 25
    COLUMN_TITLE_WIDTH = sizes.MUSICTAB_PLAYLIST_COLUMNTITLE_WIDTH
    COLUMN_DURATION_WIDTH = sizes.MUSICTAB_PLAYLIST_COLUMNDURATION_WIDTH
    IMGS_SIZE = (ROW_HEIGHT,ROW_HEIGHT)

    n_rows = 14

    def __init__(self, w, *args, **kwargs):

        #selectmode="browse"    -> Cannot select multiple songs
        #show="tree"            -> Without headers
        super().__init__(w,
            show="tree",
            selectmode="browse",
            height=Playlist.n_rows,
            *args, **kwargs)

        self["columns"] = ("#duration")
        self.column("#0", width=Playlist.COLUMN_TITLE_WIDTH)
        self.column("#duration", width=Playlist.COLUMN_DURATION_WIDTH)

        self.imgs = {
            "play"      : PhotoImage(data=b64img.btn_TV_play),
            "playing"   : PhotoImage(data=b64img.btn_TV_playing),
            "none"      : TkSolid(size=Playlist.IMGS_SIZE, color=config.colors["BG"])
        }


        #Resize
        w.bind("<Configure>", self._resize)
        self._resize_timer = None
        #Stop hovering itemTV when stop hovering in TV
        self.bind("<Leave>", self._movItemLeave)
        #fun: Scroll does not detect the change of itemTV, we must do it manually
        self.bind("<MouseWheel>", self._movItem)
        #Edit song when right click in itemTV
        self.bind("<Button-3>", lambda event: LabelEditSong(self, event) if self.identify_row(event.y) != "" else None)


        self.__song_hover_id = Song.NONE_ID


        setlocale(LC_ALL, "")   #Accepts special characters from all languages

    #__________________________________________________

    def _resize(self, event:Event):
        '''
        fun: The window flickers, and when is maximized it resized randomly
        '''

        OTHER_HEIGHT = 130  #Initially as tk_main_w.winfo_height - self.winfo_height()

        Playlist.n_rows = (event.height-OTHER_HEIGHT) // Playlist.ROW_HEIGHT
        self.configure(height=Playlist.n_rows)
        self.update()

        def resize_w():
            tk_main_w = tk.Widget.nametowidget(self, ".")
            tk_main_w.geometry("400x{}".format(self.winfo_height()+OTHER_HEIGHT))
            tk_main_w.update()

        #The manual resizing will be cancelled for now if the user continues to resize during the waiting period
        if self._resize_timer is not None:
            self.after_cancel(self._resize_timer)
        self._resize_timer = self.after(100, resize_w)


    def _movItemLeave(self, _event):
        #"self.__song_hover_id" may have no value when the TV is not completely full
        #"self.playback.song_playing.id" is not modified
        if self.__song_hover_id!=Song.NONE_ID and self.__song_hover_id!=self.playback.song_playing.id:
            self.tag_configure(str(self.__song_hover_id),
                image=self.imgs["none"],
                background=config.colors["TV_BG"],
                foreground=config.colors["TV_FG"])
            self.__song_hover_id = Song.NONE_ID


    def _movItem(self, event:Event):
        #Fix down scroll
        if event.delta == -120:
            #if its not the beginning
            if self.identify_row(Playlist.ROW_HEIGHT*(Playlist.n_rows +1)):
                event_y = event.y + Playlist.ROW_HEIGHT
            else: return
        #Fix up scroll
        elif event.delta == 120:
            #If its not the end
            if self.identify_row(-Playlist.ROW_HEIGHT):
                event_y = event.y - Playlist.ROW_HEIGHT
            else: return
        #Not scroll
        else:
            event_y = event.y

        item_hover_id = int(self.identify_row(event_y))

        #If motion to another itemTV
        if item_hover_id != self.__song_hover_id:
            #Reset previous hover itemTV
            if self.__song_hover_id != Song.NONE_ID:
                if self.__song_hover_id != self.playback.song_playing.id:
                    self.tag_configure(str(self.__song_hover_id),
                        image=self.imgs["none"],
                        background=config.colors["TV_BG"],
                        foreground=config.colors["TV_FG"])
                else:
                    self.tag_configure(str(self.__song_hover_id),
                        background=config.colors["TV_BG"])
            #Config new hover itemTV
            if item_hover_id != self.playback.song_playing.id:
                self.tag_configure(str(item_hover_id),
                    image=self.imgs["play"],
                    background=config.colors["TV_BG_HOVER"],
                    foreground=config.colors["TV_FG_HOVER"])

        self.__song_hover_id = item_hover_id

    #___

    def setFocus(self, id:int):
        self.selection_set(str(id))
        self.focus(str(id))
        self.see(str(id))


    def setPlay(self, id:int):
        self.tag_configure(str(id),
            image=self.imgs["playing"],
            foreground=config.colors["TV_FG_PLAYING"])


    def setPause(self, id:int):
        self.tag_configure(str(id),
            image=self.imgs["play"])


    def setUnload(self, id:int):
        self.tag_configure(str(id),
            image=self.imgs["none"],
            foreground=config.colors["TV_FG"])

    #___

    def setPlayback(self, playback):
        self.playback = playback

    #___

    def setPlaylist(self, playlist_path:str, filter:str, sortby:Tuple[str,bool]):
        self.delPlaylist()

        for file in os.scandir(playlist_path):
            if file.is_file and Song.supported_format(file.name):
                self.playback.songs.append(Song(file.path))

        self.filterName(filter, refresh=False)
        self.sortBy(*sortby, refresh=False)
        self.refresh()


    def delPlaylist(self):
        self.playback.songs.clear()
        self.playback.songs_previous_id.clear()
        self.delete(*self.get_children())

    #___

    #Insert song in TV
    def __insertSongTV(self, song:Song, pos:Union[int,"end"]="end"):
        self.insert(
            "", pos,
            text="   "+song.name,
            values=(song.getFormattedTime(),),
            iid=str(song.id), tags=str(song.id))

        #fun: The previous state if it was filtered remains
        if song.id != self.playback.song_playing.id:
            self.tag_configure(str(song.id),
                image=self.imgs["none"])

        self.tag_bind(str(song.id), "<Motion>", callback=self._movItem)


    #Move song in TV
    def move(self, song:Song, pos_new:int):
        self.delete(str(song.id))
        self.__insertSongTV(song, pos_new)


    #Insert song in playlist/TV
    def append(self, song:Song):
        self.playback.songs.append(song)
        self.__insertSongTV(song)
        self.selection_set(str(song.id))
        self.see(str(song.id))


    #Remove song in playlist/TV
    def remove(self, song:Song):
        self.playback.songs.remove(song)
        if song.id in self.playback.songs_previous_id:
            self.playback.songs_previous_id.remove(song.id)
        self.delete(str(song.id))

    #___

    def exists(self, id:int):
        return super().exists(str(id))


    def isListed(self, id:int):
        return self.playback.getSongById(id)!=Song(Song.NONE_SONG) and self.playback.getSongById(id).visible


    def items(self):
        return list(map(int, self.get_children()))


    def firstItemVisible(self):
        return int(self.identify_row(Playlist.ROW_HEIGHT))


    def next(self, id:int):
        nextid = super().next(str(id))
        return int(nextid) if nextid else Song.NONE_ID

    #___

    def refresh(self):
        self.delete(*self.get_children())
        for song in self.playback.songs:
            if song.visible:
                self.__insertSongTV(song)


    def filterName(self, song_name:str, refresh=True):
        for song in self.playback.songs:
            song.visible = song_name.lower() in song.name.lower()

        if refresh: self.refresh()


    def sortBy(self, atr:str, reverse:bool, refresh=True):
        if atr == "title":
            self.playback.songs.sort(reverse=reverse, key=lambda song: strxfrm(song.name))
        else:
            self.playback.songs.sort(reverse=reverse, key=lambda song: attrgetter(atr)(song))

        if refresh: self.refresh()


#==================================================


class LabelEditSong(tk.Frame):
    def __init__(self, playlist:Playlist, event:Event, *args, **kwargs):

        self.playlist = playlist
        self.playlist_handler = playlist.master.playlist_control.playlist_handler_set
        self.playback = playlist.master.playback


        song_id = int(playlist.identify_row(event.y))
        self.song = self.playback.getSongById(song_id)

        coord = playlist.bbox(song_id)
        self.__coord_y = coord[1]

        colors = self.__colorItemTV()


        #highlightthickness=1 -> With outline
        super().__init__(self.playlist,
            width=int(coord[2]) - Playlist.ROW_HEIGHT, height=coord[3],
            background=colors[0],
            highlightthickness=1,
            *args, **kwargs)
        self.place(x=25, y=coord[1])


        self.entry_edit_song = tk.Entry(self,
            width=sizes.MUSICTAB_PLAYLIST_LABELEDITSONG_ENTRYEDITSONG_WIDTH,
            background=colors[0],
            foreground=colors[1],
            borderwidth=0)
        self.entry_edit_song.grid(row=0, column=0, padx=(7,7))

        self.entry_edit_song.insert(0, self.song.name)
        self.entry_edit_song.icursor(5)
        self.entry_edit_song.focus()

        self.separator = ttk.Separator(self, orient="vertical")
        self.separator.grid(row=0, column=1, sticky="ns", pady=2)

        self.btn_rename = customtk.TkButtonImgHoverBg(self,
            command=self._rename,
            imgs=(PhotoImage(data=b64img.btn_TV_edit_rename),),
            bg=colors[0],
            bg_on_hover=config.colors["BTN_BG_HOVER"])
        self.btn_rename.grid(row=0, column=2)

        self.btn_move = customtk.TkButtonImgHoverBg(self,
            command=self._move,
            imgs=(PhotoImage(data=b64img.btn_TV_edit_move),),
            bg=colors[0],
            bg_on_hover=config.colors["BTN_BG_HOVER"])
        self.btn_move.grid(row=0, column=3, padx=2)

        self.btn_delete = customtk.TkButtonImgHoverBg(self,
            command=self._del,
            imgs=(PhotoImage(data=b64img.btn_TV_edit_delete),),
            bg=colors[0],
            bg_on_hover=config.colors["BTN_BG_HOVER"])
        self.btn_delete.grid(row=0, column=4)


        #Destroy when click in TV
        self.playlist.bind_all("<Button-1>", self._destroyLabel)
        #Destroy when scroll in TV
        self.playlist.bind("<MouseWheel>", self._destroyLabel)
        #Destroy when right click to open new label in TV
        self.playlist.bind("<Button-3>", self._destroyLabel)

    #______________________________________________________________________________________

    def _destroyLabel(self, event:Event=None):
        #Do nothing if left click in LabelEditSong
        if event and str(event.widget).startswith(str(self)):
            return

        #New label if it is the right click
        if event and event.num==3 and self.playlist.identify_row(event.y)!="":
            LabelEditSong(self.playlist, event)

        #Unbind or bind by default
        else:
            self.playlist.unbind("<Button-1>")
            self.playlist.bind("<MouseWheel>", self.playlist._movItem)
            self.playlist.bind("<Button-3>", lambda event: LabelEditSong(self.playlist, event) if self.playlist.identify_row(event.y) != "" else None)
        self.destroy()

    #___

    def __isTheSongPlaying(self):
        return self.playback.song_playing == self.song


    def __colorItemTV(self) -> Tuple[str,str]:
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

    def __canbeEdited(self, msg_error:str):
        if self.__isTheSongPlaying():
            messagebox.showerror(msg_error, _("Song is playing"))

        elif not os.path.exists(config.playlist["path"]):
            messagebox.showwarning(msg_error, _("The folder does not to exist"))
            self.playlist_handler.delPlaylist(config.general["playlist"])

        elif not os.path.exists(self.song.path):
            messagebox.showerror(msg_error, _("The song does not to exist"))
            self.playlist.remove(self.song)

        else:
            return True
        return False


    def _rename(self):
        song_name_new = self.entry_edit_song.get()
        if validEntryText(song_name_new, text_original=self.song.name):

            if self.__canbeEdited(_("Rename failed")):
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
        def _move(playlist:str):
            if self.__canbeEdited(_("Move failed")):
                playlist_dst_path = config.user_config["Playlists"][playlist]["path"]

                if not os.path.exists(playlist_dst_path):
                    messagebox.showwarning(_("Move failed"), _("Destination folder does not exist"))
                    self.playlist_handler.delPlaylist(playlist, in_tv=False)

                else:
                    try:
                        shutil.copy2(src=self.song.path, dst=playlist_dst_path)
                    except:
                        messagebox.showerror(_("Move failed"), _("Unknown action not allowed"))

        self.menu = tk.Menu(self.playlist,
            bg=config.colors["BG"],
            activebackground=config.colors["TV_BG_HOVER"],
            activeforeground=config.colors["FG"],
            tearoff=False)

        menu_maxwidth = 0
        f = font.Font(font=font.nametofont("font"))

        for playlist in config.user_config["Playlists"]:
            if playlist != config.general["playlist"]:
                #https://stackoverflow.com/questions/11723217/python-lambda-doesnt-remember-argument-in-for-loop
                self.menu.add_command(label=playlist, command=lambda playlist=playlist: _move(playlist))

                width = f.measure(playlist)
                if width > menu_maxwidth:
                    menu_maxwidth = width

        tk_main_w = tk.Widget.nametowidget(self, ".")
        coord_x = tk_main_w.winfo_x() - menu_maxwidth + 320
        coord_y = tk_main_w.winfo_y() + self.__coord_y + sizes.MUSICTAB_PLAYLIST_LABELEDITSONG_MENU_HEIGHT

        self.menu.tk_popup(coord_x, coord_y)

        self._destroyLabel()


    def _del(self):
        if self.__canbeEdited(_("Delete failed")):
            try:
                os.remove(self.song.path)
                self.playlist.remove(self.song)
            except:
                messagebox.showerror(_("Delete failed"), _("Unknown action not allowed"))

        self._destroyLabel()