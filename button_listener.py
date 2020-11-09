import os
import json
import datetime
import time

from threading import Thread
from pynput import keyboard
from config import *


class ButtonListener:
    def __init__(self):
        self.count_press = 0
        self.buttons = {}

    def start(self):
        Thread(target=self.write_data).start()
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()
        listener.join()

    def on_press(self, key):
        if key == keyboard.Key.esc:
            return False  # stop listener
        try:
            k = key.char  # single-char keysda
        except:
            k = key.name  # other keys
        if k is not None:
            if k.isalpha():
                self.count_press += 1
                self.buttons[k] = self.buttons.get(k, 0) + 1

    def restart(self):
        self.__init__()

    def write_data(self):
        while True:
            current_time = datetime.datetime.now()
            if current_time.strftime('%H:%M')[3:] == '00' or is_test:
                try:
                    if file_name_buttons not in os.listdir(os.path.curdir):
                        with open(file_name_buttons, 'w') as f:
                            f.write(json.dumps({}))
                        file_data = {}
                    else:
                        a = open(file_name_buttons, 'r').read()
                        file_data = json.loads(a)
                    time_for_write = (current_time - datetime.timedelta(hours=1)).strftime('%H:%M')
                    current_date = datetime.datetime.now()
                    if time_for_write == '23:00':
                        current_date -= datetime.timedelta(days=1)
                    today_data = file_data.get(current_date.strftime('%d.%m.%y'), {})
                    today_data[time_for_write] = {'buttons': self.buttons, 'count_press': self.count_press}
                    file_data[current_date.strftime('%d.%m.%y')] = today_data
                    with open(file_name_buttons, 'w') as f:
                        f.write(json.dumps(file_data))
                    self.restart()
                    time.sleep(60)
                except Exception as ex:
                    print('Ошибка записи данных клава:', ex)


if __name__ == '__main__':
    ButtonListener().start()
