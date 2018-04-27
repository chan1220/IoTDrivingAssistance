from db_requester import *


# db = db_requester('http://49.236.136.179:5000')
# print(db.request('request/car', {'id': 'cshyeon'}))


db = db_requester('http://49.236.136.179:5000')
#print(db.request('register/user', {'id': '0', 'name': 'chan', 'token': '1234'}))


# 차량에서 넣는 부분
# print(db.request('update/gps', {'id': '0', 'lat': '37', 'lon': '38'}))
# print(db.request('update/drive', {'id': 0, 'fuel_efi': 15.3, 'speed': 30}))
# print(db.request('update/record', {'id': '123', 'start_time': '2018-01-01',  'fuel_efi': 15.4, 'avr_speed': 22, 'hard_rpm': 5, 'hard_break': 6, 'hard_accel': 7, 'score': 77, 'distance': 15.6}))

print(db.request('/request/position', {'id':'09a7d17fc', 'start_time':'2018-04-02 00:00:00', 'end_time':'2018-04-20 00:00:00'}))
# print(db.request('/request/car', {}))
# print(db.request('/request/position', {}))