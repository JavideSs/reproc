from tkinter import *
from tkinter import ttk
from threading import Thread
import os

from cdAnimation import CDimg
from config import *
from main import Main

class TabMusic():
    def __init__(self, w, tab1):

        self.w = w

        self.program = Main()

        style = ttk.Style()
        style.configure("MenuUp.TFrame",background=color_menu_up)
        style.configure("MenuDown.TFrame",background=color_menu_down)
        style.configure("TimeBar.Horizontal.TScale",background=color_menu_up)
        style.configure("MusicList.Treeview",rowheight=25,background=color_playlist,font=font)
        style.layout("MusicList.Treeview",[("Treeview.treearea",{"sticky":"nswe"})])
        style.layout("MusicList.Treeview.Item",[("Treeitem.padding",{"children":[('Treeitem.image',{"side":"left","sticky":""}),("Treeitem.text",{"side":"left","sticky":""})]})])

        self.menu_up = ttk.Frame(tab1, style="MenuUp.TFrame")
        self.menu_up.grid(row=0, column=0, columnspan=2, sticky="we")

        self.img_cd = CDimg(self.menu_up, folder_img+"/_CDfinal.gif")
        self.img_cd.grid(row=0, column=0, rowspan=2)

        self.menuplay = ttk.Frame(self.menu_up, style="MenuUp.TFrame")
        self.menuplay.grid(row=0, column=1)

        self.state_btn_random = False
        self.img_btn_random_on = PhotoImage(file=folder_img+"/AleatorioOn.png")
        self.img_btn_random_off = PhotoImage(file=folder_img+"/AleatorioOff.png")
        self.btn_random = Button(self.menuplay, image=self.img_btn_random_off, command=self.setRandom, borderwidth=0,
                            background=color_menu_up, activebackground=color_menu_up, highlightbackground=color_menu_up)
        self.btn_random.grid(row=0, column=0, padx=(8,0), pady=(5,0))

        self.state_btn_bucle = False
        self.img_btn_bucle_on = PhotoImage(file=folder_img+"/BucleOn.png")
        self.img_btn_bucle_off = PhotoImage(file=folder_img+"/BucleOff.png")
        self.btn_bucle = Button(self.menuplay, image=self.img_btn_bucle_off, command=self.setBucle, borderwidth=0,
                            background=color_menu_up, activebackground=color_menu_up, highlightbackground=color_menu_up)
        self.btn_bucle.grid(row=0, column=1, padx=(0,10), pady=(5,0))

        self.separador1 = ttk.Separator(self.menuplay, orient="vertical")
        self.separador1.grid(row=0, column=2, sticky="ns", pady=(5,0))

        self.img_btn_playizq = PhotoImage(file=folder_img+"/PlayIzq.png")
        self.btn_playizq = Button(self.menuplay, image=self.img_btn_playizq, command=self.playizq, borderwidth=0,
                            background=color_menu_up, activebackground=color_menu_up, highlightbackground=color_menu_up)
        self.btn_playizq.grid(row=0, column=3, padx=(10,2), pady=(5,0))

        self.img_btn_play = PhotoImage(file=folder_img+"/Play.png")
        self.img_btn_playing = PhotoImage(file=folder_img+"/Playing.png")
        self.btn_playpause = Button(self.menuplay, image=self.img_btn_play, command=self.playpause, borderwidth=0,
                            background=color_menu_up, activebackground=color_menu_up, highlightbackground=color_menu_up)
        self.btn_playpause.grid(row=0, column=4, padx=(2,2), pady=(5,0))

        self.img_btn_playder = PhotoImage(file=folder_img+"/PlayDer.png")
        self.btn_playder = Button(self.menuplay, image=self.img_btn_playder, command=self.playder, borderwidth=0,
                            background=color_menu_up, activebackground=color_menu_up, highlightbackground=color_menu_up)
        self.btn_playder.grid(row=0, column=5, padx=(2,10), pady=(5,0))

        self.separador2 = ttk.Separator(self.menuplay, orient="vertical")
        self.separador2.grid(row=0, column=6, sticky="ns", pady=(5,0))

        self.state_btn_volumen = True
        self.set_volumen_anterior = 100
        self.img_btn_volumen_on = PhotoImage(file=folder_img+"/VolumenOn.png")
        self.img_btn_volumen_off = PhotoImage(file=folder_img+"/VolumenOff.png")
        self.btn_volumen = Button(self.menuplay, command=self.quitVolumen, image=self.img_btn_volumen_on, borderwidth=0,
                            background=color_menu_up, activebackground=color_menu_up, highlightbackground=color_menu_up)
        self.btn_volumen.grid(row=0, column=7, padx=(10,0), pady=(5,0))

        self.scale_volumen = Scale(self.menuplay, command=self.setVolumen, from_=0, to_=100, length=50, orient="horizontal", showvalue=False,
                                width=10, background=color_menu_up, highlightbackground=color_menu_up, troughcolor=color_menu_up, relief="flat", sliderrelief="ridge")
        self.scale_volumen.set(100)
        self.scale_volumen.grid(row=0, column=8, pady=(5,0))

        self.menusong = ttk.Frame(self.menu_up, style="MenuUp.TFrame")
        self.menusong.grid(row=1, column=1)

        self.txt_time1_update = StringVar()
        self.txt_time1_update.set(" 0:00")
        self.txt_time1 = ttk.Label(self.menusong, textvariable=self.txt_time1_update, background=color_menu_up, font=(None, 7))
        self.txt_time1.grid(row=0, column=0, sticky="ws")

        self.txt_song_update = StringVar()
        self.txt_song_update.set(".....play any song.....")
        self.txt_song = ttk.Label(self.menusong, textvariable=self.txt_song_update, font=font, background=color_menu_up, padd=(0,0,0,5))
        self.txt_song.grid(row=0, column=1)

        self.txt_time2 = ttk.Label(self.menusong, text="00:00", background=color_menu_up, font=(None, 7))
        self.txt_time2.grid(row=0, column=2, sticky="es")

        self.scale_time = ttk.Scale(self.menusong, style="TimeBar.Horizontal.TScale", from_=0, to_=100, value=0, length=300, orient="horizontal")
        self.scale_time.grid(row=1, column=0, columnspan=3)

        self.playlist = ttk.Treeview(tab1, style="MusicList.Treeview", height=14, selectmode="browse", show="tree")
        self.playlist.grid(row=1, column=0)
        self.playlist_scroll = ttk.Scrollbar(tab1, command=self.playlist.yview)
        self.playlist_scroll.grid(row=1, column=1, sticky='ns')
        self.playlist.configure(yscroll=self.playlist_scroll.set)
        self.playlist["columns"]=("#duration")
        self.playlist.column("#0", width=350)
        self.playlist.column("#duration", width=50)

        self.menu_down = ttk.Frame(tab1, style="MenuDown.TFrame", height=85)
        self.menu_down.grid(row=2, column=0, columnspan=2, sticky="we")

        self.state_sortdate = 0
        self.img_btn_sortdate = PhotoImage(file=folder_img+"/SortDate.png")
        self.img_btn_sortdate_up = PhotoImage(file=folder_img+"/SortDateUp.png")
        self.img_btn_sortdate_down = PhotoImage(file=folder_img+"/SortDateDown.png")
        self.btn_sortdate = Button(self.menu_down, image=self.img_btn_sortdate, command=self.sortDate, borderwidth=0,
                            background=color_menu_down, activebackground=color_menu_down, highlightbackground=color_menu_down)
        self.btn_sortdate.grid(row=0, column=0, padx=(5,1), pady=(5,5))

        self.state_sorttitle = 0
        self.img_btn_sorttitle = PhotoImage(file=folder_img+"/SortTitle.png")
        self.img_btn_sorttitle_up = PhotoImage(file=folder_img+"/SortTitleUp.png")
        self.img_btn_sorttitle_down = PhotoImage(file=folder_img+"/SortTitleDown.png")
        self.btn_sorttitle = Button(self.menu_down, image=self.img_btn_sorttitle, command=self.sortTitle, borderwidth=0,
                            background=color_menu_down, activebackground=color_menu_down, highlightbackground=color_menu_down)
        self.btn_sorttitle.grid(row=0, column=1, padx=(1,1), pady=(5,5))

        self.state_sorttime = 0
        self.img_btn_sorttime = PhotoImage(file=folder_img+"/SortTime.png")
        self.img_btn_sorttime_up = PhotoImage(file=folder_img+"/SortTimeUp.png")
        self.img_btn_sorttime_down = PhotoImage(file=folder_img+"/SortTimeDown.png")
        self.btn_sorttime = Button(self.menu_down, image=self.img_btn_sorttime, command=self.sortTime, borderwidth=0,
                            background=color_menu_down, activebackground=color_menu_down, highlightbackground=color_menu_down)
        self.btn_sorttime.grid(row=0, column=2, padx=(1,5), pady=(5,5))

        self.string_vars_entry = StringVar()
        self.string_vars_entry.trace("w", lambda name, index, mode, var=self.string_vars_entry: self.search(var.get()))
        self.entry_search = ttk.Entry(self.menu_down, textvariable=self.string_vars_entry, width=width_entry, foreground="#9665AA", font=font)
        self.entry_search.grid(row=0, column=3, padx=(0,0), pady=(5,5))
        self.entry_search.bind("<FocusIn>", self.entryClear)
        self.entry_search.bind("<FocusOut>", self.entryText)
        self.entry_search.insert(0, "Search song...")

        self.img_btn_quitsearch = PhotoImage(file=folder_img+"/QuitSearch.png")
        self.btn_search = Button(self.menu_down, image=self.img_btn_quitsearch, command=lambda: self.search(""), borderwidth=0)
        self.btn_search.grid(row=0, column=4, padx=(0,5), pady=(5,5))

        self.img_btn_openfolder = PhotoImage(file=folder_img+"/MusicFolder.png")
        self.btn_openfolder = Button(self.menu_down, image=self.img_btn_openfolder, command=lambda: os.system(r'start %windir%\explorer.exe "{0}"'.format(folder_music)),
                                borderwidth=0, background=color_menu_down, activebackground=color_menu_down, highlightbackground=color_menu_down)
        self.btn_openfolder.grid(row=0, column=5, padx=(5,5), pady=(5,5))

        self.addItemsToPlaylist()

        self.playlist.bind("<Button-1>", self.playSongTree)
        self.playlist.bind("<Return>", self.playSong)
        self.w.bind_all("<space>", self.playpause)

        self.scale_time.bind("<ButtonRelease-1>", self.setTime)

        self.playing = False

        self.w.after(1000, self.updateTimeSong)

