from win32api import *
from win32gui import *
import win32con
import sys, os
import struct
import time

class WindowsBalloonTip:

    def __init__(self):
        message_map = {win32con.WM_DESTROY: self.OnDestroy,}
        # Register the Window class.
        count=1
        wc= WNDCLASS()
        self.hinst = wc.hInstance = GetModuleHandle(None)
        wc.lpszClassName = "PythonTaskbar"
        wc.lpfnWndProc = message_map
                # could also specify a wndproc.
        self.classAtom = RegisterClass(wc)

    def popup_windows(self, title, msg,destroy_time=3):
        # Create the Window.
        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        # wc.hbrBackground = win32con.COLOR_SCROLLBAR
        self.hwnd = CreateWindow( self.classAtom, "Taskbar", style, \
                0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
                0, 0, self.hinst, None)
        UpdateWindow(self.hwnd)
        iconPathName = os.path.abspath(os.path.join( sys.path[0], "astro.ico")) 
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        try:
           hicon = LoadImage(self.hinst, iconPathName, \
                    win32con.IMAGE_ICON, 0, 0, icon_flags)
        except:
          hicon = LoadIcon(0, win32con.IDI_APPLICATION)
        flags = NIF_ICON | NIF_MESSAGE | NIF_TIP
        nid = (self.hwnd,0, flags, win32con.WM_USER+20, hicon, "tooltip")
        Shell_NotifyIcon(NIM_ADD, nid)
        Shell_NotifyIcon(NIM_MODIFY, \
                         (self.hwnd, 0, NIF_INFO, win32con.WM_USER+20,\
                          hicon, "Balloon  tooltip",msg,200,title))
        time.sleep(destroy_time)
        DestroyWindow(self.hwnd)
        #UnregisterClass(self.classAtom, self.hinst)

    def OnDestroy(self, hwnd, msg, wparam, lparam):
    #def OnDestroy(self,):
        nid = (self.hwnd, 0)
        Shell_NotifyIcon(NIM_DELETE, nid)
        PostQuitMessage(0) # Terminate the app.

def balloon_tip():
    w = WindowsBalloonTip()
    return w

if __name__ == '__main__':
    #balloon_tip("Title for popup","This is the popup's message")
    title='Title Test '
    msg='sample message !!'
    wd_obj=WindowsBalloonTip()
    wd_obj.popup_windows(title=title,msg=msg)
