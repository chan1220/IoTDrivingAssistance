from PyQt5 import QtCore, QtGui, QtWidgets
from doraemon import *
from sensor import sensor


#
# 이벤트 핸들러의 파라미터 이름 바꾸기
# gps의 on_changed_gps에 연결한 mainform의 이벤트랑, sensor.py에서 연결한 이벤트가 둘 다 호출이 되는지 확인
# qtdesigner를 이용해서 디자인 원래 구성했던대로 설정
#

class mainform(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.setupUi(self)
		self.retranslateUi(self)
		self.sensor = sensor(self)
		self.sensor.obd.on_changed_fuel_use.connect(self.on_changed_fuel_use)
		self.sensor.obd.on_changed_avr_fuel.connect(self.on_changed_avr_fuel)
		self.sensor.obd.on_changed_distance.connect(self.on_changed_distance)
		self.sensor.obd.on_changed_save.connect(self.on_changed_save)
		self.sensor.obd.on_changed_ife.connect(self.on_changed_ife)
		self.sensor.obd.on_changed_hbreak_count.connect(self.on_changed_hbreak_count)
		self.sensor.obd.on_hard_accel.connect(self.on_hard_accel)
		self.sensor.obd.on_hard_rpm.connect(self.on_hard_rpm)
		self.sensor.obd.on_changed_rpm.connect(self.on_changed_rpm)
		self.sensor.obd.on_changed_speed.connect(self.on_changed_speed)
		self.sensor.obd.on_changed_throttle.connect(self.on_changed_throttle)
		self.sensor.obd.on_changed_fuel_cut.connect(self.on_changed_fuel_cut)
		self.sensor.gps.on_changed_gps.connect(self.on_changed_gps)
		self.label_fct.setPixmap(QtGui.QPixmap('fct_off.png').scaled(100, 100))
		self.sensor.start()

	def on_changed_fuel_use(self, a): # 총 기름 사용량
		self.label_fam.setText(str(round(float(a),2)))
		self.label_fpi.setText((round(float(a) * 1550, 2)))

	def on_changed_avr_fuel(self, a): # 평균연비
        pass
		# self.lcd_fuel_efi.display(round(float(a),2))

	def on_changed_distance(self, a): # 주행거리
		self.label_dis.setText(str(round(float(a),2)))

	def on_changed_save(self, a): # 절약거리
		self.label_sdi.setText(str(round(float(a),2)))

	def on_changed_ife(self, a): # 순간연비
		self.gauge_fef.render(round(float(a),2))

	def on_changed_hbreak_count(self, a): #급정차
		self.gauge_window.bstp_cnt.display(int(a))

	def on_hard_accel(self, a):	# 급출발
		self.gauge_window.bspd_cnt.display(int(a))

	def on_hard_rpm(self, a): # 고RPM
        pass
		# self.lcd_hard_rpm.display(int(a))

	def on_changed_rpm(self, a): # RPM
		self.gauge_window.render_rpm(int(a))

	def on_changed_speed(self, a):	# 속도
		self.gauge_window.render_spd(int(a))

	def on_changed_throttle(self, a): # 쓰로틀 개방
        pass
		# self.lcd_throttle.display(round(float(a),2))

	def on_changed_fuel_cut(self, a): # 퓨얼 컷
		if a:
			self.label_fct.setPixmap(QtGui.QPixmap('fct_on.png').scaled(100, 100))
		else:
			self.label_fct.setPixmap(QtGui.QPixmap('fct_off.png').scaled(100, 100))

	def on_changed_gps(self, position):
		print("gps : ",position)

		


if __name__ == '__main__':
	import sys
	app = QtWidgets.QApplication(sys.argv)
	instance = mainform()
	instance.show()
	sys.exit(app.exec_())
