from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QAbstractItemView, QFileDialog, QWidget, \
    QDialog, QDialogButtonBox, QVBoxLayout, QLabel
import sys
from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries, QStackedBarSeries, QBarCategoryAxis
from PyQt5.QtGui import QPainter, QPixmap, QColor, QIcon
from PyQt5.QtCore import Qt
import os
import time
import logging

from DB_module import DB_bot

from front import Ui_Form
import listeners
import datetime
import xlsxwriter
import json

if "icons" not in os.listdir(os.path.curdir):
    os.mkdir("./icons/")


def get_count_press(name, arg_name='count_press'):
    data = json.loads(open(name, 'r').read())
    result = 0
    for row in data[datetime.datetime.now().strftime('%d.%m.%y')].values():
        result += row[arg_name]
    return result


def merge_dicts(d_1, d_2):
    result = {}
    for key, val in list(d_1.items()) + list(d_2.items()):
        result[key] = result.get(key, 0) + val
    return result


def get_most_press_button():
    data = json.loads(open("buttons_data.json", 'r').read())
    result = {}
    for row in data[datetime.datetime.now().strftime('%d.%m.%y')].values():
        result = merge_dicts(row['buttons'], result)
    result = sorted(result.items(), key=lambda x: x[1], reverse=True)
    if result:
        return result[0]
    return ('', 0)


class CustomDialog(QDialog):

    def __init__(self, *args, **kwargs):
        super(CustomDialog, self).__init__(*args, **kwargs)

        self.setWindowTitle("Дополнительная статистика")
        self.layout = QVBoxLayout()

        try:
            self.label_mouse_clicks = QLabel(self,
                                             text=f'Количество кликов за день: {get_count_press("mouse_data.json")}')
            self.label_mouse_distance = QLabel(self, text=f'Дистанция, '
                                                          f'пройденная мышкой: {int(get_count_press("mouse_data.json", "distance"))}px')
            self.label_button_press = QLabel(self,
                                             text=f'Количество'
                                                  f' нажатий клавиатуры за день: {get_count_press("buttons_data.json")}')
            name, count_press = get_most_press_button()
            if count_press == 1:
                word_count_data = 'нажатие'
            elif 1 < count_press < 5:
                word_count_data = 'нажатия'
            else:
                word_count_data = 'нажатий'
            self.label_button_most_press = QLabel(self,
                                                  text=f'Самая '
                                                       f'популярная клавиша: {name} ({count_press} {word_count_data})')

            self.layout.addWidget(self.label_mouse_clicks)
            self.layout.addWidget(self.label_mouse_distance)
            self.layout.addWidget(self.label_button_press)
            self.layout.addWidget(self.label_button_most_press)
        except Exception as ex:
            self.error_label = QLabel(self, f'Произошла ошибка: {ex}')

        self.setLayout(self.layout)


def get_session_index(data, session):
    if session in data:
        return data.index(session)
    return -1


def get_seconds_current_day():
    current_time = datetime.datetime.now()
    return int(current_time.hour) * 3600 + int(current_time.minute) * 60 + int(current_time.second)


class ImageWidget(QWidget):

    def __init__(self, imagePath, parent):
        super(ImageWidget, self).__init__(parent)
        self.picture = QPixmap(imagePath)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.picture)


