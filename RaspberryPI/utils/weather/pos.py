import json
import urllib.request

def get_addr(lat, lon):
	client_secret = "POIL6v8UJMgD7AvkB1gChNX7U7AmfWXMyOPzqace"
	client_id = "67zyvca5yy"
	encText = urllib.parse.quote("{},{}".format(lon, lat))
	url = "https://naveropenapi.apigw.ntruss.com/map-reversegeocode/v2/gc?coords=" + encText + "&output=json"
	request = urllib.request.Request(url)
	request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
	request.add_header("X-NCP-APIGW-API-KEY",client_secret)
	response = urllib.request.urlopen(request)
	rescode = response.getcode()
	if(rescode==200):
		response_body = response.read().decode('utf-8')
		get_json = json.loads(response_body)
		#print(response_body)

		print(get_json['results'][1]['region']['area1']['name'] + ' ' + get_json['results'][1]['region']['area2']['name'] + ' ' + get_json['results'][1]['region']['area3']['name'])
	else:
		print("Error Code:" + rescode)
		return 'error'

if __name__ == "__main__":
	print(get_addr(37.502,127.097))