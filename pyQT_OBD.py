from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui

import time
import obd
import os
import sys
class MyMainGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OBD II info")
        self.setGeometry(0, 0, 480, 320)

        self.lcd_speed = QLCDNumber(self)
        self.lcd_speed.setGeometry(QtCore.QRect(10, 30, 131, 100))
        self.lcd_speed.setObjectName("lcd_speed")
        self.lcd_rpm = QLCDNumber(self)
        self.lcd_rpm.setGeometry(QtCore.QRect(170, 30, 131, 100))
        self.lcd_rpm.setObjectName("lcd_rpm")
        self.lcd_throttle = QLCDNumber(self)
        self.lcd_throttle.setGeometry(QtCore.QRect(330, 30, 131, 100))
        self.lcd_throttle.setObjectName("lcd_Throttle")
        self.lcd_distance = QLCDNumber(self)
        self.lcd_distance.setGeometry(QtCore.QRect(10, 180, 131, 100))
        self.lcd_distance.setObjectName("lcd_distance")
        self.lcd_fuel = QLCDNumber(self)
        self.lcd_fuel.setGeometry(QtCore.QRect(170, 180, 131, 100))
        self.lcd_fuel.setObjectName("lcd_fuel")
        self.lcd_currentfuel = QLCDNumber(self)
        self.lcd_currentfuel.setGeometry(QtCore.QRect(330, 180, 131, 100))
        self.lcd_currentfuel.setObjectName("lcd_currentfuel")
        
        #LCD
        self.label = QLabel(self)
        self.label.setGeometry(QtCore.QRect(10, 10, 90, 20))
        self.label.setObjectName("label")
        self.label.setText("SPD(Km/h)")
        self.label_2 = QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(170, 10, 90, 20))
        self.label_2.setObjectName("label_2")
        self.label_2.setText("RPM")
        self.label_3 = QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(330, 10, 90, 20))
        self.label_3.setObjectName("label_3")
        self.label_3.setText("Throttle(%)")
        self.label_4 = QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(10, 160, 90, 20))
        self.label_4.setObjectName("label_4")
        self.label_4.setText("Dist(Km)")
        self.label_5 = QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(170, 160, 90, 20))
        self.label_5.setObjectName("label_5")
        self.label_5.setText("Oil(L)")
        self.label_6 = QLabel(self)
        self.label_6.setGeometry(QtCore.QRect(330, 160, 90, 20))
        self.label_6.setObjectName("label_6")
        self.label_6.setText("CRF(Km/L)")



        self.th = Worker()
        self.th.change_rpm.connect(self.lcd_rpm.display)
        self.th.change_speed.connect(self.lcd_speed.display)
        self.th.change_distance.connect(self.lcd_distance.display)
        self.th.change_throttle.connect(self.lcd_throttle.display)
        self.th.change_sfuel.connect(self.lcd_currentfuel.display)
        self.th.change_lfuel.connect(self.lcd_fuel.display)
        self.th.start()



class Worker(QThread):
    change_speed = pyqtSignal(int)
    change_rpm = pyqtSignal(int)
    change_distance = pyqtSignal(float)
    change_throttle = pyqtSignal(float)
    change_lfuel = pyqtSignal(float)
    change_sfuel = pyqtSignal(float)

    def __init__(self):
        QThread.__init__(self)
        self.cond = QWaitCondition()
        self.mutex = QMutex()
        self.cnt = 0
        self._status = True


        self.m_rpm = 1
        self.m_vss = 1
        self.m_dis = 0
        self.m_tmp = 1
        self.m_maf = 1
        self.m_map = 1
        self.m_trt = 1

        self.m_cl = 0
        self.m_total_fuel = 0

        print("Setup OBDII Connection.....")
        print("Setup complete!!")

        self.connection = obd.Async()
        self.connection.watch(obd.commands.RPM, callback=self.set_rpm)
        self.connection.watch(obd.commands.SPEED, callback=self.set_speed)
        self.connection.watch(obd.commands.THROTTLE_POS, callback=self.set_throttle)
        self.connection.watch(obd.commands.INTAKE_PRESSURE, callback=self.set_map)
        self.connection.watch(obd.commands.INTAKE_TEMP, callback=self.set_tmp)
        self.connection.start()
    def __del__(self):
        self.wait()

    def set_rpm(self,r):
        if r.value.magnitude == 0:
            self.m_rpm = 0.01
        else:
            self.m_rpm = r.value.magnitude
        self.change_rpm.emit(self.m_rpm)

    def set_speed(self,r):
        self.m_vss = r.value.magnitude
        self.change_speed.emit(self.m_vss)
        self.change_distance.emit(round(self.m_dis,2))

    def set_throttle(self,r):
        self.m_trt = r.value.magnitude
        self.change_throttle.emit(round(self.m_trt,2))

    def set_tmp(self,r):
        self.m_tmp = r.value.magnitude
        self.m_maf = ( self.m_rpm * self.m_map * 34.8 ) / ( self.m_tmp * 1.8 + 32 )
        self.m_cl = (30000 * self.m_vss) / self.m_maf
        
        self.m_total_fuel = self.m_total_fuel + self.m_maf / (14.7 * 0.73*10000000)

        self.change_sfuel.emit(round(self.m_cl,2)) # Current Fuel
        self.change_lfuel.emit(round(self.m_total_fuel,2)) # Total Fuel
        self.change_distance.emit(round(self.m_dis,2))
    def set_map(self,r):
        if r.value.magnitude == 0:
            self.m_map = 0.01
        else:
            self.m_map = r.value.magnitude



    def run(self):
        while True:
            self.m_dis = self.m_dis + (self.m_vss / 3600) # calc m/s
            self.msleep(1000)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyMainGui()
    myWindow.showMaximized()

    app.exec_()

