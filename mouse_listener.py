import math
import os
import json
import datetime
import time

from threading import Thread
from pynput.mouse import Listener
from config import *


class MouseListener:
    def __init__(self):
        self.old_x, old_y = None, None
        self.distance = 0
        self.clicks = 0

    def start(self):
        Thread(target=self.write_data).start()
        with Listener(
                on_move=self.on_move,
                on_click=self.on_click) as listener:
            listener.join()

    def on_move(self, x, y):
        if self.old_x and self.old_y:
            self.distance += math.sqrt((self.old_x - x) ** 2 + (self.old_y - y) ** 2)
        self.old_x, self.old_y = x, y

    def on_click(self, x, y, button, pressed):
        self.clicks += 1

    def get_distance(self):
        return self.distance

    def restart(self):
        self.__init__()

    def write_data(self):
        while True:
            current_time = datetime.datetime.now()
            if current_time.strftime('%H:%M')[3:] == '00' or is_test:
                try:
                    if file_name_mouse not in os.listdir(os.path.curdir):
                        with open(file_name_mouse, 'w') as f:
                            print(2)
                            f.write(json.dumps({}))
                        file_data = {}
                    else:
                        a = open(file_name_mouse, 'r').read()
                        if a == '':
                            a = '{}'
                        file_data = json.loads(a)
                    time_for_write = (current_time - datetime.timedelta(hours=1)).strftime('%H:%M:%S')
                    current_date = datetime.datetime.now()
                    print({'distance': self.distance, 'count_press': self.clicks // 2})
                    # if time_for_write == '23:00':
                    #     current_date -= datetime.timedelta(days=1)
                    today_data = file_data.get(current_date.strftime('%d.%m.%y'), {})
                    today_data[time_for_write] = {'distance': self.distance, 'count_press': self.clicks}
                    file_data[current_date.strftime('%d.%m.%y')] = today_data
                    with open(file_name_mouse, 'w') as f:
                        f.write(json.dumps(file_data))
                    self.restart()
                    time.sleep(1)
                except Exception as ex:
                    print('Ошибка записи данных клава:', ex)


if __name__ == '__main__':
    MouseListener().start()
