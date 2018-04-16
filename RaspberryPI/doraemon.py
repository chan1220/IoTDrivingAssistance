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
        MainWindow.resize(800, 450)
        MainWindow.setStyleSheet("QMainWindow{\n"
" background: black;\n"
"}\n"
"\n"
"QWidget{\n"
" background: black;\n"
"}\n"
"QLabel{\n"
" color: white;\n"
"}\n"
"\n"
"QLCDNumber{\n"
" color: white;\n"
" border : 1px solid white;\n"
"}\n"
"QGraphicsView\n"
"{\n"
" border : 1px solid white;\n"
"}\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget_3 = RPMGauge(self.centralwidget)
        self.widget_3.setGeometry(QtCore.QRect(0, 0, 270, 270))
        self.widget_3.setObjectName("widget_3")
        self.widget_2 = SpeedGauge(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(520, 0, 270, 270))
        self.widget_2.setObjectName("widget_2")
        self.lcd_fuel_efi = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd_fuel_efi.setGeometry(QtCore.QRect(410, 20, 100, 100))
        self.lcd_fuel_efi.setObjectName("lcd_fuel_efi")
        self.lcd_distance = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd_distance.setGeometry(QtCore.QRect(280, 160, 100, 100))
        self.lcd_distance.setObjectName("lcd_distance")
        self.lcd_current_fuel = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd_current_fuel.setGeometry(QtCore.QRect(410, 160, 100, 100))
        self.lcd_current_fuel.setObjectName("lcd_current_fuel")
        self.lcd_total_fuel = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd_total_fuel.setGeometry(QtCore.QRect(280, 20, 100, 100))
        self.lcd_total_fuel.setObjectName("lcd_total_fuel")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(280, 0, 100, 12))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(8)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(410, 0, 100, 12))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(8)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(280, 140, 100, 12))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(8)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(410, 140, 100, 12))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(8)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.lcd_hard_accel = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd_hard_accel.setGeometry(QtCore.QRect(20, 290, 100, 100))
        self.lcd_hard_accel.setObjectName("lcd_hard_accel")
        self.lcd_hard_break = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd_hard_break.setGeometry(QtCore.QRect(150, 290, 100, 100))
        self.lcd_hard_break.setObjectName("lcd_hard_break")
        self.lcd_hard_rpm = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd_hard_rpm.setGeometry(QtCore.QRect(280, 290, 100, 100))
        self.lcd_hard_rpm.setObjectName("lcd_hard_rpm")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(20, 270, 100, 12))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(8)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(150, 270, 100, 12))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(8)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(280, 270, 100, 12))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(8)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.lcd_save = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd_save.setGeometry(QtCore.QRect(410, 290, 100, 100))
        self.lcd_save.setObjectName("lcd_save")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(410, 270, 100, 12))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(8)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.lcd_throttle = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcd_throttle.setGeometry(QtCore.QRect(540, 290, 100, 100))
        self.lcd_throttle.setObjectName("lcd_throttle")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(540, 270, 100, 12))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(8)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(670, 270, 100, 12))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(8)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.label_fct = QtWidgets.QLabel(self.centralwidget)
        self.label_fct.setGeometry(QtCore.QRect(670, 290, 100, 100))
        self.label_fct.setStyleSheet("border: 1px solid white;")
        self.label_fct.setText("")
        self.label_fct.setObjectName("label_fct")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
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
        self.label_3.setText(_translate("MainWindow", "기름소모량(L)"))
        self.label_4.setText(_translate("MainWindow", "평균연비(Km/L)"))
        self.label_5.setText(_translate("MainWindow", "주행거리(Km)"))
        self.label_6.setText(_translate("MainWindow", "순간연비(Km/L)"))
        self.label_7.setText(_translate("MainWindow", "급가속"))
        self.label_8.setText(_translate("MainWindow", "급정차"))
        self.label_9.setText(_translate("MainWindow", "고RPM"))
        self.label_10.setText(_translate("MainWindow", "절약거리(Km)"))
        self.label_11.setText(_translate("MainWindow", "쓰로틀 개방(%)"))
        self.label_12.setText(_translate("MainWindow", "퓨얼컷"))

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

