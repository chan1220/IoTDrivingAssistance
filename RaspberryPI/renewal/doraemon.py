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
        MainWindow.resize(826, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 801, 281))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_3 = RPMGauge(self.horizontalLayoutWidget)
        self.widget_3.setObjectName("widget_3")
        self.label = QtWidgets.QLabel(self.widget_3)
        self.label.setGeometry(QtCore.QRect(20, 20, 64, 15))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.widget_3)
        self.widget_2 = SpeedGauge(self.horizontalLayoutWidget)
        self.widget_2.setObjectName("widget_2")
        self.label_2 = QtWidgets.QLabel(self.widget_2)
        self.label_2.setGeometry(QtCore.QRect(40, 10, 64, 15))
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.widget_2)
        self.widget = FEFGauge(self.horizontalLayoutWidget)
        self.widget.setObjectName("widget")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(20, 20, 64, 15))
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.widget)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 280, 801, 271))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lcd_distance = QtWidgets.QLCDNumber(self.horizontalLayoutWidget_2)
        self.lcd_distance.setObjectName("lcd_distance")
        self.horizontalLayout_2.addWidget(self.lcd_distance)
        self.lcd_current_fuel = QtWidgets.QLCDNumber(self.horizontalLayoutWidget_2)
        self.lcd_current_fuel.setObjectName("lcd_current_fuel")
        self.horizontalLayout_2.addWidget(self.lcd_current_fuel)
        self.lcd_total_fuel = QtWidgets.QLCDNumber(self.horizontalLayoutWidget_2)
        self.lcd_total_fuel.setObjectName("lcd_total_fuel")
        self.horizontalLayout_2.addWidget(self.lcd_total_fuel)
        self.lcd_fuel_efi = QtWidgets.QLCDNumber(self.horizontalLayoutWidget_2)
        self.lcd_fuel_efi.setObjectName("lcd_fuel_efi")
        self.horizontalLayout_2.addWidget(self.lcd_fuel_efi)
        self.label_4 = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 826, 21))
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
        self.label.setText(_translate("MainWindow", "테스트"))
        self.label_2.setText(_translate("MainWindow", "테스트"))
        self.label_3.setText(_translate("MainWindow", "테스트"))
        self.label_4.setText(_translate("MainWindow", "TextLabel"))

from FEFGauge import FEFGauge
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

