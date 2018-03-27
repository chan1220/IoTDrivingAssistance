# ====== PyQt5 =======
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# ===== Widgets ======
import RPMGauge
import SpeedGauge
import Bar
import FEFGauge
# ====== Control ======
import time
import obd
import os
import sys
import RPi.GPIO as GPIO
import uuid # to get mac addr
import datetime
import pymysql
class MyDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("my Gauge")
        self.setGeometry(0, 0, 800, 450)

        # =============== Widget Init =================         
        self.gauge_rpm = RPMGauge.RPMGauge(self)
        self.gauge_spd = SpeedGauge.SpeedGauge(self)
        self.gauge_trt = Bar.Bar(self)
        self.gauge_dis = QLCDNumber(self)
        self.gauge_fuel = QLCDNumber(self)
        self.gauge_fef = FEFGauge.FEFGauge(self)
        self.gauge_fct = QLabel(self)
        self.gauge_save = QLCDNumber(self)

        # ============== Init Label ===================
        lavel_dis = QLabel(self)
        lavel_fuel = QLabel(self)
        lavel_fct = QLabel(self)
        lavel_save = QLabel(self)
        lavel_dis.setText("DIST(Km)")
        lavel_fuel.setText("FUEL(L)")
        lavel_fct.setText("Fuel-Cut")
        lavel_save.setText("Save(Km)")
        lavel_fuel.setStyleSheet('color: white')
        lavel_dis.setStyleSheet('color: white')
        lavel_fct.setStyleSheet('color: white')
        lavel_save.setStyleSheet('color: white')

        # ================= Widget Position ==============
        self.gauge_rpm.setGeometry(450, 0, 350, 350) # RPM 게이지
        self.gauge_spd.setGeometry(0, 0,350 ,350 ) # 속도게이지
        self.gauge_trt.setGeometry(320, 265,160 ,45 ) # 쓰로틀바디 게이지
        self.gauge_fef.setGeometry(320, 320,160 ,45 ) # 연비 게이지
        lavel_fct.setGeometry(370,180,80,20)
        self.gauge_fct.setGeometry(370,200,60,60) # 퓨얼컷
        self.gauge_fct.setPixmap(QPixmap('fct_on.png').scaled(60,60))
        lavel_dis.setGeometry(30,320,80,20)
        self.gauge_dis.setGeometry(30,340,80,60)
        lavel_fuel.setGeometry(690,320,80,20)
        self.gauge_fuel.setGeometry(690,340,80,60)
        lavel_save.setGeometry(600,320,80,20)
        self.gauge_save.setGeometry(600,340,80,60)
        # ================= Back Color ====================
        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(palette)
        
        
        # ================== Worker ==========================
        self.worker = Worker()
        self.worker.change_rpm.connect(self.gauge_rpm.render)
        self.worker.change_spd.connect(self.gauge_spd.render)
        self.worker.change_dis.connect(self.gauge_dis.display)
        self.worker.change_trt.connect(self.gauge_trt.render)
        self.worker.change_fef.connect(self.gauge_fef.render)
        self.worker.change_fuel.connect(self.gauge_fuel.display)
        self.worker.change_fct.connect(self.set_fct_image)
        self.worker.change_save.connect(self.gauge_save.display)
        self.worker.start()
    # ================= set Fuel-Cut image ============
    def set_fct_image(self,img_path):
            self.gauge_fct.setPixmap(QPixmap(img_path).scaled(60,60))



