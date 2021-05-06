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

sep = os.sep
folder_music = os.getcwd() + sep+"Music"
folder_img = os.getcwd() + sep+"program" + sep+"img"

color_reproc = "#CBD8E3"
color_reproc2 = "#e0e0e0"
color_playlist = "#f7f0f7"
color_entry = "#9665AA"

if sys.platform == "win32":
    font = ("calibri",10)
    tabs_padd = 76
    entry_search_width = 20
    open_folder_music = r'start %windir%\explorer.exe "{0}"'.format(folder_music)

else:
    font = ("calibri",8)
    tabs_padd = 55
    entry_search_width = 18
    open_folder_music = 'xdg-open {0}'.format(folder_music)