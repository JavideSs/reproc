import tkinter as tk
from tkinter import ttk
from threading import Thread
import os
from PIL import Image, ImageTk
from io import BytesIO

from .main1Music import Main
from .extraCDAnimation import CDgif
from ._config import *
from ._iconbase64 import *


class TabMusic():
    def __init__(self, w):
        self.w = w

        init_program_thread = Thread(target=self.init_program); init_program_thread.start()

        style = ttk.Style()
        style.configure("MenuUp.TFrame", background=color_reproc)
        style.configure("MenuDown.TFrame", background=color_reproc2)
        style.configure("TimeBar.Horizontal.TScale", background=color_reproc)
        style.configure("MusicList.Treeview", rowheight=25, background=color_playlist, foreground="gray30", font=font)
        style.map("MusicList.Treeview", background=[("selected", "#bed2e2")], foreground=[("selected","dark violet")])
        #Expandir color si no hay suficientes items
        style.layout("MusicList.Treeview",[("Treeview.treearea",{"sticky":"nswe"})])
        #Eliminar rectangulo seleccionador
        style.layout("MusicList.Treeview.Item",[("Treeitem.padding",{"children":[("Treeitem.image",{"side":"left","sticky":""}),("Treeitem.text",{"side":"left","sticky":""})]})])

        #_
        self.menu_up = ttk.Frame(w, style="MenuUp.TFrame")
        self.menu_up.grid(row=0, column=0, columnspan=2, sticky="we")

        self.song_art_default = tk.PhotoImage(data=song_art_default)
        self.song_art_fix = tk.PhotoImage(data=song_art_fix)
        self.canvas = tk.Canvas(self.menu_up, width=80, height=80, background=color_entry,  highlightthickness=0)
        self.canvas.grid(row=0, column=0, rowspan=2, padx=10, pady=(10,5))
        self.canvas.create_image(-4,0,image=self.song_art_default, anchor="nw")
        self.img_art = self.canvas.create_image(0,0,image=None, anchor="nw")
        self.canvas.create_image(-4,0,image=self.song_art_fix, anchor="nw")
        self.img_cd = CDgif(self.canvas, folder_img + sep+"_Logo.gif")

        self.menu_up_play = ttk.Frame(self.menu_up, style="MenuUp.TFrame")
        self.menu_up_play.grid(row=0, column=1)

        self.img_btn_random_on = tk.PhotoImage(data=img_btn_random_on)
        self.img_btn_random_off = tk.PhotoImage(data=img_btn_random_off)
        self.btn_random = tk.Button(self.menu_up_play, image=self.img_btn_random_off, command=self.setRandom, borderwidth=0,
                            background=color_reproc, activebackground=color_reproc, highlightbackground=color_reproc)
        self.btn_random.grid(row=0, column=0, padx=(5,0), pady=(5,0))

        self.img_btn_bucle_on = tk.PhotoImage(data=img_btn_bucle_on)
        self.img_btn_bucle_off = tk.PhotoImage(data=img_btn_bucle_off)
        self.btn_bucle = tk.Button(self.menu_up_play, image=self.img_btn_bucle_off, command=self.setBucle, borderwidth=0,
                            background=color_reproc, activebackground=color_reproc, highlightbackground=color_reproc)
        self.btn_bucle.grid(row=0, column=1, padx=(0,10), pady=(5,0))

        self.separador1 = ttk.Separator(self.menu_up_play, orient="vertical")
        self.separador1.grid(row=0, column=2, sticky="ns", pady=(5,0))

        self.img_btn_playizq = tk.PhotoImage(data=img_btn_playizq)
        self.btn_playizq = tk.Button(self.menu_up_play, image=self.img_btn_playizq, command=self.playPrevious, borderwidth=0,
                            background=color_reproc, activebackground=color_reproc, highlightbackground=color_reproc)
        self.btn_playizq.grid(row=0, column=3, padx=(10,2), pady=(5,0))

        self.img_btn_play = tk.PhotoImage(data=img_btn_play)
        self.img_btn_playing = tk.PhotoImage(data=img_btn_playing)
        self.btn_playpause = tk.Button(self.menu_up_play, image=self.img_btn_play, command=self.playpause, borderwidth=0,
                            background=color_reproc, activebackground=color_reproc, highlightbackground=color_reproc)
        self.btn_playpause.grid(row=0, column=4, padx=(2,2), pady=(5,0))

        self.img_btn_playder = tk.PhotoImage(data=img_btn_playder)
        self.btn_playder = tk.Button(self.menu_up_play, image=self.img_btn_playder, command=self.playNext, borderwidth=0,
                            background=color_reproc, activebackground=color_reproc, highlightbackground=color_reproc)
        self.btn_playder.grid(row=0, column=5, padx=(2,10), pady=(5,0))

        self.separador2 = ttk.Separator(self.menu_up_play, orient="vertical")
        self.separador2.grid(row=0, column=6, sticky="ns", pady=(5,0))

        self.state_btn_volumen = True
        self.set_volumen_anterior = 100
        self.img_btn_volumen_on = tk.PhotoImage(data=img_btn_volumen_on)
        self.img_btn_volumen_off = tk.PhotoImage(data=img_btn_volumen_off)
        self.btn_volumen = tk.Button(self.menu_up_play, image=self.img_btn_volumen_on, command=self.quitVolumen, borderwidth=0,
                            background=color_reproc, activebackground=color_reproc, highlightbackground=color_reproc)
        self.btn_volumen.grid(row=0, column=7, padx=(10,0), pady=(5,0))

        self.scale_volumen = tk.Scale(self.menu_up_play, command=self.setVolumen, from_=0, to_=100, length=50, orient="horizontal", showvalue=False,
                                width=10, background=color_reproc, highlightbackground=color_reproc, troughcolor=color_reproc, relief="flat", sliderrelief="ridge")
        self.scale_volumen.set(100)
        self.scale_volumen.grid(row=0, column=8, pady=(5,0))

        self.menu_up_song = ttk.Frame(self.menu_up, style="MenuUp.TFrame")
        self.menu_up_song.grid(row=1, column=1)

        self.state_txt_time1 = tk.StringVar()
        self.state_txt_time1.set(" 0:00")
        self.txt_time1 = ttk.Label(self.menu_up_song, textvariable=self.state_txt_time1, font=(None,7), background=color_reproc)
        self.txt_time1.grid(row=0, column=0, sticky="ws")

        self.state_txt_song = tk.StringVar()
        self.state_txt_song.set(".....Play any song.....")
        self.txt_song = ttk.Label(self.menu_up_song, textvariable=self.state_txt_song, font=font, background=color_reproc)
        self.txt_song.grid(row=0, column=1, pady=(0,3))

        self.state_txt_time2 = tk.StringVar()
        self.state_txt_time2.set(" 0:00")
        self.txt_time2 = ttk.Label(self.menu_up_song, textvariable=self.state_txt_time2, font=(None,7), background=color_reproc)
        self.txt_time2.grid(row=0, column=2, sticky="es")

        self.state_scale_time = tk.DoubleVar()
        self.scale_time = ttk.Scale(self.menu_up_song, style="TimeBar.Horizontal.TScale", from_=0, to_=100, value=0, variable=self.state_scale_time, length=300, orient="horizontal")
        self.scale_time.grid(row=1, column=0, columnspan=3)
        #Actualizar state_time al soltar el scale
        self.scale_time.bind("<ButtonRelease-1>", self.setTime)
        #Posicionar state_time directamente
        self.scale_time.bind("<Button-1>", self.setTimeInstant)

        #_
        self.playlist = ttk.Treeview(w, style="MusicList.Treeview", height=14, selectmode="browse", show="tree")
        self.playlist.grid(row=1, column=0)
        self.playlist_scroll = ttk.Scrollbar(w, command=self.playlist.yview)
        self.playlist_scroll.grid(row=1, column=1, sticky="ns")
        self.playlist.configure(yscroll=self.playlist_scroll.set)
        self.playlist["columns"]=("#duration")
        self.playlist.column("#0", width=350)
        self.playlist.column("#duration", width=50)
        #Reproducir cancion al clickar sobre la imagen
        self.playlist.bind("<Button-1>", self.playFromTree)
        #Reproducir cancion al pulsar return
        self.playlist.bind("<Return>", self.play)
        
        #_
        self.menu_down = ttk.Frame(w, style="MenuDown.TFrame", height=85)
        self.menu_down.grid(row=2, column=0, columnspan=2, sticky="we")

        self.state_sorttitle = True
        self.img_btn_sorttitle = tk.PhotoImage(data=img_btn_sorttitle)
        self.img_btn_sorttitle_up = tk.PhotoImage(data=img_btn_sorttitle_up)
        self.img_btn_sorttitle_down = tk.PhotoImage(data=img_btn_sorttitle_down)
        self.btn_sorttitle = tk.Button(self.menu_down, image=self.img_btn_sorttitle_up, command=self.sortTitle, borderwidth=0,
                            background=color_reproc2, activebackground=color_reproc2, highlightbackground=color_reproc2)
        self.btn_sorttitle.grid(row=0, column=0, padx=(5,1), pady=(5,5))

        self.state_sortdate = 0
        self.img_btn_sortdate = tk.PhotoImage(data=img_btn_sortdate)
        self.img_btn_sortdate_up = tk.PhotoImage(data=img_btn_sortdate_up)
        self.img_btn_sortdate_down = tk.PhotoImage(data=img_btn_sortdate_down)
        self.btn_sortdate = tk.Button(self.menu_down, image=self.img_btn_sortdate, command=self.sortDate, borderwidth=0,
                            background=color_reproc2, activebackground=color_reproc2, highlightbackground=color_reproc2)
        self.btn_sortdate.grid(row=0, column=1, padx=(1,1), pady=(5,5))

        self.state_sorttime = 0
        self.img_btn_sorttime = tk.PhotoImage(data=img_btn_sorttime)
        self.img_btn_sorttime_up = tk.PhotoImage(data=img_btn_sorttime_up)
        self.img_btn_sorttime_down = tk.PhotoImage(data=img_btn_sorttime_down)
        self.btn_sorttime = tk.Button(self.menu_down, image=self.img_btn_sorttime, command=self.sortTime, borderwidth=0,
                            background=color_reproc2, activebackground=color_reproc2, highlightbackground=color_reproc2)
        self.btn_sorttime.grid(row=0, column=2, padx=(1,5), pady=(5,5))

        self.state_entry_search = tk.StringVar()
        #Buscar cancion al escribit o borrar un caracter
        self.state_entry_search.trace("w", lambda name, index, mode, var=self.state_entry_search: self.search(var.get()))
        self.entry_search = ttk.Entry(self.menu_down, textvariable=self.state_entry_search, font=font, width=entry_search_width, foreground=color_entry)
        self.entry_search.grid(row=0, column=3, padx=(0,0), pady=(5,5))
        self.entry_search.insert(0, "Search song...")
        #Limpiar texto al dejar focus
        self.entry_search.bind("<FocusIn>", self.entryClear)
        #Agregar texto predeterminado al dejar de hacer focus
        self.entry_search.bind("<FocusOut>", self.entryText)

        self.img_btn_quitsearch = tk.PhotoImage(data=img_btn_quitsearch)
        self.btn_search = tk.Button(self.menu_down, image=self.img_btn_quitsearch, command=lambda: self.search(self.entry_search.get(), True), borderwidth=0)
        self.btn_search.grid(row=0, column=4, padx=(0,5), pady=(5,5))

        self.img_btn_openfolder = tk.PhotoImage(data=img_btn_openfolder)
        self.btn_openfolder = tk.Button(self.menu_down, image=self.img_btn_openfolder, command=lambda: os.system(open_folder_music),
                                borderwidth=0, background=color_reproc2, activebackground=color_reproc2, highlightbackground=color_reproc2)
        self.btn_openfolder.grid(row=0, column=5, padx=(5,5), pady=(5,5))

        self.img_btn_refresh = tk.PhotoImage(data=img_btn_refresh)
        self.btn_refresh = tk.Button(self.menu_down, image=self.img_btn_refresh, command=self.refresh_init_program,
                                borderwidth=0, background=color_reproc2, activebackground=color_reproc2, highlightbackground=color_reproc2)
        self.btn_refresh.grid(row=0, column=6, padx=(0,5), pady=(5,5))

        self.img_btn_playinlist = tk.PhotoImage(data=img_btn_playinlist)
        self.img_btn_playinginlist = tk.PhotoImage(data=img_btn_playinginlist)

        #Play/Pause cuando se pulsa space
        self.w.bind_all("<space>", self.event_playpause)
        self.w.bind_all("<Right>", self.event_advance)
        self.w.bind_all("<Left>", self.event_advance)

        init_program_thread.join()
        self.addItemsToPlaylist()

        self.playing = False
        self.id_now = 0

