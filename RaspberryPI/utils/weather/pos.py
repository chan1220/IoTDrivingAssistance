import json
import urllib.request

def get_addr(lat, lon):
	client_id = "6vNW1jYKk6ETlhsx4QAB"
	client_secret = "80mPSyDfbA"
	encText = urllib.parse.quote("{},{}".format(lon, lat))
	url = "https://openapi.naver.com/v1/map/reversegeocode?query=" + encText

	request = urllib.request.Request(url)
	request.add_header("X-Naver-Client-Id",client_id)
	request.add_header("X-Naver-Client-Secret",client_secret)
	response = urllib.request.urlopen(request)
	rescode = response.getcode()
	if(rescode==200):
		response_body = response.read().decode('utf-8')

		get_json = json.loads(response_body)
		
		return get_json['result']['items'][0]['addrdetail']['sido'] + ' ' + get_json['result']['items'][0]['addrdetail']['sigugun'] + ' '+ get_json['result']['items'][0]['addrdetail']['dongmyun']

	else:
		print("Error Code:" + rescode)
		return 'error'

if __name__ == "__main__":
	print(get_addr(37,127))