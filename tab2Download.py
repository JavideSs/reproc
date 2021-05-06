import tkinter as tk
from tkinter import ttk
import youtube_dl
from urllib import parse, request
import re

from main2Download import Main
from extraHelpLabel import HelpWLabel
from _config import *
from _iconbase64 import *


class TabDownload():
    def __init__(self, w, tab2):
        self.w = w

        style = ttk.Style()
        style.configure("MenuUp.TFrame", background=color_reproc)
        style.configure("BtnAdd.TButton", background=color_reproc, font=(None,10))
        style.map("TButton",foreground=[("active","#cca9eb")])

        style.layout("AddList.Treeview.Item",[("Treeitem.padding",{"children":[("Treeitem.image",{"side":"left","sticky":""}),("Treeitem.text",{"side":"left","sticky":""})]})])
        style.configure("AddList.Treeview.Heading", font=("calibri",8), foreground="navy")
        style.configure("AddList.Treeview", font=("calibri",8), foreground="navy", borderwidth = 10, relief = 'flat')

        self.menu_up = ttk.Frame(tab2, style="MenuUp.TFrame")
        self.menu_up.grid(row=0, column=0, columnspan=2, sticky="we")

        self.img_btn_help = tk.PhotoImage(data=img_btn_help)
        self.btn_help = tk.Button(self.menu_up, image=self.img_btn_help, command=self.helpWLabel, borderwidth=0,
                            background=color_reproc, activebackground=color_reproc, highlightbackground=color_reproc)
        self.btn_help.grid(row=0, column=0, sticky="e", padx=(30,5), pady=(5,0))

        self.txt_entry_keywords = ttk.Label(self.menu_up, text="KeyWords  /  URL  /  PlayList URL :", font=(None,8,"bold"), background=color_reproc)
        self.txt_entry_keywords.grid(row=0, column=1, sticky="w", pady=(5,0))

        self.btn_paste_keywords = tk.Button(self.menu_up, text="Paste", command=self.paste, font=(None, 8, "underline"), takefocus=False, borderwidth=0,
                                    background=color_reproc, activebackground=color_reproc, highlightbackground=color_reproc, activeforeground="blue")
        self.btn_paste_keywords.grid(row=0, column=2, sticky="w", pady=(8,0))

        self.entry_keywords = ttk.Entry(self.menu_up, width=40, foreground=color_entry, font=font)
        self.entry_keywords.grid(row=1, column=0, columnspan=3, padx=(36,0), pady=(0,5))

        self.btn_add_keywords = ttk.Button(self.menu_up, style="BtnAdd.TButton", text="Add", width=4, takefocus=False)
        self.btn_add_keywords.grid(row=1, column=3, padx=(0,36), pady=(0,5))

        #_
        self.addlist = ttk.Treeview(tab2, style="AddList.Treeview", height=10, selectmode="extended")
        self.addlist.grid(row=1, column=0)
        self.addlist_scroll = ttk.Scrollbar(tab2, command=self.addlist.yview)
        self.addlist_scroll.grid(row=1, column=1, sticky="ns")
        self.addlist.configure(yscroll=self.addlist_scroll.set)
        self.addlist["columns"] = ("#duration", "#size", "#status")
        self.addlist.column("#0", width=195)
        self.addlist.column("#duration", width=75)
        self.addlist.column("#size", width=50)
        self.addlist.column("#status", width=50)
        self.addlist.heading("#0", text="Name", anchor="center")
        self.addlist.heading("#duration", text="Duration", anchor="center")
        self.addlist.heading("#size", text="Size", anchor="center")
        self.addlist.heading("#status", text="Status", anchor="center")

        self.addlist.insert("", "end", text="gf", values=("s","d","ee"))
        self.addlist.insert("", "end", text="gf", values=("s","d","ee"))
        self.addlist.insert("", "end", text="gf", values=("s","d","ee"))
        self.addlist.bind('<Button-1>', self.handle_click)

        self.program = Main()

        tab2.bind("<space>", lambda event: None)

#__________________________________________________________________________________________________________________________________________________________________________________________________
    def handle_click(self, event):
        if self.addlist.identify_region(event.x, event.y) == "separator":
            return "break"

    def helpWLabel(self):
        try:
            #Visualizar ventana de ayuda
            self.lbl_help.showW()
        except:
            #No se ha creado la ventana de ayuda
            self.lbl_help = HelpWLabel(self.w.winfo_x()+10, self.w.winfo_y()+10)


    def paste(self):
        #Copiar lo que hay en el portapapeles al entry
        self.entry_keywords.delete(0, tk.END)
        try: self.entry_keywords.insert(0, self.w.clipboard_get())
        except: pass


    def descargar(self):
        busqueda = self.entry_keywords.get()

        enlace_convert = parse.urlencode({"search_query": busqueda})
        enlace_final = request.urlopen("http://www.youtube.com/results?" + enlace_convert)
        resultados = re.findall(r"/watch\?v=(.{11})", enlace_final.read().decode())
        url=resultados[0]

        ydl_opc = {
            "format": "bestaudio/worstvideo",
            "outtmpl": folder_music+"/%(title)s.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opc) as ydl:
            ydl.cache.remove()
            ydl.download([url])


#Agregar max de descargas
#si el clipboard no hay nada copiado salta error
