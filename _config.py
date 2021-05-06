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

color_reproc = "#CBD8E3"
color_reproc2 = "#e0e0e0"

color_playlist = "#f7f0f7"
color_addlist = ""

color_entry = "#9665AA"

if sys.platform == "win32":
    folder_music = os.getcwd()+r"\Music"
    folder_img = os.getcwd()+r"\img"
    font = ("calibri",10)
    tabs_padd = 76
    entry_search_width = 24
    open_folder_music = r'start %windir%\explorer.exe "{0}"'.format(folder_music)

else:
    folder_music = os.getcwd()+r"\Music"
    folder_img = os.getcwd()+r"\img"
    font = ("calibri",8)
    tabs_padd = 55
    entry_search_width = 23
    open_folder_music = 'xdg-open {0}'.format(folder_music)

#https://i.ytimg.com/vi/url/hqdefault.jpg
