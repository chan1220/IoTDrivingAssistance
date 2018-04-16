from db_requester import *


# db = db_requester('http://49.236.136.179:5000')
# print(db.request('request/car', {'id': 'cshyeon'}))


db = db_requester('http://49.236.136.179:5000')
#print(db.request('register/user', {'id': '0', 'name': 'chan', 'token': '1234'}))
print(db.request('update/gps', {'id': '0', 'lat': '37', 'lon': '38'}))
print(db.request('update/drive', {'id': 0, 'fuel_efi': 15.3, 'speed': 30}))