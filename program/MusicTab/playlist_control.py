import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog
from ui import customtk

from ui import images as b64img
from ui.images.utilities import *
from ui import validEntryText

from data import config
from data.data_types import *

from .song import Song

import os
import shutil
from threading import Thread

#==================================================

class PlaylistControl(ttk.Frame):
    def __init__(self, w, *args, **kwargs):
        self.EMPTY_SEARCH_TEXT = _("Search song...")    #fun: After defined _ by gettext


        self.playlist = w.playlist


        super().__init__(w, *args, **kwargs)


        self.playlist_handler_edit = customtk.TkButtonImgHoverBg(self,
            command=lambda: TopLevelPlaylistEdit(self) if config.general["playlist"] != "" else None,
            imgs=(PhotoImage(data=b64img.btn_configplaylist),),
            bg=config.colors["BG"],
            bg_on_hover=config.colors["BTN_BG_HOVER"])
        self.playlist_handler_edit.grid(row=0, column=0, sticky="nsew")

        self.playlist_handler_set = PlaylistHandlerSet(self)
        self.playlist_handler_set.grid(row=0, column=1, sticky="nsew", padx=(5,8), pady=5)

        #When the text is changed, triggers "self._search()"
        self.state_entry_search = tk.StringVar()
        self.state_entry_search.trace_add("write", self._search)

        self.entry_search = ttk.Entry(self,
            width=15,
            textvariable=self.state_entry_search)
        self.entry_search.grid(row=0, column=2, sticky="nsew", pady=5)
        self.entry_search.insert(0, self.EMPTY_SEARCH_TEXT)
        self.entry_search.bind("<FocusIn>", self._entryFocusEnter)
        self.entry_search.bind("<FocusOut>", self._entryFocusLeave)

        self.btn_search = customtk.TkButtonImgHoverBg(self,
            command=self._entryClear,
            imgs=(PhotoImage(data=b64img.btn_quitsearch),),
            bg=config.colors["BG"],
            bg_on_hover=config.colors["BTN_BG_HOVER"])
        self.btn_search.grid(row=0, column=3, sticky="nsew", padx=(0,5), pady=5)

        self.btn_sorttitle = customtk.TkButtonImgHoverBg(self,
            command=lambda: self._sortPlaylist(self.btn_sorttitle, "title"),
            imgs=(PhotoImage(data=b64img.btn_sorttitle),
                PhotoImage(data=b64img.btn_sorttitle_up),
                PhotoImage(data=b64img.btn_sorttitle_down)),
            bg=config.colors["BG"],
            bg_on_hover=config.colors["BTN_BG_HOVER"])
        self.btn_sorttitle.grid(row=0, column=4, sticky="nsew")

        self.btn_sortdate = customtk.TkButtonImgHoverBg(self,
            command=lambda: self._sortPlaylist(self.btn_sortdate, "date"),
            imgs=(PhotoImage(data=b64img.btn_sortdate),
                PhotoImage(data=b64img.btn_sortdate_up),
                PhotoImage(data=b64img.btn_sortdate_down)),
            bg=config.colors["BG"],
            bg_on_hover=config.colors["BTN_BG_HOVER"],
            change_img_on_click=True)
        self.btn_sortdate.grid(row=0, column=5, sticky="nsew")

        self.btn_sorttime = customtk.TkButtonImgHoverBg(self,
            command=lambda: self._sortPlaylist(self.btn_sorttime, "time"),
            imgs=(PhotoImage(data=b64img.btn_sorttime),
                PhotoImage(data=b64img.btn_sorttime_up),
                PhotoImage(data=b64img.btn_sorttime_down)),
            bg=config.colors["BG"],
            bg_on_hover=config.colors["BTN_BG_HOVER"],
            change_img_on_click=True)
        self.btn_sorttime.grid(row=0, column=6, sticky="nsew")


        self.btn_sorttitle.set_img(1)
        self.__btn_sort_active = [self.btn_sorttitle, 1]

    #__________________________________________________

    def _entryFocusEnter(self, _event):
        #Delete default text
        if self.entry_search.get() == self.EMPTY_SEARCH_TEXT:
            self.entry_search.delete(0, "end")


    def _entryFocusLeave(self, _event):
        #Delete text and insert default text if is invalid text
        if not validEntryText(self.entry_search.get()):
            self.entry_search.delete(0, "end")
            self.entry_search.insert(0, self.EMPTY_SEARCH_TEXT)
            config.playlist["filter"] = ""

    #___

    def _entryClear(self):
        #Delete text and insert default text if there is no focus
        if self.entry_search.get() != self.EMPTY_SEARCH_TEXT:
            self.entry_search.delete(0, "end")
            config.playlist["filter"] = ""
            if self.focus_get() != self.entry_search:
                self.entry_search.insert(0, self.EMPTY_SEARCH_TEXT)


    def _search(self, *_event):
        song_name = self.state_entry_search.get()
        if song_name != self.EMPTY_SEARCH_TEXT:
            self.playlist.filterName(song_name)
            config.playlist["filter"] = song_name


    def setSearch(self, song_name:str):
        if validEntryText(song_name):
            self.entry_search.delete(0, "end")
            self.entry_search.insert(0, song_name)
        else:
            self._entryClear()

    #___

    def _sortPlaylist(self, btn:customtk.TkButtonImgHoverBg, atr:str):
        #If click on another sort btn
        if btn != self.__btn_sort_active[0]:
            self.__btn_sort_active[0].set_img(0)            #Previous btn to normal
            if btn == self.btn_sorttitle: btn.set_img(1)    #Set title btn to up, the others are set automatically
            self.__btn_sort_active = [btn, 1]               #States are updated
            self.playlist.sortBy(atr, False)
            config.playlist["sortby"] = [atr, False]

        #If click on the same sort btn
        else:
            #If the btn was in up
            if self.__btn_sort_active[1] == 1:
                if btn == self.btn_sorttitle: btn.set_img(2)      #Set title btn to down, the others are set automatically
                self.__btn_sort_active[1] = 2                     #States are updated
                self.playlist.sortBy(atr, True)
                config.playlist["sortby"] = [atr, True]

            #If the btn was in down
            elif self.__btn_sort_active[1] == 2:
                self.btn_sorttitle.set_img(1)                     #Set title btn to down, the others are set automatically
                self.__btn_sort_active = [self.btn_sorttitle, 1]  #States are updated
                self.playlist.sortBy("title", False)
                config.playlist["sortby"] = ["title", False]

    def sortPlaylistForcedStates(self, atr:str, reverse:bool):
        sort = 1 if not reverse else 2

        if atr == "date":
            self.btn_sortdate.set_img(sort)
            self.btn_sorttitle.set_img(0)
            self.btn_sorttime.set_img(0)
            self.__btn_sort_active[0] = self.btn_sortdate

        elif atr == "time":
            self.btn_sorttime.set_img(sort)
            self.btn_sorttitle.set_img(0)
            self.btn_sortdate.set_img(0)
            self.__btn_sort_active[0] = self.btn_sorttime

        else:
            self.btn_sorttitle.set_img(sort)
            self.btn_sortdate.set_img(0)
            self.btn_sorttime.set_img(0)
            self.__btn_sort_active[0] = self.btn_sorttitle

        self.__btn_sort_active[1] = sort


    def sortPlaylistForced(self, atr:str, reverse:bool):
        self.sortPlaylistForcedStates(atr, reverse)
        self.playlist.sortBy(atr, reverse)


