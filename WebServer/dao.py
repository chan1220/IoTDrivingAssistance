from flask import Flask
from flask_mysqldb import MySQL
import datetime


class dao(MySQL):
	def __init__(self, app, host='localhost', port=3306, uname='root', upw='doraemon', dbname='doraemon'):
		app.config['MYSQL_HOST'] = host
		app.config['MYSQL_PORT'] = port
		app.config['MYSQL_DB']   = dbname
		app.config['MYSQL_USER'] = uname
		app.config['MYSQL_PASSWORD'] = upw
		MySQL.__init__(self, app)

	def get_position(self, id, start_time, end_time):
		cursor = self.connection.cursor()
		cursor.execute('''SELECT * FROM position WHERE car_id=%s and pos_time between %s and %s''', (id, start_time, end_time))

		data = []
		for element in cursor.fetchall():
			data.append({'id': element[0], 'datetime': str(element[1]), 'lat': element[2], 'lon': element[3]})

		return data
		

	def get_parking(self, usr_id):
		cursor = self.connection.cursor()
		cursor.execute('''SELECT car.car_id, car.car_name,position.pos_time, position.pos_x, position.pos_y FROM car,position where USR_ID = %s order by pos_time desc limit 1''', (usr_id,))

		data = []
		for element in cursor.fetchall():
			data.append({'car_id': element[0], 'car_name': element[1], 'pos_time': str(element[2]), 'pos_x': element[3], 'pos_y': element[4]})

		return data

			
	def get_drive(self, car_id, start_time, end_time):
		cursor = self.connection.cursor()
		cursor.execute("SELECT * FROM drive where car_id = %s and pos_time between %s and %s",(car_id, start_time, end_time))

		data = []
		for element in cursor.fetchall():
			data.append({'fuel_efi': element[2], 'speed': element[3]}) # 'datetime': str(element[1]), 

		return data
		
			

	def add_position(self, id, lat, lon):
		cursor = self.connection.cursor()
		cursor.execute('''INSERT INTO position (car_id, pos_time, pos_x, pos_y) VALUES(%s, now(), %s, %s)''', (id, lat, lon))
		self.connection.commit()
		return {'id': id, 'position': {'lat': lat, 'lon': lon}}
		


	def add_drive(self, id, fuel_efi, speed):
		cursor = self.connection.cursor()
		cursor.execute('''INSERT INTO drive (car_id, pos_time, fuel_efi, speed) VALUES(%s, now(), %s, %s)''', (id, fuel_efi, speed))
		self.connection.commit()
		return {'id': id, 'fuel_efi': fuel_efi, 'speed': speed}
		
	def add_record(self, id, start_time, fuel_efi, avr_speed, hard_rpm, hard_break, hard_accel, score, distance):
		cursor = self.connection.cursor()
		cursor.execute('''INSERT INTO record (car_id, start_time, fuel_efi, speed, rpm, brk_num, acl_num, score, distance, end_time) VALUES(%s, %s, %s, %s, %s, %s ,%s, %s, %s, now())''', (id, start_time, fuel_efi, avr_speed, hard_rpm, hard_break, hard_accel, score, distance))
		self.connection.commit()
		return {'car_id': id, 'start_time': start_time,  'fuel_efi': fuel_efi, 'avr_speed': avr_speed, 'hard_rpm': hard_rpm, 'hard_break': hard_break, 'hard_accel': hard_accel, 'score': score, 'distance': distance}


	def set_car(self, car_id, usr_id, car_name, volume, fuel, fuel_efi):
		query = '''
				INSERT INTO car (car_id, usr_id, car_name, volume, fuel, fuel_efi)
				VALUES ('{car_id}', '{usr_id}', '{car_name}', '{volume}', '{fuel}', '{fuel_efi}')
				ON DUPLICATE KEY UPDATE
				car_name = '{car_name}',
				volume = '{volume}',
				fuel = '{fuel}',
				fuel_efi = '{fuel_efi}'
				'''.format(car_id=car_id, usr_id=usr_id, car_name=car_name, volume=volume, fuel=fuel, fuel_efi=fuel_efi)
		cursor = self.connection.cursor()
		cursor.execute(query);
		self.connection.commit()
		return self.get_car(usr_id)

		

	def get_car(self, usr_id):
		cursor = self.connection.cursor()
		cursor.execute("SELECT * FROM car WHERE usr_id LIKE %s", (usr_id,))

		data = []
		for element in cursor.fetchall():
			data.append({'car_id': element[0], 'usr_id': str(element[1]), 'car_name': element[2], 'volume': element[3], 'fuel': element[4], 'fuel_efi': element[5]})

		return data
		

	def register_user(self, id, name, token):
		query = '''
				INSERT INTO users (usr_id, usr_name, token)
				VALUES ('{id}', '{name}', '{token}')
				ON DUPLICATE KEY UPDATE
				usr_name = '{name}',
				token = '{token}'
				'''.format(id=id, name=name, token=token)
		cursor = self.connection.cursor()
		cursor.execute(query);
		self.connection.commit()

		return self.get_user(id)
		

	def get_user(self, id):
		cursor = self.connection.cursor()
		cursor.execute('''SELECT * FROM users WHERE usr_id LIKE %s''', (id,))
		data = cursor.fetchone()
		return {'id': data[0], 'name': data[1], 'token': data[2]}
		
		
	def get_record(self, id, start_date, end_date):
		cursor = self.connection.cursor()
		cursor.execute("SELECT record.car_id, record.start_time, record.end_time, record.fuel_efi, record.speed, record.rpm, record.brk_num, record.acl_num, record.score, record.distance FROM car,record WHERE USR_ID=%s and START_TIME between %s and %s",(id, start_date + " 00:00:00", end_date + " 23:59:59") )
		data = []
		for element in cursor.fetchall():
			data.append({'car_id': element[0], 'start_time': str(element[1]), 'end_time': str(element[2]), 'fuel_efi': str(element[3]), 'speed': element[4], 'rpm': element[5], 'brk_num': element[6], 'acl_num': element[7], 'score': element[8], 'distance': element[9], 'position': self.get_position(element[0], str(element[1]), str(element[2])), 'drive': self.get_drive(element[0], str(element[1]), str(element[2]))})

		return data


	def get_record_recent(self, id):
		cursor = self.connection.cursor()
		cursor.execute("SELECT record.car_id, record.start_time, record.end_time, record.fuel_efi, record.speed, record.rpm, record.brk_num, record.acl_num, record.score, record.distance FROM car,record WHERE USR_ID=%s order by record.start_time desc limit 1",(id,) )
		data = []
		for element in cursor.fetchall():
			data.append({'car_id': element[0], 'start_time': str(element[1]), 'end_time': str(element[2]), 'fuel_efi': str(element[3]), 'speed': element[4], 'rpm': element[5], 'brk_num': element[6], 'acl_num': element[7], 'score': element[8], 'distance': element[9], 'position':self.get_position(element[0], str(element[1]), str(element[2]))})

		return data

	def get_token_by_carid(self, car_id):
		cursor = self.connection.cursor()
		cursor.execute("SELECT users.token FROM users RIGHT OUTER JOIN car ON users.usr_id = car.usr_id WHERE car.car_id LIKE %s", (car_id, ))
		data = cursor.fetchone()
		return data[0]