#__________________________________________________________________________________________________________________________________________________________________________________________________

    def addItemsToPlaylist(self):
        for song in self.playlist.get_children():
            self.playlist.delete(song)

        self.img_playlist = PhotoImage(file=folder_img+"/PlayInList.png")
        for song in self.program.getNameSongs():
            if not song.time[0]:
                self.playlist.insert('', 'end', text="  "+song.name, image=self.img_playlist, values=("{:2d}:{:02d}".format(song.time[1],song.time[2])))
            else:
                self.playlist.insert('', 'end', text="  "+song.name, image=self.img_playlist, values=("{1d}:{:2d}:{:02d}".format(song.time[0],song.time[1],song.time[2])))

    #__________________________________________________________________

    def displayMetadata(self):
        self.txt_time1_update.set(" 0:00")
        self.scale_time.set(0)
        song_name =self.metadata.name
        song_name = song_name if len(song_name)<35 else song_name[:35]+"..."
        self.txt_song_update.set(song_name)
        self.btn_playpause.config(image=self.img_btn_playing)
        if self.playing:
            self.img_cd.play(); self.img_cd.after_cancel(self.img_cd.cancel)
        else:
            self.img_cd.play()
        self.playing = True


    def playSongTree(self, event):
        if 10 < event.x < 30:
            fix = Thread(target=self.playSong)
            fix.start()

    def playSong(self, event=None):
            self.metadata = self.program.playByName(self.playlist.item(self.playlist.selection())["text"][2:])
            self.displayMetadata()

    def playpause(self, event=None):
        if self.playing:
            self.program.pauseSong()
            self.btn_playpause.config(image=self.img_btn_play)
            self.img_cd.after_cancel(self.img_cd.cancel)
            self.playing = False
        else:
            try:
                self.program.resumeSong()
                self.btn_playpause.config(image=self.img_btn_playing)
                self.img_cd.play()
                self.playing = True
            except:
                self.metadata = self.program.playByOrder()
                self.displayMetadata()


    def playizq(self):
        pass


    def playder(self):
        pass

    #__________________________________________________________________

    def setRandom(self):
        if self.state_btn_random:
            self.btn_random.config(image=self.img_btn_random_off)
            self.state_btn_random = False
        else:
            self.btn_random.config(image=self.img_btn_random_on)
            self.state_btn_random = True


    def setBucle(self):
        if self.state_btn_bucle:
            self.btn_bucle.config(image=self.img_btn_bucle_off)
            self.state_btn_bucle = False
        else:
            self.btn_bucle.config(image=self.img_btn_bucle_on)
            self.state_btn_bucle = True

    #__________________________________________________________________

    def quitVolumen(self):
        if self.state_btn_volumen:
            self.program.setVolumen(0)
            self.set_volumen_anterior = self.scale_volumen.get()
            self.scale_volumen.set(0)
            self.btn_volumen.config(image=self.img_btn_volumen_off)
            self.state_btn_volumen = False
        else:
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

    def updateTimeSong(self):
        if self.playing:
            scale_time = self.scale_time.get()
            secons_song = self.metadata.secons

            self.scale_time.set(scale_time + 100/secons_song)
            s_total = round((scale_time * secons_song)/100)
            m, s = divmod(s_total,60)
            h, m = divmod(m,60)
            if not h:
                self.txt_time1_update.set("{:2d}:{:02d}".format(int(m),int(s)))
            else:
                self.txt_time1_update.set("{1d}:{:2d}:{:02d}".format(int(h),int(m),int(s)))

        self.w.after(1000, self.updateTimeSong)


    def setTime(self, state):
        time = round((self.scale_time.get() * self.metadata.secons)/100)
        self.program.setTime(time)

    #__________________________________________________________________

    def sortDate(self):
        if self.state_sorttitle%3 != 0:
            self.btn_sorttitle.config(image=self.img_btn_sorttitle)
            self.state_sorttitle = 0
        if self.state_sorttime%3 != 0:
            self.state_sorttime = 0
            self.btn_sorttime.config(image=self.img_btn_sorttime)

        self.state_sortdate += 1
        if self.state_sortdate%3 == 0:
            self.btn_sortdate.config(image=self.img_btn_sortdate)
        elif self.state_sortdate%3 == 1:
            self.btn_sortdate.config(image=self.img_btn_sortdate_down)
        else:
            self.btn_sortdate.config(image=self.img_btn_sortdate_up)


    def sortTitle(self):
        if self.state_sortdate%3 != 0:
            self.btn_sortdate.config(image=self.img_btn_sortdate)
            self.state_sortdate = 0
        if self.state_sorttime%3 != 0:
            self.btn_sorttime.config(image=self.img_btn_sorttime)
            self.state_sorttime = 0

        self.state_sorttitle += 1
        if self.state_sorttitle%3 == 0:
            self.btn_sorttitle.config(image=self.img_btn_sorttitle)
        elif self.state_sorttitle%3 == 1:
            self.btn_sorttitle.config(image=self.img_btn_sorttitle_down)
        else:
            self.btn_sorttitle.config(image=self.img_btn_sorttitle_up)


    def sortTime(self):
        if self.state_sortdate%3 != 0:
            self.btn_sortdate.config(image=self.img_btn_sortdate)
            self.state_sortdate = 0
        if self.state_sorttitle%3 != 0:
            self.btn_sorttitle.config(image=self.img_btn_sorttitle)
            self.state_sorttitle = 0

        self.state_sorttime += 1
        if self.state_sorttime%3 == 0:
            self.btn_sorttime.config(image=self.img_btn_sorttime)
        elif self.state_sorttime%3 == 1:
            self.btn_sorttime.config(image=self.img_btn_sorttime_down)
        else:
            self.btn_sorttime.config(image=self.img_btn_sorttime_up)

    #__________________________________________________________________

    def entryClear(self, event):
        if self.entry_search.get() == "Search song...":
            self.entry_search.delete(0, END)


    def entryText(self, event):
        if  len(self.entry_search.get()) - self.entry_search.get().count(" ") == 0:
            self.entry_search.delete(0, END)
            self.entry_search.insert(0, "Search song...")


    def search(self, song_name):
        if song_name != "Search song...":
            self.program.filterNameSongs(song_name)
            self.addItemsToPlaylist()
        if song_name == "":
            self.entry_search.delete(0, END)
