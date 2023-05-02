import os
import platform
import subprocess

#==================================================

#If there is not text or all the text there is are spaces
#len(self.entry_search.get()) - self.entry_search.get().count(" ") == 0
#And if old text is not the same as the new text
def validEntryText(text:str, text_original:str="") -> bool:
    return any(filter(lambda i: i!=" ", text)) and text!=text_original


def open_file(filename:str):
    if platform.system() == "Windows":
        os.startfile(filename)
    else:
        opener = "open" if platform.system() == "Darwin" else "xdg-open"
        subprocess.call([opener, filename])