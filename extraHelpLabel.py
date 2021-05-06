import tkinter as tk
from tkinter.ttk import Separator

from _config import *
from _iconbase64 import img_wlbl_help_url


class HelpWLabel():
    def __init__(self, w_x, w_y):
        self.w_help = tk.Toplevel()
        self.w_help.title("Help")
        self.w_help.geometry("320x330+{0}+{1}".format(w_x, w_y))
        self.w_help.resizable(False,False)

        self.txt_intro = tk.Label(self.w_help, text="Reproc download songs from YouTube", foreground="blue4")
        self.txt_intro.grid(row=0, sticky="w", padx=10)

        self.lblframe_methods = tk.LabelFrame(self.w_help, text="Three methods to download a song", font=(None,10,"bold"))
        self.lblframe_methods.grid(row=1, sticky="we", padx=10, pady=(5,10))

        self.lbltxt_keywords = tk.Label(self.lblframe_methods, text="- KeyWords:", font=(None,9,"italic"))
        self.lbltxt_keywords.grid(row=0, sticky="w")

        text_txt_keywords = "As if the search for the song was done from YouTube.\nThe first search result will be added."
        self.txt_keywords = tk.Message(self.lblframe_methods, text=text_txt_keywords, width=300)
        self.txt_keywords.grid(row=1, sticky="w")

        self.separador1 = Separator(self.lblframe_methods, orient="horizontal")
        self.separador1.grid(row=2, sticky="we")

        self.lbltxt_url = tk.Label(self.lblframe_methods, text="- URL:", font=(None,9,"italic"))
        self.lbltxt_url.grid(row=3, sticky="w")

        text_txt_url = "Pasting the link of the song."
        self.txt_url = tk.Message(self.lblframe_methods, text=text_txt_url, width=300)
        self.txt_url.grid(row=4, sticky="w")

        self.separador2 = Separator(self.lblframe_methods, orient="horizontal")
        self.separador2.grid(row=5, sticky="we")

        self.lbltxt_playlisturl = tk.Label(self.lblframe_methods, text="- PlayList URL:", font=(None,9,"italic"))
        self.lbltxt_playlisturl.grid(row=6, sticky="w")

        text_txt_playlisturl = "Pasting the link of the playlist.\nAll the songs belonging to that playlist will be added.\nPrivate playlist or mixes can not download."
        self.txt_playlisturl = tk.Message(self.lblframe_methods, text=text_txt_playlisturl, width=300)
        self.txt_playlisturl.grid(row=7, sticky="w")

        self.lblframe_url = tk.LabelFrame(self.w_help, text="What is a URL?", font=(None,10,"bold"))
        self.lblframe_url.grid(row=2, sticky="we", padx=10)

        self.img_lbl_url = tk.PhotoImage(data=img_wlbl_help_url)
        self.lbl_url= tk.Label(self.lblframe_url, image=self.img_lbl_url)
        self.lbl_url.grid(row=0, column=0, sticky="w")

    def showW(self):
        self.w_help.deiconify()
