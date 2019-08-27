from db_requester import *


# db = db_requester('http://49.236.136.179:5000')
# print(db.request('request/car', {'id': 'cshyeon'}))

db = db_requester('http://15.164.149.11:5000')
# print(db.request('register/user', {'id': '110169985313641949566', 'name': 'chan', 'token': 'eOWvXXe5FIg:APA91bG56DRSf3ta4Qsb7OGCzsV08613OsqbCMCEiZ5x5WJNl3mB_fU-N90udDa90_g1WIZsALZL8P9pSKGjhcUss8xOAuwlEBHcpy5hA7xyH3MpXHtr1sHAeBary4ZUYHHppuaV0jHv'}))


# 차량에서 넣는 부분
# print(db.request('/update/gps', {'id':'149767337947949', 'lat':37.4993255, 'lon':127.0975084}))
# print(db.request('update/drive', {'id': '149767337947949', 'fuel_efi': 15.3, 'speed': 34}))
# print(db.request('update/record', {'id': '149767337947949', 'start_time': '2019-08-27 15:30:00', 'fuel_efi': 15.45, 'avr_speed': 22, 'hard_rpm': 5, 'hard_break': 6, 'hard_accel': 7, 'score': 77, 'distance': 15.6}))

# App에서 받아오는 부분
# print(db.request('/request/car', {'usr_id': '110169985313641949566'}))
# print(db.request('/request/code', {'usr_id': '110169985313641949566'}))
# print(db.request('/request/position', {'car_id' : '149767337947949', 'start_time' : '2018-01-01 00:00:00', 'end_time' : '2020-01-01 00:00:00'}))
# print(db.request('/request/record', {'usr_id':'110169985313641949566', 'start_date':'2018-09-02', 'end_date':'2018-10-02'}))
# print(db.request('/request/parking', {'usr_id':'110169985313641949566'}))
# print(db.request('/request/record_recent', {'usr_id':'110169985313641949566'}))
# print(db.request('/request/chart', {'usr_id':'110169985313641949566'}))
# print(db.request('/update/car', {'car_id':'149767337947949', 'usr_id':'110169985313641949566', 'car_name':'789', 'volume':'10', 'fuel':'가솔린', 'fuel_efi':"12"}))
# print(db.request('/delete/car', {'car_id':'149767337947949'}));