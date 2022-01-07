import shutil
import os
import ctypes
import msvcrt
import subprocess
from sys import stdout, stdin
from blessed import Terminal

from ctypes import wintypes
from os import system, name

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
user32 = ctypes.WinDLL('user32', use_last_error=True)

SW_MAXIMIZE = 3

kernel32.GetConsoleWindow.restype = wintypes.HWND
kernel32.GetLargestConsoleWindowSize.restype = wintypes._COORD
kernel32.GetLargestConsoleWindowSize.argtypes = (wintypes.HANDLE,)
user32.ShowWindow.argtypes = (wintypes.HWND, ctypes.c_int)

class Screen:

    def __init__(self):
        self.terminal_cols, self.terminal_rows =  self.maximize_console()
        self.terminal = None #holds blessed terminal object

    def maximize_console(self,lines=None): #fits the terminal to user screen
        fd = os.open('CONOUT$', os.O_RDWR)
        try:
            hCon = msvcrt.get_osfhandle(fd)
            max_size = kernel32.GetLargestConsoleWindowSize(hCon)
            if max_size.X == 0 and max_size.Y == 0:
                raise ctypes.WinError(ctypes.get_last_error())
        finally:
            os.close(fd)
        cols = max_size.X
        hWnd = kernel32.GetConsoleWindow()
        if cols and hWnd:
            if lines is None:
                lines = max_size.Y
            else:
                lines = max(min(lines, 9999), max_size.Y)
            subprocess.check_call('mode.com con cols={} lines={}'.format(
                                    cols, lines))
            user32.ShowWindow(hWnd, SW_MAXIMIZE)

        return shutil.get_terminal_size()

    def initialize_blessed(self):
        term = Terminal()
        self.terminal = term
        return term

    def ask_dimensions(self):
        term = self.terminal
        print(term.move_xy((term.width-26)//2, (term.height-2)//2) + "Enter the board dimensions")
        rows = input(term.move_xy((term.width-22)//2, term.height//2)+"Enter number of rows: ")
        cols = input(term.move_xy((term.width-22)//2, (term.height+2)//2)+"Enter number of cols: ")
        return [rows,cols]
