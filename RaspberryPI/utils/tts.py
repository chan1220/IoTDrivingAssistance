import json
import urllib.request
import subprocess

class TTS():
	def play_mp3(self, path):
		subprocess.Popen(['mpg123', '-q', path]).wait()

	def play_tts(self, text, speaker='mijin'):
		client_id = "67zyvca5yy"           # <= 변경 
		client_secret = "POIL6v8UJMgD7AvkB1gChNX7U7AmfWXMyOPzqace" # <= 변경
		encText = urllib.parse.quote(text)
		data = "speaker=" + speaker + "&speed=0&text=" + encText; # jinho,mijin, clara, matt, shinji, yuri
		url = "https://naveropenapi.apigw.ntruss.com/voice/v1/tts"
		request = urllib.request.Request(url)
		request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
		request.add_header("X-NCP-APIGW-API-KEY",client_secret)
		response = urllib.request.urlopen(request, data=data.encode('utf-8'))
		rescode = response.getcode()

		if(rescode==200):
			print("TTS mp3 저장")
			response_body = response.read()
			with open("temp", "wb") as f:
				f.write(response_body)
			self.play_mp3('temp')
		else:
			print("Error Code:" + rescode)


if __name__ == "__main__":
	print("시작")
	hehe = TTS()
	hehe.play_tts("헤헤헤헤 밥먹으러 갑시다", 'yuri')
	print("종료")

	# client_id = "0q3bfmoxfq"
	# client_secret = "BZmuC2syLUFzfZhqZhQYGKXCtmxl4Dnvq4cWnVGb"
	# encText = urllib.parse.quote("반갑습니다 네이버")
	# data = "speaker=mijin&speed=0&text=" + encText;
	# url = "https://naveropenapi.apigw.ntruss.com/voice/v1/tts"
	# request = urllib.request.Request(url)
	# request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
	# request.add_header("X-NCP-APIGW-API-KEY",client_secret)
	# response = urllib.request.urlopen(request, data=data.encode('utf-8'))
	# rescode = response.getcode()
	# if(rescode==200):
	# 	print("TTS mp3 저장")
	# 	response_body = response.read()
	# 	with open('1111.mp3', 'wb') as f:
	# 		f.write(response_body)
	# else:
	# 	print("Error Code:" + rescode)

	# subprocess.Popen(['mpg123', '-q', '1111.mp3']).wait()