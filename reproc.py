from tkinter import Tk
from tkinter.ttk import Style
#from customTk import Win7Features

from data import config, images as b64img
from data.images.utilities import b64ToTk
from program import MusicTab

import gettext

#==================================================

class Reproc(Tk):
    def __init__(self):

        super().__init__()

        self.title("Reproc")
        self.iconphoto(True, b64ToTk(b64img.icon_reproc))
        self.geometry("400x480")

        self.resizable(False, False)
        self.eval("tk::PlaceWindow . center")
        self.protocol("WM_DELETE_WINDOW", self.onDelete)

        self.style = Style(self)
        self.setTheme()
        self.setLanguage()

        self.tab_music = MusicTab(self)
        self.tab_music.pack()

        '''
        self.win7_features = Win7Features(self)
        self.win7_features.createThumbBar(
            self.tab_music.fprevious,
            self.tab_music.fplaypause,
            self.tab_music.fnext,
        )
        '''

    #__________________________________________________

    def onDelete(self):
        self.saveJson()
        #self.win7_features.releaseThumbBar()


    def saveJson(self):
        self.tab_music.saveJson()
        config.save_user_config()
        self.destroy()


    def setTheme(self):
        theme = config.general["theme"]
        self.tk.call("source",
            config.os.path.join("customTk", "ttk_themes", theme + ".tcl"))
        self.style.theme_use(theme)
        #reconfig windows


    def setLanguage(self):
        language = gettext.translation("base",
            localedir=config.os.path.join("data", "locale"),
            languages=[config.general["language"]])
        language.install()
        _ = language.gettext


#==================================================


if __name__ == "__main__":
    app = Reproc()
    app.mainloop()