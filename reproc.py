from tkinter import Tk
from tkinter.ttk import Style
from ui import WinFeatures

from ui import images as b64img
from ui.images.utilities import *

from data import config

from program import MusicTab

import os
import gettext

#==================================================

class Reproc(Tk):
    def __init__(self):

        super().__init__()

        self.title("Reproc")
        self.iconphoto(True, b64ToTk(b64img.icon))

        self.geometry("400x480")
        self.eval("tk::PlaceWindow . center")
        self.resizable(width=False, height=True)

        self.protocol("WM_DELETE_WINDOW", self.onExit)

        self.style = Style(self)
        self.setTheme()
        self.setLanguage()


        self.tab_music = MusicTab(self)
        self.tab_music.pack(fill="both", expand=True)

        #Functions valid only for platforms that support it
        self.win_features = WinFeatures(self)
        self.win_features.createThumbBar(
            self.tab_music.fprevious,
            self.tab_music.fplaypause,
            self.tab_music.fnext,
        )

    #__________________________________________________

    def onExit(self):
        self.saveJson()
        self.win_features.releaseThumbBar()
        self.destroy()


    def saveJson(self):
        '''
        Other saves are updated when their associated event is called
        '''
        config.general.update(self.tab_music.playback.getStates())
        config.save_user_config()


    def setTheme(self):
        theme = config.general["theme"]
        self.tk.call("source",
            os.path.join("ui", "ttk_themes", theme + ".tcl"))
        self.style.theme_use(theme)
        #reconfig window


    def setLanguage(self):
        language = gettext.translation("base",
            localedir=os.path.join("data", "locale"),
            languages=[config.general["lang"]])
        language.install()
        _ = language.gettext
        #reconfig window


#==================================================


if __name__ == "__main__":
    app = Reproc()
    app.mainloop()