import os
import sys


author='''
                    Created by:
        __                                  __
        /               ,       /         /    )
       /    __              __ /    __   (__      __
      /    /   ) | /  /   /   /   /___)     |    (_ `
 (___/    (___(  |/  /   (___/   (___  (____/   (__)
______________________________________________________'''

color_menu_up = "#CBD8E3"
color_tab1_playlist = "#f7f0f7"
color_tab1_menu_down = "#e0e0e0"

if sys.platform == "win32":
    folder_music = os.getcwd()+r"\Music"
    folder_img = os.getcwd()+r"\img"
    font = ("calibri",10)
    tabs_padd = 76
    entry_search_width = 24
    openfolder_music = r'start %windir%\explorer.exe "{0}"'.format(folder_music)

else:
    folder_music = os.getcwd()+r"/Music"
    folder_img = os.getcwd()+r"/img"
    font = ("calibri",8)
    tabs_padd = 55
    entry_search_width = 23
    openfolder_music = 'nautilus --browser {0}'.format(folder_music)
