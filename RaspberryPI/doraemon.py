# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'doraemon.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 480)
        MainWindow.setStyleSheet("QMainWindow\n"
"{\n"
" background-image : url(bg.jpg);\n"
"}\n"
"QLabel{\n"
" color: white;\n"
"}\n"
"\n"
"QLCDNumber{\n"
" color: white;\n"
"\n"
"}\n"
"QGraphicsView\n"
"{\n"
" border : 1px solid white;\n"
"}\n"
"\n"
"\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget_5 = QtWidgets.QWidget(self.centralwidget)
        self.widget_5.setGeometry(QtCore.QRect(10, 10, 390, 420))
        self.widget_5.setStyleSheet("background: rgb(39, 41, 43);\n"
"border-radius: 15px;\n"
"border : 1px solid black;\n"
"")
        self.widget_5.setObjectName("widget_5")
        self.widget_6 = QtWidgets.QWidget(self.widget_5)
        self.widget_6.setGeometry(QtCore.QRect(0, 300, 385, 100))
        self.widget_6.setStyleSheet("border-radius: 0px;\n"
"border : solid ;\n"
"")
        self.widget_6.setObjectName("widget_6")
        self.LCD_save_distance = QtWidgets.QLCDNumber(self.widget_6)
        self.LCD_save_distance.setGeometry(QtCore.QRect(0, 35, 190, 50))
        self.LCD_save_distance.setObjectName("LCD_save_distance")
        self.label_15 = QtWidgets.QLabel(self.widget_6)
        self.label_15.setGeometry(QtCore.QRect(10, 0, 180, 20))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(8)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("border-top: 1px solid white;")
        self.label_15.setObjectName("label_15")
        self.LCD_hard_accel = QtWidgets.QLCDNumber(self.widget_6)
        self.LCD_hard_accel.setGeometry(QtCore.QRect(270, 0, 110, 50))
        self.LCD_hard_accel.setStyleSheet("border-bottom: 1px solid white;\n"
"border-top: 1px solid white;")
        self.LCD_hard_accel.setObjectName("LCD_hard_accel")
        self.label_16 = QtWidgets.QLabel(self.widget_6)
        self.label_16.setGeometry(QtCore.QRect(200, 0, 70, 50))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(8)
        self.label_16.setFont(font)
        self.label_16.setStyleSheet("border-left: 1px solid white;\n"
"border-bottom: 1px solid white;\n"
"border-top: 1px solid white;")
        self.label_16.setObjectName("label_16")
        self.LCD_hard_break = QtWidgets.QLCDNumber(self.widget_6)
        self.LCD_hard_break.setGeometry(QtCore.QRect(270, 50, 110, 50))
        self.LCD_hard_break.setObjectName("LCD_hard_break")
        self.label_17 = QtWidgets.QLabel(self.widget_6)
        self.label_17.setGeometry(QtCore.QRect(200, 50, 70, 50))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(8)
        self.label_17.setFont(font)
        self.label_17.setStyleSheet("border-left: 1px solid white;\n"
"")
        self.label_17.setObjectName("label_17")
        self.widget_7 = QtWidgets.QWidget(self.widget_5)
        self.widget_7.setGeometry(QtCore.QRect(0, 200, 385, 100))
        self.widget_7.setStyleSheet("border-radius: 0px;\n"
"border : solid ;\n"
"")
        self.widget_7.setObjectName("widget_7")
        self.label_18 = QtWidgets.QLabel(self.widget_7)
        self.label_18.setGeometry(QtCore.QRect(200, 0, 70, 50))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(8)
        self.label_18.setFont(font)
        self.label_18.setStyleSheet("border-left: 1px solid white;\n"
"border-bottom: 1px solid white;")
        self.label_18.setObjectName("label_18")
        self.LCD_distance = QtWidgets.QLCDNumber(self.widget_7)
        self.LCD_distance.setGeometry(QtCore.QRect(270, 0, 110, 50))
        self.LCD_distance.setStyleSheet("border-bottom: 1px solid white;\n"
"")
        self.LCD_distance.setObjectName("LCD_distance")
        self.LCD_total_fuel = QtWidgets.QLCDNumber(self.widget_7)
        self.LCD_total_fuel.setGeometry(QtCore.QRect(270, 50, 110, 50))
        self.LCD_total_fuel.setStyleSheet("")
        self.LCD_total_fuel.setObjectName("LCD_total_fuel")
        self.label_19 = QtWidgets.QLabel(self.widget_7)
        self.label_19.setGeometry(QtCore.QRect(200, 50, 70, 50))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(8)
        self.label_19.setFont(font)
        self.label_19.setStyleSheet("border-left: 1px solid white;")
        self.label_19.setObjectName("label_19")
        self.LCD_fuel_price = QtWidgets.QLCDNumber(self.widget_7)
        self.LCD_fuel_price.setGeometry(QtCore.QRect(0, 35, 190, 50))
        self.LCD_fuel_price.setObjectName("LCD_fuel_price")
        self.label_20 = QtWidgets.QLabel(self.widget_7)
        self.label_20.setGeometry(QtCore.QRect(10, 0, 100, 20))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(8)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.cf_wraper = QtWidgets.QWidget(self.widget_5)
        self.cf_wraper.setGeometry(QtCore.QRect(2, 10, 385, 85))
        self.cf_wraper.setStyleSheet("background: white;\n"
"border-radius: 15px;\n"
"border : 1px solid white;\n"
"")
        self.cf_wraper.setObjectName("cf_wraper")
        self.GAUGE_current_fuel = CuFEFGauge(self.cf_wraper)
        self.GAUGE_current_fuel.setGeometry(QtCore.QRect(0, 0, 385, 85))
        self.GAUGE_current_fuel.setStyleSheet("")
        self.GAUGE_current_fuel.setObjectName("GAUGE_current_fuel")
        self.label_eco = QtWidgets.QLabel(self.GAUGE_current_fuel)
        self.label_eco.setGeometry(QtCore.QRect(125, 5, 40, 40))
        self.label_eco.setText("")
        self.label_eco.setObjectName("label_eco")
        self.av_wraper = QtWidgets.QWidget(self.widget_5)
        self.av_wraper.setGeometry(QtCore.QRect(2, 100, 385, 85))
        self.av_wraper.setStyleSheet("background: white;\n"
"border-radius: 15px;\n"
"border : 1px solid white;\n"
"")
        self.av_wraper.setObjectName("av_wraper")
        self.GAUGE_average_fuel = AvFEFGauge(self.av_wraper)
        self.GAUGE_average_fuel.setGeometry(QtCore.QRect(0, 0, 385, 85))
        self.GAUGE_average_fuel.setStyleSheet("")
        self.GAUGE_average_fuel.setObjectName("GAUGE_average_fuel")
        self.widget_8 = QtWidgets.QWidget(self.centralwidget)
        self.widget_8.setGeometry(QtCore.QRect(410, 10, 385, 420))
        self.widget_8.setStyleSheet("background: rgb(39, 41, 43);\n"
"border-radius: 15px;\n"
"border : 1px solid black;\n"
"")
        self.widget_8.setObjectName("widget_8")
        self.GAUGE_rpm = RPMGauge(self.widget_8)
        self.GAUGE_rpm.setGeometry(QtCore.QRect(60, 0, 271, 191))
        self.GAUGE_rpm.setStyleSheet("border: rgb(39, 41, 43);")
        self.GAUGE_rpm.setObjectName("GAUGE_rpm")
        self.button_next = QtWidgets.QPushButton(self.widget_8)
        self.button_next.setGeometry(QtCore.QRect(320, 20, 40, 20))
        self.button_next.setStyleSheet("color: white;\n"
"border: 1px solid white")
        self.button_next.setObjectName("button_next")
        self.GAUGE_SPEED = SpeedGauge(self.widget_8)
        self.GAUGE_SPEED.setGeometry(QtCore.QRect(0, 180, 381, 251))
        self.GAUGE_SPEED.setStyleSheet("border: rgb(39, 41, 43);")
        self.GAUGE_SPEED.setObjectName("GAUGE_SPEED")
        self.button_prev = QtWidgets.QPushButton(self.widget_8)
        self.button_prev.setGeometry(QtCore.QRect(20, 20, 40, 20))
        self.button_prev.setStyleSheet("color: white;\n"
"border: 1px solid white")
        self.button_prev.setObjectName("button_prev")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "도라에몽"))
        self.label_15.setText(_translate("MainWindow", "절약거리(Km)"))
        self.label_16.setText(_translate("MainWindow", "급가속"))
        self.label_17.setText(_translate("MainWindow", "급정차"))
        self.label_18.setText(_translate("MainWindow", "주행거리(Km)"))
        self.label_19.setText(_translate("MainWindow", "기름소모량(L)"))
        self.label_20.setText(_translate("MainWindow", "사용 유류비(원)"))
        self.button_next.setText(_translate("MainWindow", "Next"))
        self.button_prev.setText(_translate("MainWindow", "Prev"))

from AvFEFGauge import AvFEFGauge
from CuFEFGauge import CuFEFGauge
from RPMGauge import RPMGauge
from SpeedGauge import SpeedGauge

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

