import platform

#==================================================

'''
Tkinter fun:
Depending on the system, the interface can have:
- Different appearance
- Different measures

This file tries to set all random size variables
'''

if platform.system() == "Windows":
    MUSICTAB_PLAYLIST_COLUMNTITLE_WIDTH = 335
    MUSICTAB_PLAYLIST_COLUMNDURATION_WIDTH = 50
    MUSICTAB_PLAYLIST_LABELEDITSONG_ENTRYEDITSONG_WIDTH = 45
    MUSICTAB_PLAYLIST_LABELEDITSONG_MENU_HEIGHT = 150
    MUSICTAB_PLAYLISTCONTROL_PLAYLISTHANDLERSET_WIDTH = 13
    MUSICTAB_PLAYLISTCONTROL_ENTRYSEARCH_WIDTH = 15
    MUSICTAB_PLAYLISTCONTROL_TOPLEVELPLAYLISTEDIT_GEOMETRY = (200,210)

elif platform.system() == "Linux":
    if platform.freedesktop_os_release()["NAME"] == "Ubuntu":
        MUSICTAB_PLAYLIST_COLUMNTITLE_WIDTH = 330
        MUSICTAB_PLAYLIST_COLUMNDURATION_WIDTH = 55
        MUSICTAB_PLAYLIST_LABELEDITSONG_ENTRYEDITSONG_WIDTH = 32
        MUSICTAB_PLAYLIST_LABELEDITSONG_MENU_HEIGHT = 120
        MUSICTAB_PLAYLISTCONTROL_PLAYLISTHANDLERSET_WIDTH = 12
        MUSICTAB_PLAYLISTCONTROL_ENTRYSEARCH_WIDTH = 10
        MUSICTAB_PLAYLISTCONTROL_TOPLEVELPLAYLISTEDIT_GEOMETRY = (240,230)

else:
    MUSICTAB_PLAYLIST_COLUMNTITLE_WIDTH = 330
    MUSICTAB_PLAYLIST_COLUMNDURATION_WIDTH = 55
    MUSICTAB_PLAYLIST_LABELEDITSONG_ENTRYEDITSONG_WIDTH = 35
    MUSICTAB_PLAYLIST_LABELEDITSONG_MENU_HEIGHT = 120
    MUSICTAB_PLAYLISTCONTROL_PLAYLISTHANDLERSET_WIDTH = 10
    MUSICTAB_PLAYLISTCONTROL_ENTRYSEARCH_WIDTH = 10
    MUSICTAB_PLAYLISTCONTROL_TOPLEVELPLAYLISTEDIT_GEOMETRY = (240,230)