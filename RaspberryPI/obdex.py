from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal
import obd
import time
import datetime
import gyroex

class obdex(QtCore.QThread):

	on_updated 				= QtCore.pyqtSignal(object)
	on_changed_fuel_use     = QtCore.pyqtSignal(object)
	on_changed_avr_fuel     = QtCore.pyqtSignal(object)
	on_changed_distance     = QtCore.pyqtSignal(object)
	on_changed_save         = QtCore.pyqtSignal(object)
	on_changed_ife          = QtCore.pyqtSignal(object)
	on_changed_hbreak_count = QtCore.pyqtSignal(object)
	on_hard_accel           = QtCore.pyqtSignal(object)
	on_hard_rpm             = QtCore.pyqtSignal(object)
	on_changed_rpm          = QtCore.pyqtSignal(object)
	on_changed_speed        = QtCore.pyqtSignal(object)
	on_changed_throttle     = QtCore.pyqtSignal(object)
	on_changed_fuel_cut     = QtCore.pyqtSignal(object)
	on_drive_terminate 		= QtCore.pyqtSignal(object)
	on_changed_eco_das 		= QtCore.pyqtSignal(object)
	on_changed_dtc 			= QtCore.pyqtSignal(object)

	def __init__(self, parent=None, engine_volume=2.0):
		QtCore.QThread.__init__(self, parent)
		self.gyro 		= gyroex.gyroex()
		self.gyro.on_changed_gyro.connect(self._on_update_eco_das)
		self.enabled	= False

		self.volume     = engine_volume     # 배기량

		# OBD Info
		self.rpm        = 1         # RPM
		self.speed      = 0         # 속도(Km/H)
		self.throttle   = 0         # 쓰로틀 개방정도
		self.map        = 1         # 매니폴드 압력(Kpa) //
		self.iat        = 0         # 흡기 온도(Intake Air Temp) //
		self.is_fct     = False     # Fuel-Cut 여부

		# calced Info
		self.ife        = 0         # 순간연비(Instance Fuel Efficiency)(Km/L)
		self.distance   = 0         # 주행거리(Km)
		self.save       = 0         # 관성주행거리(Km)
		self.fuel_use   = 0         # 기름 사용량(L)
		self.eng_stat   = False     # 시동 여부 //

		self.prev_speed = 0
		self.start_time = datetime.datetime.now()

		# 주행 습관
		self.hard_break = 0
		self.hard_rpm   = 0
		self.hard_accel = 0

		self.is_eco_das = False
	def __del__(self):
		pass

	def stop(self):
		self.enabled = False

	def run(self):
		self.gyro.start()
		self.enabled = True
		try:
			self.connection = obd.Async()
			while not self.connection.is_connected() or not self.connection.status() == obd.OBDStatus.CAR_CONNECTED:
				self.connection.stop()
				print('Connection failed : Wait 5 seconds...')
				time.sleep(5)
				self.connection = obd.Async()
			print('connection success!')

			self.connection.watch(obd.commands.GET_DTC)
			self.connection.start()

			while self.connection.query(obd.commands.GET_DTC).is_null():
				print('Scanning trouble code..')
				time.sleep(1)
			self.on_changed_dtc.emit(self.connection.query(obd.commands.GET_DTC).value)
			
			self.connection.stop()
			self.connection.unwatch(obd.commands.GET_DTC, callback=None)
			self.connection.watch(obd.commands.RPM,             callback=self._on_update_rpm)
			self.connection.watch(obd.commands.SPEED,           callback=self._on_update_speed)
			self.connection.watch(obd.commands.THROTTLE_POS,    callback=self._on_update_throttle)
			self.connection.watch(obd.commands.INTAKE_PRESSURE, callback=self._on_update_map)
			self.connection.watch(obd.commands.INTAKE_TEMP,     callback=self._on_update_iat)
			# self.connection.watch(obd.commands.FUEL_STATUS,     callback=self._on_update_fct)
			self.connection.watch(obd.commands.	FUEL_PRESSURE,  callback=self._on_update_fct)
			self.connection.start()
			
			while not self.eng_stat:
				print('Wait Engine Start...')
				time.sleep(1)
			print('Engine start!')

			begin_time = time.time()
			while self.enabled and self.eng_stat:
				self._update_fuel_use()    # 기름소모량
				self._update_distance()    # 주행거리
				self._update_hard_accl()   # 급가속 횟수
				self._update_hard_break()  # 급정차 횟수
				self._update_hard_rpm()    # 고 RPM 횟수
				self.on_updated.emit(self)
				elapsed_time = time.time() - begin_time
				time.sleep((1 - elapsed_time) % 1)
				begin_time = time.time()

			self.on_drive_terminate.emit(self)
			
			self.connection.stop() # obd connection stop
			self.gyro.stop() # gyro thread stop
			self.connection.unwatch_all()
			print("dirve finished!!")
		except Exception as e:
			print(e)
			enabled = False
	def _get_maf(self):     # MAF 계산
		maf = 28.97 * (self.volume * 0.85 * ((self.rpm * self.map / (self.iat + 273.15)) / 120)) / 8.314
		if maf == 0:
			maf = 0.01
		return maf

	def _update_instance_fuel_efy(self):   # 순간연비 계산
		self.ife = (14.7 * 6.17 * 454 * 0.621371 * self.speed * 0.425144) / (3600 * self._get_maf())
		if self.is_fct:
			self.on_changed_ife.emit(99.9)
		else:
			self.on_changed_ife.emit(self.ife)

	# --- 1초에 한번만 호출되는 함수들 ----
	def _update_fuel_use(self):    # 총 기름 소모량 계산(1초에 1번 호출)
		if self.eng_stat is not True:
			return

		if not self.is_fct:
			self.fuel_use = self.fuel_use + self._get_maf() / (14.7 * 0.73 * 1000)  # 백만
			self.on_changed_fuel_use.emit(self.fuel_use)

		if self.fuel_use != 0:      # 평균 연비 계산
			avr_fuel = self.distance / self.fuel_use
			self.on_changed_avr_fuel.emit(avr_fuel)

	def _update_distance(self):    # 주행거리 계산(1초에 1번 호출)
		if self.eng_stat is not True:
			return

		self.distance = self.distance + (self.speed / 3600)  # 이동거리 계산
		self.on_changed_distance.emit(self.distance)
		if self.is_fct:     # Fuel-Cut이 걸려있는 경우 절약거리를 계산
			self.save = self.save + (self.speed / 3600)
			self.on_changed_save.emit(self.save)

	def _update_hard_break(self):  # 급브레이크 계산 (1초에 1번 호출)
		if self.eng_stat is not True:
			return

		if (self.speed > 50) & ((self.prev_speed - self.speed) > 10):
			self.hard_break += 1
			self.on_changed_hbreak_count.emit(self.hard_break)

		self.prev_speed = self.speed

	def _update_hard_accl(self):   # 급가속 계산 (1초에 1번 호출)
		if self.eng_stat is not True:
			return

		if self.throttle > 40:
			self.hard_accel += 1
			self.on_hard_accel.emit(self.hard_accel)

	def _update_hard_rpm(self):     # 고알피엠 계산 (1초에 1번 호출)
		if self.eng_stat is not True:
			return

		if self.rpm > 3000:
			self.hard_rpm += 1
			self.on_hard_rpm.emit(self.hard_rpm)

	# --- obd.async에 으해 호출되는 함수들 ----
	def _on_update_rpm(self, r):
		if not r.is_null():
			self.rpm = r.value.magnitude
			self.on_changed_rpm.emit(self.rpm)

			self.eng_stat = True if self.rpm > 500 else False
			if self.eng_stat is False:
				self.enabled = False

			self._update_instance_fuel_efy()
		else:
			self.eng_stat = not self.connection.query(obd.commands.RPM).is_null()

	def _on_update_speed(self, r):
		if not r.is_null():
			self.speed = r.value.magnitude
			self.on_changed_speed.emit(self.speed)
			self._update_instance_fuel_efy()
		else:
			pass

	def _on_update_throttle(self, r):
		if not r.is_null():
			self.throttle = r.value.magnitude
			self.on_changed_throttle.emit(self.throttle)
		else:
			pass

	def _on_update_map(self, r):
		if not r.is_null():
			self.map = r.value.magnitude
			self._update_instance_fuel_efy()
		else:
			pass

	def _on_update_iat(self, r):
		if not r.is_null():
			self.iat = r.value.magnitude
			self._update_instance_fuel_efy()
		else:
			pass

	# Real Car 
	# def _on_update_fct(self, r):
	# 	if not r.is_null():
	# 		current_fct = True if 'fuel cut' in r.value[0] else False
	# 		if self.is_fct is not current_fct:
	# 			self.on_changed_fuel_cut.emit(current_fct)
	# 			self.is_fct = current_fct
		# else:
		# 	self.eng_stat = False

	# Simulation
	def _on_update_fct(self, r):
		if not r.is_null():
			current_fct = True if r.value.magnitude < 50 else False
			if self.is_fct is not current_fct:
				self.on_changed_fuel_cut.emit(current_fct)
				self.is_fct = current_fct
		else:
			pass

	def _on_update_eco_das(self, r):
		current_eco_das = True if r > 30 and self.speed > 40 and self.rpm > 2000 else False
		if self.is_eco_das is not current_eco_das:
			self.on_changed_eco_das.emit(current_eco_das)
			self.is_eco_das = current_eco_das
