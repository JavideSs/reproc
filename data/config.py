from data.data_types import *

import os
import platform
import json

SYSTEM = platform.system()
SYSTEM_ARCH = platform.architecture()[0]
JSON_FPATH = os.path.join("data", "user_config.json")

#==================================================

with open(JSON_FPATH) as json_user_config:
    user_config = json.loads(json_user_config.read())

def save_user_config():
    with open(JSON_FPATH, "w") as json_user_config:
        json.dump(user_config, json_user_config, indent=4)


general:Dict = user_config["State"]
playlist:Dict = {}   #user_config["Playlists"][general["playlist"]]
colors:Dict = user_config["Themes"][user_config["State"]["theme"]]

#==================================================

if SYSTEM == "Windows":
    SUPPORTED_SONG_FORMATS = (".mp3",".ogg")

elif SYSTEM == "Linux":
    SUPPORTED_SONG_FORMATS = (".ogg")

elif SYSTEM == "Darwin":
    SUPPORTED_SONG_FORMATS = (".ogg")

else:
    SUPPORTED_SONG_FORMATS = (".ogg")