#==================================================


class PlaylistHandlerSet(ttk.Frame):
    def __init__(self, w:PlaylistControl, *args, **kwargs):
        self.EMPTY_MENUBTN:str = _("Select Playlist")    #fun: After defined _ by gettext


        self.playlist = w.playlist
        self.playlist_control = w
        self.playback = w.master.playback


        super().__init__(w, *args, **kwargs)


        self.menubtn = ttk.Menubutton(self,
            direction="above",
            width=13,
            text=config.general["playlist"])
        self.menubtn.pack()

        self.menu = tk.Menu(self.menubtn,
            bg=config.colors["BG"],
            activebackground=config.colors["TV_BG_HOVER"],
            activeforeground=config.colors["FG"],
            tearoff=False)

        self.menu.add_command(label=_("Import Playlist"), command=self._newPlaylist)
        self.menu.add_separator()
        for playlist in config.user_config["Playlists"]:
            #https://stackoverflow.com/questions/11723217/python-lambda-doesnt-remember-argument-in-for-loop
            func_get_set_playlist = lambda playlist=playlist: self.setPlaylist(playlist)
            self.menu.add_command(label=playlist, command=func_get_set_playlist)
        self.menubtn.configure(menu=self.menu)

    #__________________________________________________

    def _newPlaylist(self):
        folder = filedialog.askdirectory(title=_("Select folder for new playlist"))
        if folder == "": return

        playlist = os.path.basename(folder)

        if playlist not in config.user_config["Playlists"]:
            config.user_config["Playlists"][playlist] = {
                "path":os.path.normcase(folder),
                "sortby":["title",False],
                "filter":""
            }

            self.menu.add_command(label=playlist, command=lambda: self.setPlaylist(playlist))

        self.setPlaylist(playlist)


    def setPlaylist(self, playlist:str):
        def setPlaylist(playlist:str, playlist_path:str):
            #self.playback.songs is updating, prevent editing it
            def config_state_widget(widget, state):
                for child in widget.children.values():
                    try: child.configure(state=state)
                    except: pass

            self.menubtn["text"] = playlist
            self.playlist_control.setSearch(config.playlist["filter"])  #No songs yet, write event has effect on nothing
            self.playlist_control.sortPlaylistForcedStates(*config.playlist["sortby"])

            config_state_widget(self.playlist_control, "disable")
            self.playlist.setPlaylist(playlist_path, config.playlist["filter"], config.playlist["sortby"])
            config_state_widget(self.playlist_control, "normal")

        if playlist == "":
            self.menubtn["text"] = self.EMPTY_MENUBTN
            return

        playlist_dict = config.user_config["Playlists"][playlist]
        playlist_path = playlist_dict["path"]

        if not os.path.exists(playlist_path):
            messagebox.showerror(_("Load failed"), _("The folder does not to exist"))
            self.delPlaylist(playlist)
            return

        config.general["playlist"] = playlist
        config.playlist = playlist_dict

        Thread(
            target=setPlaylist,
            args=(playlist, playlist_path),
            daemon=True
        ).start()


    def renamePlaylist(self, playlist_new:str, playlist_new_path:str):
        playlist_old = config.general["playlist"]
        config.general["playlist"] = playlist_new
        config.user_config["Playlists"][playlist_new] = config.user_config["Playlists"].pop(playlist_old)
        config.playlist = config.user_config["Playlists"][playlist_new]
        config.playlist["path"] = playlist_new_path

        self.menu.entryconfig(str(self.menu.index(playlist_old)), label=playlist_new, command=lambda: self.setPlaylist(playlist_new))
        self.menubtn["text"] = playlist_new

        #Change the path of each song in the playlist
        for song in self.playback.songs:
            song.path = os.path.join(playlist_new_path, song.name) + song.extension


    def delPlaylist(self, playlist:str, in_tv:bool=True):
        config.user_config["Playlists"].pop(playlist)
        self.menu.delete(playlist)

        if in_tv:
            config.general["playlist"] = ""
            self.menubtn["text"] = self.EMPTY_MENUBTN
            self.playlist.delPlaylist()


