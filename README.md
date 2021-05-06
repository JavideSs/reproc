# Reproc - Local Music Player
Reproc is a free-open music player written in python with tkinter, ttk.

![Screenshot](program/img/reproc.jpg?raw=true "App interface")

-----

# How to use it

## Interface

### Insert songs
The songs are imported from the "Music" folder of the directory where "app.py" is located.
To access it directly from the app, just click on the folder at the bottom right; if you need to update the status of the songs you will have to click the refresh button next to it.
### Music player
Reproc use the pygame mixer module to reproduce songs, it is recommended that these do not vary in kbps so as not to appreciate delay in each reproduction.
There are options to play in a loop and in random mode, sort the playlist according to name, creation date or time, filter songs by name, and other basic characteristics.
For the extraction of metadata from the songs, the TinyTag module is used, which also allows to view the cover art if the song has it.
### Events
- With the SPACE KEY we can play/pause /continue the song
- With the ENTER KEY we can reproduce the song selected in the playlist
- With the TWO ARROW KEYS we can move forward/backward 5s of the current song

## Toolbar
So that the app does not disturb in the taskbar, it has been designed in such a way that when it is minimized it disappears from the taskbar and goes to the toolbar, from which it can be controlled perfectly, as well as return again to the app interface

![Screenshot](program/img/Toolbar.jpg?raw=true "ToolBar")

-----

# Contributing
1. Pull Request
- https://github.com/JavideSs/Reproc
2. Through Email
- javimelladoo@gmail.com
3. Through Instagram
- https://www.instagram.com/javidess

-----

## Upcoming updates
- Edit song names from the playlist
- Tab of app settings and appearance modification
- Tab of download songs from youtube using youtube-dl