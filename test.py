from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QAbstractItemView
import sys
from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries, QStackedBarSeries, QBarCategoryAxis
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import numpy as np
import time

from DB_module import DB_bot

from test_form import Ui_Form


class MyWidget(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("PyQt BarChart")
        self.setGeometry(100, 100, 680, 900)
        self.show()
        self.c = DB_bot()
        self.buttonRefresh.clicked.connect(self.update)
        self.chartView = None
        self.update()

    def update(self):
        self.update_graph()
        self.update_list()

    def update_graph(self):
        self.verticalLayout.removeWidget(self.chartView)
        low = QBarSet("Сон")
        high = QBarSet("Работа")

        current_time = time.time()
        sessions = self.c.get_sessions_by_date(current_time - 86400)
        sorted_data = {}
        for row in sessions:
            hour = (current_time - row[-1]) / 3600
            if hour % 1 > 0:
                hour = int(hour) + 1
            sorted_data[hour] = sorted_data.get(hour, []) + [row]

        # low << -52 << -50 << -45.3 << -37.0 << -25.6 << -8.0 << -6.0 << -11.8 << -19.7 << -32.8 << -43.0 << -48.0
        for j in range(24):
            if j in sorted_data.keys():
                high.append(sum([i[2] for i in sorted_data[j]]) // 60)
        # high << 11.9 << 12.8 << 18.5 << 26.5 << 32.0 << 34.8 << 38.2 << 34.8 << 29.8 << 20.4 << 15.1 << 11.8

        series = QStackedBarSeries()
        series.append(low)
        series.append(high)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Статистика использования ПК")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        categories = [str(i) for i in range(0, 24)]

        axis = QBarCategoryAxis()
        axis.append(categories)
        axis.setTitleText("Время")
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)
        chart.axisY(series).setRange(-52, 52)
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
        self.tableWidget.setRowCount(len(data_by_programms))
        self.tableWidget.setHorizontalHeaderLabels(["Программа", "Длительность (мин.)"])
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        for i, row in enumerate(sorted(list(data_by_programms.items()), key=lambda x: x[1], reverse=True)):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(row[0]))
            duration = int(row[1] // 60) if row[1] // 60 % 1 == 0 else row[1] // 60
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(duration)))
        self.tableWidget.resizeColumnsToContents()


#
app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec_())
