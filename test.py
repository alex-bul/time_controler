from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QAbstractItemView, QFileDialog
import sys
from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries, QStackedBarSeries, QBarCategoryAxis
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import numpy as np
import time
import logging

from DB_module import DB_bot

from test_form import Ui_Form
import listeners
import datetime


def get_seconds_current_day():
    current_time = datetime.datetime.now()
    return int(current_time.hour) * 3600 + int(current_time.minute) * 60 + int(current_time.second)


class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()

        self.widget = parent.plainTextEdit
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)


class MyWidget(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("PyQt BarChart")
        self.setGeometry(100, 100, 770, 700)
        self.show()
        self.c = DB_bot()
        self.buttonRefresh.clicked.connect(self.update)
        self.pushButton_2.clicked.connect(self.saveFileDialog)
        self.chartView = None
        self.update()

        logTextBox = QTextEditLogger(self)
        # self.plainTextEdit.setTextInteractionFlags(Qt.TextSelectableByMouse)
        logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        logging.getLogger().addHandler(logTextBox)
        logging.getLogger().setLevel(logging.DEBUG)

    def update(self):
        self.update_graph()
        self.update_list()

    def update_graph(self):
        self.verticalLayout.removeWidget(self.chartView)
        low = QBarSet("Сон")
        high = QBarSet("Работа")

        current_time = time.time()
        sessions = self.c.get_sessions_by_date(current_time - get_seconds_current_day())
        sorted_data = {}
        for row in sessions:
            hour = (current_time - row[-1]) / 3600
            if hour % 1 > 0:
                hour = int(hour) + 1
            sorted_data[hour] = sorted_data.get(hour, []) + [row]

        for j in range(24):
            if j in sorted_data.keys():
                result = sum([i[2] for i in sorted_data[j]]) // 60
                high.append(result)
                low.append(-(60 - result))
            else:
                high.append(0)
                low.append(0)

        series = QStackedBarSeries()
        series.append(low)
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
        chart.axisY(series).setRange(-60, 60)
        chart.axisY(series).setTitleText("Длительность (мин.)")
        chart.setMinimumWidth(20)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        self.chartView = QChartView(chart)
        self.chartView.setRenderHint(QPainter.Antialiasing)

        self.chartView = QChartView(chart)
        # self.chartView.setGeometry(100, 100, 100, 100)
        self.chartView.setRenderHint(QPainter.Antialiasing)
        self.verticalLayout.addWidget(self.chartView)

    def update_list(self):
        current_time = time.time()
        sessions = self.c.get_sessions_by_date(current_time - 86400)
        data_by_programms = {}
        for row in sessions:
            data_by_programms[row[1]] = data_by_programms.get(row[1], 0) + row[2]
        self.tableWidget.setColumnCount(2)  # Устанавливаем три колонки
        # self.tableWidget.setRowCount(len(data_by_programms))
        self.tableWidget.setHorizontalHeaderLabels(["Программа", "Длительность (мин.)"])
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        for i, row in enumerate(sorted(list(data_by_programms.items()), key=lambda x: x[1], reverse=True)):
            duration = int(row[1] // 60) if row[1] // 60 % 1 == 0 else row[1] // 60
            if duration:

                if self.tableWidget.rowCount() <= i:
                    self.tableWidget.insertRow(self.tableWidget.rowCount())
                self.tableWidget.setItem(i, 0, QTableWidgetItem(row[0]))
                self.tableWidget.setItem(i, 1, QTableWidgetItem(str(duration)))
        self.tableWidget.resizeColumnsToContents()

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

        with open(fileName, 'w') as file:
            file.write('ddddd')


def run_window():
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    listeners.start_all_listener()
    run_window()
