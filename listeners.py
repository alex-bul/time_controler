import win32gui
import win32api
import win32ui
import win32con
import win32process

import datetime
import time
import psutil
import os

from test import run_window
from threading import Thread
from mouse_listener import MouseListener
from button_listener import ButtonListener
from DB_module import DB_bot

import logging


#
# logging.info('dddddddd')


def start_all_listener():
    a = Thread(target=start_mouse_listener)
    a.setName('mouse_listener')
    a.start()

    a = Thread(target=start_button_listener)
    a.setName('button_listener')
    a.start()

    a = Thread(target=start_window_listener)
    a.setName('window_listener')
    a.start()


def save_image(path, title):
    path = path.replace("\\", "/")
    icoX = win32api.GetSystemMetrics(win32con.SM_CXICON)

    large, small = win32gui.ExtractIconEx(path, 0)
    win32gui.DestroyIcon(small[0])

    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    hbmp = win32ui.CreateBitmap()
    hbmp.CreateCompatibleBitmap(hdc, icoX, icoX)
    hdc = hdc.CreateCompatibleDC()

    hdc.SelectObject(hbmp)
    hdc.DrawIcon((0, 0), large[0])

    savePath = "./icons/"
    # print(hdc)
    hbmp.SaveBitmapFile(hdc, savePath + f"{title}.bmp")
    # bmpinfo = dataBitMap.GetInfo()


class WindowListener:
    def __init__(self):
        self.current_procces = {}
        self.c = DB_bot()
        # self.clear_sessions()

    def create_session(self, procces):
        if procces['title'] == '':
            procces['title'] = 'Рабочий стол'
        self.c.create_new_session(None, procces['title'], procces['duration'], procces['executable_path'],
                                  procces['start_date'])

    def get_current_window(self):
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        if pid >= 0:
            path = psutil.Process(pid).exe()
            title = win32gui.GetWindowText(hwnd).split('-')[-1].strip()
            if path != self.current_procces.get('executable_path', '') or datetime.datetime.now().strftime('%H:%M')[
                                                                          3:] == '00':
                logging.info(f'начата сессия {title}')
                self.current_procces.clear()
                self.current_procces['title'] = title
                self.current_procces['duration'] = 0
                self.current_procces['executable_path'] = path
                self.current_procces['start_date'] = time.time()
                self.create_session(self.current_procces)
            self.current_procces['duration'] += 0.5
            self.c.set_duration_last_session(self.current_procces['duration'])

    def start(self):
        while True:
            try:
                self.get_current_window()
                time.sleep(0.5)
            except Exception as ex:
                print(f'Ошибка получения окна: {ex}')

    def clear_sessions(self):
        self.c.delete_all_sessions()


def start_button_listener():
    ButtonListener().start()


def start_mouse_listener():
    MouseListener().start()


def start_window_listener():
    WindowListener().start()

# a = Thread(target=run_window)
# a.setName('run_window')
# a.start()
# run_window()
