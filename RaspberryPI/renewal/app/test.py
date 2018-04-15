from db_requester import *


# db = db_requester('http://49.236.136.179:5000')
# print(db.request('request/car', {'id': 'cshyeon'}))


db = db_requester('http://49.236.136.179:5000')
print(db.request('register/user', {'id': '0', 'name': 'cshyeon', 'token': '1234'}))