class Worker(QThread):
    # ======== signal init ============
    change_spd      = pyqtSignal(int)
    change_rpm      = pyqtSignal(int)
    change_dis      = pyqtSignal(float)
    change_trt      = pyqtSignal(float)
    change_fef      = pyqtSignal(float)
    change_fuel     = pyqtSignal(float)
    change_fct      = pyqtSignal(str)
    change_save     = pyqtSignal(float)
    def __init__(self):
        QThread.__init__(self)
        self.cond = QWaitCondition()
        self.mutex = QMutex()
        self.cnt = 0
        self._status = True


        self.m_rpm = 0.0001 # RPM
        self.m_vss = 0.0001 # SPEED
        self.m_dis = 0      # 주행거리
        self.m_tmp = 1      # 흡기온도
        self.m_maf = 1      # 매니폴드 에어플로우
        self.m_map = 1      # 매니폴드 절대압력
        self.m_trt = 1      # 쓰로틀바디 개방정도

        self.m_cl = 0       # 순간연비
        self.m_total_fuel = 0 # 토탈 유류 소비량

        self.m_prev_speed = 0
        # DATABASE
        self.m_startTime = datetime.datetime.now() # 주행 시작 시간
        self.m_endTime = datetime.datetime.now() # 주행 종료 시간

        self.m_break = 0 # 급정차 횟수
        self.m_accel = 0 # 급가속(초)
        self.m_high_rpm = 0 # 고RPM(초)
        self.m_avr_speed = 0 # 평균 주행 속도
        self.m_total_time_sec = 0 # 주행 시간(초)
        self.m_score = 0 # 주행 점수
        self.m_total_time_sec = 0 # 총 주행 시간(초단위)
        self.m_save = 0 # Fuel-Cut으로 절약한 거리
        self.m_isFCT = False # Fuel-Cut 여부
        self.initOBDConnection()


    def __del__(self):
        self.wait()
        #self.connection.close()

    def get_mac(self):
        mac_num = hex(uuid.getnode()).replace('0x', '').upper()
        mac = ':'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
        return mac
    #  ====================== Init OBD Connection ==============================
    def initOBDConnection(self):
        self.connection = obd.Async()
        self.connection.watch(obd.commands.RPM,             callback=self.set_rpm)
        self.connection.watch(obd.commands.SPEED,           callback=self.set_speed)
        self.connection.watch(obd.commands.THROTTLE_POS,    callback=self.set_throttle)
        self.connection.watch(obd.commands.INTAKE_PRESSURE, callback=self.set_map)
        self.connection.watch(obd.commands.INTAKE_TEMP,     callback=self.set_tmp)
        self.connection.watch(obd.commands.FUEL_STATUS,     callback=self.set_fct)
        self.connection.start()

    def endOBDConnection(self):
        self.connection.stop()
        self.connection.unwatch_all()
        self.connection.close()
    # ================== OBD Callback Functions ===========================
    def set_fct(self,r):
        value = r.value
        if "fuel cut" in value[0]:
            GPIO.output(40,True)
            self.m_isFCT = True
            self.change_fct.emit("fct_on.png")
        else:
            GPIO.output(40,False)
            self.m_isFCT = False
            self.change_fct.emit("fct_off.png")
    def set_rpm(self,r):
        value = r.value.magnitude
        if value == 0:
            self.m_rpm = 0.0001
        else:
            self.m_rpm = value
        self.change_rpm.emit(self.m_rpm)

    def set_speed(self,r):
        value = r.value.magnitude
        self.m_vss = value
        self.change_spd.emit(self.m_vss)

    def set_throttle(self,r):
        self.m_trt = r.value.magnitude
        self.change_trt.emit(round(self.m_trt,2))

    def set_tmp(self,r):
        self.m_tmp = r.value.magnitude
        self.m_maf = 28.97 * ( 0.85 * 1.5 * ((self.m_rpm * self.m_map / (self.m_tmp +273.15)) / 120) ) / 8.314
        self.m_cl = (14.7 * 6.17 * 454 * 0.621371 * self.m_vss * 0.425144) / (3600 * self.m_maf)
        self.change_fef.emit(round(self.m_cl,1)) # Current Fuel
        
    def set_map(self,r):
        value = r.value.magnitude
        if value == 0:
            self.m_map = 0.001
        else:
            self.m_map = value

    # ===================== Calc Function(Sec) =============================================
    def calc_fuel(self):
        self.m_total_fuel = self.m_total_fuel + self.m_maf / (14.7 * 0.73 * 1000) # 백만
        self.change_fuel.emit(round(self.m_total_fuel,2)) # Total Fuel

    def calc_dis(self):
        self.m_dis = self.m_dis + (self.m_vss / 3600) # 이동거리 계산
        self.change_dis.emit(round(self.m_dis,2))
        if self.m_isFCT:                                # Fuel-Cut이 걸려있는 경우 절약거리를 계산
            self.m_save = self.m_save + (self.m_vss / 3600)
            self.change_save.emit(round(self.m_save,2))
    # ===================== Calc Driving Score ===============================================
    def calc_hard_break(self): # 속력이 10 이상 감소하면 return 1
        if (self.m_vss > 50) & ((self.m_prev_speed - self.m_vss) > 10):
            self.m_break = self.m_break + 1
        self.m_prev_speed = self.m_vss

    def calc_hard_accl(self): # 쓰로틀이 40% 이상 개방되있으면 급가속
         if self.m_trt > 40:
            self.m_accel = self.m_accel + 1 

    def calc_hard_rpm(self): # RPM이 3000 이상이면 고RPM
        if self.m_rpm > 3000:
            self.m_high_rpm = self.m_high_rpm +1 

    def isEnginStart(self):
        if self.m_rpm > 500:
            return True
        else:
            return False

    def calc_drive_score(self):
        self.m_score = 100 - self.m_break * 5 - self.m_high_rpm *2 - self.m_accel/self.m_total_time_sec * 1000
        if self.m_score < 0:
            self.m_score = 0

    def calc_avr_speed(self):
        self.m_total_time_sec = (self.m_endTime - self.m_startTime).seconds # 주행 경과시간 계산
        print(self.m_total_time_sec)
        self.m_avr_speed = self.m_dis * 3600 / self.m_total_time_sec

    def insertDB(self):
        db = pymysql.connect(host='127.0.0.1', port=3306, user='chan', passwd='kyun3624', db='pidb',charset='utf8',autocommit=True) # DB 개방
        cursor = db.cursor()
        sql_query = "INSERT RECORD VALUES('%s','%s',%lf,%d,%d,%d,%d,%d,%lf,'%s')" %(self.get_mac(), self.m_startTime, self.m_dis/self.m_total_fuel, self.m_avr_speed, self.m_high_rpm, self.m_break, self.m_accel, self.m_score, self.m_dis, self.m_endTime)
        cursor.execute(sql_query)
        db.close()
        print("DB ok")
    # ========================== RUN ====================================================
    def run(self):
        
        while True:
            if self.isEnginStart():
                self.m_startTime = datetime.datetime.now() # 시동시간
                print("Engin start! : " + str(self.m_startTime))
                
                while self.isEnginStart():
                    self.calc_fuel()        # 토탈 기름 소모량 계산
                    self.calc_dis()         # 이동거리 계산
                    self.calc_hard_break()  # 급정차 횟수 계산
                    self.calc_hard_accl()   # 급가속 시간 계산
                    self.calc_hard_rpm()    # 고RPM 시간 계산
        
                    self.msleep(1000)# 1sec

                self.m_endTime = datetime.datetime.now() # 시동 종료 시간

                print("Engin Stop! : " + str(self.m_endTime))
                
                self.calc_avr_speed() # 평속 계산
                self.calc_drive_score() # 주행점수 계산
                self.insertDB() # DB에 데이터 기록
                break
                



if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(40,GPIO.OUT)
    app = QApplication(sys.argv)
    dialog = MyDialog()
    dialog.show()
    app.exec_()
