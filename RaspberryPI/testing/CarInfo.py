import obd
import threading
import time

class CarInfo(threading.Thread):
    def __init__(self, engine_volume=1.5):
        threading.Thread.__init__(self)
        self.volume     = engine_volume     # 배기량

        # OBD Info
        self.rpm        = 1         # RPM
        self.speed      = 0         # 속도(Km/H)
        self.throttle   = 0         # 쓰로틀 개방정도
        self.map        = 1         # 매니폴드 압력(Kpa)
        self.iat        = 0         # 흡기 온도(Intake Air Temp)
        self.is_fct     = False     # Fuel-Cut 여부

        # calced Info
        self.maf        = 1         # Mass Air Flow
        self.ife        = 0         # 순간연비(Instance Fuel Efficiency)(Km/L)
        self.distance   = 0         # 주행거리(Km)
        self.save       = 0         # 관성주행거리(Km)
        self.fuel_use   = 0         # 기름 사용량(L)
        self.eng_stat   = False     # 시동 여부
        self.avr_fuel   = 0         # 평균 연비

        self.prev_speed = 0

        # 주행 습관
        self.hard_break = 0
        self.hard_rpm   = 0
        self.hard_accel = 0

        self.init_connection()

    def run(self):

        while not self.eng_stat:    # 엔진이 가동될때 까지 대기
            print('wait engine start.....')

        start_time = time.time()
        while self.eng_stat:        # 엔진이 가동되는 동안 계산
            print('calculation loop....')
            self.calc_fuel_use()    # 기름소모량
            self.calc_distance()    # 주행거리
            self.calc_hard_accl()   # 급가속 횟수
            self.calc_hard_break()  # 급정차 횟수
            self.calc_hard_rpm()    # 고 RPM 횟수
            time.sleep(1.0 - ((time.time() - start_time) % 1.0))           # 1초 정지

        print('engine stop!!')
        self.release_connection()   # OBD 연결 종료



    def init_connection(self):
        self.connection = obd.Async('/dev/rfcomm0')
        # 해당 값들이 변경될 때 다음의 callback 함수 호출
        self.connection.watch(obd.commands.RPM,             callback=self.set_rpm)
        self.connection.watch(obd.commands.SPEED,           callback=self.set_speed)
        self.connection.watch(obd.commands.THROTTLE_POS,    callback=self.set_throttle)
        self.connection.watch(obd.commands.INTAKE_PRESSURE, callback=self.set_map)
        self.connection.watch(obd.commands.INTAKE_TEMP,     callback=self.set_iat)
        self.connection.watch(obd.commands.FUEL_STATUS,     callback=self.set_fct)
        self.connection.start()

    def release_connection(self):
        self.connection.stop()
        self.connection.unwatch_all()
        self.connection.close()

    def calc_maf(self):     # MAF 계산
        self.maf = 28.97 * (self.volume * ((self.rpm * self.map / (self.iat + 273.15)) / 120)) / 8.314
        if self.maf == 0:
            self.maf = 1
    def calc_instance_fuel_efy(self):   # 순간연비 계산
        self.ife = (14.7 * 6.17 * 454 * 0.621371 * self.speed * 0.425144) / (3600 * self.maf)

    # -------------------- 1초에 1번 호출하는 함수 -----------------------------
    def calc_fuel_use(self):    # 총 기름 소모량 계산(1초에 1번 호출)
        if not self.is_fct:
            self.fuel_use = self.fuel_use + self.maf / (14.7 * 0.73 * 1000)  # 백만

        if self.fuel_use != 0:      # 평균 연비 계산
            self.avr_fuel = self.distance / self.fuel_use

    def calc_distance(self):    # 주행거리 계산(1초에 1번 호출)
        self.distance = self.distance + (self.speed / 3600)  # 이동거리 계산
        if self.is_fct:     # Fuel-Cut이 걸려있는 경우 절약거리를 계산
            self.save = self.save + (self.speed / 3600)

    def calc_hard_break(self):  # 급브레이크 계산 (1초에 1번 호출)
        if (self.speed > 50) & ((self.prev_speed - self.speed) > 10):
            self.hard_break += 1
        self.prev_speed = self.speed

    def calc_hard_accl(self):   # 급가속 계산 (1초에 1번 호출)
        if self.throttle > 40:
            self.hard_accel += 1

    def calc_hard_rpm(self):     # 고알피엠 계산 (1초에 1번 호출)
        if self.rpm > 3000:
            self.hard_rpm += 1
    # ---------------------------------------------------------------------------------

    def set_rpm(self, r):
        if r:
            value = r.value.magnitude
            self.rpm = value
            if self.rpm > 500:
                self.eng_stat = True
            else:
                self.eng_stat = False
            self.calc_maf()
            self.calc_instance_fuel_efy()
        else:
            self.eng_stat = False

    def set_speed(self, r):
        if r:
            value = r.value.magnitude
            self.speed = value
            self.calc_maf()
            self.calc_instance_fuel_efy()
        else:
            self.eng_stat = False

    def set_throttle(self, r):
        if r:
            value = r.value.magnitude
            self.throttle = value
        else:
            self.eng_stat = False

    def set_map(self, r):
        if r:
            value = r.value.magnitude
            self.map = value
            self.calc_maf()
            self.calc_instance_fuel_efy()
        else:
            self.eng_stat = False

    def set_iat(self, r):
        if r:
            value = r.value.magnitude
            self.iat = value
            self.calc_maf()
            self.calc_instance_fuel_efy()
        else:
            self.eng_stat = False

    def set_fct(self, r):
        if r:
            value = r.value
            if "fuel cut" in value[0]:      # 퓨얼컷이 걸렸을때
                self.is_fct = True
            else:
                self.is_fct = False
        else:
            self.eng_stat = False


if __name__ == '__main__':
    car = CarInfo()
    car.start()
    import os
    import datetime
    while True:
        #os.system('clear')
        print('RPM : \t\t',car.rpm)
        print('Speed : \t',car.speed)
        print('Throttle : \t',car.throttle)
        print('Distance : \t',car.distance)
        print('Fuel-Use : \t',car.fuel_use)
        print('Inst Fuel : \t',car.ife)
        print('Fuel-Cut : \t',car.is_fct)
        print('Saving Dist : \t',car.save)

        with open('carlog.txt', 'a') as f:
            f.write('--------{}-------\n'.format(datetime.datetime.now()))
            f.write('RPM : \t\t{}\n'.format(car.rpm))
            f.write('Speed : \t{} Km/H\n'.format(car.speed))
            f.write('Throttle : \t{} %\n'.format(car.throttle))
            f.write('Distance : \t{} Km\n'.format(car.distance))
            f.write('Fuel-Use : \t{} L\n'.format(car.fuel_use))
            f.write('Inst Fuel : \t{} Km/L\n'.format(car.ife))
            f.write('Fuel-Cut : \t{}\n'.format(car.is_fct))
            f.write('Saving Dist : \t{} Km\n\n'.format(car.save))

        time.sleep(1)