class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super(QTextEditLogger, self).__init__()

        self.widget = parent.plainTextEdit
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class MyWidget(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Time control")
        self.setGeometry(100, 100, 770, 700)
        self.setWindowIcon(QIcon('analytics.png'))

        self.chartView = QChartView()
        self.verticalLayout.addWidget(self.chartView)
        self.c = DB_bot()
        self.buttonRefresh.clicked.connect(self.update)
        self.pushButton_export.clicked.connect(self.saveFileDialog)
        self.pushButton_stats.clicked.connect(self.openStatDialog)
        self.current_table_data = []
        self.update()
        self.setLayout(self.verticalLayout_2)

        logTextBox = QTextEditLogger(self)
        logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        logging.getLogger().addHandler(logTextBox)
        logging.getLogger().setLevel(logging.DEBUG)

        w = QWidget(self)
        w.setLayout(self.verticalLayout_2)
        self.setCentralWidget(w)

    def update(self):
        self.update_graph()
        self.update_list()

    def update_graph(self):
        try:
            low = QBarSet("Сон")
            high = QBarSet("Работа")
            high.setColor(QColor(115, 199, 82))

            current_time = time.time()
            start_day_time = current_time - get_seconds_current_day()
            sessions = self.c.get_sessions_by_date(start_day_time)
            sorted_data = {}
            for row in sessions:
                hour = (row[-1] - start_day_time) / 3600 + 1
                if hour % 1 > 0.99:
                    hour = int(hour) + 1
                hour = int(hour)
                sorted_data[hour] = sorted_data.get(hour, []) + [row]
            for j in range(1, 25):
                if j in sorted_data.keys():
                    result = sum([i[2] for i in sorted_data[j]]) // 60
                    high.append(result)
                    low.append(-(60 - result))
                else:
                    high.append(0)
                    low.append(0)
            series = QStackedBarSeries()
            series.append(high)

            chart = QChart()
            chart.addSeries(series)
            chart.setTitle("Статистика использования ПК")
            chart.setAnimationOptions(QChart.SeriesAnimations)

            categories = [str(i) for i in range(1, 25)]

            axis = QBarCategoryAxis()
            axis.append(categories)
            axis.setTitleText("Время")
            chart.createDefaultAxes()
            chart.setAxisX(axis, series)
            chart.axisY(series).setRange(0, 60)
            chart.axisY(series).setTitleText("Длительность (мин.)")
            chart.setMinimumWidth(20)

            chart.legend().setVisible(True)
            chart.legend().setAlignment(Qt.AlignBottom)

            self.chartView.setChart(chart)
            self.chartView.setRenderHint(QPainter.Antialiasing)
        except Exception as ex:
            logging.info(f'Ошибка обновления графика, попоробуйте снова!')

    def update_list(self):
        try:
            current_time = time.time()
            start_day_time = current_time - get_seconds_current_day()
            sessions = self.c.get_sessions_by_date(start_day_time)
            data_by_programms = {}
            executable_paths = {}
            for row in sessions:
                data_by_programms[row[1]] = data_by_programms.get(row[1], 0) + row[2]
                executable_paths[row[1]] = row[3]
            self.tableWidget.setColumnCount(3)  # Устанавливаем три колонки
            self.tableWidget.setHorizontalHeaderLabels(["Иконка", "Программа", "Длительность (мин.)"])
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            table_data = sorted(list(data_by_programms.items()), key=lambda x: x[1], reverse=True)
            for i, row in enumerate(table_data):
                if i != get_session_index(self.current_table_data, row):
                    duration = int(row[1] // 60) if row[1] // 60 % 1 == 0 else row[1] // 60
                    if duration:
                        if self.tableWidget.rowCount() <= i:
                            self.tableWidget.insertRow(self.tableWidget.rowCount())
                        if row[0] not in os.listdir("./icons"):
                            listeners.save_image(executable_paths[row[0]], row[0])
                        self.tableWidget.setCellWidget(i, 0, ImageWidget(f'./icons/{row[0]}.bmp', self))
                        self.tableWidget.setItem(i, 1, QTableWidgetItem(row[0]))
                        self.tableWidget.setItem(i, 2, QTableWidgetItem(str(duration)))
            self.current_table_data = table_data.copy()
            self.tableWidget.resizeColumnsToContents()
        except Exception as ex:
            logging.info(f'Ошибка обновления статистики, попоробуйте снова!')

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            if '.xlsx' not in fileName:
                fileName = fileName.strip('\n .') + '.xlsx'
            workbook = xlsxwriter.Workbook(fileName)
            worksheet = workbook.add_worksheet()

            for column, title in enumerate(["Программа", "Длительность (мин.)"]):
                worksheet.write(0, column, title)

            row = 1
            for title, duration in self.current_table_data:
                duration = int(duration // 60) if duration // 60 % 1 == 0 else duration // 60
                if duration:
                    worksheet.write(row, 0, title)
                    worksheet.write(row, 1, duration)
                    row += 1

            worksheet.write(row, 0, 'Общее время')
            worksheet.write(row, 1, f'=SUM(B2:B{row})')

            workbook.close()

    def openStatDialog(self):
        dlg = CustomDialog(self)
        dlg.exec_()


def run_window():
    try:
        app = QApplication(sys.argv)
        app.setAttribute(Qt.AA_DisableWindowContextHelpButton)
        ex = MyWidget()
        ex.show()
        sys.exit(app.exec_())
    except Exception as ex:
        run_window()
        logging.info(f'Произошла ошибка, программа перезапущена!')

if __name__ == '__main__':
    listeners.start_all_listener()
    run_window()
    print(1)
