# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test_form.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(768, 690)
        font = QtGui.QFont()
        font.setFamily("Mongolian Baiti")
        Form.setFont(font)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 741, 261))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.graph_layout = QtWidgets.QVBoxLayout()
        self.graph_layout.setObjectName("graph_layout")
        self.verticalLayout.addLayout(self.graph_layout)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(500, 290, 191, 31))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(10)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(94, 207, 255);\n"
"color: white;\n"
"font: 81 11pt \"Open Sans\";\n"
" border-radius: 50px;\n"
"")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("profits.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(16, 16))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(90, 290, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.buttonRefresh = QtWidgets.QPushButton(Form)
        self.buttonRefresh.setGeometry(QtCore.QRect(20, 290, 51, 23))
        self.buttonRefresh.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.buttonRefresh.setIcon(icon1)
        self.buttonRefresh.setObjectName("buttonRefresh")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(10, 340, 741, 192))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Form)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 560, 741, 111))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 540, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 320, 141, 16))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Другая статистика"))
        self.pushButton_2.setText(_translate("Form", "Экспорт"))
        self.label.setText(_translate("Form", "Лог"))
        self.label_2.setText(_translate("Form", "Все время использования"))
