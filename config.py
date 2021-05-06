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
color_playlist = "#f7f0f7"
color_menu_down = "#e0e0e0"

if sys.platform == "win32":
    folder_music = os.getcwd()+r"\Music"
    folder_img = os.getcwd()+r"\img"
    font = ("calibri",10)
    tabs_padd = 76
    width_entry = 24
else:
    folder_music = os.getcwd()+r"/Music"
    folder_img = os.getcwd()+r"/img"
    font = ("calibri",8)
    tabs_padd = 55
    width_entry = 23