from data.data_types import *

import platform
from ctypes import windll

#==================================================

class ThumbBar():
    def __init__(self, w, img_path:str, btns:Tuple[Tuple[str,Callable],...], btnsset:Tuple[int]): pass
    def set(self, pos:int, id:int): pass
    def release(self): pass

'''
The module only works for python versions compatible with the version used to compile the module
Available: python3.7-32bits and python3.10-64bits
'''

try:
    if platform.architecture()[0] == "64bit":
        from .CThumbBar import ThumbBar_x64 as CThumbBar
    else:
        from .CThumbBar import ThumbBar_Win32 as CThumbBar

    class ThumbBar(ThumbBar):
        def __init__(self, w, img_path, btns, btnsset):
            self.hWnd = windll.user32.GetParent(w.winfo_id())

            CThumbBar.create(self.hWnd, img_path, btns, btnsset)

        def set(self, pos, id):
            CThumbBar.update(pos, id)

        def release(self):
            CThumbBar.release()

except: pass

#'LRESULT CALLBACK WndProc()' in python
'''
import win32api, win32gui, win32con

class ThumbBar():
    def __init__(self, w, img_path:str, btns:Tuple[Tuple[str,Callable],...], btnsset:Tuple[int]):
        self.btns = btns

        self.hWnd = win32gui.GetParent(w.winfo_id())

        self.wndproctk = win32api.GetWindowLong(self.hWnd, win32con.GWL_WNDPROC)
        win32gui.SetWindowLong(self.hWnd, win32con.GWL_WNDPROC, self.wndproc)

        _ThumbBar.create(self.hWnd, img_path, btns, btnsset)

    def wndproc(self, hWnd, message, wParam, lParam):
        if message == win32con.WM_COMMAND:
            for i in range(len(self.btns)):
                if i+90 == wParam & 0xFFFF:
                    self.btns[i][1]()

        return win32gui.CallWindowProc(self.wndproctk, hWnd, message, wParam, lParam)

    def set(self, pos, id):
        _ThumbBar.update(pos, id)

    def release(self):
        _ThumbBar.release()
'''