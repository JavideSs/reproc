from infi.systray import SysTrayIcon


class ModeTray():
    def __init__(self, w, t1):
        self.w = w
        self.controls = t1

        self.w.bind("<Unmap>", self.modeStray)
        #Evitar que <Unmap> funcione con el boton de cerrar, ya que no hay puto evento para el minimizado
        self.w.protocol("WM_DELETE_WINDOW", lambda: self.w.quit())
        #Count porque no se porque putas se produce el evento varias veces
        self.count = 0

        item_playpause = ("Play / Pause", None, lambda systray: self.controls.playpause())
        item_playnext = ("Play Next", None, lambda systray: self.controls.playNext())
        item_playprevious = ("Play Previuous", None, lambda systray: self.controls.playPrevious())
        item_separator1 = ("__________________", None, lambda systray: None)
        item_random = ("Set/Quit Random", None, lambda systray: self.controls.setRandom())
        item_bucle = ("Set/Quit Bucle", None, lambda systray: self.controls.setBucle())
        item_separator2 = ("__________________", None, lambda systray: None)
        item_open = ("Open", None, self.openW)
        
        menu_options = (item_playpause, item_playnext, item_playprevious, item_separator1, item_random, item_bucle, item_separator2, item_open)
        self.systray = SysTrayIcon(None, "Reproc", menu_options, default_menu_index=7, on_quit=self.exitW)

#_____________________________________________________________________________________________________________________

    def modeStray(self, event):
        #Evitar que <Unmap> se ejecute varias veces y que funcione con los botones de cambio de tab
        if not self.count and self.w.state() == "iconic":
            self.count += 1
            self.w.withdraw()
            self.systray.start()

    #__________________________________________________________________

    #Acabar programa si systray->quit
    def exitW(self, systray):
        if self.w.state() == "withdrawn":
            self.w.quit()


    #Reabrir programa si systray->open
    def openW(self, systray):
        self.count = 0
        self.w.deiconify()
        #La unica puta manera to close systray, que llama a on_quit
        #por lo que hay que verificar en on_quit que el programa no ha sido deiconfy
        systray._destroy(None,None,None,None)
