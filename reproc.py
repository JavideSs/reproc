
from tkinter import *
from tkinter import ttk
from urllib import parse, request

import os
import re
import random
import threading

import wave
import youtube_dl
import simpleaudio


class App:

    def __init__(self,w):
        w.title('Reproc')
        w.geometry("500x500")
        w.resizable(0,0)

        self.imput = Entry(w)
        self.imput.grid(row=0, column=0)
        self.imput.focus()

        self.btn1 = Button(w, text='Descargar', command=self.descargar)
        self.btn1.grid(row=1, column=0)

        self.btn2 = Button(w, text='Play/Stop', command=self.play)
        self.btn2.grid(row=0, column=1)

        self.btn3 = Button(w, text='Pause/Resume', command=self.pause)
        self.btn3.grid(row=1, column=1)

        self.tabla = ttk.Treeview(w, height=15, selectmode="browse")
        self.tabla.grid(row=2, column=0, columnspan=2)
        self.tabla.heading("#0", text='Canciones', anchor=CENTER)
        self.tabla.column("#0",width=500, stretch=NO)
        self.tabla.bind("<ButtonRelease-1>", self.click)

        self.btn4 = Button(w, text='Open folder', command=self.explorer)
        self.btn4.grid(row=4, column=0)

        s = ttk.Style()
        s.theme_use('clam')
        s.configure("bar.Horizontal.TProgressbar",troughcolor ='grey', background='black', bordercolor="black",darkcolor="black",lightcolor="black")
        self.bar = ttk.Progressbar(w, length=300,style="bar.Horizontal.TProgressbar",value=50)
        self.bar.grid(row=3,column=0)

        self.song_on_bool = False
        self.song_play_bool = True

        self.getMusic()

    def descargar(self):

        busqueda = self.imput.get()

        enlace_convert = parse.urlencode({'search_query': busqueda})
        enlace_final = request.urlopen('http://www.youtube.com/results?' + enlace_convert)
        resultados = re.findall('href=\"\\/watch\\?v=(.{11})', enlace_final.read().decode())
        url = 'https://www.youtube.com/watch?v=d5XJ2GiR6Bo'


        ydl_opc = {
            'format': 'bestaudio/worstvideo',
            'outtmpl': '/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '320',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opc) as ydl:
            ydl.cache.remove()
            ydl.download([url])


        self.getMusic()


    def on(self, song_name=None):
        if(song_name == None):
            song_name_random = random.choice([name for name in os.listdir("./") if (os.path.isfile(name) and name.endswith(".wav"))])
            self.wave_read = wave.open(song_name_random,"rb")
        else:
            self.wave_read = wave.open(song_name,"rb")
        self.wave_read.setpos(200000)
        print(self.wave_read.getnframes())
        wave_obj = simpleaudio.WaveObject.from_wave_read(self.wave_read)
        self.play_obj = wave_obj.play()

    def explorer(self):
        a = os.getcwd()+"/Musica"
        os.system("start. "+"a")


    def onBucle(self):
        while True:
            if not self.play_obj.is_playing() and self.song_on_bool:
                self.on()

    def play(self):

        if not self.song_on_bool:
            try:
                self.on(self.song_name)
            except:
                self.on()

            hilo_bucle = threading.Thread(target=self.onBucle)
            hilo_bucle.start()
            self.song_on_bool = True

        else:
            self.play_obj.stop()
            self.song_on_bool = False

    def pause(self):

        if self.song_play_bool:
            self.play_obj.pause()
            self.song_play_bool = False

        else:
            self.play_obj.resume()
            self.song_play_bool = True

    def getMusic(self):
        with os.scandir("./") as it:
            for v in it:
                if v.is_file():
                    self.tabla.insert("",0,text=v.name)

    def click(self, event):
        self.song_name = self.tabla.item(self.tabla.selection())["text"]

if __name__ == "__main__":
    try:
        os.mkdir(os.getcwd()+"/Musica")
    except:
        pass

    os.chdir(os.getcwd()+"/Musica")
    win = Tk()
    app = App(win)
    win.mainloop()



    '''
    self.gif = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open(self.folder_img+"/CD-Icon2.jpg").resize((100,100),Image.ANTIALIAS))]
    self.lbl_img = Label(self.frame_music); self.animate()
    self.lbl_img.grid(row=0, column=0)
    
    def animate(self, frame=0):
        self.lbl_img.configure(image=self.gif[frame])
        self.w.after(20, lambda: self.animate((frame+1) % len(self.gif)))
    '''
