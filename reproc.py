from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk, ImageSequence

from urllib import parse, request

import youtube_dl
from pyglet import media
import pyglet

import threading
import subprocess
import random
import gc
import os
import re

from img.gif import CDimg


class App:

    def __init__(self, w):

        self.folder_music = os.getcwd()+"/Music"
        self.folder_img = os.getcwd()+"/img"

        self.w = w
        w.title('Reproc')
        w.geometry("570x435")
        w.resizable(0,0)


        #Estilos
        style = ttk.Style(w)
        style.configure('Treeview', rowheight=25)
        style.configure("Treeview.Heading", foreground="#004788")
        style.layout('nodotbox.Treeview.Item',[('Treeitem.padding',{'children':[('Treeitem.text',{'side':'left','sticky':''})]})])


        #Elementos
        self.lista = ttk.Treeview(w, height=15, padding=5, selectmode="browse", style='nodotbox.Treeview')
        self.lista.grid(row=0, column=1, rowspan=2)

        lista_scroll = ttk.Scrollbar(w, orient='vertical', command=self.lista.yview)
        lista_scroll.grid(row=0, column=2, sticky='ns', rowspan=2)
        #___________________________________________________________________________________________________________________
        self.frame_music = LabelFrame(w, padx=10, width=30)
        self.frame_music.grid(row=0, column=0, sticky="n")

        self.img_izq = PhotoImage(file=self.folder_img+"/Izq.png")
        self.btn_izq = Button(self.frame_music, image=self.img_izq, borderwidth=0)
        self.btn_izq.grid(row=1, column=1,sticky="nw")

        self.img_play = PhotoImage(file=self.folder_img+"/Play.png")
        self.img_playing = PhotoImage(file=self.folder_img+"/Playing.png")
        self.btn_playpause = Button(self.frame_music, image=self.img_play, borderwidth=0, command=self.play_button)
        self.btn_playpause.grid(row=1, column=2, sticky="nw")

        self.img_der = PhotoImage(file=self.folder_img+"/Der.png")
        self.btn_der = Button(self.frame_music, image=self.img_der, borderwidth=0)
        self.btn_der.grid(row=1, column=3, sticky="nw")

        self.lbl_name = Label(self.frame_music, text="Trevor something - all night", width=20)
        self.lbl_name.grid(row=2, column=0, columnspan=4)

        self.linetime = ttk.Scale(self.frame_music, from_=0, to_=100, orient="horizontal", length=200)
        self.linetime.grid(row=3,column=0, columnspan=4, pady=5)
        #___________________________________________________________________________________________________________________
        self.frame_download = LabelFrame(w, text="Download Music")
        self.frame_download.grid(row=1, column =0, sticky="n")

        self.entry_download = ttk.Entry(self.frame_download, text="Link")
        self.entry_download.grid(row=0, column=0)

        self.btn_download = Button(self.frame_download, text="Dowload")
        self.btn_download.grid(row=0, column=1)

        self.entry_download = ttk.Entry(self.frame_download, text="Song")
        self.entry_download.grid(row=1, column=0)

        self.btn_search = Button(self.frame_download, text="Search", command=self.download)
        self.btn_search.grid(row=1, column=1)


        #Configuracion elementos
        self.lista.configure(yscroll=lista_scroll.set)
        self.lista.heading("#0", text='  PlayList \t\t\t [Open Music Folder]', anchor="w")
        self.lista.column("#0", width=300)


        #Eventos
        self.lista.bind("<Button-1>", self.play_click)
        self.lista.bind("<Return>", self.play_enter)
        self.lista.bind_all("<space>", self.pause_space)


        #Añadir musica
        self.playlist = []
        try:
            os.mkdir(self.folder_music)
        except:
            self.getMusic()
        finally:
            os.chdir(self.folder_music)

        #Variables globales
        self.btn_playpause_active = False
        self.is_off = False
        self.song_active = False
        self.song_stop = False
        self.song_play = False
        self.song_pause = False
        self.song_continue = False

        self.hilo_reproductor = threading.Thread(target=self.bucle_reproductor)
        self.hilo_reproductor.start()

        self.player = media.Player()
    #____________________________________________________________________________


    def download(self):
        busqueda = self.entry_download.get()

        enlace_convert = parse.urlencode({'search_query': busqueda})
        enlace_final = request.urlopen('http://www.youtube.com/results?' + enlace_convert)
        resultados = re.findall('href=\"\\/watch\\?v=(.{11})', enlace_final.read().decode())
        url = resultados[0]

        ydl_opc = {
            'format': 'bestaudio/worstvideo',
            'outtmpl': '/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opc) as ydl:
            ydl.cache.remove()
            ydl.download([url])


    def bucle_reproductor(self):
        while not self.is_off:

            self.getMusicAfter()

            if self.song_stop:
                self.player.stop()
                self.song_stop = False
                self.song_active = False


            if self.song_play:
                if self.song_active:
                    self.play_obj.stop()

                song_name = self.lista.item(self.lista.selection())["text"]
                source = media.StaticSource(media.load(song_name[9:]))
                self.player.queue(source)
                self.player.play()
                pyglet.app.run()

                self.song_play = False
                self.song_active = True

                self.btn_playpause_active = True
                self.btn_playpause.configure(image=self.img_playing)
                self.btn_playpause.image = self.img_playing


            if self.song_pause:
                self.player.play()
                self.song_pause = False

                self.btn_playpause_active = False
                self.btn_playpause.configure(image=self.img_play)
                self.btn_playpause.image = self.img_play

            if self.song_continue:
                self.player.resume()
                self.song_continue = False

                self.btn_playpause_active = True
                self.btn_playpause.configure(image=self.img_playing)
                self.btn_playpause.image = self.img_playing


    def getMusic(self):

        with os.scandir(self.folder_music) as it:
            for v in it:
                if v.is_file() and v.name.endswith(".wav"):
                    self.playlist.append(v.name)
                    self.lista.insert("","end",text=" [ > ]   " + v.name)

    def getMusicAfter(self):
        with os.scandir(self.folder_music) as it:
            for v in it:
                if v.is_file() and v.name.endswith(".wav") and not v.name in self.playlist:
                    self.playlist.append(v.name)
                    self.playlist.sort()
                    self.lista.insert("","end",text=" [ > ]   " + v.name)


    def play_enter(self, event):
        pass


    def pause_space(self, event):
        pass


    def play_click(self, event):
        if 12 < event.x < 32:
            self.song_play = True

        elif 204<event.x<310 and 15<event.y<25:
            os.system("start. "+self.folder_music)


    def play_button(self):
        if self.btn_playpause_active:
            self.song_pause = True
        else:
            if self.play_obj.is_playing():
                self.song_continue = True
            else:
                self.song_play = True


#________________________________________________________

if __name__ == "__main__":
    win = ThemedTk()
    win.set_theme("arc")
    app = App(win)
    win.mainloop()
    app.is_off = True
