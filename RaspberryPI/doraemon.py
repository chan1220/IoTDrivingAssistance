# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'doraemon.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
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
        self.widget_5.setGeometry(QtCore.QRect(10, 10, 390, 460))
        self.widget_5.setStyleSheet("QWidget#widget_5{\n"
"background: rgb(39, 41, 43);\n"
"border-radius: 15px;\n"
"border : 1px solid black;\n"
"}")
        self.widget_5.setObjectName("widget_5")
        self.widget_6 = QtWidgets.QWidget(self.widget_5)
        self.widget_6.setGeometry(QtCore.QRect(0, 340, 385, 100))
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
        self.widget_7.setGeometry(QtCore.QRect(0, 240, 385, 100))
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
        self.cf_wraper.setGeometry(QtCore.QRect(2, 50, 385, 85))
        self.cf_wraper.setStyleSheet("background: white;\n"
"border-top-left-radius: 15px;\n"
"border-top-right-radius: 15px;\n"
"border : 1px solid white;\n"
"")
        self.cf_wraper.setObjectName("cf_wraper")
        self.GAUGE_current_fuel = CuFEFGauge(self.cf_wraper)
        self.GAUGE_current_fuel.setGeometry(QtCore.QRect(0, 0, 385, 85))
        self.GAUGE_current_fuel.setStyleSheet("")
        self.GAUGE_current_fuel.setObjectName("GAUGE_current_fuel")
        self.av_wraper = QtWidgets.QWidget(self.widget_5)
        self.av_wraper.setGeometry(QtCore.QRect(2, 140, 385, 85))
        self.av_wraper.setStyleSheet("background: white;\n"
"border-bottom-left-radius: 15px;\n"
"border-bottom-right-radius: 15px;\n"
"border : 1px solid white;")
        self.av_wraper.setObjectName("av_wraper")
        self.GAUGE_average_fuel = AvFEFGauge(self.av_wraper)
        self.GAUGE_average_fuel.setGeometry(QtCore.QRect(0, 0, 385, 85))
        self.GAUGE_average_fuel.setStyleSheet("")
        self.GAUGE_average_fuel.setObjectName("GAUGE_average_fuel")
        self.label_temperature_img = QtWidgets.QLabel(self.widget_5)
        self.label_temperature_img.setGeometry(QtCore.QRect(10, 10, 35, 35))
        self.label_temperature_img.setText("")
        self.label_temperature_img.setPixmap(QtGui.QPixmap("temperature.png"))
        self.label_temperature_img.setObjectName("label_temperature_img")
        self.label_humidity_img = QtWidgets.QLabel(self.widget_5)
        self.label_humidity_img.setGeometry(QtCore.QRect(142, 10, 35, 35))
        self.label_humidity_img.setText("")
        self.label_humidity_img.setPixmap(QtGui.QPixmap("humidity.png"))
        self.label_humidity_img.setObjectName("label_humidity_img")
        self.label_temperature = QtWidgets.QLabel(self.widget_5)
        self.label_temperature.setGeometry(QtCore.QRect(40, 15, 75, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_temperature.setFont(font)
        self.label_temperature.setStyleSheet("QLabel#label_temperature{\n"
"background-color: rgb(91, 146, 174);\n"
"border-top-right-radius: 10px;\n"
"border-bottom-right-radius: 10px;\n"
"}")
        self.label_temperature.setAlignment(QtCore.Qt.AlignCenter)
        self.label_temperature.setObjectName("label_temperature")
        self.label_humidity = QtWidgets.QLabel(self.widget_5)
        self.label_humidity.setGeometry(QtCore.QRect(172, 15, 75, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_humidity.setFont(font)
        self.label_humidity.setStyleSheet("QLabel#label_humidity{\n"
"background-color: rgb(91, 146, 174);\n"
"border-top-right-radius: 10px;\n"
"border-bottom-right-radius: 10px;\n"
"}")
        self.label_humidity.setAlignment(QtCore.Qt.AlignCenter)
        self.label_humidity.setObjectName("label_humidity")
        self.label_CO2_img = QtWidgets.QLabel(self.widget_5)
        self.label_CO2_img.setGeometry(QtCore.QRect(275, 10, 35, 35))
        self.label_CO2_img.setText("")
        self.label_CO2_img.setPixmap(QtGui.QPixmap("CO2.png"))
        self.label_CO2_img.setObjectName("label_CO2_img")
        self.label_CO2 = QtWidgets.QLabel(self.widget_5)
        self.label_CO2.setGeometry(QtCore.QRect(305, 15, 75, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_CO2.setFont(font)
        self.label_CO2.setStyleSheet("QLabel#label_CO2{\n"
"background-color: rgb(91, 146, 174);\n"
"border-top-right-radius: 10px;\n"
"border-bottom-right-radius: 10px;\n"
"}")
        self.label_CO2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_CO2.setObjectName("label_CO2")
        self.widget_6.raise_()
        self.widget_7.raise_()
        self.cf_wraper.raise_()
        self.av_wraper.raise_()
        self.label_temperature.raise_()
        self.label_temperature_img.raise_()
        self.label_humidity.raise_()
        self.label_humidity_img.raise_()
        self.label_CO2.raise_()
        self.label_CO2_img.raise_()
        self.widget_8 = QtWidgets.QWidget(self.centralwidget)
        self.widget_8.setGeometry(QtCore.QRect(410, 10, 385, 460))
        self.widget_8.setStyleSheet("QWidget#widget_8{\n"
"    background: rgb(39, 41, 43);\n"
"    border-radius: 15px;\n"
"    border : 1px solid black;\n"
"}")
        self.widget_8.setObjectName("widget_8")
        self.label_stt = QtWidgets.QLabel(self.widget_8)
        self.label_stt.setGeometry(QtCore.QRect(70, 40, 290, 180))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_stt.setFont(font)
        self.label_stt.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_stt.setWordWrap(True)
        self.label_stt.setObjectName("label_stt")
        self.label_tts = QtWidgets.QLabel(self.widget_8)
        self.label_tts.setGeometry(QtCore.QRect(20, 210, 290, 180))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_tts.setFont(font)
        self.label_tts.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_tts.setWordWrap(True)
        self.label_tts.setObjectName("label_tts")
        self.gaugewidget = GaugeWidget(self.widget_8)
        self.gaugewidget.setGeometry(QtCore.QRect(0, 0, 385, 420))
        self.gaugewidget.setObjectName("gaugewidget")
        self.diagnosticwidget = DiagnosticWidget(self.widget_8)
        self.diagnosticwidget.setGeometry(QtCore.QRect(-1, -1, 385, 420))
        self.diagnosticwidget.setStyleSheet("color: rgb(100, 100, 100);")
        self.diagnosticwidget.setObjectName("diagnosticwidget")
        self.weatherwidget = WeatherWidget(self.widget_8)
        self.weatherwidget.setGeometry(QtCore.QRect(-1, -1, 385, 420))
        self.weatherwidget.setObjectName("weatherwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

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
        self.label_temperature.setText(_translate("MainWindow", "999"))
        self.label_humidity.setText(_translate("MainWindow", "100"))
        self.label_CO2.setText(_translate("MainWindow", "100"))
        self.label_stt.setText(_translate("MainWindow", "..."))
        self.label_tts.setText(_translate("MainWindow", "..."))

from widget.diagnostic.DiagnosticWidget import DiagnosticWidget
from widget.gauge.AvFEFGauge import AvFEFGauge
from widget.gauge.CuFEFGauge import CuFEFGauge
from widget.gauge.GaugeWidget import GaugeWidget
from widget.weather.WeatherWidget import WeatherWidget

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

