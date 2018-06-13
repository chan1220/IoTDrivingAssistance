from db_requester import *


# db = db_requester('http://49.236.136.179:5000')
# print(db.request('request/car', {'id': 'cshyeon'}))

db = db_requester('http://49.236.136.179:5000')
# print(db.request('register/user', {'id': '0', 'name': 'chan', 'token': '1234'}))


# 차량에서 넣는 부분
# print(db.request('update/gps', {'id': '0', 'lat': '37', 'lon': '38'}))
# print(db.request('update/drive', {'id': 0, 'fuel_efi': 15.3, 'speed': 30}))
# print(db.request('update/record', {'id': '09a7d17fc', 'start_time': '2018-01-01',  'fuel_efi': 15.45, 'avr_speed': 22, 'hard_rpm': 5, 'hard_break': 6, 'hard_accel': 7, 'score': 77, 'distance': 15.6}))

# print(db.request('/request/position', {'id':'09a7d17fc', 'start_time':'2018-04-02 00:00:00', 'end_time':'2018-04-20 00:00:00'}))
# print(db.request('/request/car', {'usr_id': '110169985313641949566'}))
# print(db.request('/request/position', {}))
print(db.request('/request/record', {'usr_id':'110169985313641949566', 'start_date':'2018-05-02', 'end_date':'2018-05-02'}))
# print(db.request('/update/car', {'fuel': 'Gasoline', 'car_name': 'Kalos', 'volume': '1500', 'car_id': '09a7d17fc', 'usr_id': '110169985313641949566', 'fuel_efi': '14.2'}))
# print(db.request('/request/parking', {'usr_id':'110169985313641949566'}))
# print(db.request('/request/record_recent', {'usr_id':'110169985313641949566'}))
# print(db.request('/update/gps', {'id':'09a7d17fc', 'lat':37.3400774, 'lon':126.7331836}))