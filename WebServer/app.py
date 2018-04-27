from flask import Flask, request
from dao import dao
import json

app = Flask(__name__)
model = dao(app)

@app.route('/update/gps', methods=['POST'])
def on_update_gps():
	ret = {'success': True}
	try:
		data = json.loads(request.data.decode('utf-8'))
		ret['data'] = model.add_position(data['id'], data['lat'], data['lon'])
	except Exception as e:
		ret['success'] = False
		ret['error'] = str(e)
	finally:
		return json.dumps(ret)


@app.route('/update/drive', methods=['POST'])
def on_update_drive():
	ret = {'success': True}
	try:
		data = json.loads(request.data.decode('utf-8'))
		ret['data'] = model.add_drive(data['id'], data['fuel_efi'], data['speed'])
	except Exception as e:
		ret['success'] = False
		ret['error'] = str(e)
	finally:
		return json.dumps(ret)


@app.route('/update/car', methods=['POST'])
def on_update_car():
	ret = {'success': True}
	try:
		data = json.loads(request.data.decode('utf-8'))
		ret['data'] = model.set_car(data['id'], data['uid'], data['cname'], data['volume'], data['fuel'], data['fuel_efi'])
	except Exception as e:
		ret['success'] = False
		ret['error'] = str(e)
	finally:
		return json.dumps(ret)


@app.route('/update/record', methods=['POST'])
def on_update_record():
	ret = {'success': True}
	try:
		data = json.loads(request.data.decode('utf-8'))
		ret['data'] = model.add_record(data['id'], data['start_time'], data['fuel_efi'], data['avr_speed'], data['hard_rpm'], data['hard_break'], data['hard_accel'], data['score'], data['distance'])
	except Exception as e:
		ret['success'] = False
		ret['error'] = str(e)
	finally:
		return json.dumps(ret)


@app.route('/request/position', methods=['POST'])
def on_request_position():
	ret = {'success': True}
	try:
		data = json.loads(request.data.decode('utf-8'))
		ret['data'] = model.get_position(data['id'], data['start_time'], data['end_time'])
	except Exception as e:
		ret['success'] = False
		ret['error'] = str(e)
	finally:
		return json.dumps(ret)


@app.route('/request/car', methods=['POST'])
def on_request_car():
	ret = {'success': True}
	try:
		data = json.loads(request.data.decode('utf-8'))
		ret['data'] = model.get_car(data['id'])
	except Exception as e:
		ret['success'] = False
		ret['error'] = str(e)
	finally:
		return json.dumps(ret)


@app.route('/register/user', methods=['POST'])
def on_register_user():
	ret = {'success': True}
	try:
		data = json.loads(request.data.decode('utf-8'))
		ret['data'] = model.register_user(data['id'], data['name'], data['token'])
	except Exception as e:
		ret['success'] = False
		ret['error'] = str(e)
	finally:
		return json.dumps(ret)


if __name__ == '__main__':
	app.run(host='0.0.0.0')