#==================================================


class TopLevelPlaylistEdit(customtk.TkPopup):
    def __init__(self, w:PlaylistControl, *args, **kwargs):

        self.playlist = w.playlist
        self.playlist_handler_set = w.playlist_handler_set
        self.playback = w.master.playback

        super().__init__(w,
            coord=(100,150),
            geometry="200x205",
            title="Playlist Control Panel",
            bg_bar=config.colors["WIDGET_BG1"],
            bg=config.colors["BG"],
            *args, **kwargs)


        self.entry_playlist = ttk.Entry(self.w)
        self.entry_playlist.grid(row=0, column=0, padx=(5,0), pady=(5,0))
        self.entry_playlist.insert(0, config.general["playlist"])

        self.btn_save_playlist_name = customtk.TkButtonImgHoverBg(self.w,
            command=self._renamePlaylist,
            imgs=(PhotoImage(data=b64img.btn_TV_edit_rename),),
            bg=config.colors["BG"],
            bg_on_hover=config.colors["BTN_BG_HOVER"])
        self.btn_save_playlist_name.grid(row=0, column=1, sticky="nsew", pady=(5,0))

        self.btn_delete_playlist = customtk.TkButtonImgHoverBg(self.w,
            command=self._delPlaylist,
            imgs=(PhotoImage(data=b64img.btn_TV_edit_delete),),
            bg=config.colors["BG"],
            bg_on_hover=config.colors["BTN_BG_HOVER"])
        self.btn_delete_playlist.grid(row=0, column=2, sticky="nsew", padx=(0,5), pady=(5,0))

        self.frame_path = customtk.TkFrameInfo(self.w,
            text=_("Path:"),
            lbl_width=5, info_width=25,
            info_bg=config.colors["BG"])
        self.frame_path.grid(row=1, column=0, columnspan=3, padx=5, pady=(10,5))
        self.frame_path.insert(config.playlist["path"])

        self.frame_size = customtk.TkFrameInfo(self.w,
            text=_("Size on disk:"),
            lbl_width=18, info_width=10,
            info_bg=config.colors["BG"])
        self.frame_size.grid(row=2, column=0, columnspan=3, padx=5)
        playlist_size_MB = sum(map(lambda song: os.path.getsize(song.path), self.playback.songs)) // (1024*1024)
        self.frame_size.insert(f"{playlist_size_MB} MB")

        self.frame_num = customtk.TkFrameInfo(self.w,
            text=_("Number of songs:"),
            lbl_width=18, info_width=10,
            info_bg=config.colors["BG"])
        self.frame_num.grid(row=3, column=0, columnspan=3, padx=5, pady=(5,10))
        playlist_len = len(self.playback.songs)
        self.frame_num.insert(str(playlist_len))

        self.btn_add_songs = customtk.TkButtonTextHoverFg(self.w,
            command=self._addSongs,
            text=_("----- [Add songs] -----"),
            bg = config.colors["BG"],
            fg=config.colors["FG"],
            fg_on_hover="blue")
        self.btn_add_songs.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=5)

        self.btn_open_folder = customtk.TkButtonImgHoverBg(self.w,
            command=lambda: os.startfile(config.playlist["path"]),
            imgs=(PhotoImage(data=b64img.btn_openfolder),),
            bg=config.colors["BG"],
            bg_on_hover=config.colors["BTN_BG_HOVER"])
        self.btn_open_folder.grid(row=5, column=0, columnspan=3, sticky="nsew", padx=5, pady=10)

    #__________________________________________________

    def _renamePlaylist(self):
        if self.playback.isSongPlayingInPlaylist():
            messagebox.showerror(_("Rename failed"), _("Song playing in the playlist"))
            return

        playlist_name_new = self.entry_playlist.get()
        if validEntryText(playlist_name_new, text_original=config.general["playlist"]):
            try:
                playlist_path_new = os.path.join(os.path.dirname(config.playlist["path"]), playlist_name_new)
                os.rename(config.playlist["path"], playlist_path_new)

                self.playlist_handler_set.renamePlaylist(playlist_name_new, playlist_path_new)
                self.frame_path.insert(config.playlist["path"])
            except:
                messagebox.showerror(_("Rename failed"), _("Unknown action not allowed"))


    def _delPlaylist(self):
        self.bell()
        state_delete = messagebox.askyesnocancel(_("Delete"), _("Do you also want to delete the playlist from the disk?"))

        if state_delete is None: return

        if state_delete and self.playback.isSongPlayingInPlaylist():
            messagebox.showerror(_("Delete failed"), _("Song playing in the playlist"))
            return

        self.playlist_handler_set.delPlaylist(config.general["playlist"])

        if state_delete:
            shutil.rmtree(config.playlist["path"])

        self.destroy()


    def _addSongs(self):
        songs_path = filedialog.askopenfilenames(title=_("Select"))
        if not songs_path: return

        for song_path in songs_path:
            song_name = os.path.basename(song_path)

            if not song_name.endswith(config.SUPPORTED_SONG_FORMATS):
                messagebox.showerror(_("Load failed"), _("Sound format not supported "))
                continue

            try:
                song_path_new = os.path.join(config.playlist["path"], song_name)
                shutil.copy2(src=song_path, dst=config.playlist["path"])

                self.playlist.append(Song(song_path_new))
                self.frame_size.insert(str(int(self.frame_size.get()[:-3]) + (os.path.getsize(song_path_new) // (1024*1024))))
                self.frame_num.insert(str(int(self.frame_num.get()) + 1))
            except:
                messagebox.showerror(_("Load failed"), _("Unknown action not allowed"))