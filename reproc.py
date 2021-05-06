__author__='''
                    Created by:
        __                                  __
        /               ,       /         /    )
       /    __              __ /    __   (__      __
      /    /   ) | /  /   /   /   /___)     |    (_ `
 (___/    (___(  |/  /   (___/   (___  (____/   (__)
______________________________________________________
                __Alicante project__
'''
print(__author__)

#________________________________________________________


from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk, ImageSequence

from urllib import parse, request

import youtube_dl
import wave
import simpleaudio

import threading
import subprocess
import random
import os
import re

class CDimg(Label):
    def __init__(self, w, filename):
        img = Image.open(filename)
        seq =  []

        try:
            while True:
                seq.append(img.copy())
                img.seek(len(seq)) # skip to next frame
        except EOFError:
            pass

        try:
            self.delay = img.info['duration']
        except KeyError:
            self.delay = 100

        first = seq[0].convert('RGBA')
        self.frames = [ImageTk.PhotoImage(first)]

        Label.__init__(self, w, image=self.frames[0])

        lut = [1] * 256
        lut[img.info["transparency"]] = 0

        temp = seq[0]
        for image in seq[1:]:
            mask = image.point(lut, "1")
            temp.paste(image, None, mask)
            frame = temp.convert('RGBA')
            self.frames.append(ImageTk.PhotoImage(frame))

        self.idx = 0
        self.cancel = self.after(100, self.play)

    def play(self):
        self.config(image=self.frames[self.idx])
        self.idx += 1
        if self.idx == len(self.frames):
            self.idx = 0
        self.cancel = self.after(self.delay, self.play)


class App:

    def __init__(self, w):

        self.folder_music = os.getcwd()+"/Music"
        self.folder_img = os.getcwd()+"/img"

        self.w = w
        w.title('Reproc')
        w.geometry("600x435")
        w.resizable(0,0)

        #Estilos
        style = ttk.Style(w)

        style.configure('Treeview', rowheight=25)
        style.configure("Treeview.Heading", foreground="#004788")
        style.layout('nodotbox.Treeview.Item',[('Treeitem.padding',{'children':[('Treeitem.text',{'side':'left','sticky':''})]})])

        #Elementos
        self.lista = ttk.Treeview(w, height=15, padding=5, selectmode="browse", style='nodotbox.Treeview')
        self.lista.grid(row=0, column=1)

        lista_scroll = ttk.Scrollbar(w, orient='vertical', command=self.lista.yview)
        lista_scroll.grid(row=0, column=2, sticky='ns')


        self.frame_music = LabelFrame(w, padx=10, width=30)
        self.frame_music.grid(row=0, column=0, sticky="nw")

        self.img_cd = CDimg(self.frame_music, self.folder_img+"/CDFinal.gif")
        self.img_cd.after_cancel(self.img_cd.cancel)
        self.img_cd.grid(row=0, column=0, rowspan=2, sticky="nw", pady=10)

        self.img_izq = PhotoImage(file=self.folder_img+"/Izq.png")
        self.btn_izq = Button(self.frame_music, image=self.img_izq, borderwidth=0)
        self.btn_izq.grid(row=1, column=1,sticky="nw")

        self.img_play = PhotoImage(file=self.folder_img+"/Play.png")
        self.img_pause = PhotoImage(file=self.folder_img+"/Playing.png")
        self.btn_playpause = Button(self.frame_music, image=self.img_play, borderwidth=0, command=self.play_button)
        self.btn_playpause.grid(row=1, column=2, sticky="nw")

        self.img_der = PhotoImage(file=self.folder_img+"/Der.png")
        self.btn_der = Button(self.frame_music, image=self.img_der, borderwidth=0)
        self.btn_der.grid(row=1, column=3, sticky="nw")

        self.lbl_name = Label(self.frame_music, text="Trevir something - all night", width=20)
        self.lbl_name.grid(row=2, column=0, columnspan=4)

        self.linetime = ttk.Scale(self.frame_music, from_=0, to_=100, orient="horizontal", length=200)
        self.linetime.grid(row=3,column=0, columnspan=4, pady=5)


        #Configuracion elementos
        self.lista.configure(yscroll=lista_scroll.set)
        self.lista.heading("#0", text='  PlayList \t\t\t [Open Music Folder]', anchor="w")
        self.lista.column("#0", width=300)


        #Eventos
        self.lista.bind("<Button-1>", self.play_click)
        self.lista.bind("<Return>", self.play_enter)
        self.lista.bind_all("<space>", self.pause_space)


        #Añadir musica
        try:
            os.mkdir(self.folder_music)
        except:
            self.getMusic()
        finally:
            os.chdir(self.folder_music)

        #Variables globales
        self.song_active = False
        self.song_play = True
        self.btn_playpause_active = False


    def getMusic(self):
        with os.scandir(self.folder_music) as it:
            for v in it:
                if v.is_file():
                    self.lista.insert("","end",text=" [ > ]   " + v.name)

    def play_enter(self, event):
        pass

    def pause_space(self, event):
        pass

    def play_click(self, event):
        if 12 < event.x < 32:

            if self.song_active:
                self.play_obj.stop()
                self.img_cd.after_cancel(self.img_cd.cancel)

            song_name = self.lista.item(self.lista.selection())["text"]
            self.wave_read = wave.open(song_name[9:],"rb")
            wave_obj = simpleaudio.WaveObject.from_wave_read(self.wave_read)
            self.play_obj = wave_obj.play()
            self.song_active = True
            self.song_play = True
            self.img_cd.play()

            self.btn_playpause.configure(image=self.img_pause)
            self.btn_playpause.image = self.img_pause
            self.btn_playpause_active = True

    def play_button(self):
        if not self.btn_playpause_active:
            self.btn_playpause.configure(image=self.img_pause)
            self.btn_playpause.image = self.img_pause
            self.btn_playpause_active = True

            if not self.song_active:
                if self.lista.selection():
                    song_name = self.lista.item(self.lista.selection())["text"]
                    self.wave_read = wave.open(song_name[9:],"rb")

                else:
                    song_name = random.choice([name for name in os.listdir("./") if (os.path.isfile(name) and name.endswith(".wav"))])
                    self.wave_read = wave.open(song_name,"rb")


                wave_obj = simpleaudio.WaveObject.from_wave_read(self.wave_read)
                self.play_obj = wave_obj.play()
                self.song_active = True
                self.img_cd.play()

            else:
                self.play_obj.resume()
                self.song_play = True
                self.img_cd.play()

        else:
            self.btn_playpause.configure(image=self.img_play)
            self.btn_playpause.image = self.img_play
            self.btn_playpause_active = False

            self.play_obj.pause()
            self.song_play = False
            self.img_cd.after_cancel(self.img_cd.cancel)


#________________________________________________________

if __name__ == "__main__":
    win = ThemedTk()
    win.set_theme("arc")
    app = App(win)
    win.mainloop()
