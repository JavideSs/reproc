import json, os, platform

SYSTEM = platform.system()
JSON_FILE_PATH = os.path.join("data", "user_config.json")

#==================================================

with open(JSON_FILE_PATH) as json_user_config:
    user_config = json.loads(json_user_config.read())

def save_user_config():
    with open(JSON_FILE_PATH, "w") as json_user_config:
        json.dump(user_config, json_user_config, indent=4)


general = user_config["State"]
playlist = {}   #user_config["Playlists"][general["playlist"]]
colors = user_config["Themes"][user_config["State"]["theme"]]

#==================================================

if SYSTEM == "Windows":
    CMD_TO_OPEN_EXPLORER = 'start %windir%\explorer.exe "{}"'
    SUPPORTED_SONG_FORMATS = (".mp3",".ogg")

elif SYSTEM == "Linux":
    CMD_TO_OPEN_EXPLORER = 'xdg-open {}'
    SUPPORTED_SONG_FORMATS = (".ogg")

elif SYSTEM == "Darwin":
    CMD_TO_OPEN_EXPLORER = ""
    SUPPORTED_SONG_FORMATS = (".ogg")

else:
    CMD_TO_OPEN_EXPLORER = ""
    SUPPORTED_SONG_FORMATS = (".ogg")