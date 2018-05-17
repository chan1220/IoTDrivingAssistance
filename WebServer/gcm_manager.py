from gcm import GCM

def send_gcm_message(token, message):
	API_KEY = "AAAAB3M5t78:APA91bHX2-CxEDzYUiHRkCyGMXYRHqY3ivZswhl0EosKayO8oFWJYotG3HBIDMG48DwFgZNmV-Vk51MBfhvkpSqtj-9HpawnX98D0ppnLcba4bM7bx3NK9uiT5lsPAOpk1ZADwbjc9AD"
	gcm = GCM(API_KEY)
	data = {'message': 'message', 'param2': 'value2'}

	# Downstream message using JSON request
	reg_ids = [token]
	response = gcm.json_request(registration_ids=reg_ids, data=data)

	# Downstream message using JSON request with extra arguments
	res = gcm.json_request(registration_ids=reg_ids, data=data, collapse_key='uptoyou', delay_while_idle=True, time_to_live=3600)