#__________________________________________________________________________________________________________________________________________________________________________________________________

    def init_program(self):
        self.program = Main()

    def refresh_init_program(self):
        del self.program
        self.program = Main()
        self.addItemsToPlaylist()

    def addItemsToPlaylist(self):
        #Eliminamos canciones anteriores
        for song in self.playlist.get_children():
            self.playlist.delete(song)

        #Agregamos canciones nuevas
        for song in self.program.getNameSongs():
            self.playlist.insert("", "end", text="  "+song.name, values=(song.time), iid=song.id, tag=song.id)
            self.playlist.tag_configure(song.id, image=self.img_btn_playinlist)

    #__________________________________________________________________

    def displaySelectionTree(self):
        if self.program.isSongLoad() and self.playlist.exists(self.song_info.id):
            #Focus a esa cancion y mover scroll hacia ella
            self.playlist.selection_set(self.song_info.id)
            self.playlist.see(self.song_info.id)
            #Color a esa cancion y default a la cancion anterior
            self.playlist.tag_configure(self.id_now, foreground="gray30", image=self.img_btn_playinlist)
            self.playlist.tag_configure(self.song_info.id, foreground="dark violet", image=self.img_btn_playinginlist)
            self.id_now = self.song_info.id


    def displayInfo(self):
        self.state_scale_time.set(0)
        self.state_txt_time1.set(" 0:00")
        self.state_txt_time2.set(self.song_info.time)

        song_name = self.song_info.name
        song_name = song_name if len(song_name)<40 else song_name[:40]+"..."
        self.state_txt_song.set(song_name)

        if not self.playing:
            self.btn_playpause.config(image=self.img_btn_playing)
            self.playlist.tag_configure(self.song_info.id, image=self.img_btn_playinginlist)
            self.img_cd.play()
            self.playing = True

        self.displaySelectionTree()

        if self.song_info.art_data != None:
            song_art_pre = Image.open(BytesIO(self.song_info.art_data))
            song_art_pre.thumbnail([80,80],Image.ANTIALIAS)
            self.song_art = ImageTk.PhotoImage(song_art_pre)
        else:
            self.song_art = None
        self.canvas.itemconfig(self.img_art, image=self.song_art)

    #__________________________________________________________________

    def updateTimeSong(self):
        if self.playing:
            state_scale_time = self.state_scale_time.get()
            song_secons = self.song_info.secons

            #El scale.time que habia antes + Regla de 3: song.secons->0.1s, 100->?
            self.state_scale_time.set(state_scale_time + 100/song_secons*0.1)
            #Regla de 3: 100->scale.time, song.secons->?
            time = round((state_scale_time * song_secons)/100)
            self.state_txt_time1.set(Main.formatoTime(time))

            #Si ha acabado la cancion...
            if self.state_scale_time.get() > 100:
                self.playNext()


    def setTime(self, event):
        if self.program.isSongLoad():
            #Regla de 3: 100->scale.secons, song.secons->?
            time = round((self.state_scale_time.get() * self.song_info.secons)/100)
            self.program.setTime(time)


    def setTimeInstant(self, event):
        self.scale_time.event_generate("<Button-3>", x=event.x, y=event.y)
        return "break"

    #__________________________________________________________________

    def event_playpause(self, event):
        #Si no hay focus en entry_search
        if event.widget != self.entry_search:
            self.playpause()


    def event_advance(self, event):
        #Si no hay focus en entry_search
        if event.widget != self.entry_search:
            state_scale_time = self.state_scale_time.get()
            song_secons = self.song_info.secons

            #Regla de 3: 100->scale.secons, song.secons->?
            time = round((state_scale_time * song_secons)/100)

            if event.keysym == "Right":
                #Si hay segundos de sobra -> adelantar 5
                if self.song_info.secons > time+5:
                    self.program.setTime(time+5)
                    self.state_scale_time.set(state_scale_time + 100/song_secons*5)
                    self.state_txt_time1.set(Main.formatoTime(time+5))
                #Si no -> play siguiente cancion
                else:
                    self.playNext()

            else:
                #Si hay segundos de sobra -> atrasar 5
                if time > 5:
                    self.program.setTime(time-5)
                    self.state_scale_time.set(state_scale_time - 100/song_secons*5)
                    self.state_txt_time1.set(Main.formatoTime(time-5))
                #Si no -> rewind cancion
                else:
                    self.program.setTime(0)
                    self.state_scale_time.set(0)
                    self.state_txt_time1.set(Main.formatoTime(0))

    #__________________________________________________________________

    def playFromTree(self, event):
        #Si se hace click en la posicion de la imagen...
        if 10 < event.x < 30:
            #Fix bug porque se producia el evento antes que la seleccion
            Thread(target=self.play).start()


    def play(self, event=None):
        if self.program.isSongLoad() and int(self.playlist.selection()[0]) == self.song_info.id:
            self.playpause()
        else:
            self.song_info = self.program.playById(int(self.playlist.selection()[0]))
            self.displayInfo()


    def playpause(self):
        if self.playing:
            self.program.pause()

            self.btn_playpause.config(image=self.img_btn_play)
            self.playlist.tag_configure(self.song_info.id, image=self.img_btn_playinlist)
            #Fix que a veces no se cancela
            while True:
                status_cancel = self.img_cd.cancel
                self.img_cd.canvas.after_cancel(self.img_cd.cancel)
                if status_cancel == self.img_cd.cancel: break
            self.playing = False

        else:
            if self.program.isSongLoad():
                self.program.resume()

                self.btn_playpause.config(image=self.img_btn_playing)
                self.playlist.tag_configure(self.song_info.id, image=self.img_btn_playinginlist)
                self.img_cd.play()
                self.playing = True

            else:
                self.playNext()


    def playNext(self):
        #Si existe (debido a la busqueda) y no es el ultimo item -> play siguiente cancion
        if (self.playing or self.program.isSongLoad()) and self.playlist.exists(self.song_info.id) and (self.playlist.index(self.song_info.id)<len(self.playlist.get_children())):
            self.song_info = self.program.playNext(self.playlist.next(self.song_info.id))
        #Si no, si existen canciones (debido a la busqueda) -> play primera cancion
        elif any(self.playlist.get_children()):
            self.song_info = self.program.playNext("")

        self.displayInfo()


    def playPrevious(self):
        song = self.program.playPrevious()
        if song:
            self.song_info = song
            self.displayInfo()


    #__________________________________________________________________

    def entryClear(self, event):
        if self.entry_search.get() == "Search song...":
            self.entry_search.delete(0, tk.END)


    def entryText(self, event):
        #Si el texto es todo espacios...
        if len(self.entry_search.get()) - self.entry_search.get().count(" ") == 0:
            self.entry_search.delete(0, tk.END)
            self.entry_search.insert(0, "Search song...")


    def search(self, song_name, quit=False):
        if song_name != "Search song...":
            if quit:
                self.entry_search.delete(0, tk.END)

                self.displaySelectionTree()
            else:
                self.program.filterNameSongs(song_name)

                self.addItemsToPlaylist()
                self.displaySelectionTree()


    #__________________________________________________________________

    def setRandom(self):
        if self.program.state_random:
            self.btn_random.config(image=self.img_btn_random_off)
            self.program.state_random = False

        else:
            self.btn_random.config(image=self.img_btn_random_on)
            self.program.state_random = True


    def setBucle(self):
        if self.program.state_bucle:
            self.btn_bucle.config(image=self.img_btn_bucle_off)
            self.program.state_bucle = False

        else:
            self.btn_bucle.config(image=self.img_btn_bucle_on)
            self.program.state_bucle = True

    #__________________________________________________________________

    def quitVolumen(self):
        if self.state_btn_volumen:
            self.program.setVolumen(0)
            self.set_volumen_anterior = self.scale_volumen.get()

            self.scale_volumen.set(0)
            self.btn_volumen.config(image=self.img_btn_volumen_off)
            self.state_btn_volumen = False
        else:
            #Recuperar volumen anterior
            self.program.setVolumen(self.set_volumen_anterior)

            self.scale_volumen.set(self.set_volumen_anterior)
            self.btn_volumen.config(image=self.img_btn_volumen_on)
            self.state_btn_volumen = True


    def setVolumen(self, state):
        volumen = self.scale_volumen.get()/100
        self.program.setVolumen(volumen)

        if volumen == 0:
            self.btn_volumen.config(image=self.img_btn_volumen_off)
            self.state_btn_volumen = False
        else:
            self.btn_volumen.config(image=self.img_btn_volumen_on)
            self.state_btn_volumen = True

    #__________________________________________________________________

    def sortTitle(self):
        if self.state_sortdate%3 != 0:
            self.btn_sortdate.config(image=self.img_btn_sortdate)
            self.state_sortdate = 0
        if self.state_sorttime%3 != 0:
            self.btn_sorttime.config(image=self.img_btn_sorttime)
            self.state_sorttime = 0

        #Z-A
        if self.state_sorttitle:
            self.btn_sorttitle.config(image=self.img_btn_sorttitle_down)
            self.state_sorttitle = False

            self.program.orderBy(True, "name")

        #A-Z
        else:
            self.btn_sorttitle.config(image=self.img_btn_sorttitle_up)
            self.state_sorttitle = True

            self.program.orderBy(False, "name")

        self.addItemsToPlaylist()
        self.displaySelectionTree()


    def sortDate(self):
        #Reset sorttime si esta activo
        if self.state_sorttime%3 != 0:
            self.btn_sorttime.config(image=self.img_btn_sorttime)
            self.state_sorttime = 0

        self.state_sortdate += 1

        #A-Z
        if self.state_sortdate%3 == 0:
            self.btn_sortdate.config(image=self.img_btn_sortdate)
            self.btn_sorttitle.config(image=self.img_btn_sorttitle_up)
            self.state_sorttitle = True

            self.program.orderBy(False, "name")

        #New-Old
        elif self.state_sortdate%3 == 1:
            self.btn_sortdate.config(image=self.img_btn_sortdate_up)
            self.btn_sorttitle.config(image=self.img_btn_sorttitle)

            self.program.orderBy(True, "date")

        #Old-New
        else:
            self.btn_sortdate.config(image=self.img_btn_sortdate_down)
            self.btn_sorttitle.config(image=self.img_btn_sorttitle)

            self.program.orderBy(False, "date")

        self.addItemsToPlaylist()
        self.displaySelectionTree()


    def sortTime(self):
        #Reset sortdate si esta activo
        if self.state_sortdate%3 != 0:
            self.btn_sortdate.config(image=self.img_btn_sortdate)
            self.state_sortdate = 0

        self.state_sorttime += 1

        #A-Z
        if self.state_sorttime%3 == 0:
            self.btn_sorttime.config(image=self.img_btn_sorttime)
            self.btn_sorttitle.config(image=self.img_btn_sorttitle_up)
            self.state_sorttitle = True

            self.program.orderBy(False, "name")

        #Corto-Largo
        elif self.state_sorttime%3 == 1:
            self.btn_sorttime.config(image=self.img_btn_sorttime_up)
            self.btn_sorttitle.config(image=self.img_btn_sorttitle)

            self.program.orderBy(False, "time")

        #Largo-Corto
        else:
            self.btn_sorttime.config(image=self.img_btn_sorttime_down)
            self.btn_sorttitle.config(image=self.img_btn_sorttitle)

            self.program.orderBy(True, "time")

        self.addItemsToPlaylist()
        self.displaySelectionTree()
